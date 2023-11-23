import os
import platform
import subprocess
import sys
import threading
import requests
from bs4 import BeautifulSoup


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
        # 检查文件是否存在，如果存在则删除
        if os.path.exists(image_filename):
            os.remove(image_filename)
        with open(image_filename, 'wb') as file:
            file.write(img_data)
        print(f'{os.path.basename(image_filename)} downloaded.')
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")


def download_images(input_url, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    url = input_url

    response = requests.get(url)
    response.raise_for_status()  #

    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('span', {'id': 'thread_subject'})
    output_text = ''
    if not title:
        print('找不到标题')
        return
    else:
        title_text = title.get_text().replace('/', '_').replace('\\', '_')
        output_text = title_text.replace('【', '[').replace('】', ']').replace('（', '(').replace('）', ')')
        print(output_text)
    divs = soup.find_all('div', class_='t_fsz')
    base_url = url.split('forum.php')[0]

    threads = []
    count = 0
    for div in divs:
        ignore_js_ops = div.find_all('ignore_js_op')
        for ignore_js_op in ignore_js_ops:
            count += 1
            thread = threading.Thread(target=process_image,
                                      args=(ignore_js_op, base_url, folder_path, output_text, count))
            threads.append(thread)
            thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()


def process_image(ignore_js_op, base_url, folder_path, output_text, count):
    file_link = ""
    imgs = ignore_js_op.find_all('img')
    for img in imgs:
        file_link = img.get('file')
        if file_link:
            file_link = base_url + file_link
    if file_link:
        file_link = file_link
        image_filename = os.path.join(folder_path, f'{output_text}_{count}.{file_link.split(".")[-1]}')
    download_image(file_link, image_filename)


def main(url):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(current_directory, '缩略图')

    download_images(url, img_path)
    open_file_explorer(img_path)


testurl = 'https://laowang.vip/forum.php?mod=viewthread&tid=1221077'
if __name__ == "__main__":
    url = str(sys.argv[1]) if len(sys.argv) > 1 else testurl
    main(url)
