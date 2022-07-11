import os
import time
import numpy as np
import pandas as pd
import csv
import math
import random
from sklearn.model_selection import KFold,StratifiedKFold
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import StratifiedKFold
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from scipy import interp
from itertools import cycle
from sklearn.model_selection import KFold,LeaveOneOut,LeavePOut,ShuffleSplit



def ReadMyCsv(SaveList, fileName):
    csv_reader = csv.reader(open(fileName))
    for row in csv_reader:
        for i in range(len(row)):
            row[i] = float(row[i])
        SaveList.append(row)
    return

def storFile(data, fileName):
    with open(fileName, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    return

def MyEnlarge(x0, y0, width, height, x1, y1, times, mean_fpr, mean_tpr, thickness=1, color = 'blue'):
    def MyFrame(x0, y0, width, height):
        import matplotlib.pyplot as plt
        import numpy as np

        x1 = np.linspace(x0, x0, num=20)
        y1 = np.linspace(y0, y0, num=20)
        xk = np.linspace(x0, x0 + width, num=20)
        yk = np.linspace(y0, y0 + height, num=20)

        xkn = []
        ykn = []
        counter = 0
        while counter < 20:
            xkn.append(x1[counter] + width)
            ykn.append(y1[counter] + height)
            counter = counter + 1

        plt.plot(x1, yk, color='k', linestyle=':', lw=3, alpha=1)
        plt.plot(xk, y1, color='k', linestyle=':', lw=3, alpha=1)
        plt.plot(xkn, yk, color='k', linestyle=':', lw=3, alpha=1)
        plt.plot(xk, ykn, color='k', linestyle=':', lw=3, alpha=1)

        return

    width2 = times * width
    height2 = times * height
    MyFrame(x0, y0, width, height)
    MyFrame(x1, y1, width2, height2)


    xp = np.linspace(x0 + width, x1, num=20)
    yp = np.linspace(y0, y1 + height2, num=20)
    plt.plot(xp, yp, color='k', linestyle=':', lw=2, alpha=1)


    XDottedLine = []
    YDottedLine = []
    counter = 0
    while counter < len(mean_fpr):
        if mean_fpr[counter] > x0 and mean_fpr[counter] < (x0 + width) and mean_tpr[counter] > y0 and mean_tpr[counter] < (y0 + height):
            XDottedLine.append(mean_fpr[counter])
            YDottedLine.append(mean_tpr[counter])
        counter = counter + 1


    counter = 0
    while counter < len(XDottedLine):
        XDottedLine[counter] = (XDottedLine[counter] - x0) * times + x1
        YDottedLine[counter] = (YDottedLine[counter] - y0) * times + y1
        counter = counter + 1


    plt.plot(XDottedLine, YDottedLine, color=color, lw=2, alpha=1)
    return

def MyConfusionMatrix(y_real,y_predict):
    from sklearn.metrics import confusion_matrix
    CM = confusion_matrix(y_real, y_predict)
    print(CM)
    CM = CM.tolist()
    TN = CM[0][0]
    FP = CM[0][1]
    FN = CM[1][0]
    TP = CM[1][1]
    print('TN:%d, FP:%d, FN:%d, TP:%d' % (TN, FP, FN, TP))
    Acc = (TN + TP) / (TN + TP + FN + FP)
    Sen = TP / (TP + FN)
    Spec = TN / (TN + FP)
    Prec = TP / (TP + FP)
    MCC = (TP * TN - FP * FN) / math.sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN))

    print('Acc:', round(Acc, 4))
    print('Sen:', round(Sen, 4))
    print('Spec:', round(Spec, 4))
    print('Prec:', round(Prec, 4))
    print('MCC:', round(MCC, 4))
    Result = []
    Result.append(round(Acc, 4))
    Result.append(round(Sen, 4))
    Result.append(round(Spec, 4))
    Result.append(round(Prec, 4))
    Result.append(round(MCC, 4))
    return Result

def MyAverage(matrix):
    SumAcc = 0
    SumSen = 0
    SumSpec = 0
    SumPrec = 0
    SumMcc = 0
    counter = 0
    while counter < len(matrix):
        SumAcc = SumAcc + matrix[counter][0]
        SumSen = SumSen + matrix[counter][1]
        SumSpec = SumSpec + matrix[counter][2]
        SumPrec = SumPrec + matrix[counter][3]
        SumMcc = SumMcc + matrix[counter][4]
        counter = counter + 1
    print('AverageAcc:', SumAcc / len(matrix))
    print('AverageSen:', SumSen / len(matrix))
    print('AverageSpec:', SumSpec / len(matrix))
    print('AveragePrec:', SumPrec / len(matrix))
    print('AverageMcc:', SumMcc / len(matrix))
    return

def MyStd(result):
    import numpy as np
    NewMatrix = []
    counter = 0
    while counter < len(result[0]):
        row = []
        NewMatrix.append(row)
        counter = counter + 1
    counter = 0
    while counter < len(result):
        counter1 = 0
        while counter1 < len(result[counter]):
            NewMatrix[counter1].append(result[counter][counter1])
            counter1 = counter1 + 1
        counter = counter + 1
    StdList = []
    MeanList = []
    counter = 0
    while counter < len(NewMatrix):

        arr_std = np.std(NewMatrix[counter], ddof=1)
        StdList.append(arr_std)

        arr_mean = np.mean(NewMatrix[counter])
        MeanList.append(arr_mean)
        counter = counter + 1


    result.append(MeanList)
    result.append(StdList)

    counter = 0
    while counter < len(result):
        counter1 = 0
        while counter1 < len(result[counter]):
            result[counter][counter1] = round(result[counter][counter1] * 100, 2)
            counter1 = counter1 + 1
        counter = counter + 1

    counter = 0
    while counter < len(StdList):
        result[5][counter] = str(result[5][counter]) + str('+') + str(result[6][counter])
        counter = counter + 1

    return result

tprs = []
aucs = []
mean_fpr = np.linspace(0, 1, 1000)
i = 0
colorlist = ['red', 'gold', 'purple', 'green', 'blue', 'black']


AllResult = []

counter0 = 0
while counter0 < 5:
    print(i)

    RealAndPrediction = []
    RealAndPredictionProb = []
    RAPName = 'RealAndPredictionA+B' + str(counter0) + '.csv'
    RAPNameProb = 'RealAndPredictionProbA+B' + str(counter0) + '.csv'
    ReadMyCsv(RealAndPrediction, RAPName)
    ReadMyCsv(RealAndPredictionProb, RAPNameProb)

    Real = []
    Prediction = []
    PredictionProb = []
    counter = 0
    while counter < len(RealAndPrediction):
        Real.append(int(RealAndPrediction[counter][0]))
        Prediction.append(RealAndPrediction[counter][1])
        PredictionProb.append(RealAndPredictionProb[counter][1])
        counter = counter + 1


    fpr, tpr, thresholds = roc_curve(Real,PredictionProb)

    fpr = fpr.tolist()
    tpr = tpr.tolist()
    fpr.insert(0, 0)
    tpr.insert(0, 0)
    tprs.append(interp(mean_fpr, fpr, tpr))
    tprs[-1][0] = 0.0
    roc_auc = auc(fpr, tpr)
    aucs.append(roc_auc)
    plt.plot(fpr, tpr, lw=2, alpha=0.8, color=colorlist[i],
             label='fold %d (AUC = %0.4f)' % (i+1, roc_auc))


    MyEnlarge(0.1, 0.6, 0.2, 0.2, 0.2, 0, 2, mean_fpr, tprs[i], 1.5, colorlist[i])


    Result = MyConfusionMatrix(Real, Prediction)
    AllResult.append(Result)
    AllResult[i].append(roc_auc)

    i += 1
    counter0 = counter0 + 1


MyAverage(AllResult)


MyNew = MyStd(AllResult)
storFile(MyNew, '五折的表（由保存值生成）.csv')
print(MyNew)


mean_tpr = np.mean(tprs, axis=0)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
std_auc = np.std(aucs)
print('mean_fpr', mean_fpr)
print('mean_tpr', mean_tpr)

FprAndTpr = []
counter = 0
while counter < len(mean_fpr):
    pair = []
    pair.append(mean_fpr[counter])
    pair.append(mean_tpr[counter])
    FprAndTpr.append(pair)
    counter = counter + 1
storFile(FprAndTpr, 'RNAInterFprAndTprA+B.csv')
plt.plot(mean_fpr, mean_tpr, color='black',
         label=r'Mean (AUC = %0.4f)' % (mean_auc),
         lw=3, alpha=1)



plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.xlabel('False Positive Rate',fontsize=15)
plt.ylabel('True Positive Rate',fontsize=15)

plt.legend(bbox_to_anchor=(0.57, 0.84))


plt.savefig('ROC-5fold.svg')
plt.savefig('ROC-5fold.tif')
plt.show()























