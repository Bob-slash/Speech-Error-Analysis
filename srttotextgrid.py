import datetime
import numpy
from itertools import groupby

import sys # to get command line arguments

from string import digits
from collections import namedtuple

# Input and output files as arguments
input_file_path= "complex_onset_worwav-subs.srt"
output_file_path = "test.textgrid"

# open .srt file

with open(input_file_path) as f:
    res = [list(g) for b,g in groupby(f, lambda x: bool(x.strip())) if b]

output_file = open(output_file_path,'w')

Subtitle = namedtuple('Subtitle', 'number start end content')

subs = []

for sub in res:
    if len(sub) >= 3: # not strictly necessary
        sub = [x.strip() for x in sub]
        number, start_end, *content = sub # py3 syntax
        start, end = start_end.split(' --> ')
        subs.append(Subtitle(number, start, end, content))

listOfTimes = []
for s in subs:
  listOfTimes.append(s.start)
  listOfTimes.append(s.end)


# strip the date information from them
mydates = [ datetime.datetime.strptime(listOfTimes[x], "%H:%M:%S,%f").time() for x in range(len(listOfTimes)) ]

# convert microseconds/minutes/seconds to only seconds
milliseconds = numpy.array([x.microsecond for x in mydates]) / 1000000
seconds = numpy.array([x.second for x in mydates])
minutes = numpy.array([x.minute for x in mydates]) * 60
hours = numpy.array([x.hour for x in mydates]) * 60 * 60
times = milliseconds + seconds + minutes + hours # this is a list of all times in seconds
numberOfIntervals = times.size//2

#ok, now that we have a list of times, we can figure out the max time and start by creating the preamble for our .textgrid
maxTime = max(times)

# now let's extract the text
text = []
for s in subs:
  _ = ""
  for t in s.content:
    _ += t + " | "

  text.append(_[:-3])

# write textgrid preamble
output_file.write("File type = \"ooTextFile\"" + '\n')
output_file.write("Object class = \"TextGrid\""+ '\n')
output_file.write('\n')
output_file.write("xmin = 0"+ '\n')
output_file.write("xmax = " + str(maxTime)+ '\n')
output_file.write("tiers? <exists>"+ '\n')
output_file.write("size = 1"+ '\n')
output_file.write("item []: "+ '\n')
output_file.write("\t item [1]:"+ '\n')
output_file.write("\t\t class = \"IntervalTier\""+ '\n')
output_file.write("\t\t name = \"silences\""+ '\n')
output_file.write("\t\t xmin = 0"+ '\n')
output_file.write("\t\t xmax = " + str(maxTime)+ '\n')
output_file.write("\t\t intervals: size = " + str(numberOfIntervals) +'\n')

for i in range(1, numberOfIntervals + 1): # I know it's weird, but I was getting fenceposting errors
  output_file.write("\t\t intervals [" + str(i) + "]:" + "\n")
  output_file.write("\t\t\t xmin = " + str(times.item((i * 2) - 2)) + "\n") # get the ith element from the array
  output_file.write("\t\t\t xmax = " + str(times.item((i * 2 ) - 1)) + "\n") # ith element + 1
  output_file.write("\t\t\t text = \"" + text[i - 1] + "\"\n")

output_file.close()