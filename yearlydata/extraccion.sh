# Unzip and remove junk
unzip IDEAM.txt.zip
rm -r __MACOSX/
# Get relevant data, cut to remove ancillary data, remove DOS end-of-line character, remove asterisks, write only T data to temp.txt using 12 columns (one p/ month), write to temp.txt
# In OSX, use gcut instead of cut, as the OSX version of cut doesn’t like —option-delimiter
grep -A 45 'MEDIOS  DIARIOS DE TEMPERATURA' IDEAM.txt | grep MEDIA | gcut -c22-25,31-34,40-43,49-52,58-61,67-70,76-79,85-88,94-97,103-106,112-115,121-124 --output-delimiter=' ,' | tr -d '\015' | sed 's/\*/ /g' > temp.txt
# Delete leading spaces before temps > 0, write to temp
sed 's/, \([0-9]\)/,\1/g' temp.txt > utemp.txt ; mv utemp.txt temp.txt
# Add a comma before each line (to properly count nr. of fields <=12). At this point empty fields are not recognized as fields.
sed 's/^/,/g' temp.txt > utemp.txt ; mv utemp.txt temp.txt
# Count nr. of fields < 12 for each line in temp, write to fields.txt
awk '{if (NF<12) print (12-NF)*6-1;else print 0 }' temp.txt > fields.txt
# Get required number of spaces to even out (from the right) temp.txt
awk '{print "printf " "'\''%"$1"s\\n'\''"}' fields.txt | /bin/sh > spaces.txt
# Paste side-by-side temp.txt with required spaces from spaces.txt
paste -d" " temp.txt spaces.txt > utemp.txt ; mv utemp.txt temp.txt
# Replace spaces with comma-separated fields (to get 12 fields p/line)
sed 's/      / ,    /g' temp.txt > utemp.txt ; mv utemp.txt temp.txt
# Get year+station tag for each line in temp.txt
grep -A2 'MEDIOS  DIARIOS DE TEMPERATURA' IDEAM.txt | grep ANO | awk '{print $7,$10}' > temptag.txt
# Join yr+st tags with temp.txt, write to jtemp.txt
paste temptag.txt temp.txt > jtemp.txt
# Get unique list of station codes, write to tags.txt
cut -c6-14 jtemp.txt | uniq > tags.txt
# This block writes to a file for each station.
# Create subdirectory
mkdir estaciones
# Split jtemp into files for each station, write to (stationcode).txt
awk '{print "grep "$1 " jtemp.txt > " "estaciones/"$1".txt"}' tags.txt | /bin/sh
# Get starting year of measurements for each station and write to first line of (stationcode)f.txt. Note the f.
awk '{print "head -1 estaciones/"$1".txt | cut -c1-4 > estaciones/"$1"f.txt"}' tags.txt | /bin/sh
# Append to (stationcode)f.txt file in single-format column without station or year tags. The starting year is preserved as the first value of each file.
awk '{print "cut -c15- estaciones/"$1".txt | xargs -n1 >> estaciones/"$1"f.txt"}' tags.txt | /bin/sh
# Write location (DPT+MUN) info to (stationcode)n.txt. Note the n. This takes a while, as it as it has to re-grep original file.
awk '{print "grep -m 2 -A3 "$1" IDEAM.txt | grep -A2 DEPTO | awk '\''{print $8}'\'' | xargs -n2 > estaciones/"$1"n.txt"}' tags.txt | /bin/sh
# Give a nicer format to station names (dash separated, replace nasty chars). This is stored to (stationcode)n.txt. Note the n.
cut -c1-8 tags.txt | awk '{print "sed '\''s/ /-/g'\'' estaciones/"$0"n.txt > temp.txt ; mv temp.txt estaciones/"$0"n.txt"}' | /bin/sh
cut -c1-8 tags.txt | awk '{print "sed 's/\#/N/g' estaciones/"$0"n.txt > temp.txt ; mv temp.txt estaciones/"$0"n.txt"}' | /bin/sh
# Create csv header file for plotting
cat tags.txt | cut -c1-8 | awk '{print "cat estaciones/"$1"n.txt"}' | /bin/sh | xargs -n34 > headers.txt
cat tags.txt | cut -c1-8 | xargs -n34 >> headers.txt
sed 's/ /,/g' headers.txt > utemp.txt ; mv utemp.txt headers.txt
# Create clave.csv because shut up
awk '{print "grep -m 2 -A4 "$1" IDEAM.txt | grep -A2 DEPTO | awk '\''{print $8,$2,$3}'\'' | xargs -n9 | awk '\''{print $1,$2$3,$5$6,$8}'\''"}' tags.txt | /bin/sh | sed 's/#/N/g' > clave.csv
paste -d ' ' tags.txt clave.csv | cut -c1-8,10- | sed 's/ /,/g' > utemp.txt ; mv utemp.txt clave.csv
# Cleanup
rm spaces.txt
rm temptag.txt
# In principle I don’t delete these, as they can be used as control (NF==12)
# rm temp.txt
# rm fields.txt 
# Final notes
# tags.txt should probably be cut and saved (leading spaces after station codes) 
# the option -n34 for xargs should really be based on the number of stations, and it should be obtained from an environment variable.
# the selection of mean yearly data should really be an environment variable. Oh well.