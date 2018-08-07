### Wav to MIDI to Wav
Extracts the melody notes from an audio file and exports them to MIDI and JAMS files.

The script extracts the melody from an audio file using the [Melodia](http://mtg.upf.edu/technologies/melodia) algorithm, and then segments the continuous pitch sequence into a series of quantized notes, and exports to MIDI using the provided BPM.

### Usage
```bash
python main.py [--folder FOLDER_NAME] [--bpm BPM] [--smooth SMOOTH] [--minduration MINDURATION] [--jams]
```
For example:
```bash
python main.py --folder assets/COGNIMUSE/ --bpm 146 --smooth 0.25 --minduration 0.1 --jams
```

### Notes
* *wav* to *mp3*:
```
ffmpeg -i assets/test/10.wav assets/test/10.mp3
```
* Find out *bpm* (146 in my case):
```
bpm-tag assets/test/10.mp3
```
* *wav* to *mid*:
```
python audio_to_midi_melodia.py assets/test/10.wav assets/test/10.mid 146 --smooth 0.25 --minduration 0.1 --jams
```
* *mid* to *wav* [converter](https://www.zamzar.com/convert/midi-to-wav/)
```bash
timidity 10.mid -Ow -o 10_recovered.wav
```

### Dependencies
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
pip install pydub
apt-get install ffmpeg bpm-tools
apt-get install timidity timidity-interfaces-extra
```

### Credit
[audio_to_midi_melodia](https://github.com/justinsalamon/audio_to_midi_melodia)
