# Wav to MIDI
* *wav* to *mp3*: ```ffmpeg -i assets/test/10.wav assets/test/10.mp3```
* Find out *bpm* (146 in my case): ```bpm-tag assets/test/10.mp3```
* *wav* to *mid*:
```
python audio_to_midi_melodia.py assets/test/10.wav assets/test/10.mid 146 --smooth 0.25 --minduration 0.1 --jams
```
* *mid* to *wav* [converter](https://www.zamzar.com/convert/midi-to-wav/)
```bash
timidity 10.mid -Ow -o 10_recovered.wav
```

# Credit
[audio_to_midi_melodia](https://github.com/justinsalamon/audio_to_midi_melodia)


Extract the melody notes from an audio file and export them to MIDI and (optionally) JAMS files.

The script extracts the melody from an audio file using the [Melodia](http://mtg.upf.edu/technologies/melodia) algorithm, and then segments the continuous pitch sequence into a series of quantized notes, and exports to MIDI using the provided BPM. If the `--jams` option is specified the script will also save the output as a JAMS file. Note that the JAMS file uses the original note onset/offset times estimated by the algorithm and ignores the provided BPM value.

Note: Melodia can work pretty well and is the result of [several years of research](http://www.justinsalamon.com/publications). The note segmentation/quantization code was written to be as simple as possible and will most likely not provide results that are as good as those provided by state-of-the-art note segmentation/quantization algorithms.

# Usage
```bash
>python audio_to_midi_melodia.py infile outfile bpm [--smooth SMOOTH] [--minduration MINDURATION] [--jams]
```
For example:
```bash
>python audio_to_midi_melodia.py ~/song.wav ~/song.mid 60 --smooth 0.25 --minduration 0.1 --jams
```
For further help use:
```bash
>python audio_to_midi_melodia.py --help
```

# Dependencies
* Requirements:
- Requires python 2.7 (will most likely crash on python 3, untested)
- Melodia melody extraction Vamp plugin: http://mtg.upf.edu/technologies/melodia
- Librosa: https://github.com/librosa/librosa
- Vamp python module: https://pypi.python.org/pypi/vamp
- midiutil: https://code.google.com/p/midiutil/

* Install dependencies:
```bash
pip install vamp jams numpy scipy
```
* Librosa
```bash
git clone https://github.com/librosa/librosa
cd dependencies/librosa
python setup.py build
python setup.py install
```
* [MidiUtil](https://code.google.com/p/midiutil/)
```bash
cd dependencies/MIDIUtil-0.89
python setup.py install
```
* Download [Melodia plugin](http://mtg.upf.edu/technologies/melodia) and copy all files to */usr/local/lib/vamp*
* Audio tools
```bash
apt-get install ffmpeg bpm-tools
apt-get install timidity timidity-interfaces-extra
```
