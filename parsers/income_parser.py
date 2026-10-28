import requests
import os
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def download_income_data():
    url = "https://77.rosstat.gov.ru/folder/64641"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print("Загружаем страницу (Доходы и бедность)...")
    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        print("Страница успешно загружена!")
        soup = BeautifulSoup(response.text, "html.parser")

        download_links = []
        seen_urls = set()

        for link in soup.find_all("a"):
            href = link.get("href", "")

            if ".xlsx" in href.lower() or "download" in href.lower():
                full_url = urljoin(url, href)

                if full_url in seen_urls:
                    continue
                seen_urls.add(full_url)

                file_name = None
                parent = link.parent
                for _ in range(5):
                    if not parent: break
                    text = parent.get_text(separator=" ", strip=True)
                    if len(text) > 20 and "XLSX" not in text[:10]:
                        file_name = text
                        break
                    parent = parent.parent

                if file_name:
                    file_name = re.sub(r'\d{2}\.\d{2}\.\d{4}', '', file_name)
                    file_name = re.sub(r'\d+\.\d+\s*Кб', '', file_name)
                    file_name = file_name.replace("XLSX", "").strip()
                    file_name = file_name[:80]
                else:
                    file_name = f"Документ_{len(download_links) + 1}"

                download_links.append((full_url, file_name))

        unique_links = []
        seen_names = set()
        for url_link, name in download_links:
            if name not in seen_names:
                unique_links.append((url_link, name))
                seen_names.add(name)

        print(f"Найдено уникальных файлов: {len(unique_links)}")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        save_dir = os.path.join(project_root, "data", "raw")
        os.makedirs(save_dir, exist_ok=True)

        for i, (file_url, file_name) in enumerate(unique_links, 1):
            safe_name = re.sub(r'[\\/*?:"<>|]', "", file_name)
            safe_name = safe_name[:80].strip()

            save_path = os.path.join(save_dir, f"inc_{i}_{safe_name}.xlsx")

            print(f"Скачиваем [{i}/{len(unique_links)}]: {safe_name}...")
            try:
                file_response = requests.get(file_url, headers=headers, verify=False)
                with open(save_path, "wb") as f:
                    f.write(file_response.content)
                print(f"  Сохранено: {os.path.basename(save_path)}")
            except Exception as e:
                print(f"  Ошибка: {e}")

        print("Готово!")
    else:
        print(f"Ошибка. Код: {response.status_code}")

if __name__ == "__main__":
    download_income_data()
