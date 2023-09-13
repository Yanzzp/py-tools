import json
import os
import shutil

from tencentcloud.common import credential  # 这里需要安装腾讯翻译sdk
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models


class Pytools:
    @staticmethod
    def translate(text, source, target, is_print=False):
        try:
            cred = credential.Credential("AKIDz3yhCUbChz5xa0PcmleLr9D2f6JI5g46",
                                         "vgHhz99wVpuyqWyDG5yf8NPODpEPN8vY")  # "xxxx"改为SecretId，"yyyyy"改为SecretKey
            httpProfile = HttpProfile()
            httpProfile.endpoint = "tmt.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile)

            req = models.TextTranslateRequest()
            req.SourceText = text  # 要翻译的语句
            req.Source = source  # 源语言类型
            req.Target = target  # 目标语言类型
            req.ProjectId = 0

            resp = client.TextTranslate(req)
            data = json.loads(resp.to_json_string())
            print(data)
            return data['TargetText']  # 返回翻译结果作为字符串data

        except TencentCloudSDKException as err:
            return str(err)  # 如果发生异常，将异常信息作为字符串返回

    @staticmethod
    def print_files(path):
        for path, file_dir, files in os.walk(path):
            for file_name in files:
                print(os.path.join(path, file_name))

    @staticmethod
    def delete_file(path, name):
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

    @staticmethod
    def reverse_files_num(path):
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