from praatio import textgrid
from praatio import audio
from AutoAnalysis import new_tier
import os

#Get words that are said in the recording
script = input("Enter each word cluster with a comma in between each cluster(ex. a blow a grad a blaze a grew, a blend a grid a blur a green, ...):")
clusters = script.split(",")
new_tg = textgrid.Textgrid()

#Get duration of recording
directory = "Aligner Inputs/Bobby"
duration = audio.getDuration(directory + "/" + "Complex_Onset_Word_Twisters1_7-15-23.wav")
print(duration)

#Get duration of each individual section
sub_duration = (duration-3)/20 #Length of 1 grouping
print(sub_duration)
cur_time = 1.5
entries = []
for cluster in clusters:
    for i in range(5):
        entries.append((str(cur_time), str((cur_time + sub_duration)), cluster))
        cur_time += sub_duration

entries.append((str(cur_time), str(duration), ''))

#Make Tier
new_tier(new_tg,"words",entries,"Aligner Inputs/Bobby/Complex_Onset_Word_Twisters1_7-15-23_TEST.TextGrid")
