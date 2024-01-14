"""
Goal:
Take in MFA output and using the durations of each word/phone, create
a probability table. Anything exceptionally long or exceptionally short
will be flagged as a possible error.
"""
from os.path import join
from praatio import textgrid
import os
import matplotlib.pyplot as plt

def get_intervals(tier):
    intervalList = [entry for entry in tier.entries]
    return intervalList

def get_durations(tier):
    intervalList = get_intervals(tier)
    durationList = []
    for interval in intervalList:
        durationList.append((interval.label, interval[1] - interval[0]))
    return durationList

#Create Tier
def new_tier(tg, name, entries, inputFN):
    newTier = textgrid.IntervalTier(name=name, entries=entries,
                                            minT=0, maxT=tg.maxTimestamp)
    tg.addTier(newTier)

    tg.save(inputFN, format="short_textgrid", includeBlankSpaces=True)

#Find average duration of each repeated segment
def find_average(durationList):

    averages = {}

    for duration in durationList:
        word = duration[0]
        length = duration[1]

        if word not in averages.keys():
            averages[word] = [1, length]

        elif word in averages.keys():
            averages[word][0] += 1
            averages[word][1] += length

    for key in averages.keys():
        averages[key] = averages[key][1] / averages[key][0]

    return averages

#Find longest duration
def find_long(durationList):

    longest = {}

    for duration in durationList:
        word = duration[0]
        length = duration[1]

        if word not in longest.keys():
            longest[word] = length

        elif word in longest.keys():
            if longest[word] < length:
                longest[word] = length

    return longest

def find_short(durationList):

    shortest = {}

    for duration in durationList:
        word = duration[0]
        length = duration[1]

        if word not in shortest.keys():
            shortest[word] = length

        elif word in shortest.keys():
            if shortest[word] > length:
                shortest[word] = length

    return shortest

def get_probabilities(tier):
    durationList = get_durations(tier)
    probabilities = []
    averages = find_average(durationList)
    longest = find_long(durationList)
    shortest = find_short(durationList)

    for value in durationList:
        label = value[0]
        duration = value[1]
        average = averages[label]
        long = longest[label]
        short = shortest[label]
        if label == "spn":
            probabilities.append((label, 1))

        elif duration > average:
            percent = ((duration - average) / (long - average))
            probabilities.append((label, percent))

        else:
            if average-short != 0:
                percent = ((average - duration)/(average - short))
            else:
                percent = 0
            probabilities.append((label, percent))

    return probabilities

#Make Entries

def make_entries(tier):
    intervalList = get_intervals(tier)
    probabilities = get_probabilities(tier)
    entries = []
    for i in range(len(intervalList)):
        interval = intervalList[i]
        probability = probabilities[i][1]
        if probability > 0.9:
            entries.append((str(interval[0]), str(interval[1]), str(round(probability * 100, 1)) + '%'))
    return entries

def plot_prob(entries, name):
    x = []
    y = []
    for entry in entries:
        print(entry)
        x.append((entry[1] + entry[0])/2)
        if entry[2] != '':
            y.append(float(entry[2][0:-2]))
        else:
            y.append(0)
    print(x, y)
    plt.plot(x, y, "-.")

    plt.xlabel("Time")
    plt.ylabel("Probability")
    plt.title(name)
    plt.show()

# directory = 'Aligner Inputs'
def find_probabilities():
    directory = 'Probability Outputs'
    for folderName in os.listdir(directory):
        if folderName != ".DS_Store":
            for filename in os.listdir(directory + "/" + folderName):
                if filename.endswith('.TextGrid'):
                    #Defining filename inputFN
                    inputFN = directory + "/" + folderName + "/" + filename
                    tg = textgrid.openTextgrid(inputFN, includeEmptyIntervals=False)  # Give it a file name, get back a Textgrid object
                    print(tg.tierNames)
                    words_words = False
                    for i in range(len(tg.tierNames) - 1, -1, -1):
                        if tg.tierNames[i] == "words - words":
                            tg.tierNames[i] = "words"
                        if tg.tierNames[i] == "words - phones":
                            words_words = True
                            tg.tierNames[i] = "phones"
                        if tg.tierNames[i] != "words" and tg.tierNames[i] != "phones":
                            tg.removeTier(tg.tierNames[i])
                    #Creating tiers
                    word_tier_name = "words"
                    phone_tier_name = "phones"
                    if words_words:
                        word_tier_name = "words - words"
                        phone_tier_name = "words - phones"

                    wordTier = tg.getTier(word_tier_name)
                    new_tier(tg,"word prob", make_entries(wordTier), directory + "/" + folderName + "/" + filename)
                    if phone_tier_name in tg.tierNames:
                        phoneTier = tg.getTier(phone_tier_name)
                        new_tier(tg,"phone prob", make_entries(phoneTier), directory + "/" + folderName + "/" + filename)

def plot_all_prob():
    directory = "Probability Outputs"
    folder = "Bobby"
    filename = "complex-onset-7-14-bl-gr.TextGrid"
    inputFN = directory + "/" + folder + "/" + filename
    tg = textgrid.openTextgrid(inputFN, includeEmptyIntervals=True)  # Give it a file name, get back a Textgrid object
    wordsTier = tg.getTier("word prob")
    plot_prob(wordsTier.entries, "Word Probability Plot")

    



def main():
    #find_probabilities()
    plot_all_prob()


main()