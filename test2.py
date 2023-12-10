import platform
import subprocess

from PIL import Image
import requests
from bs4 import BeautifulSoup
import os
from threading import Thread

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


def download_image(img_url, img_path):
    # 确保目录存在
    directory = os.path.dirname(img_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 下载并保存图片
    img_response = requests.get(img_url)
    if img_response.status_code == 200:
        img_data = img_response.content
        with open(img_path, 'wb') as file:
            file.write(img_data)
            print(f'{img_url} downloaded.')


def is_target_img(tag):
    # 检查标签是否为<img>，是否有onclick属性，以及是否调用了zoom函数
    return tag.name == 'img' and tag.has_attr('onclick') and 'zoom(this,' in tag['onclick']

def download_images_from_url(url):
    # 发送HTTP请求
    response = requests.get(url)
    folderPath = ""
    # 检查响应状态
    if response.status_code == 200:
        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取标题并格式化为文件夹名
        title_tag = soup.find('span', {'id': 'thread_subject'})
        if title_tag:
            folderPath = title_tag.text.strip().replace('/', '_').replace(' ', '_').replace('[', '').replace(']', '')
        else:
            print("没有找到标题")
            return

        # 查找包含图片的div
        t_fsz_content = soup.find('div', {'class': 't_fsz'})
        if not t_fsz_content:
            print("没有找到图片")
            return

        if not os.path.exists(folderPath):
            os.makedirs(folderPath)

        images_path = os.path.join(folderPath, '缩略图')
        if not os.path.exists(images_path):
            os.makedirs(images_path)
        threads = []

        # 查找所有图片并下载
        for i, img_tag in enumerate(t_fsz_content.find_all(is_target_img)):
            img_url = img_tag.get('file')
            if img_url:
                if 'cunhua.pics' in url and not img_url.startswith('http'):
                    img_url = 'https://www.cunhua.pics/' + img_url
                elif 'laowang.vip' in url and not img_url.startswith('http'):
                    img_url = 'https://laowang.vip' + img_url

                img_path = os.path.join(images_path, f'{folderPath}_{i}.jpg')
                thread = Thread(target=download_image, args=(img_url, img_path))
                thread.start()
                threads.append(thread)

        for thread in threads:
            thread.join()

        print(f"图片成功保存到 {folderPath} 文件夹。")
    else:
        print(f"获取网页失败。状态码: {response.status_code}")
    return folderPath


def create_responsive_masonry_html_for_images(directory):
    images_path = directory + '\\缩略图'
    html_content = (
        "<!DOCTYPE html>"
        "<html lang='en'>"
        "<head>"
        "<meta charset='UTF-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1.0, user-scalable=no'>"
        "<title>Responsive Image Gallery</title>"
        "<style>"
        "  .gallery {"
        "    display: flex;"
        "    flex-wrap: wrap;"
        "    justify-content: space-around;"
        "    gap: 10px;"
        "  }"
        "  .gallery div {"
        "    break-inside: avoid;"
        "    margin-bottom: 10px;"
        "  }"
        # "  .gallery img {"
        # "    width: auto;" 
        # "    height: auto;"
        # "  }"
        "</style>"
        "</head>"
        "<body>"
        "<div class='gallery'>"
    )

    # Iterate over files in the directory
    for filename in os.listdir(images_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(images_path, filename)
            with Image.open(file_path) as img:
                width, height = img.size
            img_tag = f"<div style='margin: 2px;'><img src='缩略图\\{filename}' alt='image' width='{int(width / 2)}' height='{int(height / 2)}'></div>"
            html_content += img_tag

    html_content += "</div></body></html>"

    html_file_path = os.path.join(directory, 'responsive_gallery.html')
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

    return html_file_path


url = "https://www.cunhua.pics/forum.php?mod=viewthread&tid=495148"

folderPath = download_images_from_url(url)
open_file_explorer(folderPath)
html_file_path = create_responsive_masonry_html_for_images(folderPath)
print(f"HTML file created at {html_file_path}")