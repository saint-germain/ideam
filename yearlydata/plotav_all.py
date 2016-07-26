import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['figure.figsize'] = 15, 8
df1 = pd.read_csv('headers.txt')

for i in range(0,len(df1.iloc[0])):
    a=df1.iloc[0][i]
    s='estaciones/%s.txt' % a
    df = pd.read_csv(s)
    df=df.convert_objects(convert_numeric=True)
    s1='estaciones/%sf.txt' % a
    df2 = pd.read_csv(s1)
    syr=float(df2.columns[0])
    w=df.mean(axis=1)
    plt.plot(np.arange(syr,len(w)+syr),w,label=list(df1.columns.values)[i])
    plt.xlabel('Year')
    plt.ylabel('Mean Rel. Humidity ($\%$C)')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=4, mode="expand", borderaxespad=1.)
    lgd=plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=4, mode="expand", borderaxespad=1.)    
    sn='estaciones/%sn.txt' % a
    with open (sn, "r") as myfile:
        a=myfile.read().replace('\n', '').replace('LA-','GUAJIRA-').replace('SAN-','S_ANDRES-').replace('NORTE-','N_SANT-').replace('HUIGUAJIRA-','HUILA-')
plt.title("Yearly Mean Rel. Humidity")
x1,x2,y1,y2 = plt.axis()
plt.axis([1975,2015,y1,y2])
plt.savefig("all-yearly-mean-hum", bbox_extra_artists=(lgd,), bbox_inches='tight')
#plt.show()