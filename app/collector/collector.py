from app.core.config import settings
import paramiko
import logging
import os
import json
import time

SSH_PRIVATE_KEY = settings.SSH_PRIVATE_KEY_PATH

def ensure_dependencies(ssh_client, max_retries=3):
    """
    Проверяет и устанавливает зависимости (python, pip, virtualenv) на удаленном хосте.
    """
    commands = [
        "if ! command -v python3 &> /dev/null; then sudo apt update && sudo apt install -y python3; fi",
        "if ! command -v pip3 &> /dev/null; then sudo apt install -y python3-pip; fi",
        "if ! command -v virtualenv &> /dev/null; then sudo apt install -y virtualenv; fi",
        "if ! python3 -c 'import psutil' &> /dev/null; then sudo apt update && sudo apt install -y python3-psutil; fi"
    ]

    for command in commands:
        for attempt in range(max_retries):
            stdin, stdout, stderr = ssh_client.exec_command(command)
            exit_status = stdout.channel.recv_exit_status()
            error_output = stderr.read().decode()
            if exit_status == 0:
                break
            if "Could not get lock" in error_output and attempt < max_retries - 1:
                time.sleep(5)  # Подождать 5 секунд и попробовать снова
                continue
            raise Exception(f"Ошибка выполнения команды: {command}\n{error_output}")

def run_metrics_script(ssh_client, script_path):
    """
    Запускает Python-скрипт для сбора метрик на удаленном хосте.
    """
    command = f"python3 {script_path}"
    stdin, stdout, stderr = ssh_client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    output = stdout.read().decode()
    error_output = stderr.read().decode()
    if exit_status != 0:
        raise Exception(f"Ошибка выполнения скрипта: {error_output}")
    if not output.strip():
        raise Exception(f"Скрипт не вернул данных. stderr: {error_output}")
    return output

def copy_script_to_remote(ssh_client, local_script_path, remote_script_path):
    """
    Копирует локальный скрипт на удаленный хост.
    """
    sftp = ssh_client.open_sftp()
    try:
        abs_local_script_path = os.path.abspath(local_script_path)
        if not os.path.exists(abs_local_script_path):
            logging.error(f"Локальный скрипт не найден: {abs_local_script_path}")
            raise FileNotFoundError(f"Локальный скрипт не найден: {abs_local_script_path}")
        file_size = os.path.getsize(abs_local_script_path)
        if file_size == 0:
            logging.error(f"Локальный скрипт пустой: {abs_local_script_path}")
            raise Exception(f"Локальный скрипт пустой: {abs_local_script_path}")
        logging.info(f"Копирование скрипта {abs_local_script_path} ({file_size} байт) на {remote_script_path}")
        sftp.put(abs_local_script_path, remote_script_path)
        logging.info(f"Скрипт {abs_local_script_path} успешно скопирован на {remote_script_path}.")
    except Exception as e:
        logging.error(f"Ошибка при копировании скрипта: {e}")
        raise
    finally:
        sftp.close()

def connect_and_collect_metrics(host, username, key_path, local_script_path):
    """
    Подключается к удаленному хосту, проверяет зависимости, копирует скрипт и запускает его.
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Используем относительный путь, если путь начинается с collector/
    if not os.path.isabs(local_script_path):
        abs_local_script_path = os.path.abspath(local_script_path)
    else:
        abs_local_script_path = local_script_path

    remote_script_path = os.path.join(f"/home/{username}/scripts/", os.path.basename(local_script_path))

    try:
        logging.info(f"Подключение к {host}...")
        ssh_client.connect(hostname=host, username=username, key_filename=key_path)

        logging.info("Проверка и установка зависимостей...")
        ensure_dependencies(ssh_client)

        logging.info("Создание директории для скрипта на удаленном хосте...")
        ssh_client.exec_command(f"mkdir -p /home/{username}/scripts")

        logging.info("Копирование скрипта на удаленный хост...")
        copy_script_to_remote(ssh_client, abs_local_script_path, remote_script_path)

        logging.info("Запуск скрипта сбора метрик...")
        metrics_output = run_metrics_script(ssh_client, remote_script_path)
        try:
            metrics = json.loads(metrics_output)
        except Exception as e:
            logging.error(f"Ошибка парсинга JSON: {e}. Вывод скрипта: {metrics_output}")
            raise Exception(f"Ошибка парсинга JSON: {e}. Вывод скрипта: {metrics_output}")

        logging.info("Метрики успешно собраны.")
        return metrics

    except Exception as e:
        logging.error(f"Ошибка при подключении или сборе метрик: {e}")
        raise

    finally:
        ssh_client.close()
        logging.info("Соединение закрыто.")

# Пример использования
# metrics = connect_and_collect_metrics("remote_host", "user", "path_to_key", "/path/to/metrics_script.py")
# Теперь используйте SSH_PRIVATE_KEY и SSH_PUBLIC_KEY для подключения по SSH
