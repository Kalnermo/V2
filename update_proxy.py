import requests
import shutil
import os

PROXY_URL = "http://121.127.37.120/proxy.txt"
PROXY_FILE_PATH = "proxy.txt"

def backup_proxy_file():
    # Проверяем, существует ли файл прокси
    if os.path.exists(PROXY_FILE_PATH):
        # Создаем резервную копию файла с добавлением расширения .bak
        try:
            shutil.copy(PROXY_FILE_PATH, PROXY_FILE_PATH + ".bak")
            print("Backup created successfully")
        except IOError as e:
            print(f"Error creating backup: {e}")
    else:
        print("No existing proxy file to backup.")

def update_proxy_file():
    try:
        response = requests.get(PROXY_URL)
        response.raise_for_status()  # Проверяем наличие ошибок HTTP
        with open(PROXY_FILE_PATH, "w") as file:
            file.write(response.text)
        print("Proxy list updated successfully")
    except requests.RequestException as e:
        print(f"Error updating proxy list: {e}")

if __name__ == "__main__":
    # Сначала создаем резервную копию текущего proxy.txt
    backup_proxy_file()
    
    # Затем обновляем proxy.txt с сервера
    update_proxy_file()