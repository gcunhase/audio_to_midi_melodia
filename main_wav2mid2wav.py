
import os
import glob
import argparse
from timeit import default_timer as timer
from pydub import AudioSegment


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    # parser.add_argument("--folder", default="assets/splices_audio_BMI/", help="Path to input audio file.")
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
    size_audio_files = 3  # in seconds

    subdirs = glob.glob(FOLDER)
    # subdirs = [args.folder+'audio']
    #for sub in subdirs:
    #    print(sub)
    #    files = glob.glob(sub + "/*{}".format(IFS))
    #    f = files[0]
    #    sound = AudioSegment.from_file(f)
    #    size_audio_files = len(sound)

    subdirs_final = []
    for sub in subdirs:
        print(sub)
        sub_folder = sub.split('/')[-1]
        #print(sub_folder)
        files = glob.glob(sub+"/*{}".format(IFS))
        for f in files:
            f_base = f.split(IFS)[0]
            filename = sub_folder + '_' + f_base.split('/')[-1]
            print(f_base)
            f_out = f.replace(IFS, IFS_CONVERT)

            # wav to mid
            mid_dir = '{}_mid/'.format(sub)
            if not os.path.exists(mid_dir):
                os.mkdir(mid_dir)

            command_str = 'python audio_to_midi_melodia.py {f_base}{ifs} {mid_dir}{filename}.mid {bpm} --smooth ' \
                          '{smooth} --minduration {mindur}'.format(f_base=f_base, bpm=BPM, ifs=IFS,
                                                                   smooth=args.smooth, mindur=args.minduration,
                                                                   mid_dir=mid_dir, filename=filename)
            if args.jams:
                command_str += ' --jams'
            os.system(command_str)

            # mid to wav
            rec_dir = '{}_rec/'.format(sub)
            if not os.path.exists(rec_dir):
                os.mkdir(rec_dir)
            os.system('timidity {mid_dir}{filename}.mid -Ow -o {rec_dir}{filename}_rec.wav'.
                      format(f_base=f_base, filename=filename, rec_dir=rec_dir, mid_dir=mid_dir))

            # change sample rate to 16000, 1 channel, 16 bits
            sr_dir = '{}_16000_c1_16bits_music'.format(sub)
            subdirs_final.append(sr_dir)
            if not os.path.exists(sr_dir):
                os.mkdir(sr_dir)
            os.system('sox {rec_dir}{filename}_rec.wav -c1 -b16 -r16000 {sr_dir}/{filename}.wav'.
                      format(filename=filename, rec_dir=rec_dir, sr_dir=sr_dir))

    subdirs = subdirs_final  # [args.folder+'audio_16000_c1_16bits_music']
    ## Normalize data length (all audio samples must have the same duration)
    #num_chunks = float("inf")
    #for sub in subdirs:
    #    files = glob.glob("{}/*{}".format(sub, IFS))
    #    for f in files:
    #        sound = AudioSegment.from_file(f)
    #        sound_chunks = len(sound)
    #        print("f: {}, {}, {}, {}".format(sound.rms, sound_chunks, sound.frame_rate, sound.frame_count()))
    #        if num_chunks > sound_chunks:
    #            num_chunks = sound_chunks
    #print("num_chunks: {}".format(num_chunks))

    splice_seconds = size_audio_files * 1000  # ms
    for sub in subdirs:
        files = glob.glob("{}/*{}".format(sub, IFS))
        sr_dir = '{}_eq/'.format(sub)
        if not os.path.exists(sr_dir):
            os.mkdir(sr_dir)
        for f in files:
            f_base = f.split(IFS)[0]
            filename = f_base.split('/')[-1]
    
            sound = AudioSegment.from_file(f)
            sound_chunks = len(sound)

            first_x_seconds = sound[:splice_seconds]
            first_x_seconds.export("{}{}.wav".format(sr_dir, filename), format="wav")

    #chunk_size = int(len(sound) / num_chunks  # ms))
    
    #loudness_over_time = []
    #for i in range(0, len(sound), chunk_size):
    #    chunk = sound[i:i + chunk_size]
    #loudness_over_time.append(chunk.rms)

    end_time = timer()
    print("Program took {} minutes".format((end_time-init_time)/60))  # COGNIMUSE: 47 minutes
