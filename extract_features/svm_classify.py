from sklearn import svm
import csv
import numpy as np

pos_dict = ["START","STOP","JJ","NN","``","-LRB-","WRB","LS","PRP","DT","NNP","FW","NNS","JJS","JJR","UH","$.","MD","VBD","WP","VBG","CC","''","CD","PDT","RBS","VBN","RBR","#","$","IN","VBP","WDT","SYM","NNPS","WP$","','","VB",".","VBZ","RB","PRP$","EX","POS","-RRB-",":","TO","RP","NULL"]

label_vector = []
data_vector = []
testing_vector = []
test_labels = []
precisions=[]
recalls = []
fscores = []

def compare(classer, gold):
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for x in range(0,len(classer)):
        if gold[x] == '0':
            if classer[x] == '0':
                tn += 1
            else:
                fp += 1
        else:
            if classer[x] == '1':
                tp += 1
            else:
                fn += 1
    precision = float(tp) / float (tp + fp)
    precisions.append(precision)
    recall = float(tp) / float(tp + fn)
    recalls.append(recall)
    fscore = 2 * (precision * recall) / (precision + recall)
    fscores.append(fscore)
#print "Precision: ", precision

#print "Recall: ", recall
#print "Fscore: ", fscore

def main():
    kernel = ['rbf'] #['rbf', 'linear'] 'sigmoid', 
    C = [1.0, 5.0, 10.0, 20.0, 50.0, 100.0] #0.001, 0.01, 0.05, 0.1, 0.5, 
    gamma = [0.001, 0.01, 0.1, x0.5, 1.0, 5.0, 10.0]
    #degree = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    folds = [[0,222],[222,444],[444,666],[666,888],[888,1110],[1110,1332],[1332,1554],[1554,1776],[1776,1998],[1998,2220]]

    for k in range(0, len(kernel)):
        for c in range(0, len(C)):
            for g in range(0, len(gamma)):
                precisions[:]=[]
                recalls[:] = []
                fscores[:] = []
            #for d in range(0, len(degree)):
                print "PARAMS: [kernel=",kernel[k], ", C=",C[c], ", degree=", gamma[g], "]"
                for i in range(0,len(folds)):
                    label_vector[:] = []
                    data_vector[:] = []
                    testing_vector[:] = []
                    test_labels[:] = []
                    with open("/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/extract_features/out_vecs_300.csv", 'rU') as infile:
                        reader = csv.reader(infile)
                        count = 0
                        for line in reader:
                            newline = line[0:300]
                            newline.append(float(line[301])/float(99))
                            newline.append(float(line[302]))
                            pos_2 = [0] * 49
                            pos_2[pos_dict.index(line[303])] = 1
                            newline = newline + pos_2
                            pos_1 = [0] * 49
                            pos_1[pos_dict.index(line[304])] = 1
                            newline = newline + pos_1
                            pos = [0] * 49
                            pos[pos_dict.index(line[305])] = 1
                            newline = newline + pos
                            pos1 = [0] * 49
                            pos1[pos_dict.index(line[306])] = 1
                            newline = newline + pos1
                            pos2 = [0] * 49
                            pos2[pos_dict.index(line[307])] = 1
                            newline = newline + pos2
                            newline.append(line[309])
        
                            if folds[i][0] <= count and count < folds[i][1]:
                                data_vector.append(newline)
                                label_vector.append(line[310])
                            else:
                                testing_vector.append(newline)
                                test_labels.append(line[310])
                            count += 1
                       
                        classifier = svm.SVC(C=C[c], kernel=kernel[k], gamma=gamma[g])
                        classifier.fit(data_vector, label_vector)

                        classifier_results = classifier.predict(testing_vector)
    #print classifier.score(testing_vector,test_labels)
                        compare(classifier_results, test_labels)
                print "Mean precision: ", np.mean(precisions)
                print "Mean recall: ", np.mean(recalls)
                print "Mean fscore: ",np.mean(fscores)
                       
main()

                       
        