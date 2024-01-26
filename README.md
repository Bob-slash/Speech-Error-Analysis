# Speech Error Analysis
This project aims to produce probabilities for errors in speech in a given audio recording. Using the Montreal Forced Aligner (MFA), we are able to produce Praat textgrids with accurate annotations of both words and phonemes. Using this tool, we are able to accurately pinpoint exactly the speaker may have made an error. Finally, putting these textgrids into our programs will produce a final textgrid with all MFA outputs and possible locations of error. 

# Libraries
1. `praatio` is used for interfacing with praat and creating textgrids.
2. `os` is used for organizing and reading from textgrid files.
3. `matplotlib` is used for graphing error data.
4. `whisper` is used for speech to text applications in `main.py` (has not been implemented completely yet).

# Part 1: Using the Montreal Forced Aligner
## Step 1: Preparing/Organizing Data
Create 2 empty folders. One will hold the input data while the other will hold the output data. Leave the output data folder empty before running MFA. The Input folder should be populated with one or multiple recordings with a corresponding textgrid. The textgrid must have each section of text annotated. These annotations do not have to be exact. Each recording and its corresponding textgrid must have the same file name.

## Step 2: Running the Montreal Forced Aligner
1. Download the Montreal Forced aligner through conda with line: 
```sh
conda create -n aligner -c conda-forge montreal-forced-aligner
```

2. Each time before using the aligner, you must enter the aligner environment using line: conda activate aligner
In order to use pre-prepared corpora from the montreal forced aligner, you must first download them to your environment
run these lines:
```sh
  mfa model download acoustic english_us_arpa
  mfa model download dictionary english_us_arpa
```

3. Once the corpora have been downloaded, you should validate the input data using the following line (Although this step is not necessary, it is good to check that the input is valid as to not produce faulty outputs): 
```sh
  mfa validate ~/mfa_data/my_corpus english_us_arpa english_us_arpa
```

4. Finally, to Run the input through aligner, use the following line changing the folder locations to their corresponding paths:
```sh
  mfa align ~/mfa_data/my_corpus english_us_arpa english_us_arpa ~/mfa_data/my_corpus_aligned
```

This will leave you with an output folder populated with textgrids for each recording and textgrid pair.

_For more examples, please refer to the MFA [Documentation](https://montreal-forced-aligner.readthedocs.io/en/latest/first_steps/index.html#first-steps)_

# Part 2: Analysis
## Step 1: Auto Analysis
The `AutoAnalysis.py` can produce a new folder of textgrids with error percentages annotated. A textgrid that is passed through should look like the following:
<img width="1353" alt="Screenshot 2023-10-30 at 9 05 29 PM" src="https://github.com/Bob-slash/Speech_Error_Analysis/assets/54908332/072decc1-8ea6-482e-bf19-4eac8699c629">
Currently, the percentages that are displayed are only those that show high chance of error (although this is not always actually the case). The error percentage values are calculated by taking the duration of uttered words and phonemes and comparing them to the average duration of the word or phoneme in the recording. An utterance that is exceptionally short or exceptionally long compared to the average duration will be flagged and annotated.

The `AutoAnalysis.py` can also produce a graph of the percentage of error at every point of the recording. You can do this by using the `plot_all_prob` function. It should produce a graph like this:
<img width="601" alt="Screenshot 2023-10-30 at 9 12 14 PM" src="https://github.com/Bob-slash/Speech_Error_Analysis/assets/54908332/48207dc5-d6a6-428a-a628-9d021cb52aa6">

## Step 2: Combine Textgrids (Optional)
The `Combine_Textgrid.py` can be used to combine textgrids. Although not necessary, it was used for combining hand analyzed textgrids and textgrids that were output from the AutoAnalysis.py. Directory and file names can be changed to change save locations. 

# Notes on Other Files
The `main.py` file and the srttotextgrid.py file were used in an attempt to automatically create textgrids with annotated transcriptions. The programs are still under development. 

The `main.py` file transcribes a given recording using OpenAI's Whisper library. This transcription is produced in the form of an srt file. This filetype saves both a transcription and a time stamp for each set of words. 

The `srttotextgrid.py` file takes the srt output of `main.py` and makes it into a textgrid so that the other programs can annotate it. 






