# This creates the pasted-together file.
# Go to working directory (where the station-specific data is located)
cd estaciones
# Paste all (stationcode)f.txt files side by side. First line should be the starting year of measurements. Write to ltemp.txt
cat ../tags.txt | cut -c1-8 | sed 's/$/f.txt/g' | xargs -n34 | awk '{print "paste -d \" \"  " $0}' | /bin/sh > ../ltemp.txt
cd ..
# Remove tabs from paste. Is this necessary?
sed 's/\t/ /g' ltemp.txt > utemp.txt ; mv utemp.txt ltemp.txt
# In this block we get the headers (starting year and station code) ready and formatted.
# Get and separate starting years by comma. Write to ytemp.txt
sed '1q;d' ltemp.txt | sed 's/ /,/g' > ytemp.txt
# Add a leading comma to ytemp.txt
sed 's/^/,/g' ytemp.txt > utemp.txt; mv utemp.txt ytemp.txt 
# Remove first line from ltemp (line containing st. years, not comma separated).
sed '1d' ltemp.txt > utemp.txt ; mv utemp.txt ltemp.txt 
# Add first line from ytemp (line containing st. years, comma separated) to ltemp.txt
cat ytemp.txt ltemp.txt > utemp.txt ; mv utemp.txt ltemp.txt 
rm ytemp.txt
# Get and separate station codes by comma, adding a leading comma and adding to ltemp.txt
cat tags.txt | xargs -n34 | sed 's/ /,/g' | sed 's/^/,/' > utemp.txt; cat utemp.txt ltemp.txt > otemp.txt ; mv otemp.txt ltemp.txt ; rm utemp.txt
# Get station location info (DPT+MUN), replace nasty characters. This is NOT efficient, as it has to re-grep the original file.
awk '{print "grep -m 2 -A3 "$1" IDEAM.txt | grep -A2 DEPTO | awk '\''{print $8}'\'' | xargs -n2 "}' tags.txt | /bin/sh | sed 's/#/N/g' > utemp.txt
# Separate station location info by commas, add leading comma.
sed 's/ /-/g' utemp.txt | xargs -n34 | sed 's/ /,/g' | sed 's/^/,/' > otemp.txt ; mv otemp.txt utemp.txt
# Add first line (location info) to ltemp.txt
cat utemp.txt ltemp.txt > otemp.txt ; mv otemp.txt ltemp.txt ; rm utemp.txt
