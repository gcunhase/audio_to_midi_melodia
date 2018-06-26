
import os
import glob
import argparse
from timeit import default_timer as timer

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", default="assets/COGNIMUSE/", help="Path to input audio file.")
    parser.add_argument("--bpm", type=int, default=146, help="Tempo of the track in BPM.")
    parser.add_argument("--smooth", type=float, default=0.25,
                        help="Smooth the pitch sequence with a median filter "
                             "of the provided duration (in seconds).")
    parser.add_argument("--minduration", type=float, default=0.1,
                        help="Minimum allowed duration for note (in seconds). "
                             "Shorter notes will be removed.")
    parser.add_argument("--jams", action="store_const", const=True,
                        default=False, help="Also save output in JAMS format.")

    args = parser.parse_args()

    init_time = timer()

    FOLDER = args.folder + "*"

    IFS = ".wav"  # delimiter
    IFS_CONVERT = ".mp3"
    BPM = args.bpm

    subdirs = glob.glob(FOLDER)
    for sub in subdirs:
        print(sub)
        files = glob.glob(sub+"/*{}".format(IFS))
        for f in files:
            f_base = f.split(IFS)[0]
            print(f_base)
            f_out = f.replace(IFS, IFS_CONVERT)

            # wav to mid
            os.system('python audio_to_midi_melodia.py {f_base}{ifs} {f_base}.mid {bpm} --smooth {smooth}'
                      ' --minduration {mindur} --jams'.format(f_base=f_base, bpm=BPM, ifs=IFS, smooth=args.smooth,
                                                              mindur=args.minduration))

            # mid to wav
            os.system('timidity {f_base}.mid -Ow -o {f_base}_recovered.wav'.format(f_base=f_base))

    end_time = timer()
    print("Program took {} minutes".format(60 * (end_time-init_time)))
