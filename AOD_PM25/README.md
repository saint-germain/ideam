Scripts para limpiar datos de MODIS para encontrar correlacion entre PM2.5 y AOD.
Todos los .hdf deben estar en DatosTXT_HDF
Todos los datos in situ deben estar como .csv en Datos_Insitu, con el mismo formato, p.ej. NOMBREESTACION2015.csv

Requiere tener pyhdf. Instrucciones:

OSX: 
* En mac es un poco enredado, hay que instalar hdf4 desde macports, verificar la ubicacion de los contenidos (`port contents hdf4`)
* Descargar pyhdf de http://hdfeos.org/software/pyhdf.php
* Compilar con las variables de entorno que esten de acuerdo con la ubicacion de los contenidos de las librerias de hdf4
~~~~
export INCLUDE_DIRS=/opt/local/include
export LIBRARY_DIRS=/opt/local/lib
sudo python setup.py install -i $INCLUDE_DIRS -l $LIBRARY_DIRS 
~~~~

Ubuntu: Se requiere `libhdf4-dev` y `python-hdf4`

0. Generar la lista de archivos para convertir de .hdf a .txt (fileList.txt).
~~~~
sh createfilelist.sh
~~~~
2. Convertir .hdf a .txt con ´python read_mod_aerosol_and_dump_ascii.py´
3. Filtrar datos con pixeles muertos y a un grado alrededor de Bogota con ´python extractor.py´en DatosTXT_HDF. Esto genera archivos pequeños con nombres como MOD04_3K.A2012002.1540.filtered.csv
4. Hacer la comparacion entre datos in situ y satelitales con `python extractor.py`en DatosTXT_HDF. Esto genera en .. un archivo llamado como NOMBREESTACION_data_2015.csv
5. Hacer el analisis con el cuaderno Analisis_AOD_PM25.ipynb
