import os
import re
import jieba
import logging
from collections import Counter

logger = logging.getLogger(__name__)


dir = "../crawler/data/"
files = os.listdir(dir)

print("文件数量：%d 篇" % len(files))

all_content = ""
for f in files:
    file_path = os.path.join(dir,f)
    file = open(file_path,"r",encoding="utf-8")
    content = file.read()
    content = re.sub("[A-Za-z0-9\：\·\—\，\。\“ \”]", "", content)
    seg_list = jieba.cut(content)
    all_content+=(" ".join(seg_list))

all_words=all_content.split()
c=Counter()
for x in all_words:
    if len(x)>1 and x != '\r\n':
        c[x] += 1

print('词频统计结果：')
for (k,v) in c.most_common(100):# 输出词频最高的前两个词
    print("%s:%d"%(k,v))