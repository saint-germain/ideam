# Debe correrlo en DatosTXT_HDF
# Esta es la carpeta donde se corrio el script anterior (limpieza) sobre los hdf
# Debe haber una carpeta paralela que se llama Datos_Insitu, aqui se debe guardar los .csv de los insitu
# segun los nombres de las estaciones que estan en estaciones.csv (este .csv esta en el archivo anterior ..) con la fecha
# por ejemplo kennedy2014.csv o minambiente2007.csv
# el resultado es un archivo que se llama por ejemplo kennedy_data_2013.csv que esta en el ..


import numpy as np

import pandas as pd
import os

from datetime import datetime
from datetime import timedelta
estfile="../estaciones.csv"
edf=pd.read_csv(estfile)
isfilelist=[]
for isfile in os.listdir("../Datos_Insitu/"):
    if isfile.endswith(".csv") and not(isfile.startswith(".")):
        isfilelist.append(isfile)
for isfile in isfilelist:
    filename="../Datos_Insitu/"+isfile
    df=pd.read_csv(filename,skiprows=2)
    df=df.drop(df.index[[0]])
    df=df.drop(df.index[range(len(df)-8,len(df))])
    filter=(df.PM25=='Sin Data')
    df1=df[~filter]
    filter2=(df1.PM25=='InVld')
    df1=df1[~filter2]
    filter3=(df1.PM25=='Apagado')
    df1=df1[~filter3]
    filter4=(df1.PM25=='RS232')
    df1=df1[~filter4]
    print "Hay %s datos invalidos de %s datos en %s" %(filter.sum()+filter2.sum()+filter3.sum()+filter4.sum(),len(df),isfile)
    satfilelist=[]
    pm25list=[]
    datelist=[]
    aodlist=[]
    distlist=[]
    estcerc=[]
    estmed=[]
    for satfile in os.listdir("."):
        if satfile.endswith(".csv") and satfile[10:14]==isfile[-8:-4]:
#            print satfile
            satfilelist.append(satfile)
    if len(satfilelist)==0 :
        print "No hay archivos de MODIS para el %s" % isfile[-8:-4]
    for satfile in satfilelist:
        success=False
        sdf=pd.read_csv(satfile)
        satyear=satfile[10:14]
        satyear=int(satyear)
        satday=satfile[14:17]
        satday=int(satday)
        sathour=satfile[18:20]
        sathour=int(sathour)
        satmin=satfile[20:22]
        satmin=int(satmin)

        start=datetime(satyear,01,01)
        satdate=start+timedelta(days=satday-1,hours=sathour,minutes=satmin)
        dlist=[]
        pmlist=[]

        trange=timedelta(minutes=30)
        for i in range(len(df1)):
            date=(df1["Fecha & Hora"].iloc[i])
            day=int(date[0:2])
            month=int(date[3:5])
            year=int(date[6:10])
            hour=int(date[11:13])
            minute=int(date[14:16])
            if hour < 24 :
                isdate=datetime(year,month,day,hour,minute)
            if satdate-trange <= isdate <=satdate+trange:
                dlist.append(isdate)
                try:
                    pmlist.append(int(df1.PM25.iloc[i]))
                except:
                    print "Valor invalido en pm25, posiblemente %s pero puede haber mas" % np.unique(df1.PM25)[-1]
                    print "Hay que limpiar %s" %isfile
                if isdate==satdate :
                    pmval=int(df1.PM25.iloc[i])
                    dtval=satdate
                    success=True
            if isdate > satdate+trange:
                break
        pmdf=pd.DataFrame({'Date' : dlist, 'PM25': pmlist})
        if len(pmdf) > 0 :
            stname=isfile.replace("%s.csv"%year,"").upper()
            for i in range(len(edf)):
                if edf.ESTACION.iloc[i]==stname:

                    lat=edf.LATITUD.iloc[i]
                    lon=edf.LONGITUD.iloc[i]        
            distance=np.sqrt((sdf.Latitude-lat)**2+(sdf.Longitude-lon)**2)*111.325
            ixcl=np.argmin(distance)   
            slat=sdf.Latitude.iloc[ixcl]
            slon=sdf.Longitude.iloc[ixcl]
            ixce=np.argmin((edf.LATITUD-slat)**2+(edf.LONGITUD-slon)**2)
            print "Para la estacion %s, el satelite pasa a %.2f km (%s,%s)" %(stname,distance[ixcl],day,month)
            if edf.ESTACION.iloc[ixce]!=stname :
                print "Sin embargo, la estacion mas cercana al punto por donde paso el satelite es %s" % edf.ESTACION.iloc[ixce]
            aodlist.append(sdf.Optical_Depth_Land_And_Ocean.iloc[ixcl])    
            distlist.append(distance[ixcl])
            estcerc.append(edf.ESTACION.iloc[ixce])
            estmed.append(stname)
            print "ODLAO =",sdf.Optical_Depth_Land_And_Ocean.iloc[ixcl],", PM25 = ", pmdf.PM25.iloc[0]
            if success:
                pm25list.append(pmval)
                datelist.append(satdate)
            else:
                pm25list.append(pmdf.PM25.iloc[0])
                datelist.append(pmdf.Date.iloc[0])
#            print datelist[-1], pm25list[-1],aodlist[-1],distlist[-1]
    pd.DataFrame({'Date' : datelist,'PM25' : pm25list, 'AOD' : aodlist, 'Dist' : distlist, 'EstCerc': estcerc, 'EstMed': estmed}).to_csv("../%s_data_%s.csv"%(stname,isfile[-8:-4]))
