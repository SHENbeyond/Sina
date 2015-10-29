#coding:utf-8
import sys, os
import json
import re
import pynlpir
pynlpir.open()
from pyltp import Segmentor, Postagger, Parser,NamedEntityRecognizer, SementicRoleLabeller
ROOTDIR =os.path.join(os.path.dirname(__file__),os.pardir)
sys.path.append(os.path.join(ROOTDIR, "lib"))
#设置模型文件的路径
MODELDIR=os.path.join(ROOTDIR, "ltp_data")

path = os.path.abspath(os.path.dirname(sys.argv[0]))
path_in = path+'/car_review_split.txt'
content_in  = open(path_in,'r')
path_out = path+'/test_word_list2.txt'
content_out = open(path_out,'w')
segmentor = Segmentor()
segmentor.load_with_lexicon(os.path.join(MODELDIR,"cws.model"),"/data0/dm/dict/dict.txt")
for line in content_in.readlines()[5000:10000]:
    print line
    line = re.sub("[\.\!\/_,$%^*(+\"\' ]+|[+——！，。？、~@#￥%……&*（）]+".decode('utf-8'),"".decode('utf-8'),line.decode('utf-8'))
    line = line.encode('utf-8').strip()
    words = segmentor.segment(line)
    for j in words:
        content_out.write(j+' ')
content_out.close()
