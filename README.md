# CallApiDBus testing

## Установка зависимостей 

Конфигурационный файл pyproject.toml содержит список необходимых зависимостей. Чтобы установить их, выполните следующие действия:

```bash
uv sync
source .venv/bin/activate
```
После этого зависимости будут установлены, а виртуальное окружение активировано.

## Запуск тестов

### Настройка эмулятора

Настроить эмулятор по предоставленной в докуменатации [инструкции](https://developer.auroraos.ru/doc/software_development/guides/application_testing/setup_emulator_autotests).

### Запуск тестов

На устройстве. (через параметер ```--device-ip-address``` передается IP адрес устройства):

```bash
uv run -- pytest --device-ip-address 192.168.2.15
```

На эмуляторе:

```bash
uv run -- pytest --device-ip-address localhost --device-port 2223
```

