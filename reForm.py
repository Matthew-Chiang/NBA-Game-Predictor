import numpy as np

try:
    for i in range (0,50):
        date = 20170401  + i
        repl = 'DataSets/' + str(date) + '.csv'
        my_data = np.genfromtxt(repl, delimiter=',')
        my_data = my_data[1:,1:]


        np.savetxt(repl,my_data,delimiter=",")

except IndexError:
    print(repl)
