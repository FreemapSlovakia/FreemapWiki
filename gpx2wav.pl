#!/usr/bin/perl
# synopsis:
#    gpx2wav.pl filename-to-convert.gpx

use strict;
use warnings;
if (! scalar @ARGV) {
		print "missing argument!\n";
		exit 1;
}
open IN, $ARGV[0] or die('File ',$ARGV[0],' not found');
s/(.+?)(\.gpx|)$/$1-wav.gpx/ for (my $output = $ARGV[0]);
open OU, ">${output}" or die('Cannot create output file (check permissions for '.${output}.')');
while (<IN>) {
print OU $_;
if (/AudioMarker/){
		chomp;
		s/^<name>AudioMarker-([^<]*)<\/name>/$1.amr/;
		my $audiofile = $_;
		if (-e ${audiofile}) {
				system("ffmpeg -y -i ".$audiofile." ".$audiofile.".wav");
				print OU '<link href="'.${audiofile}.'.wav"/>'."\n";
		}
}
}
close IN;
close OU;
