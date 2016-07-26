#plot_all.py
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['figure.figsize'] = 15, 8
df1 = pd.read_csv('headers.txt')
for i in range(0,len(df1.iloc[0])):
    a=df1.iloc[0][i]
    s='estaciones/%sf.txt' % a
    df = pd.read_csv(s)
    syr=float(df.columns[0])
    tot=int(len(df))
    date=np.arange(0,tot)/12.+syr
    plt.plot(date,df,label=list(df1.columns.values)[i])
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=0,
           ncol=4, mode="expand", borderaxespad=1.)
    lgd=plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=0,
           ncol=4, mode="expand", borderaxespad=1.)
    plt.xlabel('Year')
    plt.ylabel('Rel. Humidity ($\%$)')
    sn='estaciones/%sn.txt' % a
    with open (sn, "r") as myfile:
        a=myfile.read().replace('\n', '').replace('LA-','GUAJIRA-').replace('SAN-','S_ANDRES-').replace('NORTE-','N_SANT-').replace('HUIGUAJIRA-','HUILA-')  
plt.title("Monthly Mean Rel. Humidity")
x1,x2,y1,y2 = plt.axis()
plt.axis([1975,2015,y1,y2])
#plt.show()
plt.savefig("all-monthly-mean-hum", bbox_extra_artists=(lgd,), bbox_inches='tight')