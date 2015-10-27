__author__ = 'syj'
# -*- coding:UTF-8 -*-
import numpy
import time
from numpy import *
import sys
import os
from collections import  Counter

#使用的三个出入语料，分别是处理后的原始语料，词表，主题全表（未去重）
path = os.path.abspath(os.path.dirname(sys.argv[0]))
path_yuliao = path+"/baidu_segment_0619.txt"
path_words = path+"/words_filter.txt"

path_output = path+"/output_frequrncy_top10.txt"

#返回语料，path为存放预料得路径
def read_yuliao(path,k):
    content_rd = open(path,'r').read().strip().split('\n')
    items = []
    item_all = []
    content_words = []
    for line in content_rd:
        content = line.strip().split('\001',3)
        if len(content) == 4 and len(content[3]) > k:
            items.append(content[0])
            words_list = sorted(Counter(content[3].split(' ')).items(),key = lambda x : x[1],reverse=True)
            content_words.append([i[0] for i in words_list if i[1] > k])
        else:
            pass
    item_all = list(set(items))
    return items,item_all,content_words

# 返回word_all，path是存放word的路径
def read_word(path):
    return open(path, 'r').read().strip().split("\n")


#返回item_dic, 输items和item_all
def item_dic_count(items, item_all):
    item_index = {}
    for i in item_all:
        item_index[i] = items.count(i)
    return item_index


#计算统计的矩阵，以字典形式保存
def fun_kafang_dic(content_words,item_dic,items,item_all ,word_all):
    kafang_dic = {}
    for i,line_words in enumerate(content_words):
        item  = items[i]
        loc = item_all.index(item)
        word_join  = list(set(word_all).intersection(set(line_words)))
        if word_join :
            for word in word_join:
                #location = item_all.index(word)
                if word in kafang_dic.keys():
                    kafang_dic[word][loc] += 1
                else:
                    kafang_dic[word] = list(zeros(len(item_all)))
                    kafang_dic[word][loc] += 1
        else:
            pass
    return kafang_dic

def fun_kafang(kafang_dic,item_all,item_dic,N):
    kafang_matrix = {}
    for word in kafang_dic.keys():
        kafang_matrix[word] = list(zeros(len(item_all)))
        for i,item in enumerate(item_all):
            aa = kafang_dic[word][i]
            cc = item_dic[item] - aa
            bb = sum(kafang_dic[word]) - aa
            dd = N - aa - bb - cc
            fenmu = (aa+cc)*(bb+dd)*(aa+bb)*(cc+dd)
            if not fenmu ==0:
                kafang_matrix[word][i] = round(float(N *(aa*dd-cc*bb)**2)/float(fenmu),2)
            else:
                kafang_matrix[word][i] = 0
    return kafang_matrix


#输入matrix的某一行，输出前五的卡方值和相应item
def select(mat_row,item_all):
    loc_list = []
    five_list = sorted(mat_row,reverse=True)[:10]
    for i in five_list:
        if i > 0:
            location = mat_row.index(i)
            loc_list.append((item_all[location],i))
            mat_row[location] = 0
        else:
            break
    return loc_list


def output(kafang_matrix,path_output,item_all):
    output_list = {}
    output_content = open(path_output,'w')
    for word in kafang_matrix.keys():
        loc_list = select(kafang_matrix[word],item_all)
        output_list[word] = loc_list
        output_content.write(word)
        output_content.write('\t')
        print loc_list
        for j in loc_list[:-1]:
            output_content.write(j[0])
            output_content.write('\001')
        output_content.write(loc_list[-1][0])
        output_content.write('\n')
    output_content.close()
    return output_list



if __name__ == '__main__':
    start = time.clock()
    items,item_all,content_words = read_yuliao(path_yuliao,2)
    word_all = read_word(path_words)
    item_dic = item_dic_count(items,item_all)
    kafang_dic = fun_kafang_dic(content_words,item_dic,items,item_all ,word_all)
    kafang_matrix = fun_kafang(kafang_dic,item_all,item_dic,len(items))
    output_list = output(kafang_matrix,path_output,item_all)
    end = time.clock()
    time_use = end-start
    print "time:",time_use
