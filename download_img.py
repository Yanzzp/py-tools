import platform
import subprocess
import requests
from bs4 import BeautifulSoup
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(current_directory, '缩略图')
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

def download_images(url, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 发送请求获取网页内容
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('span', {'id': 'thread_subject'})
    try:
        title = title.get_text()
    except AttributeError:
        print('找不到标题')
        return

    images = soup.find_all('img', id=True)

    for i, img in enumerate(images):
        if 'file' in img.attrs:
            img_url = img['file']
            if img_url.startswith(('http://', 'https://')):
                img_data = requests.get(img_url).content
                with open(f'{folder_path}/{title}_{i}.jpg', 'wb') as file:
                    file.write(img_data)
                    print(f'{title}_{i} downloaded.')



url = 'https://www.cunhua.pics/forum.php?mod=viewthread&tid=487905&extra=page%3D1'
download_images(url, img_path)
open_file_explorer(img_path)
