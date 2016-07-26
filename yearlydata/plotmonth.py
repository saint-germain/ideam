import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
a=sys.argv[1]
print a
mpl.rcParams['figure.figsize'] = 12, 8
s='estaciones/%s.txt' % a
df = pd.read_csv(s, index_col=False,names='xabcdefghijkl')
df=df.convert_objects(convert_numeric=True)
w=df.mean(axis=0)
dev=df.std(axis=0)
plt.errorbar(np.arange(1,13),w,yerr=dev,fmt='o', ecolor='r')
plt.xlabel('Month')
plt.ylabel('Mean Rel. Humidity ($\%$)')
xlabels=['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
plt.xticks(range(0,13),xlabels)
s1='estaciones/%sf.txt' % a
df1 = pd.read_csv(s1)
syr=int(df1.columns[0])
eyr=syr+len(df1)/12
sn='estaciones/%sn.txt' % a
with open (sn, "r") as myfile:
    a=myfile.read().replace('\n', '').replace('LA-','GUAJIRA-').replace('SAN-','S_ANDRES-').replace('NORTE-','N_SANT-').replace('HUIGUAJIRA-','HUILA-')
x1,x2,y1,y2 = plt.axis()
plt.axis((0,13,y1,y2))
plt.title("Average Rel. Humidity per Month (%s-%s): "% (syr,eyr-1)+a)
plt.savefig(a+"-yrly_pattern-hum")