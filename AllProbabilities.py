import AutoAnalysis as Auto
from praatio import textgrid
import os

# Make Entries

def make_entries(tier):
    intervalList = Auto.get_intervals(tier)
    probabilities = Auto.get_probabilities(tier)
    entries = []
    for i in range(len(intervalList)):
        interval = intervalList[i]
        probability = probabilities[i][1]
        entries.append((str(interval[0]), str(interval[1]), str(round(probability * 100, 1)) + '%'))
    return entries


def find_probabilities():
    mfa_directory = "Probability Outputs"
    output_directory = "AllProb"
    for folderName in os.listdir(mfa_directory):
        print(folderName)
        if folderName != ".DS_Store":
            for filename in os.listdir(mfa_directory + "/" + folderName):
                if filename.endswith('.TextGrid'):
                    # Defining filename inputFN
                    inputFN = mfa_directory + "/" + folderName + "/" + filename
                    tg = textgrid.openTextgrid(inputFN,
                                               includeEmptyIntervals=False)  # Give it a file name, get back a Textgrid object
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
                    # Creating tiers
                    word_tier_name = "words"
                    phone_tier_name = "phones"
                    if words_words:
                        word_tier_name = "words - words"
                        phone_tier_name = "words - phones"

                    OutputFN = output_directory + "/" + folderName + "/" + "_allProbs.TextGrid" + filename
                    wordTier = tg.getTier(word_tier_name)
                    Auto.new_tier(tg, "word prob", make_entries(wordTier), OutputFN)
                    if phone_tier_name in tg.tierNames:
                        phoneTier = tg.getTier(phone_tier_name)
                        Auto.new_tier(tg, "phone prob", make_entries(phoneTier), OutputFN)

find_probabilities()