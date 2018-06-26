
import os
import glob
import sys
from timeit import default_timer as timer

init_time = timer()

FOLDER = "assets/COGNIMUSE/*"
IFS = ".wav" # delimiter
IFS_CONVERT = ".mp3"  # converto to this delimiter

# Find out bpm (146 in my case):
# wav to mp3
# os.system('ffmpeg -i {infile} {outfile} -y'.format(infile=f, outfile=f_out))
# bpm-tag {infile}.mp3
BPM = 146

subdirs = glob.glob(FOLDER)
for sub in subdirs:
    print(sub)
    files = glob.glob(sub+"/*{}".format(IFS))
    for f in files:
        f_base = f.split(IFS)[0]
        print(f_base)
        f_out = f.replace(IFS, IFS_CONVERT)

        # wav to mid
        os.system('python audio_to_midi_melodia.py {f_base}{ifs} {f_base}.mid {bpm} --smooth 0.25 --minduration 0.1 --jams'.format(f_base=f_base, bpm=BPM, ifs=IFS))

        # mid to wav
        os.system('timidity {f_base}.mid -Ow -o {f_base}_recovered.wav'.format(f_base=f_base))

end_time = timer()
print("Program took {} minutes".format(60 * (end_time-init_time)))
