本方案使用的是互信息提取每个类别的特征，根据总特征构建1990篇文档的向量表示，利用伯努利型贝叶斯模型训练模型，最后测试验证集。
使用手册：
getFeature.py:
	1.写出代用的classes的list
	2.用file2Dict函数，将1990篇文档的内容变为集合表示，[class1set, class2set,……,class10set], [doc1set, doc2set, ……, doc1990set]	3.featureToUse()函数用于构建每个类别的feature。算出每个class里的每个word的互信息，选择排序最大的k个feature。
	4.file2Words()、loadDocData、loadclassData、compute、computeMI都是辅助函数
preprocessing.py:
	1.buildVec用于把1990篇文档的词向量list用0 1表示并写入文件，需要给定匹配的featureFile的name，并写入目标file
	2.随机把feature 0 1表示的文档分隔为训练集和测试集用于后续训练
bayes.py：
	1.首先用naiveBayes训练训练集，需给定互相匹配的trainFile和k。
	2.test函数用于测试。
	3.loadTrainData、loadTestData是辅助函数。
	