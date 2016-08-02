#!/bin/bash
# amr2wav.sh - converts amr files recorded by gpsmid
# to wav format so that josm can read it and also
# create a gpx file with links to audiorecordings
#                              jose1711 gmail com
#
# syntax:
# ./amr2wav.sh <exported-waypoints-file.gpx>
#
#
#set -x
# input file is the one specified as a parameter
input=$1
# output file has '-wav' suffixed
output="${input%.gpx}-wav.gpx"
# no no, we don't want DOS line endings
sed -i 's/\r//g' "${input}"
# reset output file
> "${output}"
while read line
do
				# audiomarker means there was an audio recording done..
				echo "$line" | grep -v 'AudioMarker-GpsMid-' >> "${output}"
				if echo "$line" | grep AudioMarker &>/dev/null
				then
								audiofile="$(echo "$line" | sed 's/^<name>AudioMarker-\([^<]*\)<\/name>/\1.amr/')"
								# does the corresponding audiofile exist?
								if [ -r "$audiofile" ]
										then
										echo "$line" | sed 's/AudioMarker-GpsMid-//g' >> "${output}"
										# file exists, that's good. let's convert it to wav then
										ffmpeg -y -i "$audiofile" "$audiofile.wav" >/dev/null 2>&1 </dev/null
										# and create a <link> tag in output gpx file
										echo '<link href="'${audiofile}'.wav"/>' >> "${output}"
								fi
				fi
done < "${input}"

if [ $(ls *amr | wc -l) -ne $(ls *wav | wc -l) ] ; then
		echo "number of amr and wav files does not match. something could be WRONG"
fi
