#!/usr/bin/python

# Copyright: (c) 2016-2017, Hewlett Packard Enterprise Development LP
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_enclosure_group_facts
short_description: Retrieve facts about one or more of the OneView Enclosure Groups
description:
    - Retrieve facts about one or more of the Enclosure Groups from OneView.
version_added: "2.5"
requirements:
    - "hpOneView >= 4.0.0"
author:
    - Priyanka Sood (@soodpr)
    - Madhav Bharadwaj (@madhav-bharadwaj)
    - Ricardo Galeno (@ricardogpsf)
    - Alex Monteiro (@aalexmonteiro)
options:
    name:
      description:
        - Enclosure Group name.
    options:
      description:
        - "List with options to gather additional facts about Enclosure Group.
          Options allowed:
          C(configuration_script) Gets the configuration script for an Enclosure Group."

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Enclosure Groups
  oneview_enclosure_group_facts:
    hostname: 10.101.42.57
    username: administrator
    password: serveradmin
    api_version: 500
  no_log: true
  delegate_to: localhost

- debug: var=enclosure_groups

- name: Gather paginated, filtered and sorted facts about Enclosure Groups
  oneview_enclosure_group_facts:
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=OK'
    hostname: 10.101.42.57
    username: administrator
    password: serveradmin
    api_version: 500
  no_log: true
  delegate_to: localhost

- debug: var=enclosure_groups

- name: Gather facts about an Enclosure Group by name with configuration script
  oneview_enclosure_group_facts:
    name: "Test Enclosure Group Facts"
    options:
      - configuration_script
    hostname: 10.101.42.57
    username: administrator
    password: serveradmin
    api_version: 500
  no_log: true
  delegate_to: localhost

- debug: var=enclosure_groups
- debug: var=enclosure_group_script
'''

RETURN = '''
enclosure_groups:
    description: Has all the OneView facts about the Enclosure Groups.
    returned: Always, but can be null.
    type: dict

enclosure_group_script:
    description: The configuration script for an Enclosure Group.
    returned: When requested, but can be null.
    type: string
'''

from ansible.module_utils.oneview import OneViewModuleBase


class EnclosureGroupFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(EnclosureGroupFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):
        facts = {}
        name = self.module.params.get('name')

        if name:
            enclosure_groups = self.oneview_client.enclosure_groups.get_by('name', name)

            if enclosure_groups and "configuration_script" in self.options:
                facts["enclosure_group_script"] = self.__get_script(enclosure_groups)
        else:
            enclosure_groups = self.oneview_client.enclosure_groups.get_all(**self.facts_params)

        facts["enclosure_groups"] = enclosure_groups
        return dict(changed=False, ansible_facts=facts)

    def __get_script(self, enclosure_groups):
        script = None

        if enclosure_groups:
            enclosure_group_uri = enclosure_groups[0]['uri']
            script = self.oneview_client.enclosure_groups.get_script(id_or_uri=enclosure_group_uri)

        return script


def main():
    EnclosureGroupFactsModule().run()


if __name__ == '__main__':
    main()
