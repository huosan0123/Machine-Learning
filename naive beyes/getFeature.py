#coding=utf-8

import jieba.analyse
import os
import codecs
from numpy import *

def file2Words(fileName):
    fp = open(fileName)
    content = ''
    for line in fp.readlines():
        tmp = line.strip()
        content = content + tmp
    words = jieba.cut(content)
    uniqueWords = set([word for word in words if len(word)>=2])
    return uniqueWords

def files2Dict(classes):
    path = os.getcwd()+'\\documents collection\\'
    files = os.listdir(path)
    labelsDict = [set() for i in range(10)]    #important2
    fp1 = codecs.open('docs.txt', 'w','utf-8')
    for fileName in files:
        for index, label in enumerate(classes):
            if label in fileName:
                pos = index
                break
        fp1.write(str(pos))       #写入下标，相当于写入类别
        uniqueWords = file2Words(path+fileName)   #get string object in a doc
        for word in uniqueWords:
            fp1.write(' '+word)
            if word not in labelsDict[pos]:
                labelsDict[pos].add(word)
        fp1.write('\n')
    fp1.close()
    fp2 = codecs.open('classDict.txt', 'w','utf-8')
    for i in range(10):
        fp2.write(str(i))
        for item in labelsDict[i]:
            fp2.write(' '+item)
        fp2.write('\n')
    fp2.close()

def loadDocData():
    docDict, docLabels = [], []
    fp1 = open('docs.txt', 'r')
    for line in fp1.readlines():
        tmp = line.strip().split(' ')
        docLabels.append(int(tmp[0]))
        docDict.append(tmp[1:])
    fp1.close()
    return docDict, docLabels    ##label is int, dict is string

def loadClassData():
    classDict, classLabels = [],[]
    fp2 = open('classDict.txt', 'r')
    for line in fp2.readlines():
        tmp = line.strip().split(' ')
        classLabels.append(int(tmp[0]))
        classDict.append(tmp[1:])
    fp2.close()
    return classDict, classLabels     #label is int, dict is string

def compute(outup, outdown, inup, indown):
    return (outup/outdown)*log(inup/indown)

def computeMI(N11, N00, N10, N01):
    N = N11 + N00 + N10 + N01
    N1dot = N11 + N10
    Ndot1 = N01 + N11
    N0dot = N00 + N01
    Ndot0 = N00 + N10
    part1 = compute(N11, N, N * N11, N1dot * Ndot1)
    part2 = compute(N01, N, N * N01, N0dot * Ndot1)
    part3 = compute(N10, N, N * N10, N1dot * Ndot0)
    part4 = compute(N00, N, N * N00, N0dot * Ndot0)
    return part1+part2+part3+part4


def featureToUse(outName, k=50):      #select features based on MI
    docDict, docLabels = loadDocData()
    classDict, classLabels = loadClassData()
    print classLabels
    N = len(docLabels)
    fp = open(outName, 'w')
    for j in range(10):  #for each class       #should be 10
        print j, len(classDict[j])          #从这里其实获得每个class的编号
        miList = []
        for term in classDict[j]:    #某类里面的每一个词，计算该词和该类的互信息
            N00, N11 = 1, 1
            N01, N10 = 1, 1
            for i in range(N):    #should be N
                if docLabels[i] == classLabels[j]: #如果该文档属于这一类
                    if term in docDict[i]:         #并且该词出现在该文档中
                        N11 += 1
                    else:
                        N01 += 1
                else:
                    if term in docDict[i]:
                        N10 += 1
                    else:
                        N00 += 1
            termMI = computeMI(float(N11), float(N00), float(N10), float(N01))
            miList.append(termMI)
        miListCopy = array(miList)
        sortedIndex = miListCopy.argsort()[::-1]   #利用argsort和list切片实现降序排列
        for i in range(k):
            feature = classDict[j][sortedIndex[i]]  #按照类别的0-9下标顺序依次写入选择的feature
            fp.write(feature+' ')
        fp.write('\n')      #便于查看结果，不便于后续处理
    fp.close()

if __name__ == '__main__':
    classes = ('Sports', 'Politics', 'Medical', 'Economy', 'Agriculture',
               'Enviornment', 'Transport', 'Space', 'Education', 'Art')
    files2Dict(classes)  #将1990篇文档转换成两个set，写入文件
    featureToUse('feature_30.txt', k=30)   #计算互信息，选出最大的
    featureToUse('feature_40.txt', k=40)
    featureToUse('feature_60.txt', k=60)
    featureToUse('feature_80.txt', k=80)
    featureToUse('feature_100.txt', k=100)




