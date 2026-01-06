#!/usr/bin/python3

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Create a text file with specified content

version_added: "1.0.0"

description:
  - This module creates a text file on the remote host.
  - If the file already exists and content is the same, no changes are made.

options:
  path:
    description:
      - Path to the file that should be created.
    required: true
    type: str
  content:
    description:
      - Content that will be written into the file.
    required: true
    type: str

author:
  - Your Name
'''

EXAMPLES = r'''
- name: Create file with content
  my_own_module:
    path: /tmp/example.txt
    content: "Hello world"
'''

RETURN = r'''
changed:
  description: Whether the file was created or modified.
  type: bool
  returned: always
path:
  description: Path to the file.
  type: str
  returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    # Аргументы модуля
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        path=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']
    result['path'] = path

    # Проверка check_mode
    if module.check_mode:
        module.exit_json(**result)

    # Идемпотентность: если файл существует и содержимое совпадает, изменений нет
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                existing_content = f.read()
            if existing_content == content:
                module.exit_json(**result)
        except Exception as e:
            module.fail_json(msg=str(e), **result)

    # Запись файла
    try:
        with open(path, 'w') as f:
            f.write(content)
        result['changed'] = True
    except Exception as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
