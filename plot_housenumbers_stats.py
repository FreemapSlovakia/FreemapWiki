#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
plots a graph of count(addr:housenumber) in osm db
for wikipage http://wiki.freemap.sk/SupisneCislaKapor

to collect data a separate cronjob is needed:

housenum=$(curl -s -X POST -d @req http://overpass-api.de/api/interpreter | grep -c "addr:housenumber")
echo "$(date):$(date +%s):$housenum" >> ~/bin/osm.housenumber.stats.txt

"""
import Gnuplot

dropboxdir = '/blabla/Dropbox/Public/osm-kuzemia/'

times = []
housenums = []
with open('osm.housenumber.stats.txt') as f:
    while True:
        line = f.readline().rstrip()
        if not line:
            break
        *args, epochtime, count = line.split(':')
        times.append(epochtime)
        housenums.append(count)

g = Gnuplot.Gnuplot()
g('set xdata time')
g('set output "' + dropboxdir + 'stats.png"')
g('set term png size 640,480')
g('set timefmt "%s"')
g('set xtics format "%b %y"')
g('set xtics font "monospace, 8"')
g('set ytics font "monospace, 8"')
g('set yrange [0:400000]')
g('set title "Počet adries (addr:housenumber)\\nv OSM db na Slovensku"')

g.plot(Gnuplot.Data(times, housenums, using='1:2 with lines'))

# some data retrieved from the past
history = [
    [1154383200, 0],
    [1272664800, 15814],
    [1320102000, 45007],
    [1328050800, 49209],
    [1362178800, 68846],
    [1365199200, 70696]
]

times = [x[0] for x in history] + times
housenums = [x[1] for x in history] + housenums

g('set output "' + dropboxdir + 'stats2.png"')

g.plot(Gnuplot.Data(times, housenums, using='1:2 with lines'))
