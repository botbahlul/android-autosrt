#!/usr/bin/env python
from __future__ import absolute_import, print_function, unicode_literals
import audioop
import math
import multiprocessing
import threading
import io, sys, os, time, signal, shutil
import tempfile
import wave
import json
import requests
try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError
import pysrt
import six
import httpx

from com.arthenica.mobileffmpeg import FFmpeg
from os.path import dirname, join
from com.chaquo.python import Python

from java import dynamic_proxy, static_proxy
from java.lang import Runnable

context = Python.getPlatform().getApplication()
files_dir = str(context.getExternalFilesDir(None))
cancel_file = join(files_dir, 'cancel.txt')
cache_dir = str(context.getExternalCacheDir())
transcriptions_file = join(cache_dir, "transcriptions.txt")
region_start_file = join(cache_dir, 'region_starts.txt')
elapsed_time_file = join(cache_dir, 'elapsed_time.txt')
wav_filename = None
subtitle_file = None
translated_subtitle_file = None
converter = None
recognizer = None
extracted_regions = None
transcription = None
subtitle_folder_name = None
pool = None

GOOGLE_SPEECH_API_KEY = "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
GOOGLE_SPEECH_API_URL = "http://www.google.com/speech-api/v2/recognize?client=chromium&lang={lang}&key={key}" # pylint: disable=line-too-long

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
arraylist_language_code.append("my")
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


def vtt_formatter(subtitles, padding_before=0, padding_after=0):
    """
    Serialize a list of subtitles according to the VTT format, with optional time padding.
    """
    text = srt_formatter(subtitles, padding_before, padding_after)
    text = 'WEBVTT\n\n' + text.replace(',', '.')
    return text


def json_formatter(subtitles):
    """
    Serialize a list of subtitles as a JSON blob.
    """
    subtitle_dicts = [
        {
            'start': start,
            'end': end,
            'content': text,
        }
        for ((start, end), text)
        in subtitles
    ]
    return json.dumps(subtitle_dicts)


def raw_formatter(subtitles):
    """
    Serialize a list of subtitles as a newline-delimited string.
    """
    return ' '.join(text for (_rng, text) in subtitles)


FORMATTERS = {
    'srt': srt_formatter,
    'vtt': vtt_formatter,
    'json': json_formatter,
    'raw': raw_formatter,
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


def GoogleTranslate(text, src, dst):
    url = 'https://translate.googleapis.com/translate_a/'
    params = 'single?client=gtx&sl='+src+'&tl='+dst+'&dt=t&q='+text;
    #async with httpx.AsyncClient() as client:
    with httpx.Client(http2=True) as client:
        client.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Referer': 'https://translate.google.com',})
        response = client.get(url+params)
        #print('response.status_code = {}'.format(response.status_code))
        if response.status_code == 200:
            response_json = response.json()[0]
            #print('response_json = {}'.format(response_json))
            length = len(response_json)
            #print('length = {}'.format(length))
            translation = ""
            for i in range(length):
                #print("{} {}".format(i, response_json[i][0]))
                translation = translation + response_json[i][0]
            return translation
        return


class TranscriptionTranslator(object):
    def __init__(self, src, dest, patience=-1):
        self.src = src
        self.dest = dest
        self.patience = patience

    def __call__(self, sentence):
        translated_sentence = []
        # handle the special case: empty string.
        if not sentence:
            return None

        translated_sentence = GoogleTranslate(sentence, src=self.src, dst=self.dest)

        fail_to_translate = translated_sentence[-1] == '\n'
        while fail_to_translate and patience:
            translated_sentence = GoogleTranslate(translated_sentence, src=self.src, dest=self.dest).text
            if translated_sentence[-1] == '\n':
                if patience == -1:
                    continue
                patience -= 1
            else:
                fail_to_translate = False
        return translated_sentence


def extract_audio(filePath, channels=1, rate=16000):
    temp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    if not os.path.isfile(filePath):
        print("The given file does not exist: {0}".format(filePath))
        raise Exception("Invalid filepath: {0}".format(filePath))
    FFmpeg.execute("-y -i " + "\"" + filePath + "\"" + " -ac " + str(channels) + " -ar " + str(rate) + " " + "\"" + temp.name + "\"" )
    return temp.name, rate


#def find_speech_regions(wav_file, frame_width=4096, min_region_size=0.5, max_region_size=6):
def find_speech_regions(wav_file, frame_width=4096, min_region_size=0.3, max_region_size=8):
    reader  = wave.open(wav_file)
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


def transcribe(src, dest, filename, file_display_name, subtitle_format, activity, textview_debug):
    multiprocessing.freeze_support()
    if os.path.isfile(cancel_file):
        os.remove(cancel_file)
        class R(dynamic_proxy(Runnable)):
            def run(self):
                time.sleep(1)
                textview_debug.setText("")
                textview_debug.setText("Process has been canceled")
        activity.runOnUiThread(R())
        return

    wav_filename = None
    subtitle_file = None
    translated_subtitle_file = None

    if os.path.isfile(cancel_file):
        os.remove(cancel_file)
        class R(dynamic_proxy(Runnable)):
            def run(self):
                time.sleep(1)
                textview_debug.setText("")
                textview_debug.setText("Process has been canceled")
        activity.runOnUiThread(R())
        return

    pool = multiprocessing.pool.ThreadPool(10)

    print("Converting {} to a temporary WAV file".format(file_display_name))
    class R(dynamic_proxy(Runnable)):
        def run(self):
            textview_debug.setText("Running python script...\n");
            textview_debug.append("Converting {} to a temporary WAV file...\n".format(file_display_name))
    activity.runOnUiThread(R())
    time.sleep(1)
    wav_filename, audio_rate = extract_audio(filename)
    print("{} converted WAV file is : {}".format(file_display_name, wav_filename))
    if wav_filename:
        class R(dynamic_proxy(Runnable)):
            def run(self):
                textview_debug.append("{} converted WAV file is :\n".format(file_display_name) + wav_filename)
        activity.runOnUiThread(R())
        time.sleep(2)

    if os.path.isfile(cancel_file):
        os.remove(cancel_file)
        pool.terminate()
        pool.close()
        class R(dynamic_proxy(Runnable)):
            def run(self):
                time.sleep(1)
                textview_debug.setText("")
                textview_debug.setText("Process has been canceled")
        activity.runOnUiThread(R())
        return

    print("Finding speech regions of WAV file")
    class R(dynamic_proxy(Runnable)):
        def run(self):
            textview_debug.setText("Finding speech regions of WAV file...\n")
    activity.runOnUiThread(R())
    regions = find_speech_regions(wav_filename)
    num = len(regions)
    time.sleep(1)
    class R(dynamic_proxy(Runnable)):
        def run(self):
            textview_debug.append("Speech regions found = " + str(num) + "\n")
    activity.runOnUiThread(R())
    print("Speech regions found = {}".format(str(num)))
    time.sleep(3)

    if os.path.isfile(cancel_file):
        os.remove(cancel_file)
        pool.terminate()
        pool.close()
        class R(dynamic_proxy(Runnable)):
            def run(self):
                time.sleep(1)
                textview_debug.setText("")
                textview_debug.setText("Process has been canceled")
        activity.runOnUiThread(R())
        return

    converter = FLACConverter(source_path=wav_filename)
    recognizer = SpeechRecognizer(language=src, rate=audio_rate, api_key=GOOGLE_SPEECH_API_KEY)
    transcriptions = []

    if os.path.isfile(cancel_file):
        os.remove(cancel_file)
        pool.terminate()
        pool.close()
        class R(dynamic_proxy(Runnable)):
            def run(self):
                time.sleep(1)
                textview_debug.setText("")
                textview_debug.setText("Process has been canceled")
        activity.runOnUiThread(R())
        return

    if regions:
        time.sleep(2)
        print("Converting speech regions to FLAC files")
        extracted_regions = []
        for i, extracted_region in enumerate(pool.imap(converter, regions)):

            if os.path.isfile(cancel_file):
                os.remove(cancel_file)
                pool.terminate()
                pool.close()
                class R(dynamic_proxy(Runnable)):
                    def run(self):
                        time.sleep(1)
                        textview_debug.setText("")
                        textview_debug.setText("Process has been canceled")
                activity.runOnUiThread(R())
                return

            extracted_regions.append(extracted_region)
            pBar(i, len(regions), "Converting speech regions to FLAC : ", activity, textview_debug)
        time.sleep(1)
        pBar(len(regions), len(regions), "Converting speech regions to FLAC : ", activity, textview_debug)

        if os.path.isfile(cancel_file):
            os.remove(cancel_file)
            pool.terminate()
            pool.close()
            class R(dynamic_proxy(Runnable)):
                def run(self):
                    time.sleep(1)
                    textview_debug.setText("")
                    textview_debug.setText("Process has been canceled")
            activity.runOnUiThread(R())
            return

        time.sleep(2)
        print("Creating subtitles")
        for i, transcription in enumerate(pool.imap(recognizer, extracted_regions)):

            if os.path.isfile(cancel_file):
                os.remove(cancel_file)
                pool.terminate()
                pool.close()
                class R(dynamic_proxy(Runnable)):
                    def run(self):
                        time.sleep(1)
                        textview_debug.setText("")
                        textview_debug.setText("Process has been canceled")
                activity.runOnUiThread(R())
                return

            transcriptions.append(transcription)
            pBar(i, len(regions), "Creating subtitles : ", activity, textview_debug)
        time.sleep(1)
        pBar(len(regions), len(regions), "Creating subtitles : ", activity, textview_debug)

        if os.path.isfile(cancel_file):
            os.remove(cancel_file)
            pool.terminate()
            pool.close()
            class R(dynamic_proxy(Runnable)):
                def run(self):
                    time.sleep(1)
                    textview_debug.setText("")
                    textview_debug.setText("Process has been canceled")
            activity.runOnUiThread(R())
            return

        timed_subtitles = [(r, t) for r, t in zip(regions, transcriptions) if t]
        formatter = FORMATTERS.get(subtitle_format)
        formatted_subtitles = formatter(timed_subtitles)

        files_dir = str(context.getExternalFilesDir(None))
        subtitle_folder_name = join(files_dir, file_display_name[:-4])
        if not os.path.isdir(subtitle_folder_name):
            os.mkdir(subtitle_folder_name)
        subtitle_file = join(subtitle_folder_name, file_display_name[:-4] + "." + subtitle_format)

        if os.path.isfile(cancel_file):
            os.remove(cancel_file)
            pool.terminate()
            pool.close()
            class R(dynamic_proxy(Runnable)):
                def run(self):
                    time.sleep(1)
                    textview_debug.setText("")
                    textview_debug.setText("Process has been canceled")
            activity.runOnUiThread(R())
            return

        with open(subtitle_file, 'wb') as f:
            f.write(formatted_subtitles.encode("utf-8"))
            f.close()

        with open(subtitle_file, 'a') as f:
            f.write("\n")
            f.close()


        if (not is_same_language(src, dest)) and (os.path.isfile(subtitle_file)) and (not os.path.isfile(cancel_file)):

            if os.path.isfile(cancel_file):
                os.remove(cancel_file)
                pool.terminate()
                pool.close()
                class R(dynamic_proxy(Runnable)):
                    def run(self):
                        time.sleep(1)
                        textview_debug.setText("")
                        textview_debug.setText("Process has been canceled")
                activity.runOnUiThread(R())
                return

            translated_subtitle_file = subtitle_file[ :-4] + '.translated.' + subtitle_format

            created_regions = []
            created_subtitles = []
            for entry in timed_subtitles:
                created_regions.append(entry[0])
                created_subtitles.append(entry[1])

            transcription_translator = TranscriptionTranslator(src=src, dest=dest)
            translated_transcriptions = []
            time.sleep(1)
            print("Translating subtitles")
            for i, translated_transcription in enumerate(pool.imap(transcription_translator, created_subtitles)):

                if os.path.isfile(cancel_file):
                    os.remove(cancel_file)
                    pool.terminate()
                    pool.close()
                    class R(dynamic_proxy(Runnable)):
                        def run(self):
                            time.sleep(1)
                            textview_debug.setText("")
                            textview_debug.setText("Process has been canceled")
                    activity.runOnUiThread(R())
                    return

                translated_transcriptions.append(translated_transcription)
                pBar(i, len(transcriptions), "Translating subtitles : " , activity, textview_debug)
            time.sleep(2)
            pBar(len(transcriptions), len(transcriptions), "Translating subtitles : ", activity, textview_debug)

            if os.path.isfile(cancel_file):
                os.remove(cancel_file)
                pool.terminate()
                pool.close()
                class R(dynamic_proxy(Runnable)):
                    def run(self):
                        time.sleep(1)
                        textview_debug.setText("")
                        textview_debug.setText("Process has been canceled")
                activity.runOnUiThread(R())
                return

            timed_translated_subtitles = [(r, t) for r, t in zip(created_regions, translated_transcriptions) if t]
            formatter = FORMATTERS.get(subtitle_format)
            formatted_translated_subtitles = formatter(timed_translated_subtitles)

            with open(translated_subtitle_file, 'wb') as f:
                f.write(formatted_translated_subtitles.encode("utf-8"))
            with open(translated_subtitle_file, 'a') as f:
                f.write("\n")

            if os.path.isfile(cancel_file):
                os.remove(cancel_file)
                pool.terminate()
                pool.close()
                class R(dynamic_proxy(Runnable)):
                    def run(self):
                        time.sleep(1)
                        textview_debug.setText("")
                        textview_debug.setText("Process has been canceled")
                activity.runOnUiThread(R())
                return

            print('Temporary subtitles file created at            : {}'.format(subtitle_file))
            print('Temporary translated subtitles file created at : {}'.format(translated_subtitle_file))

            class R(dynamic_proxy(Runnable)):
                def run(self):
                    time.sleep(2)
                    textview_debug.append("\nTemporary subtitles file created at :\n")
                    textview_debug.append(subtitle_file + "\n")
                    textview_debug.append("Temporary translated subtitles file created at:\n")
                    textview_debug.append(translated_subtitle_file + "\n")
            activity.runOnUiThread(R())
            time.sleep(3)

            if os.path.isfile(cancel_file):
                os.remove(cancel_file)
                pool.terminate()
                pool.close()
                class R(dynamic_proxy(Runnable)):
                    def run(self):
                        time.sleep(1)
                        textview_debug.setText("")
                        textview_debug.setText("Process has been canceled")
                activity.runOnUiThread(R())
                return

        elif (is_same_language(src, dest)) and (os.path.isfile(subtitle_file)) and (not os.path.isfile(cancel_file)):
            print("Temporary subtitles file created at      : {}".format(subtitle_file))
            class R(dynamic_proxy(Runnable)):
                def run(self):
                    time.sleep(1)
                    textview_debug.append("\nTemporary subtitles file created at :\n")
                    textview_debug.append(subtitle_file + "\n")
            activity.runOnUiThread(R())
            time.sleep(2)

    pool.close()
    pool.join()
    pool = None
    os.remove(wav_filename)
    tmpdir = os.path.split(wav_filename)[0]
    for file in os.listdir(tmpdir):
        file_path = os.path.join(tmpdir, file)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        else:
            shutil.rmtree(file_path)

    return subtitle_file


def pBar(count_value, total, prefix, activity, textview_debug):
    bar_length = 10
    filled_up_Length = int(round(bar_length*count_value/(total)))
    percentage = round(100.0 * count_value/(total),1)
    #bar = '#' * filled_up_Length + ' ' * (bar_length - filled_up_Length)
    bar = '█' * filled_up_Length + '-' * (bar_length - filled_up_Length)
    # dynamic_proxy will make app crash if repeatly called to fast that's why we made a BARRIER 'if (int(percentage) % 10 == 0):'
    # and time.sleep(seconds)
    if (int(percentage) % 10 == 0):
        time.sleep(1)
        class R(dynamic_proxy(Runnable)):
            def run(self):
                #textview_debug.setText('%s[%10s]%3s%s\r' %(prefix, bar, int(percentage), '%'))
                textview_debug.setText('%s|%10s|%3s%s\r' %(prefix, bar, int(percentage), '%'))
        activity.runOnUiThread(R())
