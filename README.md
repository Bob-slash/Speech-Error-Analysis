# Speech_Error_Analysis
This project aims to produce probabilities for errors in speech in a given audio recording. The steps bellow will instruct you on how to organize your data using the montreal forced aligner. Then, it will show how to run those outputs through our program to produce a praat textgrid file that creates tiers in the original file that show locations with high probabilities of errors.

# Part 1: Using the Montreal Forced Aligner
## Step 1: Preparing/Organizing Data

## Step 2: Running the Montreal Forced Aligner
Download the Montreal Forced aligner through conda with line: conda create -n aligner -c conda-forge montreal-forced-aligner
Each time before using the aligner, you must enter the aligner environment using line: conda activate aligner
In order to use pre-prepared corpuses from the montreal forced aligner, you must first download them to your environment
run these lines:
  mfa model download acoustic english_us_arpa
  mfa model download dictionary english_us_arpa

