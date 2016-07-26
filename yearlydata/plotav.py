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
s1='estaciones/%sf.txt' % a
df1 = pd.read_csv(s1)
syr=float(df1.columns[0])
w=df.mean(axis=1)
plt.plot(np.arange(syr,len(w)+syr),w)
plt.xlabel('Year')
plt.ylabel('Mean Rel. Humidity ($\%$)')
sn='estaciones/%sn.txt' % a
with open (sn, "r") as myfile:
    a=myfile.read().replace('\n', '').replace('LA-','GUAJIRA-').replace('SAN-','S_ANDRES-').replace('NORTE-','N_SANT-').replace('HUIGUAJIRA-','HUILA-')
plt.title("Yearly Mean Rel. Humidity: "+a)
plt.savefig(a+"-historic_yr-hum")