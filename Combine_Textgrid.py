"""
Goal:
combine textgrids from probability outputs with the actual edits to
see all comments for the audio, and so we know where there are errors
to compare with the probability output.
"""
from praatio import textgrid
import os

mfa_directory = "Aligner Inputs"
probability_directiory = "AllProb"
output_directory = "AllProb_Final"
for folderName in os.listdir(probability_directiory):
    print(folderName)
    if folderName != ".DS_Store":
        for filename in os.listdir(mfa_directory + "/" + folderName):
            if filename.endswith('.TextGrid'):
                inputFN = mfa_directory + "/" + folderName + "/" + filename
                inputFN2 = probability_directiory + "/" + folderName + "/" + "_allProbs.TextGrid" + filename
                mfa_tg = textgrid.openTextgrid(inputFN, includeEmptyIntervals=True)
                prob_tg = textgrid.openTextgrid(inputFN2, includeEmptyIntervals=True)

                for tier in mfa_tg.tierNames:
                    if tier not in prob_tg.tierNames:
                        prob_tg.addTier(mfa_tg.getTier(tier))
                prob_tg.save(output_directory + "/" + folderName + "/" + filename + "_combined.TextGrid",
                             format="short_textgrid", includeBlankSpaces=True)
