import codecs
import jieba
import re
from zhon.hanzi import punctuation
import string

FILENAME1 = './corpus.txt'
FILENAME2 = './weixin_210K_reduced.json'
OUTPUT1 = './output.txt'
DIR = ''

def merge(dir):
    import os
    list_dir = os.listdir(dir)
    print("Num of files:", len(list_dir))
    contents = []

    for i in list_dir:
        with codecs.open(os.path.join(dir,i), 'r', 'utf-8') as f:
            text = f.read()
            contents.append(text)

    return contents

def read_json(filename):
    import json
    import random
    contents = []
    count = 0
    with codecs.open(filename, 'r', 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            count += 1
            #random sampling. typical:10-25%
            r = random.randint(0, 99)
            if r >= 80:
                result = ""

                try:
                    message = json.loads(line)
                except Exception as e:
                    print("Exception at line %d, %s" % (count, str(e)))
                else:
                    result = message["content"]

                if result != "":
                    #to lowercase
                    text = result.lower().replace("\n", "")
                    #text = re.sub(r"[%s]+" % punctuation, "", text)
                    seg_list = jieba.cut(text, cut_all=False)
                    temp = []
                    for j in seg_list:
                        if not j == ' ' and not j == '\r\n' and not j == '\n' and not j == '\r' \
                                and j not in string.punctuation:
                            temp.append(j)
                    text = " ".join(temp)
                    text = re.sub(r"[%s]+" % punctuation, "", text)
                    contents.append(text)

            if count % 5000 == 0:
                print("%d lines processed" % count)

        print("%d lines of data loaded" % len(contents))
        return contents


def split_word(filename):
    contents = []
    with codecs.open(filename, "r", "utf-8") as f1:
        lines = f1.readlines()
        for line in lines:
            temp = []
            line = re.sub(r"[%s]+" % punctuation, "", line)
            seg_list = jieba.cut(line, cut_all=False)
            for j in seg_list:
                if not j == ' ' and not j == '\r\n' and not j == '\n' and not j == '\r' \
                        and j not in punctuation:
                    temp.append(j)
            #print(temp)
            contents.append(" ".join(temp))
    return contents
    
def save(contents, filename, multiline_copy=False):
    with codecs.open(filename, "w", "utf-8") as f_out:
        for item in contents:
            f_out.write("%s " % item)
            
    if multiline_copy == True:
        with codecs.open('./output_ml.txt', "w", "utf-8") as f_ml:
            for item in contents:
                line = item.strip()
                f_ml.write("%s\n" % line)
            
if __name__ == "__main__":
    contents = read_json(FILENAME2)
    if len(contents) > 1:
        save(contents, OUTPUT1)
    else:
        print("Nothing to save")