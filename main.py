import pyTools
import jieba

Tools = pyTools.Pytools()

# Tools.divide_files_name("")

# seg_list = jieba.cut("jieba库是一款开源的中文分词工具，能够将中文文本切分成词语。",use_paddle=True)
# print(list(seg_list))
# print("Paddle Mode: " + '/'.join(list(seg_list)))

Tools.find_divide_files_name("E:\资源","Dearie")