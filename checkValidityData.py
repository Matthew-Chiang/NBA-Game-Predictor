import numpy as np

for i in range(0,50):
    dateint = 20170401 + i
    date = str(dateint)

    trainingSet = np.genfromtxt("DataSets - Copy/" + date + ".csv",delimiter=',')
    testingSet = np.genfromtxt("Labels - Copy/" + date + ".csv",delimiter=',')
    try:
        if trainingSet.shape[0] != testingSet.shape[0]:
            print("not matching sizes")
            print(date)
        if trainingSet.shape[1] != 312:
            print("not 312")
            print(date)
    except IndexError:
        print("ERROR")
        print(date)
