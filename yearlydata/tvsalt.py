import subprocess
import sys
a=sys.argv[1]
cmd = "grep -A 55 'MEDIOS  DIARIOS DE TEMPERATURA' IDEAM.txt | grep -A55 'ANO  {0}' | grep -A2 'VALORES  ANUALES' | grep MEDIA | awk '{{print $2}}' > {0}mean.txt".format(a)
p = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.wait()
cmd = "grep -A 60 'MEDIOS  DIARIOS DE TEMPERATURA' IDEAM.txt | grep -A4 'ANO  {0}' | grep ELEVACION | awk '{{print $2}}' > {0}alt.txt".format(a)
p = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.wait()
cmd = "paste -d',' {0}alt.txt {0}mean.txt > {0}tvsa.txt ; rm {0}alt.txt ;rm {0}mean.txt".format(a)
p = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.wait()
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['figure.figsize'] = 12,8
df5 = pd.read_csv('%stvsa.txt' % a,index_col=False,names='ab')
plt.scatter(df5.a,df5.b)
plt.xlabel('Altitude')
plt.ylabel('Temperature ($^\circ$C)')
plt.title('Mean Temperature for %s - All stations' % a)
plt.savefig('%stvsalt' % a)