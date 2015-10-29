#coding:utf-8
__author__ = 'syj'
import  os
import sys
import gensim

path = os.path.abspath(os.path.dirname(sys.argv[0]))
path_property = open("car_degree_dic.txt",'r')
model_w2v = gensim.models.Word2Vec.load_word2vec_format("vectors_test.bin", binary=True)
path_out = "words_degree_list.txt"
path_out_not = "words_degree_list_not_in.txt"
content_out = open(path_out,'w')
content_out_not = open(path_out_not ,'w')
#属性词
def fun_propertyset(path):
    property_set = []
    for line in path.readlines():
        property_set.append(line.strip().split('\t')[0])
    return property_set

#程度词
def fun_degree_set(path):
    degree_set = []
    for line in path.readlines():
        degree_set.append(line.strip().split('\t')[0])
    return degree_set

#情感词
def fun_emotion_set(path):
    emotion_set = []
    for line in path.readlines():
        emotion_set.append(line.strip().split('\t')[0])
    return emotion_set


def word_by_score(property_set,model):
    words_scores_dic = {}
    words_list = []
    for word_p  in property_set:
        try:
            result_w2v = model.most_similar(word_p.decode('utf-8'),topn = 50)
            #result_w2v is a tuple
            for word_w2v in result_w2v:
                if word_w2v[0] in words_scores_dic.keys():
                    words_scores_dic[word_w2v[0]].append(word_w2v[1])
                else:
                    words_scores_dic[word_w2v[0]] = [word_w2v[1]]
        except KeyError,num:
            print KeyError,':',num
            content_out_not.write(word_p+'\n')
    for ww in words_scores_dic.keys():
        words_list.append((ww,sum(words_scores_dic[ww])))
    return sorted(words_list ,key=lambda x:x[1],reverse=True)


if __name__ == '__main__':
    property_set = fun_emotion_set(path_property)
    words_list = word_by_score(property_set,model_w2v)
    for i in words_list:
        print i[0],type(i[0])
        print i[1],type(i[1])
        content_out.write(i[0].encode('utf-8')+'\t'+str(i[1])+'\n')
        print i
    content_out.close()
    content_out_not.close()
