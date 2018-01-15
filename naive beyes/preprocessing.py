#coding=utf-8

def randomDoc_Split(fileName, per = 0.2, k=50):        #use random before buildVec。打乱文档的种类，便于使用k-fold validation
    from numpy import random
    fp = open(fileName, 'r')
    docs = fp.readlines()
    fp.close()
    fp_train = open('train_'+str(k), 'w')
    fp_test = open('test_'+str(k), 'w')
    chang = len(docs)
    indices = range(chang)
    test_UP, j = int(per * chang), 0
    for i in range(chang):
        x = random.randint(0,len(indices))      #a good function, not random_integers
        if j <= test_UP:
            fp_test.write(docs[indices[x]])
        else:
            fp_train.write(docs[indices[x]])
        del indices[x]
        j += 1
    fp_train.close()
    fp_test.close()

def buildVec(featureFile, docsFile):
    #convert the features in every doc into 0 or 1, then wirte into file
    from getFeature import loadDocData
    docDict, docLabels = loadDocData()
    fp = open(featureFile, 'r')
    lines = fp.readlines()
    features = []   #vector of features
    for line in lines:
        tmp = line.strip().split(' ')
        for fea in tmp:
            features.append(fea)
    fp.close()
    fpw = open(docsFile, 'w')
    length = len(docLabels)
    for i in range(length):
        fpw.write(str(docLabels[i]))
        for item in features:
            if item in docDict[i]:    #在doc里面的vec值为1
                fpw.write(' 1')
            else:
                fpw.write(' 0')
        fpw.write('\n')
    fpw.close()

if __name__ == '__main__':
    print 'start!!!'
    buildVec('feature_30.txt', 'docVec_30.txt')
    randomDoc_Split('docVec_30.txt', per=0.2, k=30)
    print '1 done'
    buildVec('feature_40.txt', 'docVec_40.txt')
    randomDoc_Split('docVec_40.txt',per=0.2, k=40)
    print '2 done'
    buildVec('feature_50.txt', 'docVec_50.txt')
    randomDoc_Split('docVec_50.txt',per=0.2, k=50)
    print '3 done'
    buildVec('feature_60.txt', 'docVec_60.txt')
    randomDoc_Split('docVec_60.txt',per=0.2, k=60)
    print '4 done'
    buildVec('feature_80.txt', 'docVec_80.txt')
    randomDoc_Split('docVec_80.txt',per=0.2, k=80)
    print '5 done'
    buildVec('feature_100.txt', 'docVec_100.txt')
    randomDoc_Split('docVec_100.txt',per=0.2, k=100)
    print '6 done'