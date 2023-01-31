#!/usr/bin/env python
from __future__ import absolute_import, print_function, unicode_literals

import audioop
import math
import multiprocessing
import threading
import io, sys, os, time, signal
import tempfile
import wave
import json
import requests
try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

from progressbar import ProgressBar, Percentage, Bar, ETA
from pygoogletranslation import Translator
import pysrt
import six
from com.arthenica.mobileffmpeg import FFmpeg
from com.arthenica.mobileffmpeg import FFprobe
from os.path import dirname, join
from com.chaquo.python import Python

from java import dynamic_proxy, static_proxy
from java.lang import Runnable

GOOGLE_SPEECH_API_KEY = "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
GOOGLE_SPEECH_API_URL = "http://www.google.com/speech-api/v2/recognize?client=chromium&lang={lang}&key={key}" # pylint: disable=line-too-long
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0 Win64 x64)'

arraylist_language_code = []
arraylist_language_code.append("af")
arraylist_language_code.append("sq")
arraylist_language_code.append("am")
arraylist_language_code.append("ar")
arraylist_language_code.append("hy")
arraylist_language_code.append("as")
arraylist_language_code.append("ay")
arraylist_language_code.append("az")
arraylist_language_code.append("bm")
arraylist_language_code.append("eu")
arraylist_language_code.append("be")
arraylist_language_code.append("bn")
arraylist_language_code.append("bho")
arraylist_language_code.append("bs")
arraylist_language_code.append("bg")
arraylist_language_code.append("ca")
arraylist_language_code.append("ceb")
arraylist_language_code.append("ny")
arraylist_language_code.append("zh-CN")
arraylist_language_code.append("zh-TW")
arraylist_language_code.append("co")
arraylist_language_code.append("cr")
arraylist_language_code.append("cs")
arraylist_language_code.append("da")
arraylist_language_code.append("dv")
arraylist_language_code.append("nl")
arraylist_language_code.append("doi")
arraylist_language_code.append("en")
arraylist_language_code.append("eo")
arraylist_language_code.append("et")
arraylist_language_code.append("ee")
arraylist_language_code.append("fil")
arraylist_language_code.append("fi")
arraylist_language_code.append("fr")
arraylist_language_code.append("fy")
arraylist_language_code.append("gl")
arraylist_language_code.append("ka")
arraylist_language_code.append("de")
arraylist_language_code.append("el")
arraylist_language_code.append("gn")
arraylist_language_code.append("gu")
arraylist_language_code.append("ht")
arraylist_language_code.append("ha")
arraylist_language_code.append("haw")
arraylist_language_code.append("he")
arraylist_language_code.append("hi")
arraylist_language_code.append("hmn")
arraylist_language_code.append("hu")
arraylist_language_code.append("is")
arraylist_language_code.append("ig")
arraylist_language_code.append("ilo")
arraylist_language_code.append("id")
arraylist_language_code.append("ga")
arraylist_language_code.append("it")
arraylist_language_code.append("ja")
arraylist_language_code.append("jv")
arraylist_language_code.append("kn")
arraylist_language_code.append("kk")
arraylist_language_code.append("km")
arraylist_language_code.append("rw")
arraylist_language_code.append("kok")
arraylist_language_code.append("ko")
arraylist_language_code.append("kri")
arraylist_language_code.append("kmr")
arraylist_language_code.append("ckb")
arraylist_language_code.append("ky")
arraylist_language_code.append("lo")
arraylist_language_code.append("la")
arraylist_language_code.append("lv")
arraylist_language_code.append("ln")
arraylist_language_code.append("lt")
arraylist_language_code.append("lg")
arraylist_language_code.append("lb")
arraylist_language_code.append("mk")
arraylist_language_code.append("mg")
arraylist_language_code.append("ms")
arraylist_language_code.append("ml")
arraylist_language_code.append("mt")
arraylist_language_code.append("mi")
arraylist_language_code.append("mr")
arraylist_language_code.append("mni")
arraylist_language_code.append("lus")
arraylist_language_code.append("mn")
arraylist_language_code.append("mmr")
arraylist_language_code.append("ne")
arraylist_language_code.append("no")
arraylist_language_code.append("or")
arraylist_language_code.append("om")
arraylist_language_code.append("ps")
arraylist_language_code.append("fa")
arraylist_language_code.append("pl")
arraylist_language_code.append("pt")
arraylist_language_code.append("pa")
arraylist_language_code.append("qu")
arraylist_language_code.append("ro")
arraylist_language_code.append("ru")
arraylist_language_code.append("sm")
arraylist_language_code.append("sa")
arraylist_language_code.append("gd")
arraylist_language_code.append("nso")
arraylist_language_code.append("sr")
arraylist_language_code.append("st")
arraylist_language_code.append("sn")
arraylist_language_code.append("sd")
arraylist_language_code.append("si")
arraylist_language_code.append("sk")
arraylist_language_code.append("sl")
arraylist_language_code.append("so")
arraylist_language_code.append("es")
arraylist_language_code.append("su")
arraylist_language_code.append("sw")
arraylist_language_code.append("sv")
arraylist_language_code.append("tg")
arraylist_language_code.append("ta")
arraylist_language_code.append("tt")
arraylist_language_code.append("te")
arraylist_language_code.append("th")
arraylist_language_code.append("ti")
arraylist_language_code.append("ts")
arraylist_language_code.append("tr")
arraylist_language_code.append("tk")
arraylist_language_code.append("tw")
arraylist_language_code.append("ug")
arraylist_language_code.append("uk")
arraylist_language_code.append("ur")
arraylist_language_code.append("uz")
arraylist_language_code.append("vi")
arraylist_language_code.append("cy")
arraylist_language_code.append("xh")
arraylist_language_code.append("yi")
arraylist_language_code.append("yo")
arraylist_language_code.append("zu")

arraylist_language = []
arraylist_language.append("Afrikaans")
arraylist_language.append("Albanian")
arraylist_language.append("Amharic")
arraylist_language.append("Arabic")
arraylist_language.append("Armenian")
arraylist_language.append("Assamese")
arraylist_language.append("Aymara")
arraylist_language.append("Azerbaijani")
arraylist_language.append("Bambara")
arraylist_language.append("Basque")
arraylist_language.append("Belarusian")
arraylist_language.append("Bengali (Bangla)")
arraylist_language.append("Bhojpuri")
arraylist_language.append("Bosnian")
arraylist_language.append("Bulgarian")
arraylist_language.append("Catalan")
arraylist_language.append("Cebuano")
arraylist_language.append("Chichewa, Nyanja")
arraylist_language.append("Chinese (Simplified)")
arraylist_language.append("Chinese (Traditional)")
arraylist_language.append("Corsican")
arraylist_language.append("Croatian")
arraylist_language.append("Czech")
arraylist_language.append("Danish")
arraylist_language.append("Divehi, Maldivian")
arraylist_language.append("Dogri")
arraylist_language.append("Dutch")
arraylist_language.append("English")
arraylist_language.append("Esperanto")
arraylist_language.append("Estonian")
arraylist_language.append("Ewe")
arraylist_language.append("Filipino")
arraylist_language.append("Finnish")
arraylist_language.append("French")
arraylist_language.append("Frisian")
arraylist_language.append("Galician")
arraylist_language.append("Georgian")
arraylist_language.append("German")
arraylist_language.append("Greek")
arraylist_language.append("Guarani")
arraylist_language.append("Gujarati")
arraylist_language.append("Haitian Creole")
arraylist_language.append("Hausa")
arraylist_language.append("Hawaiian")
arraylist_language.append("Hebrew")
arraylist_language.append("Hindi")
arraylist_language.append("Hmong")
arraylist_language.append("Hungarian")
arraylist_language.append("Icelandic")
arraylist_language.append("Igbo")
arraylist_language.append("Ilocano")
arraylist_language.append("Indonesian")
arraylist_language.append("Irish")
arraylist_language.append("Italian")
arraylist_language.append("Japanese")
arraylist_language.append("Javanese")
arraylist_language.append("Kannada")
arraylist_language.append("Kazakh")
arraylist_language.append("Khmer")
arraylist_language.append("Kinyarwanda (Rwanda)")
arraylist_language.append("Konkani")
arraylist_language.append("Korean")
arraylist_language.append("Krio")
arraylist_language.append("Kurdish (Kurmanji)")
arraylist_language.append("Kurdish (Sorani)")
arraylist_language.append("Kyrgyz")
arraylist_language.append("Lao")
arraylist_language.append("Latin")
arraylist_language.append("Latvian (Lettish)")
arraylist_language.append("Lingala")
arraylist_language.append("Lithuanian")
arraylist_language.append("Luganda, Ganda")
arraylist_language.append("Luxembourgish")
arraylist_language.append("Macedonian")
arraylist_language.append("Malagasy")
arraylist_language.append("Malay")
arraylist_language.append("Malayalam")
arraylist_language.append("Maltese")
arraylist_language.append("Maori")
arraylist_language.append("Marathi")
arraylist_language.append("Meiteilon (Manipuri)")
arraylist_language.append("Mizo")
arraylist_language.append("Mongolian")
arraylist_language.append("Myanmar (Burmese)")
arraylist_language.append("Nepali")
arraylist_language.append("Norwegian")
arraylist_language.append("Oriya")
arraylist_language.append("Oromo (Afaan Oromo)")
arraylist_language.append("Pashto, Pushto")
arraylist_language.append("Persian (Farsi)")
arraylist_language.append("Polish")
arraylist_language.append("Portuguese")
arraylist_language.append("Punjabi (Eastern)")
arraylist_language.append("Quechua")
arraylist_language.append("Romanian, Moldavian")
arraylist_language.append("Russian")
arraylist_language.append("Samoan")
arraylist_language.append("Sanskrit")
arraylist_language.append("Scots Gaelic")
arraylist_language.append("Sepedi")
arraylist_language.append("Serbian")
arraylist_language.append("Sesotho")
arraylist_language.append("Shona")
arraylist_language.append("Sindhi")
arraylist_language.append("Sinhalese")
arraylist_language.append("Slovak")
arraylist_language.append("Slovenian")
arraylist_language.append("Somali")
arraylist_language.append("Spanish")
arraylist_language.append("Sundanese")
arraylist_language.append("Swahili (Kiswahili)")
arraylist_language.append("Swedish")
arraylist_language.append("Tajik")
arraylist_language.append("Tamil")
arraylist_language.append("Tatar")
arraylist_language.append("Telugu")
arraylist_language.append("Thai")
arraylist_language.append("Tigrinya")
arraylist_language.append("Tsonga")
arraylist_language.append("Turkish")
arraylist_language.append("Turkmen")
arraylist_language.append("Twi")
arraylist_language.append("Ukrainian")
arraylist_language.append("Urdu")
arraylist_language.append("Uyghur")
arraylist_language.append("Uzbek")
arraylist_language.append("Vietnamese")
arraylist_language.append("Welsh")
arraylist_language.append("Xhosa")
arraylist_language.append("Yiddish")
arraylist_language.append("Yoruba")
arraylist_language.append("Zulu")

map_code_of_language = dict(zip(arraylist_language, arraylist_language_code))
map_language_of_code = dict(zip(arraylist_language_code, arraylist_language))

LANGUAGE_CODES = map_language_of_code

context = Python.getPlatform().getApplication()
files_dir = str(context.getExternalFilesDir(None))
cancel_file = join(files_dir, 'cancel.txt')
cache_dir = str(context.getExternalCacheDir())
transcriptions_file = join(cache_dir, "transcriptions.txt")
region_start_file = join(cache_dir, 'region_starts.txt')
elapsed_time_file = join(cache_dir, 'elapsed_time.txt')
wav_filename = None
srt_file = None
translated_srt_file = None


def srt_formatter(subtitles, padding_before=0, padding_after=0):
    """
    Serialize a list of subtitles according to the SRT format, with optional time padding.
    """
    sub_rip_file = pysrt.SubRipFile()
    for i, ((start, end), text) in enumerate(subtitles, start=1):
        item = pysrt.SubRipItem()
        item.index = i
        item.text = six.text_type(text)
        item.start.seconds = max(0, start - padding_before)
        item.end.seconds = end + padding_after
        sub_rip_file.append(item)
    return '\n'.join(six.text_type(item) for item in sub_rip_file)


FORMATTERS = {
    'srt': srt_formatter,
}


def percentile(arr, percent):
    arr = sorted(arr)
    k = (len(arr) - 1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c: return arr[int(k)]
    d0 = arr[int(f)] * (c - k)
    d1 = arr[int(c)] * (k - f)
    return d0 + d1


def is_same_language(lang1, lang2):
    return lang1.split("-")[0] == lang2.split("-")[0]


class FLACConverter(object):
    def __init__(self, source_path, include_before=0.25, include_after=0.25):
        self.source_path = source_path
        self.include_before = include_before
        self.include_after = include_after

    def __call__(self, region):
        try:
            start, end = region
            start = max(0, start - self.include_before)
            end += self.include_after
            temp = tempfile.NamedTemporaryFile(suffix='.flac', delete=False)
            FFmpeg.execute(" -ss " + str(start) + " -t " + str(end - start) + " -y -i " + "\"" + self.source_path + "\"" + " -loglevel error " + "\"" + temp.name + "\"")
            return temp.read()

        except KeyboardInterrupt:
            return


class SpeechRecognizer(object):
    def __init__(self, language="en", rate=44100, retries=3, api_key=GOOGLE_SPEECH_API_KEY):
        self.language = language
        self.rate = rate
        self.api_key = api_key
        self.retries = retries

    def __call__(self, data):
        try:
            for i in range(self.retries):
                url = GOOGLE_SPEECH_API_URL.format(lang=self.language, key=self.api_key)
                headers = {"Content-Type": "audio/x-flac rate=%d" % self.rate}

                try:
                    resp = requests.post(url, data=data, headers=headers)
                except requests.exceptions.ConnectionError:
                    continue

                for line in resp.content.decode('utf-8').split("\n"):
                    try:
                        line = json.loads(line)
                        line = line['result'][0]['alternative'][0]['transcript']
                        return line[:1].upper() + line[1:]
                    except:
                        # no result
                        continue

        except KeyboardInterrupt:
            return



def extract_audio(filename, channels=1, rate=16000):
    temp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    if not os.path.isfile(filename):
        print("The given file does not exist: {0}".format(filename))
        raise Exception("Invalid filepath: {0}".format(filename))
    FFmpeg.execute("-y -i " + "\"" + filename + "\"" + " -ac " + str(channels) + " -ar " + str(rate) + " " + "\"" + temp.name + "\"" )
    return temp.name, rate


#def find_speech_regions(filename, frame_width=4096, min_region_size=0.5, max_region_size=6):
def find_speech_regions(filename, frame_width=4096, min_region_size=0.3, max_region_size=8):
    reader  = wave.open(filename)
    sample_width = reader.getsampwidth()
    rate = reader.getframerate()
    n_channels = reader.getnchannels()

    total_duration = reader.getnframes() / rate
    chunk_duration = float(frame_width) / rate
    n_chunks = int(total_duration / chunk_duration)

    energies = []

    for i in range(n_chunks):
        chunk = reader.readframes(frame_width)
        energies.append(audioop.rms(chunk, sample_width * n_channels))

    threshold = percentile(energies, 0.2)

    elapsed_time = 0

    regions = []
    region_start = None

    i=0
    for energy in energies:
        is_silence = energy <= threshold
        max_exceeded = region_start and elapsed_time - region_start >= max_region_size

        if (max_exceeded or is_silence) and region_start:
            if elapsed_time - region_start >= min_region_size:
                regions.append((region_start, elapsed_time))
                region_start = None

        elif (not region_start) and (not is_silence):
            region_start = elapsed_time
        elapsed_time += chunk_duration
        i=i+1

    return regions


def CountEntries(srt_file):
    e=0
    with open(srt_file, 'r', encoding='utf-8') as srt:
        while True:
            e += 1
            # read lines in order
            number_in_sequence = srt.readline()
            timecode = srt.readline()
            # whether it's the end of the file.
            if not number_in_sequence:
                break
            # put all subtitles seperated by newline into a list.
            subtitles = []
            while True:
                subtitle = srt.readline()
                # whether it's the end of a entry.
                if subtitle == '\n':
                    break
                subtitles.append(subtitle)
    total_entries = e - 1
    #print('Total Entries', total_entries)
    return total_entries


def entries_generator(srt_file):
    """Generate a entries queue.

    input:
        srt_file: The original filename. [*.srt]

    output:
        entries: A queue generator.
    """
    with open(srt_file, 'r', encoding='utf-8') as srt:
        while True:
            # read lines in order
            number_in_sequence = srt.readline()
            timecode = srt.readline()
            # whether it's the end of the file.
            if not number_in_sequence:
                break
            # put all subtitles seperated by newline into a list.
            subtitles = []
            while True:
                subtitle = srt.readline()
                # whether it's the end of a entry.
                if subtitle == '\n':
                    break
                subtitles.append(subtitle)
            yield number_in_sequence, timecode, subtitles


def translate(entries, src, dest, patience, verbose):
    """Generate the translated entries.

    args:
        entries: The entries queue.
        src: The source language.
        dest: The target language.
    """
    translator = Translator()
    count_failure = 0
    count_entries = 0

    for number_in_sequence, timecode, subtitles in entries:
        count_entries += 1
        translated_subtitles = []

        for i, subtitle in enumerate(subtitles, 1):
            # handle the special case: empty string.
            if not subtitle:
                translated_subtitles.append(subtitle)
                continue
            translated_subtitle = translator.translate(subtitle, src=src, dest=dest).text
            # handle the fail to translate case.
            fail_to_translate = translated_subtitle[-1] == '\n'
            while fail_to_translate and patience:
                if verbose:
                    print('[Failure] Retry to translate...')
                    print('The translated subtitle: {}', end=''.format(translated_subtitle))

                translated_subtitle = translator.translate(translated_subtitle, src=src, dest=dest).text
                if translated_subtitle[-1] == '\n':
                    if patience == -1:
                        continue
                    if patience == 1:
                        if verbose:
                            print('This subtitle failed to translate... [Position] entry {0} line {1}'.format(count_entries,i))
                    patience -= 1
                else:
                    fail_to_translate = False
                    if verbose:
                        print('Translate successfully. The result: {}'.format(translated_subtitle))

            translated_subtitles.append(translated_subtitle if fail_to_translate else translated_subtitle + '\n')

        if fail_to_translate:
            count_failure += 1
            print('[{}] Failure to translate current entry...'.format(count_entries))

        yield number_in_sequence, timecode, translated_subtitles, count_failure, count_entries



class SubtitleTranslator(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def __call__(self, entries):
        translator = Translator()
        translated_subtitles = []
        number_in_sequence, timecode, subtitles = entries

        for i, subtitle in enumerate(subtitles, 1):
            # handle the special case: empty string.
            if not subtitle:
                translated_subtitles.append(subtitle)
            translated_subtitle = translator.translate(subtitle, src=self.src, dest=self.dest).text
            translated_subtitle = translator.translate(translated_subtitle, src=self.src, dest=self.dest).text
            translated_subtitles.append(translated_subtitle + '\n')
        return number_in_sequence, timecode, translated_subtitles
        #yield number_in_sequence, timecode, translated_subtitles, count_failure, count_entries


class TranscriptionTranslator(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def __call__(self, transcription):
        try:
            translated_transcription = Translator().translate(transcription, src=self.src, dest=self.dest).text
            return translated_transcription

        except KeyboardInterrupt:
            return



def transcribe(src, dest, filename, activity, textView_debug):
    pool = multiprocessing.pool.ThreadPool(10)
    wav_filename = None

    if not os.path.isfile(cancel_file):

        '''
        # Use this if we want to create a copy from python script
        context = Python.getPlatform().getApplication()
        files_dir = str(context.getExternalFilesDir(None))
        content = bytes(content)
        homedir = os.environ["HOME"]
        filename = join(files_dir, uriDisplayName)
        print("filename = {}".format(filename))
        #with open(filename, "wb") as binary_file:
            #binary_file.write(content)
            #transcribe(src, dest, filename)
        binary_file = open(filename, 'wb')
        binary_file.write(content)
        '''

        print("Converting to a temporary WAV file")
        class R(dynamic_proxy(Runnable)):
            def run(self):
                textView_debug.setText("Running python script...\n\n");
                textView_debug.append("Converting to a temporary WAV file...\n\n");
        activity.runOnUiThread(R())
        time.sleep(1)

        wav_filename, audio_rate = extract_audio(filename)

        print("Converted WAV file is : {}".format(wav_filename))

        #time.sleep(2)
        class R(dynamic_proxy(Runnable)):
            def run(self):
                textView_debug.append("Converted WAV file is :\n" + wav_filename)
        activity.runOnUiThread(R())
        time.sleep(2)

    else:
        check_cancel_file()


    if not os.path.isfile(cancel_file):
        time.sleep(1)
        print("Finding speech regions of WAV file")
        class R(dynamic_proxy(Runnable)):
            def run(self):
                textView_debug.setText("Finding speech regions of WAV file...\n\n")
        activity.runOnUiThread(R())

        regions = find_speech_regions(wav_filename)
        num = len(regions)
        time.sleep(1)
        class R(dynamic_proxy(Runnable)):
            def run(self):
                textView_debug.append("Speech regions found = " + str(num))
        activity.runOnUiThread(R())
        print("Speech regions found = {}".format(str(num)))
        time.sleep(3)

        #textView_debug.append(str(regions) + "\n")
        #i=0
        #for r in regions:
            #textView_debug.append("region[" + str(i) + "] = " + str(r) + "\n");
            #i=i+1
        #textView_debug.append(str(regions));

    else:
        check_cancel_file()

    if not os.path.isfile(cancel_file):
        converter = FLACConverter(source_path=wav_filename)
        recognizer = SpeechRecognizer(language=src, rate=audio_rate, api_key=GOOGLE_SPEECH_API_KEY)
        transcriptions = []
        translated_transcriptions = []

        if regions:
            try:
                if not os.path.isfile(cancel_file):
                    print("Converting speech regions to FLAC files")

                    # widgets and pbar are from progressbar module, we don't use it because we can't show it on textview_debug
                    # we use self made pBar to show progress on textview

                    #widgets = ["Converting speech regions to FLAC files : ", Percentage(), ' ', Bar(), ' ', ETA()]
                    #pbar = ProgressBar(widgets=widgets, maxval=len(regions)).start()

                    extracted_regions = []
                    time.sleep(1)
                    for i, extracted_region in enumerate(pool.imap(converter, regions)):
                        check_cancel_file()
                        extracted_regions.append(extracted_region)
                        #pbar.update(i)
                        pBar(i, len(regions), "Converting speech regions to FLAC: ", activity, textView_debug)
                    #pbar.finish()
                    time.sleep(1)
                    pBar(len(regions), len(regions), "Converting speech regions to FLAC: ", activity, textView_debug)

                    check_cancel_file()
        
                    print("Creating transcriptions")
                    #widgets = ["Performing speech recognition           : ", Percentage(), ' ', Bar(), ' ', ETA()]
                    #pbar = ProgressBar(widgets=widgets, maxval=len(regions)).start()
                    time.sleep(1)
                    for i, transcription in enumerate(pool.imap(recognizer, extracted_regions)):
                        #check_cancel_file()
                        transcriptions.append(transcription)
                        #pbar.update(i)
                        pBar(i, len(regions), "Creating transcriptions: ", activity, textView_debug)
                    #pbar.finish()
                    time.sleep(1)
                    pBar(len(regions), len(regions), "Creating transcriptions: ", activity, textView_debug)

                    check_cancel_file()

                    timed_subtitles = [(r, t) for r, t in zip(regions, transcriptions) if t]
                    formatter = FORMATTERS.get("srt")
                    formatted_subtitles = formatter(timed_subtitles)

                    base, ext = os.path.splitext(filename)
                    srt_file = "{base}.{format}".format(base=base, format="srt")

                    with open(srt_file, 'wb') as f:
                        f.write(formatted_subtitles.encode("utf-8"))
                        f.close()

                    with open(srt_file, 'a') as f:
                        f.write("\n")
                        f.close()

                    os.remove(wav_filename)

                check_cancel_file()

                if (not is_same_language(src, dest)) and (os.path.isfile(srt_file)) and (not os.path.isfile(cancel_file)):
                    print("Translating transcriptions")
                    entries = entries_generator(srt_file)
                    translated_srt_file = srt_file[ :-4] + '_translated.srt'
                    total_entries = CountEntries(srt_file)
                    print('Total Entries = {}'.format(total_entries))

                    #prompt = "Translating from %5s to %5s         : " %(src, dest)
                    #widgets = [prompt, Percentage(), ' ', Bar(), ' ', ETA()]
                    #pbar = ProgressBar(widgets=widgets, maxval=len(transcriptions)).start()

                    subtitle_translator = SubtitleTranslator(src=src, dest=dest)
                    translated_entries = []
                    for i, translated_entry in enumerate(pool.imap(subtitle_translator, entries)):
                        check_cancel_file()
                        translated_entries.append(translated_entry)
                        pBar(i, total_entries, "Translating from %s to %s: " %(src, dest), activity, textView_debug)
                    pBar(total_entries, total_entries, "Translating from %s to %s: " %(src, dest), activity, textView_debug)

                    with open(translated_srt_file, 'w', encoding='utf-8') as f:
                        for number_in_sequence, timecode, translated_subtitles in translated_entries:
                            f.write(number_in_sequence)
                            f.write(timecode)
                            for translated_subtitle in translated_subtitles:
                                f.write(translated_subtitle)
                                f.write('\n')

                print('Done.')
                print("Original subtitles file created at      : {}".format(srt_file))
                if (not is_same_language(src, dest)) and (os.path.isfile(srt_file)) and (not os.path.isfile(cancel_file)):
                    print('Translated subtitles file created at    : {}' .format(translated_srt_file))
                    #print('Total failure to translate entries      : {0}/{1}'.format(count_failure, count_entries))
                    #failure_ratio = count_failure / count_entries
                    #if failure_ratio > 0:
                        #print('If you expect a lower failure ratio or completed translate, please check out the usage of [-p | --postion] argument.')

                class R(dynamic_proxy(Runnable)):
                    def run(self):
                        time.sleep(1)
                        textView_debug.append("\n\nSRT subtitles file created at :\n")
                        textView_debug.append(srt_file + "\n\n")
                        if (not is_same_language(src, dest)) and (os.path.isfile(srt_file)) and (not os.path.isfile(cancel_file)):
                            textView_debug.append("Translated SRT subtitles file created at:\n")
                            textView_debug.append(translated_srt_file + "\n\n")
                        textView_debug.append("Done!")
                activity.runOnUiThread(R())

            except KeyboardInterrupt:
                print("Cancelling transcription")
                if wav_filename:
                    if os.path.isfile(wav_filename): os.remove(wav_filename)
                if os.path.isfile(cancel_file): os.remove(cancel_file)
                converter = None
                recognizer = None
                for extracted_region in extracted_regions:
                    if extracted_region:
                        if os.path.isfile(extracted_region): os.remove(extracted_region)
                    extracted_regions = None
                for transcription in transcriptions:
                    transcription = None
                transcriptions = None
                if srt_file:
                    if os.path.isfile(srt_file): os.remove(srt_file)
                if translated_srt_file:
                    if os.path.isfile(translated_srt_file): os.remove(translated_srt_file)
                if pbar: pbar = None
                if pool:
                    pool.terminate()
                    pool.close()
                    pool.join()
                    pool = None
                class R(dynamic_proxy(Runnable)):
                    def run(self):
                        time.sleep(1)
                        textView_debug.setText("Process has been canceled")
                activity.runOnUiThread(R())

        else:
            check_cancel_file()

    pool.close()
    pool.join()
    pool = None

    return translated_srt_file


def main(src, dest, content, uriDisplayName, textView_debug):
    print("Starting main")
    textView_debug.append("Creating a copy of " + uriDisplayName + "\n")
    context = Python.getPlatform().getApplication()
    files_dir = str(context.getExternalFilesDir(None))
    working_dir = join(files_dir,uriDisplayName[ :-4])
    content = bytes(content)
    #homedir = os.environ["HOME"]
    filename = join(working_dir, uriDisplayName)
    print("filename = {}".format(filename))
    #with open(filename, "wb") as binary_file:
        #binary_file.write(content)
        #transcribe(src, dest, filename)
    binary_file = open(filename, 'wb')
    binary_file.write(content)
    transcribe(src, dest, filename, textView_debug)



# SPLITTED transcribe() FUNCTION

def create_copy(content, uriDisplayName, textView_debug):
    # we need to create a copy of original file because in Android API 29 Scopped Storage we can't get its REAL PATH directly
    # by copying it into a path the we knew we can then proceeed it to next steps
    files_dir = str(context.getExternalFilesDir(None))
    cancel_file = join(files_dir, 'cancel.txt')
    filename = None
    if not os.path.isfile(cancel_file):
        content = bytes(content)
        content_length = len(content)
        counter = 0
        r = 0
        filename = join(files_dir, uriDisplayName)
        print("filename = {}".format(filename))
        binary_file = open(filename, 'wb')
        binary_file.write(content)
    else:
        os.remove(cancel_file)
        class R(dynamic_proxy(Runnable)):
            def run(self):
                time.sleep(1)
                textView_debug.setText("Process has been canceled")
        activity.runOnUiThread(R())
    return filename


def convert_to_wav(filename, channels, rate, activity, textView_debug):
    print("Converting to a temporary WAV file...")
    print("filename = {}".format(filename))
    class R(dynamic_proxy(Runnable)):
        def run(self):
            textView_debug.setText("Running python script...\n\n");
            textView_debug.append("Converting to a temporary WAV file...\n\n");
    activity.runOnUiThread(R())
    time.sleep(1)

    files_dir = str(context.getExternalFilesDir(None))
    cancel_file = join(files_dir, 'cancel.txt')
    wav_filename = None
    if not os.path.isfile(cancel_file):
        temp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        if not os.path.isfile(filename):
            msg = "The given file does not exist: {0}".format(filename)
            print(msg)
            class R(dynamic_proxy(Runnable)):
                def run(self):
                    textView_debug.append(msg + "\n")
            activity.runOnUiThread(R())
            raise Exception("Invalid filepath: {0}".format(filename))
        FFmpeg.execute("-y -i " + "\"" + filename + "\"" + " -ac " + str(channels) + " -ar " + str(rate) + " " + "\"" + temp.name + "\"" )
        wav_filename = temp.name
        print("wav_filename = {}".format(wav_filename))

        class R(dynamic_proxy(Runnable)):
            def run(self):
                textView_debug.append("Converted WAV file is :\n" + temp.name)
        activity.runOnUiThread(R())
        time.sleep(3)

    else:
        check_cancel_file()

    return wav_filename


def find_audio_regions(filename, frame_width, min_region_size, max_region_size, activity, textView_debug):
    class R(dynamic_proxy(Runnable)):
        def run(self):
            textView_debug.setText("Finding speech regions of WAV file...\n\n");
    activity.runOnUiThread(R())

    files_dir = str(context.getExternalFilesDir(None))
    cache_dir = str(context.getExternalCacheDir())

    region_start_file = join(cache_dir, 'region_starts.txt')
    elapsed_time_file = join(cache_dir, 'elapsed_time.txt')
    if os.path.isfile(region_start_file): os.remove(region_start_file)
    if os.path.isfile(elapsed_time_file): os.remove(elapsed_time_file)

    cancel_file = join(files_dir, 'cancel.txt')
    if not os.path.isfile(cancel_file):
        reader = wave.open(filename)
        sample_width = reader.getsampwidth()
        rate = reader.getframerate()
        n_channels = reader.getnchannels()

        total_duration = reader.getnframes() / rate
        chunk_duration = float(frame_width) / rate

        n_chunks = int(total_duration / chunk_duration)
        energies = []

        for i in range(n_chunks):
            chunk = reader.readframes(frame_width)
            energies.append(audioop.rms(chunk, sample_width * n_channels))

        threshold = percentile(energies, 0.2)
        elapsed_time = 0

        regions = []
        region_start = None

        for energy in energies:
            is_silence = energy <= threshold
            max_exceeded = region_start and elapsed_time - region_start >= max_region_size

            if (max_exceeded or is_silence) and region_start:
                if elapsed_time - region_start >= min_region_size:
                    regions.append((region_start, elapsed_time))

                    frs = open(region_start_file, 'a')
                    frs.write(f'{region_start}\n')
                    frs.close()

                    fet = open(elapsed_time_file, 'a')
                    fet.write(f'{elapsed_time}\n')
                    fet.close()

                    region_start = None

            elif (not region_start) and (not is_silence):
                region_start = elapsed_time
            elapsed_time += chunk_duration

        num = len(regions)
        time.sleep(1)
        class R(dynamic_proxy(Runnable)):
            def run(self):
                textView_debug.append("Speech regions found = " + str(num))
        activity.runOnUiThread(R())
        time.sleep(3)

    else:
        check_cancel_file()

    #class R(dynamic_proxy(Runnable)):
        #def run(self):
            #textView_debug.append("Speech regions are :\n" + str(regions) + "\n")
    #activity.runOnUiThread(R())

    return regions


def perform_speech_recognition(filename, wav_filename, src, activity, textView_debug):
    print("Performing speech recognition...")
    time.sleep(1)
    class R(dynamic_proxy(Runnable)):
        def run(self):
            textView_debug.setText("Performing speech recognition...\n")
    activity.runOnUiThread(R())
    time.sleep(1)

    cache_dir =  str(context.getExternalCacheDir())
    files_dir = str(context.getExternalFilesDir(None))
    cancel_file = join(files_dir, 'cancel.txt')

    region_start = []
    region_start_file = join(cache_dir, 'region_starts.txt')
    elapsed_time_file = join(cache_dir, 'elapsed_time.txt')
    frs = open(region_start_file, 'r')
    for line1 in frs:
        # Remove linebreak which is the last character of the string
        curr_region_start = line1[:-1]
        # Add item to the list
        region_start.append(float(curr_region_start))
    frs.close()

    elapsed_time = []
    fet = open(elapsed_time_file, 'r')
    for line2 in fet:
        curr_elapsed_time = line2[:-1]
        elapsed_time.append(float(curr_elapsed_time))
    fet.close()

    regions = []
    for k in range(len(region_start)):
        regions.append((region_start[k], elapsed_time[k]))

    pool = multiprocessing.pool.ThreadPool(10)
    
    #check_cancel_file()

    converter = FLACConverter(source_path=wav_filename)

    check_cancel_file()

    audio_rate = 16000
    recognizer = SpeechRecognizer(language=src, rate=audio_rate, api_key=GOOGLE_SPEECH_API_KEY)
    transcriptions = []

    check_cancel_file()

    if regions:
        try:
            if not os.path.isfile(cancel_file):
                extracted_regions = []

                #widgets = ["Converting speech regions to FLAC files : ", Percentage(), ' ', Bar(), ' ', ETA()]
                #pbar = ProgressBar(widgets=widgets, maxval=len(regions)).start()

                time.sleep(1)
                print("Converting speech regions to FLAC")
                for i, extracted_region in enumerate(pool.imap(converter, regions)):
                    check_cancel_file()
                    extracted_regions.append(extracted_region)
                    pBar(i, len(regions), "Converting speech regions to FLAC: ", activity, textView_debug)
                pBar(len(regions), len(regions), "Converting speech regions to FLAC: ", activity, textView_debug) 
                time.sleep(1)

            check_cancel_file()

            if not os.path.isfile(cancel_file):
                #widgets = ["Performing speech recognition           : ", Percentage(), ' ', Bar(), ' ', ETA()]
                #pbar = ProgressBar(widgets=widgets, maxval=len(regions)).start()

                time.sleep(1)
                print("Creating transcriptions")
                for i, transcription in enumerate(pool.imap(recognizer, extracted_regions)):
                    check_cancel_file()
                    transcriptions.append(transcription)
                    pBar(i, len(regions), "Creating transcriptions: ", activity, textView_debug)
                pBar(len(regions), len(regions), "Creating transcriptions: ", activity, textView_debug)
                time.sleep(1)

                cache_dir = str(context.getExternalCacheDir())
                transcriptions_file = join(cache_dir, "transcriptions.txt")
                ft = open(transcriptions_file, 'w')
                ft.write('')
                ft.close()
                ft = open(transcriptions_file, 'a')
                for t in transcriptions:
                    if t:
                        ft.write(f'{t}\n')
                ft.close()

            check_cancel_file()
        
            timed_subtitles = [(r, t) for r, t in zip(regions, transcriptions) if t]
            formatter = FORMATTERS.get("srt")
            formatted_subtitles = formatter(timed_subtitles)

            base, ext = os.path.splitext(filename)
            srt_file = "{base}.{format}".format(base=base, format="srt")

            with open(srt_file, 'wb') as f:
                f.write(formatted_subtitles.encode("utf-8"))
                f.close()

            with open(srt_file, 'a') as f:
                f.write("\n")
                f.close()

            os.remove(wav_filename)

            check_cancel_file()
        
        except KeyboardInterrupt:
            print("Cancelling transcription")
            if wav_filename:
                if os.path.isfile(wav_filename): os.remove(wav_filename)
            if os.path.isfile(cancel_file): os.remove(cancel_file)
            converter = None
            recognizer = None
            for extracted_region in extracted_regions:
                if extracted_region:
                    if os.path.isfile(extracted_region): os.remove(extracted_region)
                extracted_regions = None
            for transcription in transcriptions:
                transcription = None
            transcriptions = None
            if srt_file:
                if os.path.isfile(srt_file): os.remove(srt_file)
            if translated_srt_file:
                if os.path.isfile(translated_srt_file): os.remove(translated_srt_file)
            if pbar: pbar = None
            if pool:
                pool.terminate()
                pool.close()
                pool.join()
                pool = None
            class R(dynamic_proxy(Runnable)):
                def run(self):
                    time.sleep(1)
                    textView_debug.setText("Process has been canceled")
            activity.runOnUiThread(R())
    
    #class C(dynamic_proxy(Runnable)):
        #def run(self):
            #time.sleep(1)
            #textView_debug.append("SRT subtitle file created at : " + srt_file + "\n");
    #activity.runOnUiThread(C())

    if pool:
        pool.close()
        pool.join()
        pool = None

    return srt_file


def perform_translation(srt_file, src, dest, activity, textView_debug):
    print("Translating transcriptions...")
    class C(dynamic_proxy(Runnable)):
        def run(self):
            textView_debug.setText("Translating transcriptions...\n\n");
    activity.runOnUiThread(C())

    files_dir = str(context.getExternalFilesDir(None))
    cache_dir = str(context.getExternalCacheDir())
    cancel_file = join(files_dir, 'cancel.txt')

    check_cancel_file()

    cache_dir = str(context.getExternalCacheDir())
    transcriptions_file = join(cache_dir, "transcriptions.txt")
    transcriptions = []
    ft = open(transcriptions_file, "r")
    for line in ft:
        curr_transcriptions = line[:-1]
        transcriptions.append(curr_transcriptions)
    ft.close()

    region_start = []
    region_start_file = join(cache_dir, 'region_starts.txt')
    elapsed_time_file = join(cache_dir, 'elapsed_time.txt')
    frs = open(region_start_file, 'r')
    for line1 in frs:
        # Remove linebreak which is the last character of the string
        curr_region_start = line1[:-1]
        # Add item to the list
        region_start.append(float(curr_region_start))
    frs.close()

    check_cancel_file()

    elapsed_time = []
    fet = open(elapsed_time_file, 'r')
    for line2 in fet:
        curr_elapsed_time = line2[:-1]
        elapsed_time.append(float(curr_elapsed_time))
    fet.close()

    regions = []
    for k in range(len(region_start)):
        regions.append((region_start[k], elapsed_time[k]))


    translated_srt_file = None
    pool = multiprocessing.pool.ThreadPool(10)

    try:
        check_cancel_file()

        if (not is_same_language(src, dest)) and (os.path.isfile(srt_file)) and (not os.path.isfile(cancel_file)):
            translated_srt_file = srt_file[ :-4] + '_translated.srt'

            entries = entries_generator(srt_file)
            total_entries = CountEntries(srt_file)
            print('Total Entries = {}'.format(total_entries))

            #prompt = "Translating from %5s to %5s         : " %(src, dest)
            #widgets = [prompt, Percentage(), ' ', Bar(), ' ', ETA()]
            #pbar = ProgressBar(widgets=widgets, maxval=total_entries).start()

            '''
            e=0
            with open(translated_srt_file, 'w', encoding='utf-8') as f:
                time.sleep(1)
                #for number_in_sequence, timecode, subtitles, count_failure, count_entries in translate(entries, src=src, dest=dest, patience="", verbose=""):
                for number_in_sequence, timecode, subtitles, count_failure, count_entries in pool.imap(translate, entries, src=src, dest=dest, patience="", verbose=""):
                    check_cancel_file()
                    f.write(number_in_sequence)
                    f.write(timecode)
                    for subtitle in subtitles:
                        f.write(subtitle)
                        f.write('\n')
                        e += 1
                        pBar(e, total_entries, "Translating from %s to %s: " %(src, dest), activity, textView_debug)
                        #pbar.update(e)
                #pbar.finish()
                pBar(total_entries, total_entries, "Translating from %s to %s: " %(src, dest), activity, textView_debug)
                time.sleep(1)
            '''

            subtitle_translator = SubtitleTranslator(src=src, dest=dest)
            translated_entries = []
            for i, translated_entry in enumerate(pool.imap(subtitle_translator, entries)):
                check_cancel_file()
                translated_entries.append(translated_entry)
                pBar(i, total_entries, "Translating from %s to %s: " %(src, dest), activity, textView_debug)
            pBar(total_entries, total_entries, "Translating from %s to %s: " %(src, dest), activity, textView_debug)

            with open(translated_srt_file, 'w', encoding='utf-8') as f:
                for number_in_sequence, timecode, translated_subtitles in translated_entries:
                    f.write(number_in_sequence)
                    f.write(timecode)
                    for translated_subtitle in translated_subtitles:
                        f.write(translated_subtitle)
                        f.write('\n')

            print('Done.')
            print("Original subtitles file created at      : {}".format(srt_file))
            print('Translated subtitles file created at    : {}' .format(translated_srt_file))
            #print('Total failure to translate entries      : {0}/{1}'.format(count_failure, count_entries))
            #failure_ratio = count_failure / count_entries
            #if failure_ratio > 0:
                #print('If you expect a lower failure ratio or completed translate, please check out the usage of [-p | --postion] argument.')

    except KeyboardInterrupt:
        print("Cancelling transcription")
        if wav_filename:
            if os.path.isfile(wav_filename):
                os.remove(wav_filename)
        if os.path.isfile(cancel_file): os.remove(cancel_file)
        converter = None
        recognizer = None
        for extracted_region in extracted_regions:
            if os.path.isfile(extracted_region): os.remove(extracted_region)
        extracted_regions = None
        for transcription in transcriptions:
            transcription = None
        transcriptions = None
        extracted_regions = None
        if srt_file:
            if os.path.isfile(srt_file): os.remove(srt_file)
        if translated_srt_file:
            if os.path.isfile(translated_srt_file): os.remove(translated_srt_file)
        class R(dynamic_proxy(Runnable)):
            def run(self):
                time.sleep(1)
                textView_debug.setText("Process has been canceled")
        activity.runOnUiThread(R())

    class R(dynamic_proxy(Runnable)):
        def run(self):
            textView_debug.append("\n\nSRT subtitles file created at :\n")
            textView_debug.append(srt_file + "\n")
            textView_debug.append("\nTranslated SRT subtitles file created at:\n")
            textView_debug.append(translated_srt_file + "\n\n")
            textView_debug.append("Done!\n")
    activity.runOnUiThread(R())

    if pool:
        pool.close()
        pool.join()
        pool = None

    cache_dir = str(context.getExternalCacheDir())
    transcriptions_file = join(cache_dir, "transcriptions.txt")
    if os.path.isfile(transcriptions_file): os.remove(transcriptions_file)
    cache_dir = str(context.getExternalCacheDir())
    region_start_file = join(cache_dir, 'region_starts.txt')
    elapsed_time_file = join(cache_dir, 'elapsed_time.txt')
    if os.path.isfile(region_start_file): os.remove(region_start_file)
    if os.path.isfile(elapsed_time_file): os.remove(elapsed_time_file)

    return translated_srt_file


def printEnvironmentDir():
    files_dir = str(context.getExternalFilesDir(None))
    print("files_dir = {}".format(files_dir))
    # /storage/emulated/0/Android/data/com.android.autosrt/files

    cache_dir = str(context.getExternalCacheDir())
    print("cache_dir = {}".format(cache_dir))
    # /storage/emulated/0/Android/data/com.android.autosrt/cache

    home_dir = os.environ["HOME"]
    print("home_dir = {}".format(home_dir))
    # /data/user/0/com.android.autosrt/files
    # same as str(context.getFilesDirs()) 

    # array /storage/emulated/0/Android/data/com.android.autosrt/files/Pictures
    picture_files_dirs = []
    picture_files_dirs = str(context.getExternalFilesDirs("Picture"))
    for pfd in picture_files_dirs:
        print("picture_files_dirs = {}".format(picture_files_dirs))

    #files_dirs = []
    #files_dirs = str(context.getExternalFilesDirs(None))
    #for fd in files_dirs:
        #print("files_dirs = {}".format(fd))

    #media_dirs = []
    #media_dirs = str(context.getExternalMediaDirs())
    #for md in media_dirs:
        #print("media_dirs = {}".format(md))
    # /storage/emulated/0/Android/media
 
    return "OK"

def pBar(count_value, total, prefix, activity, textView_debug):
    bar_length = 10
    filled_up_Length = int(round(bar_length*count_value/(total)))
    percentage = round(100.0 * count_value/(total),1)
    bar = '#' * filled_up_Length + '=' * (bar_length - filled_up_Length)
    # dynamic_proxy will make app crash if repeatly called to fast that's why we made a barrier 'if (int(percentage) % 10 == 0):'
    if (int(percentage) % 10 == 0):
        time.sleep(1)
        class R(dynamic_proxy(Runnable)):
            def run(self):
                textView_debug.setText('%s [%s] %s%s\r' %(prefix, bar, int(percentage), '%'))
        activity.runOnUiThread(R())


def progressbar(count_value, total, prefix='', suffix=''):
    bar_length = 50
    filled_up_Length = int(round(bar_length* count_value / float(total)))
    percentage = round(100.0 * count_value/float(total),1)
    bar = '#' * filled_up_Length + '=' * (bar_length - filled_up_Length)
    sys.stdout.write('%s [%s] %s%s %s\r' %(prefix, bar, percentage, '%', suffix))
    sys.stdout.flush()


def print_it(i, activity, textView_debug):
    threading.Timer(5.0, print_it, args=[i, activity, textView_debug]).start()
    #print(i)
    class R(dynamic_proxy(Runnable)):
        def run(self):
            textView_debug.setText(str(i))
    activity.runOnUiThread(R())


def check_cancel_file():
    if os.path.isfile(cancel_file):
        os.remove(cancel_file)
        if wav_filename:
            if os.path.isfile(wav_filename):
                os.remove(wav_filename)
        converter = None
        recognizer = None
        if extracted_regions:
            for extracted_region in extracted_regions:
                if os.path.isfile(extracted_region): os.remove(extracted_region)
            extracted_regions = None
        if transcriptions:
            for transcription in transcriptions:
                transcription = None
            transcriptions = None
        if srt_file:
            if os.path.isfile(srt_file): os.remove(srt_file)
        if translated_srt_file:
            if os.path.isfile(translated_srt_file): os.remove(translated_srt_file)
        class R(dynamic_proxy(Runnable)):
            def run(self):
                textView_debug.setText("Process has been canceled")
                time.sleep(1)
        activity.runOnUiThread(R())

   

if __name__ == '__main__':
    multiprocessing.freeze_support()
    sys.exit(main())
