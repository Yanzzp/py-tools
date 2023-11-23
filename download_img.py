import platform
import subprocess
import threading

import requests
from bs4 import BeautifulSoup
import os
import sys


def open_file_explorer(directory):
    os_type = platform.system()

    if os_type == 'Windows':
        os.startfile(directory)
    elif os_type == 'Linux':
        # 在WSL中使用explorer.exe打开Windows文件资源管理器
        # 将Linux路径转换为Windows路径（例如 /mnt/c/... -> C:\...）
        windows_path = directory.replace('/mnt/', '').replace('/', '\\')
        drive_letter = windows_path[0].upper()
        windows_path = f'{drive_letter}:{windows_path[1:]}'
        subprocess.run(["explorer.exe", windows_path])
    else:
        print("Unsupported OS")

def download_image(img_url, image_filename):
    try:
        img_data = requests.get(img_url).content
        with open(image_filename, 'wb') as file:
            file.write(img_data)
            print(f'{image_filename} downloaded.')
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")

def download_images(url, folder_path):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        response = requests.get(url)
        if response.status_code != 200:
            print("Failed to retrieve the webpage")
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('span', {'id': 'thread_subject'})
        if not title:
            print('找不到标题')
            return

        title_text = title.get_text().replace('/', '_').replace('\\', '_')
        output_text = title_text.replace('【', '[').replace('】', ']').replace('（', '(').replace('）', ')')
        images = soup.find_all('img', id=True)

        threads = []

        for i, img in enumerate(images):
            img_url = img.get('file')
            if img_url and img_url.startswith(('http://', 'https://')):
                image_filename = os.path.join(folder_path, f'{title_text}_{i}.jpg')
                thread = threading.Thread(target=download_image, args=(img_url, image_filename))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()


    except Exception as e:
        print(f"Error in downloading images: {e}")


mainurl = 'https://www.cunhua.pics/forum.php?mod=viewthread&tid=492854'


def main(url):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(current_directory, '缩略图')

    download_images(url, img_path)
    open_file_explorer(img_path)


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else mainurl
    main(url)
