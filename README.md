# Server Integration Tests

* test_login_page.py - тест страницы залогинивания на GM-server
* test_CRUD_user.py  - тест страницы Users. Проверка CRUD пользователя.
* test_CRUD_update.py - тест страницы Updates. Проверка CRUD прошивок.
* test_CRUD_commands.py - тест страницы Commands. Проверка CRUD комманд.

## Preparing to testing
#### Install chromedriver
https://skolo.online/documents/webscrapping/#step-1-download-chrome  
  
#### Install venv (python >=3.9 required)
```bash
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
```

#### Install pre-commit
```bash
pre-commit install -f
```

## Running tests

### Run all tests
`GMSERVER_ADDRESS=<адрес СУ> TEST_WEBDRIVER_HEADLESS=<true/false> pytest`

### Run shura tests only  
`GMSERVER_ADDRESS=<адрес СУ> TEST_WEBDRIVER_HEADLESS=<true/false> pytest shura`

### Run alice tests only  
`GMSERVER_ADDRESS=<адрес СУ> TEST_WEBDRIVER_HEADLESS=<true/false> pytest alice`

### Для локального запуска автотестов нужно сделать следующее:

0) Установить PyCharm

1) Склонировать в локальную папку проект git@git.dev.getmobit.ru:gmms/server-integration-tests.git

2) Создать виртуальное окружение

3) Установить зависимости из requirements.txt

4) Задать переменные окружения, например через ~/.bashrc, подставив свои значения (сервер, ID материнки бокса, HEADLESS - скрытое или видимое выполнение автотестов):
```
export GMSERVER_ADDRESS=http://172.16.10.192/
export TEST_GMBOX_ID=180808I1100068
export TEST_WEBDRIVER_HEADLESS=False
```

5) Запустить тесты командой ```pytest shura/tests/```