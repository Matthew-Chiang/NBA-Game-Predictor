import numpy as np

data = np.genfromtxt("DataSets/testingSet.csv",delimiter=',')

print(type(data[1][1]))

#np.random.shuffle(data)

#np.savetxt("DataSets/shuffledTestingSet.csv",data,delimiter=",")
