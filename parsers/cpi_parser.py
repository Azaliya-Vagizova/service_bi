import requests
import os
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def download_all_income_data():
    url = "https://77.rosstat.gov.ru/folder/64641"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print("Загружаем страницу Мосстата...")
    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        print("Страница успешно загружена!")
        soup = BeautifulSoup(response.text, "html.parser")

        download_links = []
        seen_urls = set()

        for link in soup.find_all("a"):
            href = link.get("href", "")

            if "download" in href.lower() or ".xlsx" in href.lower():
                if "sputnik" in href or "metrika" in href or "stat" in href:
                    continue

                full_url = urljoin(url, href)

                if full_url in seen_urls:
                    continue
                seen_urls.add(full_url)

                parent = link.parent
                text = parent.get_text(strip=True)

                if len(text) < 15:
                    parent = parent.parent
                    text = parent.get_text(strip=True)

                match = re.search(r'([А-ЯЁ][а-яё\s\-]+.*?)(?=\d+\.\d+ Кб|\d{2}\.\d{2}\.\d{4}|$)', text)
                if match:
                    file_name = match.group(1).strip()
                    file_name = file_name.replace("XLSX", "").strip()
                else:
                    file_name = f"Файл_{len(download_links) + 1}"

                download_links.append((full_url, file_name))

        print(f"Найдено уникальных файлов: {len(download_links)}")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        save_dir = os.path.join(project_root, "data", "raw")
        os.makedirs(save_dir, exist_ok=True)

        for i, (file_url, file_name) in enumerate(download_links, 1):
            safe_name = re.sub(r'[\\/*?:"<>|]', "", file_name)
            safe_name = safe_name[:60].strip()
            save_path = os.path.join(save_dir, f"inc_{i}_{safe_name}.xlsx")

            print(f"Скачиваем [{i}/{len(download_links)}]: {file_name}...")
            try:
                file_response = requests.get(file_url, headers=headers, verify=False)
                with open(save_path, "wb") as f:
                    f.write(file_response.content)
                print(f"  Сохранено: {os.path.basename(save_path)}")
            except Exception as e:
                print(f"  Ошибка: {e}")

        print("Готово!")
    else:
        print(f"Ошибка при загрузке. Код: {response.status_code}")

if __name__ == "__main__":
    download_all_income_data()
