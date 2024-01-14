from datetime import timedelta
from typing import Iterator, TextIO
import os
import whisper
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def srt_format_timestamp(seconds: float):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    return (f"{hours}:") + f"{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def write_srt(transcript: Iterator[dict], file: TextIO):
    count = 0
    for segment in transcript:
        count +=1
        print(
            f"{count}\n"
            f"{srt_format_timestamp(segment['start'])} --> {srt_format_timestamp(segment['end'])}\n"
            f"{segment['text'].replace('-->', '->').strip()}\n",
            file=file,
            flush=True,
        )

filename = "Complex_Onset_Word_Twisters3_7-16-23.wav"
language = "english"
model = whisper.load_model("medium")
result = model.transcribe(filename, verbose=True, language=language, fp16=False)
with open(os.path.join("Srt_Output", os.path.splitext(filename)[0] + f".{language}.srt"), "w") as srt:
    write_srt(result["segments"], file=srt)

"""
def transcribe_audio(path):
    model = whisper.load_model("medium") # Change this to your desired model
    print("Whisper model loaded.")
    transcribe = model.transcribe(audio=path)
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
        print(segment)

        srtFilename = os.path.join("SrtFiles", f"VIDEO_FILENAME.srt")
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    return srtFilename
    
print(transcribe_audio("Complex_Onset_Word_Twisters3_7-16-23.wav"))
"""


"""
# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("Complex_Onset_Word_Twisters3_7-16-23.wav")
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions(fp16=False)
result = whisper.decode(model, mel, options)

# print the recognized text
print(result.text)
"""