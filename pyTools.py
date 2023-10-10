import json
import os
import shutil
import jieba

from moviepy.editor import VideoFileClip, concatenate_videoclips
from tencentcloud.common import credential

from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models

with open('config.json', 'r') as config_file:
    config = json.load(config_file)


class Pytools:
    @staticmethod
    def translate(text, source, target, is_print=False):
        try:
            cred = credential.Credential(config['TencentApi']['username'],
                                         config['TencentApi']['password'])  # "xxxx"改为SecretId，"yyyyy"改为SecretKey
            httpProfile = HttpProfile()
            httpProfile.endpoint = "tmt.tencentcloudapi.com"
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile)
            req = models.TextTranslateRequest()
            req.SourceText = text  # 要翻译的语句
            req.Source = source  # 源语言类型
            req.Target = target  # 目标/语言/类型
            req.ProjectId = 0

            resp = client.TextTranslate(req)
            data = json.loads(resp.to_json_string())
            if is_print:
                print(data['TargetText'])
            return data['TargetText']  # 返回翻译结果作为字符串data

        except TencentCloudSDKException as err:
            return str(err)  # 如果发生异常，将异常信息作为字符串返回

    @staticmethod
    def print_files(path):
        for path, file_dir, files in os.walk(path):
            for file_name in files:
                print(os.path.join(path, file_name))

    @staticmethod
    def delete_file(self, path, name):
        count = 0
        for path, file_dir, files in os.walk(path):
            for file_name in files:
                if name in file_name:
                    os.remove(os.path.join(path, file_name))
                    count += 1
                    print(os.path.join(path, file_name))
                # if file_name.endswith(".rar"):
                #     os.remove(os.path.join(path, file_name))
                #     count += 1
                #     print(os.path.join(path, file_name))
            for folder in file_dir:
                if name in folder:
                    shutil.rmtree(os.path.join(path, folder))
                    count += 1
                    print(os.path.join(path, folder))
        if count != 0:
            print("删除了" + str(count) + "个文件")

    def reverse_files_num(self, path):
        vector = []
        for path, file_dir, files in os.walk(path):
            for file_name in files:
                vector.append(int(file_name.split(". ")[0]))
        vector = sorted(vector)
        maximum = vector[-1]
        for path, file_dir, files in os.walk(path):
            for file_name in files:
                # print(os.path.join(path, file_name))
                pre_name = file_name
                file_name = str(maximum + 1 - int(file_name.split(". ")[0])) + file_name[file_name.find(". "):]
                print(f"原名：{pre_name}     新名：{file_name}")
                os.rename(os.path.join(path, pre_name), os.path.join(path, file_name))

    @staticmethod
    def translate_files(path, source, target, is_print=False, is_change_name=False):
        for root, dirs, files in os.walk(path):
            for file_name in files:
                # 组合完整的文件路径
                file_path = os.path.join(root, file_name)
                translate_text = Pytools.translate(file_name, source, target, is_print)
                if is_change_name:
                    os.rename(file_path, os.path.join(root, translate_text))

    @staticmethod
    def find_divide_files_name(path, name):
        name_list = []
        for path, file_dirs, files in os.walk(path):
            # path 表示当前文件夹的路径
            # file_dirs 表示当前文件夹中的子文件夹列表
            # files 表示当前文件夹中的文件列表

            name_list += list(jieba.cut(str(file_dirs)))
        ignore_list = [' ', '，', '。', '、', '：', '“', '”', '？', '！', '《', '》', '（', '）', '【', '】', '——', '……',
                       '；', '‘', '[', ']', "'", '-', '(', ')', ',', '+', '_', '.']
        for i in ignore_list:
            while i in name_list:
                name_list.remove(i)

        print(name_list)

        if name in name_list:
            print("找到名称" + name)
        else:
            print("没有找到")

    @staticmethod
    def enmerge_videos(path1, path2):
        video1 = VideoFileClip(path1)
        video2 = VideoFileClip(path2)
        final_video = concatenate_videoclips([video1, video2], method="compose")
        final_video.write_videofile('C:\\Users\\11057\\Desktop\\out.mp4', codec='libx264')
