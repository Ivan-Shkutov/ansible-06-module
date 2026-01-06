## Домашнее задание к занятию 6 «Создание собственных модулей»

## Шкутов Иван Владимирович

### Подготовка к выполнению
1. Создайте пустой публичный репозиторий в своём любом проекте: my_own_collection.
2. Скачайте репозиторий Ansible: git clone https://github.com/ansible/ansible.git по любому, удобному вам пути.
3. Зайдите в директорию Ansible: cd ansible.
4. Создайте виртуальное окружение: python3 -m venv venv.
5. Активируйте виртуальное окружение: . venv/bin/activate. Дальнейшие действия производятся только в виртуальном окружении.
6. Установите зависимости pip install -r requirements.txt.
7. Запустите настройку окружения . hacking/env-setup.
8. Если все шаги прошли успешно — выйдите из виртуального окружения deactivate.
 Ваше окружение настроено. Чтобы запустить его, нужно находиться в директории ansible и выполнить конструкцию . venv/bin/activate && . hacking/env-setup.

![1](https://github.com/Ivan-Shkutov/my_own_collection/blob/main/1.png)

### Основная часть

Ваша цель — написать собственный module, который вы можете использовать в своей role через playbook. Всё это должно быть собрано в виде collection и отправлено в ваш репозиторий.

Шаг 1. В виртуальном окружении создайте новый my_own_module.py файл.

Перейти в директорию ansible и активировать окружение:

    cd ~/projects/ansible
    . venv/bin/activate
    . hacking/env-setup

Создать файл:

    touch my_own_module.py
    chmod +x my_own_module.py
    
Шаг 2. Наполните его содержимым:

    #!/usr/bin/python
    
    # Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
    # GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
    from __future__ import (absolute_import, division, print_function)
    __metaclass__ = type
    
    DOCUMENTATION = r'''
    ---
    module: my_test
    
    short_description: This is my test module
    
    # If this is part of a collection, you need to use semantic versioning,
    # i.e. the version is of the form "2.5.0" and not "2.4".
    version_added: "1.0.0"
    
    description: This is my longer description explaining my test module.
    
    options:
        name:
            description: This is the message to send to the test module.
            required: true
            type: str
        new:
            description:
                - Control to demo if the result of this module is changed or not.
                - Parameter description can be a list as well.
            required: false
            type: bool
    # Specify this value according to your collection
    # in format of namespace.collection.doc_fragment_name
    extends_documentation_fragment:
        - my_namespace.my_collection.my_doc_fragment_name

    author:
        - Your Name (@yourGitHubHandle)

    EXAMPLES = r'''
    # Pass in a message
    - name: Test with a message
      my_namespace.my_collection.my_test:
        name: hello world
    
    # pass in a message and have changed true
    - name: Test with a message and changed output
      my_namespace.my_collection.my_test:
        name: hello world
        new: true

    # fail the module
    - name: Test failure of the module
      my_namespace.my_collection.my_test:
        name: fail me
    '''

    RETURN = r'''
    # These are examples of possible return values, and in general should use other names for return values.
    original_message:
        description: The original name param that was passed in.
        type: str
        returned: always
        sample: 'hello world'
    message:
        description: The output message that the test module generates.
        type: str
        returned: always
        sample: 'goodbye'
    '''

    from ansible.module_utils.basic import AnsibleModule
    
    
    def run_module():
        # define available arguments/parameters a user can pass to the module
        module_args = dict(
            name=dict(type='str', required=True),
            new=dict(type='bool', required=False, default=False)
        )

        # seed the result dict in the object
        # we primarily care about changed and state
        # changed is if this module effectively modified the target
        # state will include any data that you want your module to pass back
        # for consumption, for example, in a subsequent task
            result = dict(
                changed=False,
                original_message='',
                message=''
        )

        # the AnsibleModule object will be our abstraction working with Ansible
        # this includes instantiation, a couple of common attr would be the
        # args/params passed to the execution, as well as if the module
        # supports check mode
        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
        )

        # if the user is working with this module in only check mode we do not
        # want to make any changes to the environment, just return the current
        # state with no modifications
        if module.check_mode:
            module.exit_json(**result)

        # manipulate or modify the state as needed (this is going to be the
        # part where your module will do what it needs to do)
        result['original_message'] = module.params['name']
        result['message'] = 'goodbye'

        # use whatever logic you need to determine whether or not this module
        # made any modifications to your target
        if module.params['new']:
            result['changed'] = True

        # during the execution of the module, if there is an exception or a
        # conditional state that effectively causes a failure, run
        # AnsibleModule.fail_json() to pass in the message and the result
        if module.params['name'] == 'fail me':
            module.fail_json(msg='You requested this to fail', **result)

        # in the event of a successful module execution, you will want to
        # simple AnsibleModule.exit_json(), passing the key/value results
        module.exit_json(**result)


    def main():
        run_module()


    if __name__ == '__main__':
        main()
        
Или возьмите это наполнение из статьи.

Требования к файлу my_own_module.py:

    path — путь к файлу
    content — содержимое
    - идемпотентность
    - создавать файл на удалённом хосте


Шаг 3. Заполните файл в соответствии с требованиями Ansible так, чтобы он выполнял основную задачу: module должен создавать текстовый файл на удалённом хосте по пути, определённом в параметре path, с содержимым, определённым в параметре content.

Шаг 4. Проверьте module на исполняемость локально.

Первый запуск: changed: true

Второй запуск: changed: false (идемпотентность)


Шаг 5. Напишите single task playbook и используйте module в нём.

Шаг 6. Проверьте через playbook на идемпотентность.

Объяснение:

    name — название плейбука
    hosts — на каких хостах выполнять
    gather_facts — отключаем сбор фактов
    tasks — блок с задачами (внутри tasks идёт модуль my_own_module)

Первый запуск: changed: true

Второй запуск: changed: false (идемпотентность)


Шаг 7. Выйдите из виртуального окружения.

    deactivate

Шаг 8. Инициализируйте новую collection: ansible-galaxy collection init my_own_namespace.yandex_cloud_elk.

Инициализация collection:

    ansible-galaxy collection init my_own_namespace.yandex_cloud_elk

Создана структура collection с директориями plugins/modules, roles, playbooks:

- чтобы модуль можно было использовать как часть collection, которая удобно распространяется и устанавливается.


Шаг 9. В эту collection перенесите свой module в соответствующую директорию.

Перенос модуля в collection:

    - перенёс файл my_own_module.py в my_own_namespace/yandex_cloud_elk/plugins/modules/my_own_module.py
    Чтобы Ansible мог найти модуль внутри collection через полное имя my_own_namespace.yandex_cloud_elk.my_own_module


Шаг 10. Single task playbook преобразуйте в single task role и перенесите в collection. У role должны быть default всех параметров module.

Шаг 11. Создайте playbook для использования этой role.

Шаг 12. Заполните всю документацию по collection, выложите в свой репозиторий, поставьте тег 1.0.0 на этот коммит.

Шаг 13. Создайте .tar.gz этой collection: ansible-galaxy collection build в корневой директории collection.

Собрать collection в архив .tar.gz

Находясь в корне collection my_own_namespace/yandex_cloud_elk:

    ansible-galaxy collection build

После этого в текущей директории появится файл вроде:

    my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz


Шаг 14. Создайте ещё одну директорию любого наименования, перенесите туда single task playbook и архив c collection.

Шаг 15. Установите collection из локального архива: ansible-galaxy collection install <archivename>.tar.gz.

Установить collection локально:
    
    ansible-galaxy collection install my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz

Это зарегистрирует collection в Ansible, и она станет доступна через namespace.


Шаг 16. Запустите playbook, убедитесь, что он работает.

Теперь можно использовать полный путь к модулю в collection:

    ansible localhost \
      -m my_own_namespace.yandex_cloud_elk.my_own_module \
      -a "path=/tmp/test.txt content='Hello world'" \
      -c local \
      -e "ansible_python_interpreter=/usr/bin/python3"

Шаг 17. В ответ необходимо прислать ссылки на collection и tar.gz архив, а также скриншоты выполнения пунктов 4, 6, 15 и 16.



![2](https://github.com/Ivan-Shkutov/my_own_collection/blob/main/2.png)

![3](https://github.com/Ivan-Shkutov/my_own_collection/blob/main/3.png)

![4](https://github.com/Ivan-Shkutov/my_own_collection/blob/main/4.png)

![5](https://github.com/Ivan-Shkutov/my_own_collection/blob/main/5.png)

![6](https://github.com/Ivan-Shkutov/my_own_collection/blob/main/6.png)

![7](https://github.com/Ivan-Shkutov/my_own_collection/blob/main/7.png)

