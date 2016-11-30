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
# Buscamos los datos in situ
    filename="../Datos_Insitu/"+isfile
    df=pd.read_csv(filename, names=["No","date","PM25"]) # con el formato alex
    df=df.drop(df.index[[0]]) # quitamos el encabezado
# Filtramos los datos invalidos
    filter=(df.PM25=='Sin Data')
    df1=df[~filter]
    filter2=(df1.PM25=='InVld')
    df1=df1[~filter2]
    filter3=(df1.PM25=='Apagado')
    df1=df1[~filter3]
    filter4=(df1.PM25=='RS232')
    df1=df1[~filter4]
    filter5=(df1.PM25=='<Muestra')
    df1=df1[~filter5]
# Filtramos los NaN
    filter6=np.isnan(pd.to_numeric(df1.PM25, errors='coerce'))
    df1=df1[~filter6]
# Encontramos el total de datos invalidos por filtro y los sumamos
    invdata=filter.sum()+filter2.sum()+filter3.sum()+filter4.sum()+filter5.sum()
    print "Hay %s datos invalidos de %s datos en %s" %(invdata,len(df),isfile)
# Si todos los datos estan mal, rechazamos ese in situ para esa estacion
    if(invdata==len(df)):
        print isfile+" no sera incluido en el analisis."
# Bloque de busqueda de archivos satelitales (una busqueda por cada in situ)
    if(invdata!=len(df)): # si hay datos buenos en el in situ, continua
        satfilelist=[]
        pm25list=[]
        datelist=[]
        aodlist=[]
        distlist=[]
        estcerc=[]
        estmed=[]
        for satfile in os.listdir("."):
            if satfile.endswith(".csv") and satfile[10:14]==isfile[-8:-4]: # Aqui encontramos el ano del in situ y lo comparamos con los archivos satelitales que sean de ese mismo ano
    #            print satfile
                satfilelist.append(satfile)
        if len(satfilelist)==0 :
            print "No hay archivos de MODIS para el %s" % isfile[-8:-4]
# Miramos la lista de datos disponibles de MODIS para ese ano y encontramos la fecha de cada uno con su nombre respectivo
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

            trange=timedelta(minutes=30) # dejamos media hora antes o despues para encontrar datos validos
            for i in range(len(df1)):
# Pasamos "date" a series de tiempo
                date=(df1["date"].iloc[i])
                day=pd.to_datetime(date).day
                month=pd.to_datetime(date).month
                year=pd.to_datetime(date).year
                hour=pd.to_datetime(date).hour
                minute=pd.to_datetime(date).minute
                if hour < 24 :
                    isdate=datetime(year,month,day,hour,minute)
                if satdate-trange <= isdate <=satdate+trange:
                    dlist.append(isdate)
                    try:
                        pmlist.append(float(df1.PM25.iloc[i]))
                    except:
#                        print i, df1.PM25.iloc[i]
                        print "Valor invalido en pm25, posiblemente %s pero puede haber mas" % df1.PM25.iloc[i]
                        print "Hay que limpiar %s" %isfile
                    if isdate==satdate :
                        pmval=float(df1.PM25.iloc[i])
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

