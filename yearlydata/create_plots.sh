awk '{print "python plot.py " $1}' tags.txt | /bin/sh
awk '{print "python plotmonth.py " $1}' tags.txt | /bin/sh
awk '{print "python plotav.py " $1}' tags.txt | /bin/sh
python plot_all.py
python plotav_all.py
python plotmonth_all.py