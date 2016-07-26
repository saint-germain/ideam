import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
a=sys.argv[1]
print a
mpl.rcParams['figure.figsize'] = 12, 8
s='estaciones/%sf.txt' % a
df = pd.read_csv(s)
syr=float(df.columns[0])
tot=int(len(df))
date=np.arange(0,tot)/12.+syr
plt.plot(date,df)
plt.xlabel('Year')
plt.ylabel('Rel. Humidity ($\%$)')
sn='estaciones/%sn.txt' % a
with open (sn, "r") as myfile:
    a=myfile.read().replace('\n', '').replace('LA-','GUAJIRA-').replace('SAN-','S_ANDRES-').replace('NORTE-','N_SANT-').replace('HUIGUAJIRA-','HUILA-')
plt.title("Monthly Mean Rel. Humidity: "+a)
plt.savefig(a+"-historic-hum")
