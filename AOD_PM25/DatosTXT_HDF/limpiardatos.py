# Este script elimina pixeles muertos y filtra la ubicacion hasta un grado alrededor de Bogota
# Para los datos de MODIS que ya han pasado de hdf a txt a traves de read_mod_aerosol_and_dump_ascii.py
import pandas as pd
import os
filelist=[]
for file in os.listdir("."):
    if file.endswith(".txt"):
        filelist.append(file)
for filename in filelist:
    df=pd.read_csv(filename)
    filter=df.Optical_Depth_Land_And_Ocean!=-9999
    df1=df[filter]
    df1=df1[df1.Latitude < 5.21]
    df1=df1[df1.Latitude > 4.21]
    df1=df1[df1.Longitude > -74.6]
    df1=df1[df1.Longitude < -73.6]
    if len(df1) > 0:
        df1.to_csv(filename[0:22]+'.filtered.csv')
    print filename[0:22]+" tiene %s datos" % len(df1)