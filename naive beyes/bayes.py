#coding=utf-8
from numpy import *

def loadTrainData(trainFile):
    fp = open(trainFile)
    lines = fp.readlines()
    docLabel, docVec = [], []
    for tmp in lines:
        line = tmp.strip().split(' ')
        docLabel.append(int(line[0]))
        docVec.append([int(i) for i in line[1:]])
    return docLabel, docVec       #both are int type

def loadTestData(testFile):
    fp = open(testFile)
    lines = fp.readlines()
    testLabel, testVec = [], []
    for tmp in lines:
        line = tmp.strip().split(' ')
        testLabel.append(int(line[0]))
        testVec.append([int(i) for i in line[1:]])
    return testLabel, testVec        #both are int type

def naiveBayes(trainFile, k):    #The k should be identical with feature numbers in every class
    docLabel, docVec = loadTrainData(trainFile)
    docArr = array(docVec)
    countNj = ones((10))+1                             #one dimension array
    length = len(docLabel)
    countVecIJ = ones((10, k*10))
    for j in range(length):
        countNj[docLabel[j]] += 1                   #count the docs of different classes
        countVecIJ[docLabel[j], :] += docArr[j,:]   #每行的feature向量加到计数向量部分
    pNJ = log(countNj / length)                          #return possibility of every class
    pVecIJ = ones(shape(countVecIJ))
    pNonVecIJ = ones(shape(countVecIJ))          #(10,300)
    for i in range(10):
        pVecIJ[i,:] = log(countVecIJ[i, :] / countNj[i])  #get conditional possibility
        pNonVecIJ[i,:] = log(1.0 - (countVecIJ[i, :] / countNj[i]))
    return pNJ, pVecIJ, pNonVecIJ

def test(pNJ, pVecIJ, pNonVecIJ, testFile, k):     #The k should be identical with feature numbers in every class
    testLabel, testVec = loadTestData(testFile)
    num, right = len(testLabel), 0
    testLabelArr, testArr = array(testLabel), array(testVec)
    for i in range(num):
        docArr = (testArr[i,:]*pVecIJ)+(1-testArr[i,:])*pNonVecIJ      #docArr is two dimension
        sumJ = array(zeros(10))
        for j in range(10):
            sumJ[j] = sum(docArr[j,:]) + pNJ[j]  #wrong!!!here，notice countVECIJ
        ans = sumJ.argsort()[-1]
        if ans == testLabelArr[i]:
            right += 1
    print 'accuracy=', float(right) / num


if __name__ == '__main__':
    ks = [30,40,50,60,80,100]
    for kNum in ks:
        print kNum, 'Features start'
        pNJ, pVecIJ, pNonVecIJ = naiveBayes('train_'+str(kNum), k=kNum)  # call the train function
        test(pNJ, pVecIJ, pNonVecIJ, 'test_'+str(kNum), k=kNum)