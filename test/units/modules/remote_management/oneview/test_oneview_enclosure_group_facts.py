# Copyright: (c) 2016-2017 Hewlett Packard Enterprise Development LP
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.compat.tests import unittest
from ansible.modules.remote_management.oneview.oneview_enclosure_group_facts import EnclosureGroupFactsModule
from hpe_test_utils import FactsParamsTestCase

ENCLOSURE_GROUP_NAME = "Enclosure Group Name"
ENCLOSURE_GROUP_URI = "/rest/enclosure-groups/7a298f96-fda8-480e-9747-8ad4c666f756"

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name=ENCLOSURE_GROUP_NAME,
    options=[]
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name=ENCLOSURE_GROUP_NAME,
    options=["configuration_script"]
)

ENCLOSURE_GROUPS = [{
    "name": ENCLOSURE_GROUP_NAME,
    "uri": ENCLOSURE_GROUP_URI
}]


class EnclosureGroupFactsSpec(unittest.TestCase,
                              FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, EnclosureGroupFactsModule)
        self.enclosure_groups = self.mock_ov_client.enclosure_groups
        FactsParamsTestCase.configure_client_mock(self, self.enclosure_groups)

    def test_should_get_all_enclosure_group(self):
        self.enclosure_groups.get_all.return_value = ENCLOSURE_GROUPS

        self.mock_ansible_module.params = PARAMS_GET_ALL

        EnclosureGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure_groups=ENCLOSURE_GROUPS)
        )

    def test_should_get_enclosure_group_by_name(self):
        self.enclosure_groups.get_by.return_value = ENCLOSURE_GROUPS

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        EnclosureGroupFactsModule().run()

        self.enclosure_groups.get_by.assert_called_once_with('name', ENCLOSURE_GROUP_NAME)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(enclosure_groups=ENCLOSURE_GROUPS)
        )

    def test_should_get_enclosure_group_by_name_with_options(self):
        configuration_script = "echo 'test'"
        self.enclosure_groups.get_by.return_value = ENCLOSURE_GROUPS
        self.enclosure_groups.get_script.return_value = configuration_script

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        EnclosureGroupFactsModule().run()

        self.enclosure_groups.get_by.assert_called_once_with('name', ENCLOSURE_GROUP_NAME)
        self.enclosure_groups.get_script.assert_called_once_with(id_or_uri=ENCLOSURE_GROUP_URI)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                enclosure_groups=ENCLOSURE_GROUPS,
                enclosure_group_script=configuration_script
            )
        )


if __name__ == '__main__':
    unittest.main()
