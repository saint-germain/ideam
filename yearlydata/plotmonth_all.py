import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['figure.figsize'] = 15,8
df1 = pd.read_csv('headers.txt')

for i in range(0,len(df1.iloc[0])):
    a=df1.iloc[0][i]
    s='estaciones/%s.txt' % a
    df = pd.read_csv(s, index_col=False,names='xabcdefghijkl')
    df=df.convert_objects(convert_numeric=True)
    w=df.mean(axis=0)
    dev=df.std(axis=0)
    plt.errorbar(np.arange(1,13),w,yerr=dev,fmt='o',label=list(df1.columns.values)[i])
#    plt.plot(np.arange(1,13),w,label=list(df1.columns.values)[i])
    plt.xlabel('Month')
    plt.ylabel('Mean Rel. Humidity ($\%$)')
    xlabels=['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    plt.xticks(range(0,13),xlabels)
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=4, mode="expand", borderaxespad=1.)
    lgd=plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=4, mode="expand", borderaxespad=1.)
    s1='estaciones/%sf.txt' % a
    df2 = pd.read_csv(s1)
    syr=int(df2.columns[0])
    eyr=syr+len(df2)/12
    sn='estaciones/%sn.txt' % a
    with open (sn, "r") as myfile:
        a=myfile.read().replace('\n', '').replace('LA-','GUAJIRA-').replace('SAN-','S_ANDRES-').replace('NORTE-','N_SANT-').replace('HUIGUAJIRA-','HUILA-')
    print "junk",list(df1.columns.values)[i]
    print dev
plt.title("Average Rel. Humidity per Month (%s-%s) "% (1978,2015))
x1,x2,y1,y2 = plt.axis()
plt.axis((0,13,y1,y2))
#plt.show()
plt.savefig("all-yrly-pat-hum", bbox_extra_artists=(lgd,), bbox_inches='tight')