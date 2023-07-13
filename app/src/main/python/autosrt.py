from __future__ import absolute_import, print_function, unicode_literals
import audioop
import math
import multiprocessing
import threading
import io, sys, os, time, signal, shutil
from datetime import datetime, timedelta
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
from os.path import dirname, join
from com.chaquo.python import Python

from java import dynamic_proxy, static_proxy, jvoid, Override, method, constructor, jclass
from java.lang import Runnable
from android.os import Bundle
from com.android.autosrt import R
from androidx.appcompat.widget import AppCompatTextView
from androidx.appcompat.app import AppCompatActivity
from android.widget import ProgressBar
from android.view import View, Gravity
from java.util.concurrent.atomic import AtomicReference
from android.net import Uri
from java.io import File
from android.media import MediaPlayer
import shlex

from com.arthenica.mobileffmpeg import FFmpeg, FFprobe, Config, Statistics, StatisticsCallback
'''
FFmpeg = jclass('com.arthenica.mobileffmpeg.FFmpeg')
FFprobe = jclass('com.arthenica.mobileffmpeg.FFprobe')
Config = jclass('com.arthenica.mobileffmpeg.Config')
Statistics = jclass('com.arthenica.mobileffmpeg.Statistics')
StatisticsCallback = jclass('com.arthenica.mobileffmpeg.StatisticsCallback')
'''

context = Python.getPlatform().getApplication()
files_dir = str(context.getExternalFilesDir(None))
cancel_file = join(files_dir, 'cancel.txt')
cache_dir = str(context.getExternalCacheDir())
transcriptions_file = join(cache_dir, "src_transcriptions.txt")
region_start_file = join(cache_dir, 'region_starts.txt')
elapsed_time_file = join(cache_dir, 'elapsed_time.txt')
wav_filepath = None
src_subtitle_filepath = None
dst_subtitle_filepath = None
converter = None
recognizer = None
extracted_regions = None
src_transcription = None
subtitle_folder_name = None
pool = None
lines = 0
maxLinesOfOutputMessages = 0


class Language:
    def __init__(self):
        self.list_codes = []
        self.list_codes.append("af")
        self.list_codes.append("sq")
        self.list_codes.append("am")
        self.list_codes.append("ar")
        self.list_codes.append("hy")
        self.list_codes.append("as")
        self.list_codes.append("ay")
        self.list_codes.append("az")
        self.list_codes.append("bm")
        self.list_codes.append("eu")
        self.list_codes.append("be")
        self.list_codes.append("bn")
        self.list_codes.append("bho")
        self.list_codes.append("bs")
        self.list_codes.append("bg")
        self.list_codes.append("ca")
        self.list_codes.append("ceb")
        self.list_codes.append("ny")
        self.list_codes.append("zh")
        self.list_codes.append("zh-CN")
        self.list_codes.append("zh-TW")
        self.list_codes.append("co")
        self.list_codes.append("hr")
        self.list_codes.append("cs")
        self.list_codes.append("da")
        self.list_codes.append("dv")
        self.list_codes.append("doi")
        self.list_codes.append("nl")
        self.list_codes.append("en")
        self.list_codes.append("eo")
        self.list_codes.append("et")
        self.list_codes.append("ee")
        self.list_codes.append("fil")
        self.list_codes.append("fi")
        self.list_codes.append("fr")
        self.list_codes.append("fy")
        self.list_codes.append("gl")
        self.list_codes.append("ka")
        self.list_codes.append("de")
        self.list_codes.append("el")
        self.list_codes.append("gn")
        self.list_codes.append("gu")
        self.list_codes.append("ht")
        self.list_codes.append("ha")
        self.list_codes.append("haw")
        self.list_codes.append("he")
        self.list_codes.append("hi")
        self.list_codes.append("hmn")
        self.list_codes.append("hu")
        self.list_codes.append("is")
        self.list_codes.append("ig")
        self.list_codes.append("ilo")
        self.list_codes.append("id")
        self.list_codes.append("ga")
        self.list_codes.append("it")
        self.list_codes.append("ja")
        self.list_codes.append("jv")
        self.list_codes.append("kn")
        self.list_codes.append("kk")
        self.list_codes.append("km")
        self.list_codes.append("rw")
        self.list_codes.append("gom")
        self.list_codes.append("ko")
        self.list_codes.append("kri")
        self.list_codes.append("kmr")
        self.list_codes.append("ckb")
        self.list_codes.append("ky")
        self.list_codes.append("lo")
        self.list_codes.append("la")
        self.list_codes.append("lv")
        self.list_codes.append("ln")
        self.list_codes.append("lt")
        self.list_codes.append("lg")
        self.list_codes.append("lb")
        self.list_codes.append("mk")
        self.list_codes.append("mg")
        self.list_codes.append("ms")
        self.list_codes.append("ml")
        self.list_codes.append("mt")
        self.list_codes.append("mi")
        self.list_codes.append("mr")
        self.list_codes.append("mni-Mtei")
        self.list_codes.append("lus")
        self.list_codes.append("mn")
        self.list_codes.append("my")
        self.list_codes.append("ne")
        self.list_codes.append("no")
        self.list_codes.append("or")
        self.list_codes.append("om")
        self.list_codes.append("ps")
        self.list_codes.append("fa")
        self.list_codes.append("pl")
        self.list_codes.append("pt")
        self.list_codes.append("pa")
        self.list_codes.append("qu")
        self.list_codes.append("ro")
        self.list_codes.append("ru")
        self.list_codes.append("sm")
        self.list_codes.append("sa")
        self.list_codes.append("gd")
        self.list_codes.append("nso")
        self.list_codes.append("sr")
        self.list_codes.append("st")
        self.list_codes.append("sn")
        self.list_codes.append("sd")
        self.list_codes.append("si")
        self.list_codes.append("sk")
        self.list_codes.append("sl")
        self.list_codes.append("so")
        self.list_codes.append("es")
        self.list_codes.append("su")
        self.list_codes.append("sw")
        self.list_codes.append("sv")
        self.list_codes.append("tg")
        self.list_codes.append("ta")
        self.list_codes.append("tt")
        self.list_codes.append("te")
        self.list_codes.append("th")
        self.list_codes.append("ti")
        self.list_codes.append("ts")
        self.list_codes.append("tr")
        self.list_codes.append("tk")
        self.list_codes.append("tw")
        self.list_codes.append("uk")
        self.list_codes.append("ur")
        self.list_codes.append("ug")
        self.list_codes.append("uz")
        self.list_codes.append("vi")
        self.list_codes.append("cy")
        self.list_codes.append("xh")
        self.list_codes.append("yi")
        self.list_codes.append("yo")
        self.list_codes.append("zu")

        self.list_names = []
        self.list_names.append("Afrikaans")
        self.list_names.append("Albanian")
        self.list_names.append("Amharic")
        self.list_names.append("Arabic")
        self.list_names.append("Armenian")
        self.list_names.append("Assamese")
        self.list_names.append("Aymara")
        self.list_names.append("Azerbaijani")
        self.list_names.append("Bambara")
        self.list_names.append("Basque")
        self.list_names.append("Belarusian")
        self.list_names.append("Bengali")
        self.list_names.append("Bhojpuri")
        self.list_names.append("Bosnian")
        self.list_names.append("Bulgarian")
        self.list_names.append("Catalan")
        self.list_names.append("Cebuano")
        self.list_names.append("Chichewa")
        self.list_names.append("Chinese")
        self.list_names.append("Chinese (Simplified)")
        self.list_names.append("Chinese (Traditional)")
        self.list_names.append("Corsican")
        self.list_names.append("Croatian")
        self.list_names.append("Czech")
        self.list_names.append("Danish")
        self.list_names.append("Dhivehi")
        self.list_names.append("Dogri")
        self.list_names.append("Dutch")
        self.list_names.append("English")
        self.list_names.append("Esperanto")
        self.list_names.append("Estonian")
        self.list_names.append("Ewe")
        self.list_names.append("Filipino")
        self.list_names.append("Finnish")
        self.list_names.append("French")
        self.list_names.append("Frisian")
        self.list_names.append("Galician")
        self.list_names.append("Georgian")
        self.list_names.append("German")
        self.list_names.append("Greek")
        self.list_names.append("Guarani")
        self.list_names.append("Gujarati")
        self.list_names.append("Haitian Creole")
        self.list_names.append("Hausa")
        self.list_names.append("Hawaiian")
        self.list_names.append("Hebrew")
        self.list_names.append("Hindi")
        self.list_names.append("Hmong")
        self.list_names.append("Hungarian")
        self.list_names.append("Icelandic")
        self.list_names.append("Igbo")
        self.list_names.append("Ilocano")
        self.list_names.append("Indonesian")
        self.list_names.append("Irish")
        self.list_names.append("Italian")
        self.list_names.append("Japanese")
        self.list_names.append("Javanese")
        self.list_names.append("Kannada")
        self.list_names.append("Kazakh")
        self.list_names.append("Khmer")
        self.list_names.append("Kinyarwanda")
        self.list_names.append("Konkani")
        self.list_names.append("Korean")
        self.list_names.append("Krio")
        self.list_names.append("Kurdish (Kurmanji)")
        self.list_names.append("Kurdish (Sorani)")
        self.list_names.append("Kyrgyz")
        self.list_names.append("Lao")
        self.list_names.append("Latin")
        self.list_names.append("Latvian")
        self.list_names.append("Lingala")
        self.list_names.append("Lithuanian")
        self.list_names.append("Luganda")
        self.list_names.append("Luxembourgish")
        self.list_names.append("Macedonian")
        self.list_names.append("Malagasy")
        self.list_names.append("Malay")
        self.list_names.append("Malayalam")
        self.list_names.append("Maltese")
        self.list_names.append("Maori")
        self.list_names.append("Marathi")
        self.list_names.append("Meiteilon (Manipuri)")
        self.list_names.append("Mizo")
        self.list_names.append("Mongolian")
        self.list_names.append("Myanmar (Burmese)")
        self.list_names.append("Nepali")
        self.list_names.append("Norwegian")
        self.list_names.append("Odiya (Oriya)")
        self.list_names.append("Oromo")
        self.list_names.append("Pashto")
        self.list_names.append("Persian")
        self.list_names.append("Polish")
        self.list_names.append("Portuguese")
        self.list_names.append("Punjabi")
        self.list_names.append("Quechua")
        self.list_names.append("Romanian")
        self.list_names.append("Russian")
        self.list_names.append("Samoan")
        self.list_names.append("Sanskrit")
        self.list_names.append("Scots Gaelic")
        self.list_names.append("Sepedi")
        self.list_names.append("Serbian")
        self.list_names.append("Sesotho")
        self.list_names.append("Shona")
        self.list_names.append("Sindhi")
        self.list_names.append("Sinhala")
        self.list_names.append("Slovak")
        self.list_names.append("Slovenian")
        self.list_names.append("Somali")
        self.list_names.append("Spanish")
        self.list_names.append("Sundanese")
        self.list_names.append("Swahili")
        self.list_names.append("Swedish")
        self.list_names.append("Tajik")
        self.list_names.append("Tamil")
        self.list_names.append("Tatar")
        self.list_names.append("Telugu")
        self.list_names.append("Thai")
        self.list_names.append("Tigrinya")
        self.list_names.append("Tsonga")
        self.list_names.append("Turkish")
        self.list_names.append("Turkmen")
        self.list_names.append("Twi (Akan)")
        self.list_names.append("Ukrainian")
        self.list_names.append("Urdu")
        self.list_names.append("Uyghur")
        self.list_names.append("Uzbek")
        self.list_names.append("Vietnamese")
        self.list_names.append("Welsh")
        self.list_names.append("Xhosa")
        self.list_names.append("Yiddish")
        self.list_names.append("Yoruba")
        self.list_names.append("Zulu")

        # NOTE THAT Google Translate AND Vosk Speech Recognition API USE ISO-639-1 STANDARD CODE ('al', 'af', 'as', ETC)
        # WHEN ffmpeg SUBTITLES STREAMS USE ISO 639-2 STANDARD CODE ('afr', 'alb', 'amh', ETC)

        self.list_ffmpeg_codes = []
        self.list_ffmpeg_codes.append("afr")  # Afrikaans
        self.list_ffmpeg_codes.append("alb")  # Albanian
        self.list_ffmpeg_codes.append("amh")  # Amharic
        self.list_ffmpeg_codes.append("ara")  # Arabic
        self.list_ffmpeg_codes.append("hye")  # Armenian
        self.list_ffmpeg_codes.append("asm")  # Assamese
        self.list_ffmpeg_codes.append("aym")  # Aymara
        self.list_ffmpeg_codes.append("aze")  # Azerbaijani
        self.list_ffmpeg_codes.append("bam")  # Bambara
        self.list_ffmpeg_codes.append("eus")  # Basque
        self.list_ffmpeg_codes.append("bel")  # Belarusian
        self.list_ffmpeg_codes.append("ben")  # Bengali
        self.list_ffmpeg_codes.append("bho")  # Bhojpuri
        self.list_ffmpeg_codes.append("bos")  # Bosnian
        self.list_ffmpeg_codes.append("bul")  # Bulgarian
        self.list_ffmpeg_codes.append("cat")  # Catalan
        self.list_ffmpeg_codes.append("ceb")  # Cebuano
        self.list_ffmpeg_codes.append("nya")  # Chichewa
        self.list_ffmpeg_codes.append("zho")  # Chinese
        self.list_ffmpeg_codes.append("zho-CN")  # Chinese (Simplified)
        self.list_ffmpeg_codes.append("zho-TW")  # Chinese (Traditional)
        self.list_ffmpeg_codes.append("cos")  # Corsican
        self.list_ffmpeg_codes.append("hrv")  # Croatian
        self.list_ffmpeg_codes.append("ces")  # Czech
        self.list_ffmpeg_codes.append("dan")  # Danish
        self.list_ffmpeg_codes.append("div")  # Dhivehi
        self.list_ffmpeg_codes.append("doi")  # Dogri
        self.list_ffmpeg_codes.append("nld")  # Dutch
        self.list_ffmpeg_codes.append("eng")  # English
        self.list_ffmpeg_codes.append("epo")  # Esperanto
        self.list_ffmpeg_codes.append("est")  # Estonian
        self.list_ffmpeg_codes.append("ewe")  # Ewe
        self.list_ffmpeg_codes.append("fil")  # Filipino
        self.list_ffmpeg_codes.append("fin")  # Finnish
        self.list_ffmpeg_codes.append("fra")  # French
        self.list_ffmpeg_codes.append("fry")  # Frisian
        self.list_ffmpeg_codes.append("glg")  # Galician
        self.list_ffmpeg_codes.append("kat")  # Georgian
        self.list_ffmpeg_codes.append("deu")  # German
        self.list_ffmpeg_codes.append("ell")  # Greek
        self.list_ffmpeg_codes.append("grn")  # Guarani
        self.list_ffmpeg_codes.append("guj")  # Gujarati
        self.list_ffmpeg_codes.append("hat")  # Haitian Creole
        self.list_ffmpeg_codes.append("hau")  # Hausa
        self.list_ffmpeg_codes.append("haw")  # Hawaiian
        self.list_ffmpeg_codes.append("heb")  # Hebrew
        self.list_ffmpeg_codes.append("hin")  # Hindi
        self.list_ffmpeg_codes.append("hmn")  # Hmong
        self.list_ffmpeg_codes.append("hun")  # Hungarian
        self.list_ffmpeg_codes.append("isl")  # Icelandic
        self.list_ffmpeg_codes.append("ibo")  # Igbo
        self.list_ffmpeg_codes.append("ilo")  # Ilocano
        self.list_ffmpeg_codes.append("ind")  # Indonesian
        self.list_ffmpeg_codes.append("gle")  # Irish
        self.list_ffmpeg_codes.append("ita")  # Italian
        self.list_ffmpeg_codes.append("jpn")  # Japanese
        self.list_ffmpeg_codes.append("jav")  # Javanese
        self.list_ffmpeg_codes.append("kan")  # Kannada
        self.list_ffmpeg_codes.append("kaz")  # Kazakh
        self.list_ffmpeg_codes.append("khm")  # Khmer
        self.list_ffmpeg_codes.append("kin")  # Kinyarwanda
        self.list_ffmpeg_codes.append("kok")  # Konkani
        self.list_ffmpeg_codes.append("kor")  # Korean
        self.list_ffmpeg_codes.append("kri")  # Krio
        self.list_ffmpeg_codes.append("kmr")  # Kurdish (Kurmanji)
        self.list_ffmpeg_codes.append("ckb")  # Kurdish (Sorani)
        self.list_ffmpeg_codes.append("kir")  # Kyrgyz
        self.list_ffmpeg_codes.append("lao")  # Lao
        self.list_ffmpeg_codes.append("lat")  # Latin
        self.list_ffmpeg_codes.append("lav")  # Latvian
        self.list_ffmpeg_codes.append("lin")  # Lingala
        self.list_ffmpeg_codes.append("lit")  # Lithuanian
        self.list_ffmpeg_codes.append("lug")  # Luganda
        self.list_ffmpeg_codes.append("ltz")  # Luxembourgish
        self.list_ffmpeg_codes.append("mkd")  # Macedonian
        self.list_ffmpeg_codes.append("mlg")  # Malagasy
        self.list_ffmpeg_codes.append("msa")  # Malay
        self.list_ffmpeg_codes.append("mal")  # Malayalam
        self.list_ffmpeg_codes.append("mlt")  # Maltese
        self.list_ffmpeg_codes.append("mri")  # Maori
        self.list_ffmpeg_codes.append("mar")  # Marathi
        self.list_ffmpeg_codes.append("mni-Mtei")  # Meiteilon (Manipuri)
        self.list_ffmpeg_codes.append("lus")  # Mizo
        self.list_ffmpeg_codes.append("mon")  # Mongolian
        self.list_ffmpeg_codes.append("mya")  # Myanmar (Burmese)
        self.list_ffmpeg_codes.append("nep")  # Nepali
        self.list_ffmpeg_codes.append("nor")  # Norwegian
        self.list_ffmpeg_codes.append("ori")  # Odiya (Oriya)
        self.list_ffmpeg_codes.append("orm")  # Oromo
        self.list_ffmpeg_codes.append("pus")  # Pashto
        self.list_ffmpeg_codes.append("fas")  # Persian
        self.list_ffmpeg_codes.append("pol")  # Polish
        self.list_ffmpeg_codes.append("por")  # Portuguese
        self.list_ffmpeg_codes.append("pan")  # Punjabi
        self.list_ffmpeg_codes.append("que")  # Quechua
        self.list_ffmpeg_codes.append("ron")  # Romanian
        self.list_ffmpeg_codes.append("rus")  # Russian
        self.list_ffmpeg_codes.append("smo")  # Samoan
        self.list_ffmpeg_codes.append("san")  # Sanskrit
        self.list_ffmpeg_codes.append("gla")  # Scots Gaelic
        self.list_ffmpeg_codes.append("nso")  # Sepedi
        self.list_ffmpeg_codes.append("srp")  # Serbian
        self.list_ffmpeg_codes.append("sot")  # Sesotho
        self.list_ffmpeg_codes.append("sna")  # Shona
        self.list_ffmpeg_codes.append("snd")  # Sindhi
        self.list_ffmpeg_codes.append("sin")  # Sinhala
        self.list_ffmpeg_codes.append("slk")  # Slovak
        self.list_ffmpeg_codes.append("slv")  # Slovenian
        self.list_ffmpeg_codes.append("som")  # Somali
        self.list_ffmpeg_codes.append("spa")  # Spanish
        self.list_ffmpeg_codes.append("sun")  # Sundanese
        self.list_ffmpeg_codes.append("swa")  # Swahili
        self.list_ffmpeg_codes.append("swe")  # Swedish
        self.list_ffmpeg_codes.append("tgk")  # Tajik
        self.list_ffmpeg_codes.append("tam")  # Tamil
        self.list_ffmpeg_codes.append("tat")  # Tatar
        self.list_ffmpeg_codes.append("tel")  # Telugu
        self.list_ffmpeg_codes.append("tha")  # Thai
        self.list_ffmpeg_codes.append("tir")  # Tigrinya
        self.list_ffmpeg_codes.append("tso")  # Tsonga
        self.list_ffmpeg_codes.append("tur")  # Turkish
        self.list_ffmpeg_codes.append("tuk")  # Turkmen
        self.list_ffmpeg_codes.append("twi")  # Twi (Akan)
        self.list_ffmpeg_codes.append("ukr")  # Ukrainian
        self.list_ffmpeg_codes.append("urd")  # Urdu
        self.list_ffmpeg_codes.append("uig")  # Uyghur
        self.list_ffmpeg_codes.append("uzb")  # Uzbek
        self.list_ffmpeg_codes.append("vie")  # Vietnamese
        self.list_ffmpeg_codes.append("wel")  # Welsh
        self.list_ffmpeg_codes.append("xho")  # Xhosa
        self.list_ffmpeg_codes.append("yid")  # Yiddish
        self.list_ffmpeg_codes.append("yor")  # Yoruba
        self.list_ffmpeg_codes.append("zul")  # Zulu

        self.code_of_name = dict(zip(self.list_names, self.list_codes))
        self.code_of_ffmpeg_code = dict(zip(self.list_ffmpeg_codes, self.list_codes))

        self.name_of_code = dict(zip(self.list_codes, self.list_names))
        self.name_of_ffmpeg_code = dict(zip(self.list_ffmpeg_codes, self.list_names))

        self.ffmpeg_code_of_name = dict(zip(self.list_names, self.list_ffmpeg_codes))
        self.ffmpeg_code_of_code = dict(zip(self.list_codes, self.list_ffmpeg_codes))

        self.dict = {
                        'af': 'Afrikaans',
                        'sq': 'Albanian',
                        'am': 'Amharic',
                        'ar': 'Arabic',
                        'hy': 'Armenian',
                        'as': 'Assamese',
                        'ay': 'Aymara',
                        'az': 'Azerbaijani',
                        'bm': 'Bambara',
                        'eu': 'Basque',
                        'be': 'Belarusian',
                        'bn': 'Bengali',
                        'bho': 'Bhojpuri',
                        'bs': 'Bosnian',
                        'bg': 'Bulgarian',
                        'ca': 'Catalan',
                        'ceb': 'Cebuano',
                        'ny': 'Chichewa',
                        'zh': 'Chinese',
                        'zh-CN': 'Chinese (Simplified)',
                        'zh-TW': 'Chinese (Traditional)',
                        'co': 'Corsican',
                        'hr': 'Croatian',
                        'cs': 'Czech',
                        'da': 'Danish',
                        'dv': 'Dhivehi',
                        'doi': 'Dogri',
                        'nl': 'Dutch',
                        'en': 'English',
                        'eo': 'Esperanto',
                        'et': 'Estonian',
                        'ee': 'Ewe',
                        'fil': 'Filipino',
                        'fi': 'Finnish',
                        'fr': 'French',
                        'fy': 'Frisian',
                        'gl': 'Galician',
                        'ka': 'Georgian',
                        'de': 'German',
                        'el': 'Greek',
                        'gn': 'Guarani',
                        'gu': 'Gujarati',
                        'ht': 'Haitian Creole',
                        'ha': 'Hausa',
                        'haw': 'Hawaiian',
                        'he': 'Hebrew',
                        'hi': 'Hindi',
                        'hmn': 'Hmong',
                        'hu': 'Hungarian',
                        'is': 'Icelandic',
                        'ig': 'Igbo',
                        'ilo': 'Ilocano',
                        'id': 'Indonesian',
                        'ga': 'Irish',
                        'it': 'Italian',
                        'ja': 'Japanese',
                        'jv': 'Javanese',
                        'kn': 'Kannada',
                        'kk': 'Kazakh',
                        'km': 'Khmer',
                        'rw': 'Kinyarwanda',
                        'gom': 'Konkani',
                        'ko': 'Korean',
                        'kri': 'Krio',
                        'kmr': 'Kurdish (Kurmanji)',
                        'ckb': 'Kurdish (Sorani)',
                        'ky': 'Kyrgyz',
                        'lo': 'Lao',
                        'la': 'Latin',
                        'lv': 'Latvian',
                        'ln': 'Lingala',
                        'lt': 'Lithuanian',
                        'lg': 'Luganda',
                        'lb': 'Luxembourgish',
                        'mk': 'Macedonian',
                        'mg': 'Malagasy',
                        'ms': 'Malay',
                        'ml': 'Malayalam',
                        'mt': 'Maltese',
                        'mi': 'Maori',
                        'mr': 'Marathi',
                        'mni-Mtei': 'Meiteilon (Manipuri)',
                        'lus': 'Mizo',
                        'mn': 'Mongolian',
                        'my': 'Myanmar (Burmese)',
                        'ne': 'Nepali',
                        'no': 'Norwegian',
                        'or': 'Odiya (Oriya)',
                        'om': 'Oromo',
                        'ps': 'Pashto',
                        'fa': 'Persian',
                        'pl': 'Polish',
                        'pt': 'Portuguese',
                        'pa': 'Punjabi',
                        'qu': 'Quechua',
                        'ro': 'Romanian',
                        'ru': 'Russian',
                        'sm': 'Samoan',
                        'sa': 'Sanskrit',
                        'gd': 'Scots Gaelic',
                        'nso': 'Sepedi',
                        'sr': 'Serbian',
                        'st': 'Sesotho',
                        'sn': 'Shona',
                        'sd': 'Sindhi',
                        'si': 'Sinhala',
                        'sk': 'Slovak',
                        'sl': 'Slovenian',
                        'so': 'Somali',
                        'es': 'Spanish',
                        'su': 'Sundanese',
                        'sw': 'Swahili',
                        'sv': 'Swedish',
                        'tg': 'Tajik',
                        'ta': 'Tamil',
                        'tt': 'Tatar',
                        'te': 'Telugu',
                        'th': 'Thai',
                        'ti': 'Tigrinya',
                        'ts': 'Tsonga',
                        'tr': 'Turkish',
                        'tk': 'Turkmen',
                        'tw': 'Twi (Akan)',
                        'uk': 'Ukrainian',
                        'ur': 'Urdu',
                        'ug': 'Uyghur',
                        'uz': 'Uzbek',
                        'vi': 'Vietnamese',
                        'cy': 'Welsh',
                        'xh': 'Xhosa',
                        'yi': 'Yiddish',
                        'yo': 'Yoruba',
                        'zu': 'Zulu',
                    }

        self.ffmpeg_dict = {
                                'af': 'afr', # Afrikaans
                                'sq': 'alb', # Albanian
                                'am': 'amh', # Amharic
                                'ar': 'ara', # Arabic
                                'hy': 'arm', # Armenian
                                'as': 'asm', # Assamese
                                'ay': 'aym', # Aymara
                                'az': 'aze', # Azerbaijani
                                'bm': 'bam', # Bambara
                                'eu': 'baq', # Basque
                                'be': 'bel', # Belarusian
                                'bn': 'ben', # Bengali
                                'bho': 'bho', # Bhojpuri
                                'bs': 'bos', # Bosnian
                                'bg': 'bul', # Bulgarian
                                'ca': 'cat', # Catalan
                                'ceb': 'ceb', # Cebuano
                                'ny': 'nya', # Chichewa
                                'zh': 'chi', # Chinese
                                'zh-CN': 'chi', # Chinese (Simplified)
                                'zh-TW': 'chi', # Chinese (Traditional)
                                'co': 'cos', # Corsican
                                'hr': 'hrv', # Croatian
                                'cs': 'cze', # Czech
                                'da': 'dan', # Danish
                                'dv': 'div', # Dhivehi
                                'doi': 'doi', # Dogri
                                'nl': 'dut', # Dutch
                                'en': 'eng', # English
                                'eo': 'epo', # Esperanto
                                'et': 'est', # Estonian
                                'ee': 'ewe', # Ewe
                                'fil': 'fil', # Filipino
                                'fi': 'fin', # Finnish
                                'fr': 'fre', # French
                                'fy': 'fry', # Frisian
                                'gl': 'glg', # Galician
                                'ka': 'geo', # Georgian
                                'de': 'ger', # German
                                'el': 'gre', # Greek
                                'gn': 'grn', # Guarani
                                'gu': 'guj', # Gujarati
                                'ht': 'hat', # Haitian Creole
                                'ha': 'hau', # Hausa
                                'haw': 'haw', # Hawaiian
                                'he': 'heb', # Hebrew
                                'hi': 'hin', # Hindi
                                'hmn': 'hmn', # Hmong
                                'hu': 'hun', # Hungarian
                                'is': 'ice', # Icelandic
                                'ig': 'ibo', # Igbo
                                'ilo': 'ilo', # Ilocano
                                'id': 'ind', # Indonesian
                                'ga': 'gle', # Irish
                                'it': 'ita', # Italian
                                'ja': 'jpn', # Japanese
                                'jv': 'jav', # Javanese
                                'kn': 'kan', # Kannada
                                'kk': 'kaz', # Kazakh
                                'km': 'khm', # Khmer
                                'rw': 'kin', # Kinyarwanda
                                'gom': 'kok', # Konkani
                                'ko': 'kor', # Korean
                                'kri': 'kri', # Krio
                                'kmr': 'kur', # Kurdish (Kurmanji)
                                'ckb': 'kur', # Kurdish (Sorani)
                                'ky': 'kir', # Kyrgyz
                                'lo': 'lao', # Lao
                                'la': 'lat', # Latin
                                'lv': 'lav', # Latvian
                                'ln': 'lin', # Lingala
                                'lt': 'lit', # Lithuanian
                                'lg': 'lug', # Luganda
                                'lb': 'ltz', # Luxembourgish
                                'mk': 'mac', # Macedonian
                                'mg': 'mlg', # Malagasy
                                'ms': 'may', # Malay
                                'ml': 'mal', # Malayalam
                                'mt': 'mlt', # Maltese
                                'mi': 'mao', # Maori
                                'mr': 'mar', # Marathi
                                'mni-Mtei': 'mni', # Meiteilon (Manipuri)
                                'lus': 'lus', # Mizo
                                'mn': 'mon', # Mongolian
                                'my': 'bur', # Myanmar (Burmese)
                                'ne': 'nep', # Nepali
                                'no': 'nor', # Norwegian
                                'or': 'ori', # Odiya (Oriya)
                                'om': 'orm', # Oromo
                                'ps': 'pus', # Pashto
                                'fa': 'per', # Persian
                                'pl': 'pol', # Polish
                                'pt': 'por', # Portuguese
                                'pa': 'pan', # Punjabi
                                'qu': 'que', # Quechua
                                'ro': 'rum', # Romanian
                                'ru': 'rus', # Russian
                                'sm': 'smo', # Samoan
                                'sa': 'san', # Sanskrit
                                'gd': 'gla', # Scots Gaelic
                                'nso': 'nso', # Sepedi
                                'sr': 'srp', # Serbian
                                'st': 'sot', # Sesotho
                                'sn': 'sna', # Shona
                                'sd': 'snd', # Sindhi
                                'si': 'sin', # Sinhala
                                'sk': 'slo', # Slovak
                                'sl': 'slv', # Slovenian
                                'so': 'som', # Somali
                                'es': 'spa', # Spanish
                                'su': 'sun', # Sundanese
                                'sw': 'swa', # Swahili
                                'sv': 'swe', # Swedish
                                'tg': 'tgk', # Tajik
                                'ta': 'tam', # Tamil
                                'tt': 'tat', # Tatar
                                'te': 'tel', # Telugu
                                'th': 'tha', # Thai
                                'ti': 'tir', # Tigrinya
                                'ts': 'tso', # Tsonga
                                'tr': 'tur', # Turkish
                                'tk': 'tuk', # Turkmen
                                'tw': 'twi', # Twi (Akan)
                                'uk': 'ukr', # Ukrainian
                                'ur': 'urd', # Urdu
                                'ug': 'uig', # Uyghur
                                'uz': 'uzb', # Uzbek
                                'vi': 'vie', # Vietnamese
                                'cy': 'wel', # Welsh
                                'xh': 'xho', # Xhosa
                                'yi': 'yid', # Yiddish
                                'yo': 'yor', # Yoruba
                                'zu': 'zul', # Zulu
                           }

    def get_code_of_name(self, name):
        return self.code_of_name[name]

    def get_code_of_ffmpeg_code(self, ffmpeg_code):
        return self.code_of_ffmpeg_code[ffmpeg_code]

    def get_name_of_code(self, code):
        return self.name_of_code[code]

    def get_name_of_ffmpeg_code(self, ffmpeg_code):
        return self.name_of_ffmpeg_code[ffmpeg_code]

    def get_ffmpeg_code_of_name(self, name):
        return self.ffmpeg_code_of_name[name]

    def get_ffmpeg_code_of_code(self, code):
        return self.ffmpeg_code_of_code[code]


def pbar(progress, start_time, total, info, activity, textview_progress, progress_bar, textview_percentage, textview_time):
    if progress > 0:
        elapsed_time = time.time() - start_time
        eta_seconds = (elapsed_time / progress) * (total - progress)
    else:
        eta_seconds = 0
    eta_time = timedelta(seconds=int(eta_seconds))
    eta_str = str(eta_time)
    hour, minute, second = eta_str.split(":")
    text_time = "ETA  : " + hour.zfill(2) + ":" + minute + ":" + second
    if progress == total:
        progress = 100
        elapsed_time = time.time() - start_time
        elapsed_time_seconds = timedelta(seconds=int(elapsed_time))
        elapsed_time_str = str(elapsed_time_seconds)
        hour, minute, second = elapsed_time_str.split(":")
        text_time = "Time : " + hour.zfill(2) + ":" + minute + ":" + second 
    activity.runOnUiThread(mProgressBar(textview_progress, progress_bar, textview_percentage, textview_time, progress, text_time, 100, info))


class mProgressBar(static_proxy(None, Runnable)):
    def __init__(self, textview_progress, progress_bar, textview_percentage, textview_time, progress, text_time, total, info):
        super(mProgressBar, self).__init__()
        self.progress = progress
        self.text_time = text_time
        self.total = total
        self.info = info
        self.textview_progress = textview_progress
        self.progress_bar = progress_bar
        self.textview_percentage = textview_percentage
        self.textview_time = textview_time
        self.progress_bar.setMax(self.total)

    @Override(jvoid, [])
    def run(self):
        self.textview_progress.setText(self.info)
        self.progress_bar.setProgress(self.progress)
        self.textview_percentage.setText(str(self.progress) + "%")
        self.textview_time.setText(self.text_time)


class MyStatisticsCallback(dynamic_proxy(StatisticsCallback)):
    def __init__(self, info, media_duration, start_time, activity, textview_progress, progress_bar, textview_percentage, textview_time):
        super(MyStatisticsCallback, self).__init__()
        self.info = info
        self.media_duration = media_duration
        self.start_time = start_time
        self.activity = activity
        self.textview_progress = textview_progress
        self.progress_bar = progress_bar
        self.textview_percentage = textview_percentage
        self.textview_time = textview_time
        self.progress = AtomicReference(0.0)
        Config.resetStatistics()

    def apply(self, newStatistics):
        print(f"self.media_duration = {self.media_duration}")

        getTime = newStatistics.getTime()
        print(f"getTime = {getTime}")

        self.progress.set(getTime/self.media_duration)
        print(f"self.progress = {self.progress}")

        progressFinal = int(self.progress.get()*100)
        print(f"progressFinal = {progressFinal}")

        pbar(progressFinal, self.start_time, 100, self.info, self.activity, self.textview_progress, self.progress_bar, self.textview_percentage, self.textview_time)

        if int(getTime/1000) >= int(self.media_duration/1000):
            pbar(100, self.start_time, 100, self.info, self.activity, self.textview_progress, self.progress_bar, self.textview_percentage, self.textview_time)


class WavConverter:
    def get_subtitle_languages_and_duration(self, media_filepath):
        # Run ffprobe to get stream information
        command = [
                    '-hide_banner',
                    '-v', 'error',
                    '-loglevel', 'error',
                    '-of', 'json',
                    '-show_entries',
                    'format:stream',
                    media_filepath
                  ]

        FFprobe.execute(command)
        output = Config.getLastCommandOutput()

        metadata = json.loads(output)
        streams = metadata['streams']
        duration = int(float(metadata['format']['duration'])*1000)

        # Find the subtitle stream with language metadata
        subtitle_languages = []
        for stream in streams:
            if stream['codec_type'] == 'subtitle' and 'tags' in stream and 'language' in stream['tags']:
                language = stream['tags']['language']
                subtitle_languages.append(language)

        return subtitle_languages, duration

    def __init__(self, channels=1, rate=16000, start_time=None, activity=None, textview_progress=None, progress_bar=None, textview_percentage=None, textview_time=None):
        self.channels = channels
        self.rate = rate
        self.start_time = start_time
        self.activity = activity
        self.textview_progress = textview_progress
        self.progress_bar = progress_bar
        self.textview_percentage = textview_percentage
        self.textview_time = textview_time

    def __call__(self, media_filepath):
        if not os.path.isfile(media_filepath):
            print(f"The given file does not exist: '{media_filepath}'")
            raise Exception(f"Invalid file: '{media_filepath}'")

        temp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)

        ffmpeg_command = [
                            '-hide_banner',
                            '-loglevel', 'error',
                            '-v', 'error',
                            '-y',
                            '-i', media_filepath,
                            '-ac', str(self.channels),
                            '-ar', str(self.rate),
                            temp.name
                         ]

        try:
            media_file_display_name = os.path.basename(media_filepath).split('/')[-1]
            info = "Converting to WAV file"
            existing_languages, total_duration = self.get_subtitle_languages_and_duration(media_filepath)

            Config.enableRedirection()
            Config.enableStatisticsCallback(MyStatisticsCallback(info, total_duration, self.start_time, self.activity, self.textview_progress, self.progress_bar, self.textview_percentage, self.textview_time))

            FFmpeg.execute(ffmpeg_command)

            temp.close()

            return temp.name, self.rate

        except Exception as e:
            print(e)
            return


class SpeechRegionFinder:
    @staticmethod
    def percentile(arr, percent):
        arr = sorted(arr)
        k = (len(arr) - 1) * percent
        f = math.floor(k)
        c = math.ceil(k)
        if f == c: return arr[int(k)]
        d0 = arr[int(f)] * (c - k)
        d1 = arr[int(c)] * (k - f)
        return d0 + d1

    def __init__(self, frame_width=4096, min_region_size=0.5, max_region_size=6):
        self.frame_width = frame_width
        self.min_region_size = min_region_size
        self.max_region_size = max_region_size

    def __call__(self, wav_filepath):
        try:
            reader = wave.open(wav_filepath)
            sample_width = reader.getsampwidth()
            rate = reader.getframerate()
            n_channels = reader.getnchannels()
            total_duration = reader.getnframes() / rate
            chunk_duration = float(self.frame_width) / rate
            n_chunks = int(total_duration / chunk_duration)
            energies = []
            for i in range(n_chunks):
                chunk = reader.readframes(self.frame_width)
                energies.append(audioop.rms(chunk, sample_width * n_channels))
            threshold = self.percentile(energies, 0.2)
            elapsed_time = 0
            regions = []
            region_start = None
            for energy in energies:
                is_silence = energy <= threshold
                max_exceeded = region_start and elapsed_time - region_start >= self.max_region_size
                if (max_exceeded or is_silence) and region_start:
                    if elapsed_time - region_start >= self.min_region_size:
                        regions.append((region_start, elapsed_time))
                        region_start = None
                elif (not region_start) and (not is_silence):
                    region_start = elapsed_time
                elapsed_time += chunk_duration
            return regions

        except Exception as e:
            print(e)
            return


class FLACConverter(object):
    def __init__(self, wav_filepath, include_before=0.25, include_after=0.25):
        self.wav_filepath = wav_filepath
        self.include_before = include_before
        self.include_after = include_after

    def __call__(self, region):
        try:
            start, end = region
            start = max(0, start - self.include_before)
            end += self.include_after
            temp = tempfile.NamedTemporaryFile(suffix='.flac', delete=False)

            ffmpeg_command = [
                                '-hide_banner',
                                '-loglevel', 'error',
                                '-v', 'error',
                                '-ss', str(start),
                                '-t', str(end - start),
                                '-y',
                                '-i', self.wav_filepath,
                                temp.name
                             ]

            FFmpeg.execute(ffmpeg_command)
            content = temp.read()
            temp.close()
            return content

        except Exception as e:
            print(e)
            return


class SpeechRecognizer(object):
    def __init__(self, language="en", rate=48000, retries=3, api_key="AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw", timeout=30):
        self.language = language
        self.rate = rate
        self.api_key = api_key
        self.retries = retries
        self.timeout = timeout

    def __call__(self, data):
        try:
            for i in range(self.retries):
                url = "http://www.google.com/speech-api/v2/recognize?client=chromium&lang={lang}&key={key}".format(lang=self.language, key=self.api_key)
                headers = {"Content-Type": "audio/x-flac rate=%d" % self.rate}

                try:
                    resp = requests.post(url, data=data, headers=headers, timeout=self.timeout)
                except requests.exceptions.ConnectionError:
                    try:
                        resp = httpx.post(url, data=data, headers=headers, timeout=self.timeout)
                    except httpx.exceptions.NetworkError:
                        continue

                for line in resp.content.decode('utf-8').split("\n"):
                    try:
                        line = json.loads(line)
                        line = line['result'][0]['alternative'][0]['transcript']
                        return line[:1].upper() + line[1:]
                    except:
                        # no result
                        continue

        except Exception as e:
            print(e)
            return


class SentenceTranslator(object):
    def __init__(self, src, dst, patience=-1, timeout=30):
        self.src = src
        self.dst = dst
        self.patience = patience
        self.timeout = timeout

    def __call__(self, sentence):
        try:
            translated_sentence = []
            # handle the special case: empty string.
            if not sentence:
                return None
            translated_sentence = self.GoogleTranslate(sentence, src=self.src, dst=self.dst, timeout=self.timeout)
            fail_to_translate = translated_sentence[-1] == '\n'
            while fail_to_translate and patience:
                translated_sentence = self.GoogleTranslate(translated_sentence, src=self.src, dst=self.dst, timeout=self.timeout).text
                if translated_sentence[-1] == '\n':
                    if patience == -1:
                        continue
                    patience -= 1
                else:
                    fail_to_translate = False

            return translated_sentence

        except Exception as e:
            print(e)
            return

    def GoogleTranslate(self, text, src, dst, timeout=30):
        url = 'https://translate.googleapis.com/translate_a/'
        params = 'single?client=gtx&sl='+src+'&tl='+dst+'&dt=t&q='+text;
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Referer': 'https://translate.google.com',}

        try:
            response = requests.get(url+params, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                response_json = response.json()[0]
                length = len(response_json)
                translation = ""
                for i in range(length):
                    translation = translation + response_json[i][0]
                return translation
            return

        except requests.exceptions.ConnectionError:
            with httpx.Client() as client:
                response = client.get(url+params, headers=headers, timeout=self.timeout)
                if response.status_code == 200:
                    response_json = response.json()[0]
                    length = len(response_json)
                    translation = ""
                    for i in range(length):
                        translation = translation + response_json[i][0]
                    return translation
                return

        except Exception as e:
            print(e)
            return


class SubtitleFormatter:
    supported_formats = ['srt', 'vtt', 'json', 'raw']

    def __init__(self, format_type):
        self.format_type = format_type.lower()
        
    def __call__(self, subtitles, padding_before=0, padding_after=0):
        try:
            if self.format_type == 'srt':
                return self.srt_formatter(subtitles, padding_before, padding_after)
            elif self.format_type == 'vtt':
                return self.vtt_formatter(subtitles, padding_before, padding_after)
            elif self.format_type == 'json':
                return self.json_formatter(subtitles)
            elif self.format_type == 'raw':
                return self.raw_formatter(subtitles)
            else:
                raise ValueError(f'Unsupported format type: {self.format_type}')

        except Exception as e:
            print(e)
            return

    def srt_formatter(self, subtitles, padding_before=0, padding_after=0):
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

    def vtt_formatter(self, subtitles, padding_before=0, padding_after=0):
        """
        Serialize a list of subtitles according to the VTT format, with optional time padding.
        """
        text = self.srt_formatter(subtitles, padding_before, padding_after)
        text = 'WEBVTT\n\n' + text.replace(',', '.')
        return text

    def json_formatter(self, subtitles):
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

    def raw_formatter(self, subtitles):
        """
        Serialize a list of subtitles as a newline-delimited string.
        """
        return ' '.join(text for (_rng, text) in subtitles)


class SubtitleWriter:
    def __init__(self, regions, transcripts, format):
        self.regions = regions
        self.transcripts = transcripts
        self.format = format
        self.timed_subtitles = [(r, t) for r, t in zip(self.regions, self.transcripts) if t]

    def get_timed_subtitles(self):
        return self.timed_subtitles

    def write(self, declared_subtitle_filepath):
        try:
            formatter = SubtitleFormatter(self.format)
            formatted_subtitles = formatter(self.timed_subtitles)
            saved_subtitle_filepath = declared_subtitle_filepath
            if saved_subtitle_filepath:
                subtitle_file_base, subtitle_file_ext = os.path.splitext(saved_subtitle_filepath)
                if not subtitle_file_ext:
                    saved_subtitle_filepath = "{base}.{format}".format(base=subtitle_file_base, format=self.format)
                else:
                    saved_subtitle_filepath = declared_subtitle_filepath
            with open(saved_subtitle_filepath, 'wb') as f:
                f.write(formatted_subtitles.encode("utf-8"))

        except Exception as e:
            print(e)
            return


class SRTFileReader:
    def __init__(self):
        self.timed_subtitles = []

    def __call__(self, srt_file_path):
        try:
            """
            Read SRT formatted subtitles file and return subtitles as list of tuples
            """
            #timed_subtitles = []
            with open(srt_file_path, 'r') as srt_file:
                lines = srt_file.readlines()
                # Split the subtitles file into subtitle blocks
                subtitle_blocks = []
                block = []
                for line in lines:
                    if line.strip() == '':
                        subtitle_blocks.append(block)
                        block = []
                    else:
                        block.append(line.strip())
                subtitle_blocks.append(block)

                # Parse each subtitle block and store as tuple in timed_subtitles list
                for block in subtitle_blocks:
                    if block:
                        # Extract start and end times from subtitle block
                        start_time_str, end_time_str = block[1].split(' --> ')
                        time_format = '%H:%M:%S,%f'
                        start_time_time_delta = datetime.strptime(start_time_str, time_format) - datetime.strptime('00:00:00,000', time_format)
                        start_time_total_seconds = start_time_time_delta.total_seconds()
                        end_time_time_delta = datetime.strptime(end_time_str, time_format) - datetime.strptime('00:00:00,000', time_format)
                        end_time_total_seconds = end_time_time_delta.total_seconds()
                        # Extract subtitle text from subtitle block
                        subtitle = ' '.join(block[2:])
                        self.timed_subtitles.append(((start_time_total_seconds, end_time_total_seconds), subtitle))
                return self.timed_subtitles

        except Exception as e:
            print(e)
            return


class SubtitleStreamParser:
    def __init__(self):
        self._indexes = []
        self._languages = []
        self._timed_subtitles = []
        self._number_of_streams = 0

    def get_subtitle_streams(self, media_filepath):
        ffprobe_command = [
                            '-hide_banner',
                            '-v', 'error',
                            '-loglevel', 'error',
                            '-print_format', 'json',
                            '-show_entries', 'stream=index:stream_tags=language',
                            '-select_streams', 's',
                            media_filepath
                          ]

        try:
            FFprobe.execute(ffprobe_command)
            output = Config.getLastCommandOutput()

            streams = json.loads(output)['streams']

            subtitle_streams = []
            empty_stream_exists = False

            for index, stream in enumerate(streams, start=1):
                language = stream['tags'].get('language')
                subtitle_streams.append({'index': index, 'language': language})

                # Check if 'No subtitles' stream exists
                if language == 'No subtitles':
                    empty_stream_exists = True

            # Append 'No subtitles' stream if it exists
            if not empty_stream_exists:
                subtitle_streams.append({'index': len(streams) + 1, 'language': 'No subtitles'})

            return subtitle_streams

        except Exception as e:
            print(e)
            return None

    def get_timed_subtitles(self, media_filepath, subtitle_stream_index):
        #map_string = f"0:s:{subtitle_stream_index-1}?"

        media_file_display_name = os.path.basename(media_filepath).split('/')[-1]
        files_dir = str(context.getExternalFilesDir(None))
        subtitle_folder_name = join(files_dir, media_file_display_name[:-4])
        if not os.path.isdir(subtitle_folder_name):
            os.mkdir(subtitle_folder_name)
        subtitle_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-4]}.srt"

        ffmpeg_command = [
                            '-hide_banner',
                            '-loglevel', 'error',
                            '-v', 'error',
                            '-y',
                            '-i', media_filepath,
                            '-map', f'0:s:{subtitle_stream_index-1}?',
                            '-c:s', 'text',
                            subtitle_filepath
                         ]

        try:
            Config.enableRedirection()
            FFmpeg.execute(ffmpeg_command)
            output = Config.getLastCommandOutput()

            if os.path.isfile(subtitle_filepath):
                srt_file_reader = SRTFileReader()
                timed_subtitles = srt_file_reader(subtitle_filepath)
            else:
                timed_subtitles = None

            return timed_subtitles

        except Exception as e:
            print(e)
            return None

    def number_of_streams(self):
        return self._number_of_streams

    def indexes(self):
        return self._indexes

    def languages(self):
        return self._languages

    def timed_subtitles(self):
        return self._timed_subtitles

    def index_of_language(self, language):
        for i in range(self.number_of_streams()):
            if self.languages()[i] == language:
                return i+1
            return

    def language_of_index(self, index):
        return self.languages()[index-1]

    def timed_subtitles_of_index(self, index):
        return self.timed_subtitles()[index-1]

    def timed_subtitles_of_language(self, language):
        for i in range(self.number_of_streams()):
            if self.languages()[i] == language:
                return self.timed_subtitles()[i]

    def __call__(self, media_filepath):
        subtitle_streams = self.get_subtitle_streams(media_filepath)
        print(f"subtitle_streams = {subtitle_streams}")

        subtitle_streams_data = []
        if subtitle_streams:
            for subtitle_stream in subtitle_streams:
                subtitle_stream_index = subtitle_stream['index']
                subtitle_stream_language = subtitle_stream['language']
                print(f"Stream Index: {subtitle_stream_index}, Language: {subtitle_stream_language}")
                subtitle_streams_data.append((subtitle_stream_index, subtitle_stream_language))

        subtitle_streams_data_with_timed_subtitles = []

        for subtitle_stream_index in range(len(subtitle_streams)):
            index, language = subtitle_streams_data[subtitle_stream_index]
            self._indexes.append(index)
            self._languages.append(language)
            self._timed_subtitles.append(self.get_timed_subtitles(media_filepath, subtitle_stream_index+1))
            subtitle_streams_data_with_timed_subtitles.append((index, language, self.get_timed_subtitles(media_filepath, subtitle_stream_index+1)))

        self._number_of_streams = len(subtitle_streams_data_with_timed_subtitles)

        print(f"subtitle_streams_data_with_timed_subtitles = {subtitle_streams_data_with_timed_subtitles}")
        return subtitle_streams_data_with_timed_subtitles


class MediaSubtitleRenderer:
    def get_subtitle_languages_and_duration(self, media_filepath):
        # Run ffprobe to get stream information
        command = [
                    '-hide_banner',
                    '-v', 'error',
                    '-loglevel', 'error',
                    '-of', 'json',
                    '-show_entries',
                    'format:stream',
                    media_filepath
                  ]

        FFprobe.execute(command)
        output = Config.getLastCommandOutput()

        metadata = json.loads(output)
        streams = metadata['streams']
        duration = int(float(metadata['format']['duration'])*1000)

        # Find the subtitle stream with language metadata
        subtitle_languages = []
        for stream in streams:
            if stream['codec_type'] == 'subtitle' and 'tags' in stream and 'language' in stream['tags']:
                language = stream['tags']['language']
                subtitle_languages.append(language)

        return subtitle_languages, duration

    def __init__(self, subtitle_path=None, language=None, output_path=None, start_time=None, activity=None, textview_progress=None, progress_bar=None, textview_percentage=None, textview_time=None):
        self.subtitle_path = subtitle_path
        self.language = language
        self.output_path = output_path
        self.start_time = start_time
        self.activity = activity
        self.textview_progress = textview_progress
        self.progress_bar = progress_bar
        self.textview_percentage = textview_percentage
        self.textview_time = textview_time

    def __call__(self, media_filepath):
        if not os.path.isfile(media_filepath):
            print(f"The given file does not exist: '{media_filepath}'")
            raise Exception(f"Invalid file: '{media_filepath}'")

        try:
            scale_switch = "'trunc(iw/2)*2'\:'trunc(ih/2)*2'"
            ffmpeg_command = [
                                '-hide_banner',
                                '-loglevel', 'error',
                                '-v', 'error',
                                '-y',
                                '-i', media_filepath,
                                '-vf', f'subtitles={shlex.quote(self.subtitle_path)},scale={scale_switch}',
                                '-c:v', 'libx264',
                                '-crf', '23',
                                '-preset', 'medium',
                                '-c:a', 'copy',
                                self.output_path
                             ]

            media_file_display_name = os.path.basename(media_filepath).split('/')[-1]
            info = f"Rendering '{self.language}' subtitles"
            existing_languages, total_duration = self.get_subtitle_languages_and_duration(media_filepath)

            Config.enableRedirection()
            Config.enableStatisticsCallback(MyStatisticsCallback(info, total_duration, self.start_time, self.activity, self.textview_progress, self.progress_bar, self.textview_percentage, self.textview_time))

            FFmpeg.execute(ffmpeg_command)

            if os.path.isfile(self.output_path):
                return self.output_path
            else:
                return None

        except Exception as e:
            print(e)
            return


class MediaSubtitleEmbedder:
    def get_subtitle_languages_and_duration(self, media_filepath):
        # Run ffprobe to get stream information
        command = [
                    '-hide_banner',
                    '-v', 'error',
                    '-loglevel', 'error',
                    '-of', 'json',
                    '-show_entries',
                    'format:stream',
                    media_filepath
                  ]

        FFprobe.execute(command)
        output = Config.getLastCommandOutput()

        metadata = json.loads(output)
        streams = metadata['streams']
        duration = int(float(metadata['format']['duration'])*1000)

        # Find the subtitle stream with language metadata
        subtitle_languages = []
        for stream in streams:
            if stream['codec_type'] == 'subtitle' and 'tags' in stream and 'language' in stream['tags']:
                language = stream['tags']['language']
                subtitle_languages.append(language)

        return subtitle_languages, duration

    def __init__(self, subtitle_path=None, language=None, output_path=None, start_time=None, activity=None, textview_progress=None, progress_bar=None, textview_percentage=None, textview_time=None):
        self.subtitle_path = subtitle_path
        self.language = language
        self.output_path = output_path
        self.start_time = start_time
        self.activity = activity
        self.textview_progress = textview_progress
        self.progress_bar = progress_bar
        self.textview_percentage = textview_percentage
        self.textview_time = textview_time

    def __call__(self, media_filepath):
        if not os.path.isfile(media_filepath):
            print(f"The given file does not exist: '{media_filepath}'")
            raise Exception(f"Invalid file: '{media_filepath}'")

        try:
            existing_languages, total_duration = self.get_subtitle_languages_and_duration(media_filepath)

            if self.language in existing_languages:
                return

            else:
                # Determine the next available subtitle index
                next_index = len(existing_languages)

                ffmpeg_command = [
                                    '-hide_banner',
                                    '-loglevel', 'error',
                                    '-v', 'error',
                                    '-y',
                                    '-i', media_filepath,
                                    '-sub_charenc', 'UTF-8',
                                    '-i', self.subtitle_path,
                                    '-c:v', 'copy',
                                    '-c:a', 'copy',
                                    '-scodec', 'mov_text',
                                    '-metadata:s:s:' + str(next_index), f'language={shlex.quote(self.language)}',
                                    '-map', '0',
                                    '-map', '1',
                                    self.output_path
                                 ]

                subtitle_file_display_name = os.path.basename(self.subtitle_path).split('/')[-1]
                media_file_display_name = os.path.basename(media_filepath).split('/')[-1]
                info = f"Embedding '{self.language}' subtitles"

                #print(f"EMBEDDER : media_filepath = '{media_filepath}' , size = {os.path.getsize(media_filepath)} , total_duration = {total_duration}")

                Config.enableRedirection()
                Config.enableStatisticsCallback(MyStatisticsCallback(info, total_duration, self.start_time, self.activity, self.textview_progress, self.progress_bar, self.textview_percentage, self.textview_time))

                FFmpeg.execute(ffmpeg_command)

                if os.path.isfile(self.output_path):
                    return self.output_path
                else:
                    return None

        except Exception as e:
            print(e)
            return


class MediaSubtitleRemover:
    def get_subtitle_languages_and_duration(self, media_filepath):
        # Run ffprobe to get stream information
        command = [
                    '-hide_banner',
                    '-v', 'error',
                    '-loglevel', 'error',
                    '-of', 'json',
                    '-show_entries',
                    'format:stream',
                    media_filepath
                  ]

        FFprobe.execute(command)
        output = Config.getLastCommandOutput()

        metadata = json.loads(output)
        streams = metadata['streams']
        duration = int(float(metadata['format']['duration'])*1000)

        # Find the subtitle stream with language metadata
        subtitle_languages = []
        for stream in streams:
            if stream['codec_type'] == 'subtitle' and 'tags' in stream and 'language' in stream['tags']:
                language = stream['tags']['language']
                subtitle_languages.append(language)

        return subtitle_languages, duration

    def __init__(self, output_path=None, start_time=None, activity=None, textview_progress=None, progress_bar=None, textview_percentage=None, textview_time=None):
        self.output_path = output_path
        self.start_time = start_time
        self.activity = activity
        self.textview_progress = textview_progress
        self.progress_bar = progress_bar
        self.textview_percentage = textview_percentage
        self.textview_time = textview_time

    def __call__(self, media_filepath):
        if not os.path.isfile(media_filepath):
            print(f"The given file does not exist: '{media_filepath}'")
            raise Exception(f"Invalid file: '{media_filepath}'")

        try:
            ffmpeg_command = [
                                '-hide_banner',
                                '-loglevel', 'error',
                                '-v', 'error',
                                '-y',
                                '-i', media_filepath,
                                '-c', 'copy',
                                '-sn',
                                self.output_path
                             ]

            media_file_display_name = os.path.basename(media_filepath).split('/')[-1]
            info = f"Removing subtitles streams"
            start_time = time.time()
            existing_languages, total_duration = self.get_subtitle_languages_and_duration(media_filepath)

            Config.enableRedirection()
            Config.enableStatisticsCallback(MyStatisticsCallback(info, total_duration, self.start_time, self.activity, self.textview_progress, self.progress_bar, self.textview_percentage, self.textview_time))

            FFmpeg.execute(ffmpeg_command)

            if os.path.isfile(self.output_path):
                return self.output_path
            else:
                return None

            if os.path.isfile(self.output_path):
                return self.output_path
            else:
                return None

        except Exception as e:
            print(e)
            return



def is_same_language(lang1, lang2):
    return lang1.split("-")[0] == lang2.split("-")[0]


'''
def get_media_duration(video_path):
    ffprobe_command = ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
    FFprobe.execute(ffprobe_command)
    output = Config.getLastCommandOutput()
    print(f"output = {output}")
    
    try:
        duration = int(float(output) * 1000)  # Convert to milliseconds
    except ValueError as e:
        duration = 0
        print("Error parsing video duration:", e)
    
    return duration


def convert_to_wav(media_filepath, start_time, activity, textview_progress, progress_bar, textview_percentage, textview_time):
    channels=1
    rate=16000
    temp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    if not os.path.isfile(media_filepath):
        print("The given file does not exist: {0}".format(media_filepath))
        raise Exception("Invalid filepath: {0}".format(media_filepath))

    Config.enableRedirection()
    file = File(media_filepath)
    fileUri = Uri.fromFile(file)
    #media_duration = MediaPlayer.create(activity, fileUri).getDuration()
    media_duration = get_media_duration(media_filepath)
    print("media_duration = {}".format(media_duration))
    info = "Converting to WAV file"
    Config.enableStatisticsCallback(MyStatisticsCallback(info, media_duration, start_time, activity, textview_progress, progress_bar, textview_percentage, textview_time))

    FFmpeg.execute("-y -i " + "\"" + media_filepath + "\"" + " -ac " + str(channels) + " -ar " + str(rate) + " " + "\"" + temp.name + "\"")
    return temp.name, rate

def percentile(arr, percent):
    arr = sorted(arr)
    k = (len(arr) - 1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c: return arr[int(k)]
    d0 = arr[int(f)] * (c - k)
    d1 = arr[int(c)] * (k - f)
    return d0 + d1


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
'''


def transcribe(src, dst, media_filepath, media_file_display_name, subtitle_format, embed_src, embed_dst, force_recognize, activity, textview_output_messages, textview_progress, progress_bar, textview_percentage, textview_time):

    multiprocessing.freeze_support()

    print(f"media_filepath = '{media_filepath}'")

    base, ext = os.path.splitext(media_filepath)
    media_file_display_name = os.path.basename(media_filepath).split('/')[-1]
    print(f"media_file_display_name = '{media_file_display_name}'")
    media_file_format = ext[1:]
    print(f"media_file_format = '{media_file_format}'")

    language = Language()
    removed_media_filepaths = []
    results = []

    pool = multiprocessing.pool.ThreadPool(10)

    print(f"src = {src}")
    print(f"dst = {dst}")
    print(f"embed_src = {embed_src}")
    print(f"embed_dst = {embed_dst}")
    print(f"force_recognize = {force_recognize}")

    files_dir = str(context.getExternalFilesDir(None))
    dashChars_file_display_name = "dashChars"
    dashChars_filepath = join(files_dir, dashChars_file_display_name)
    dashChars_file = open(dashChars_filepath, "r")
    dashChars = dashChars_file.read()
    dashChars_file.close()

    Config.disableRedirection()
    Config.resetStatistics()
    Config.enableRedirection()

    activity.runOnUiThread(appendText(textview_output_messages, "Running python script...\n"))

    # CHECKING SUBTITLE STREAMS
    if force_recognize == False:

        src_subtitle_filepath = None
        dst_subtitle_filepath = None
        src_embedded_media_filepath = None
        dst_embedded_media_filepath = None
        ffmpeg_src_language_code = None
        ffmpeg_dst_language_code = None

        # NO TRANSLATE (src == dst)
        # CHECKING ffmpeg_src_language_code SUBTITLE STREAM ONLY, IF EXISTS WE PRINT IT AND EXTRACT IT
        if is_same_language(src, dst):

            if os.path.isfile(cancel_file):
                os.remove(cancel_file)
                return

            print(f"Checking subtitles streams...")
            activity.runOnUiThread(appendText(textview_output_messages, f"Checking subtitles streams...\n"))

            ffmpeg_src_language_code = language.ffmpeg_code_of_code[src]

            subtitle_stream_parser = SubtitleStreamParser()
            subtitle_streams_data = subtitle_stream_parser(media_filepath)
            print(f"subtitle_streams_data = {subtitle_streams_data}")

            if os.path.isfile(cancel_file):
                os.remove(cancel_file)
                return

            if subtitle_streams_data and subtitle_streams_data != []:

                src_subtitle_stream_timed_subtitles = subtitle_stream_parser.timed_subtitles_of_language(ffmpeg_src_language_code)

                if ffmpeg_src_language_code in subtitle_stream_parser.languages():

                    if os.path.isfile(cancel_file):
                        os.remove(cancel_file)
                        return

                    print(f"Is '{ffmpeg_src_language_code}' subtitle stream exist : Yes")
                    activity.runOnUiThread(appendText(textview_output_messages, f"Is '{ffmpeg_src_language_code}' subtitle stream exist : Yes\n"))

                    subtitle_stream_regions = []
                    subtitle_stream_transcripts = []
                    for entry in src_subtitle_stream_timed_subtitles:
                        subtitle_stream_regions.append(entry[0])
                        subtitle_stream_transcripts.append(entry[1])

                    files_dir = str(context.getExternalFilesDir(None))
                    subtitle_folder_name = join(files_dir, media_file_display_name[:-len(media_file_format)-1])
                    if not os.path.isdir(subtitle_folder_name):
                        os.mkdir(subtitle_folder_name)

                    src_subtitle_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.{src}.{subtitle_format}"
                    src_subtitle_file_display_name = os.path.basename(src_subtitle_filepath).split('/')[-1]

                    writer = SubtitleWriter(subtitle_stream_regions, subtitle_stream_transcripts, subtitle_format)
                    writer.write(src_subtitle_filepath)

                    if os.path.isfile(src_subtitle_filepath) and src_subtitle_filepath not in results:
                        results.append(src_subtitle_filepath)

                    if os.path.isfile(cancel_file):
                        os.remove(cancel_file)
                        return

                    print(f"Extracting '{ffmpeg_src_language_code}' subtitle stream as : '{src_subtitle_filepath}'")
                    activity.runOnUiThread(appendText(textview_output_messages, f"Extracting '{ffmpeg_src_language_code}' subtitle stream as :\n'{src_subtitle_filepath}'\n"))

                    if os.path.isfile(cancel_file):
                        os.remove(cancel_file)
                        return

                    # no translate process

                    # print overall results
                    if os.path.isfile(src_subtitle_filepath):

                        print(f"\nTemporary results for '{media_file_display_name}' :")
                        activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))
                        activity.runOnUiThread(appendText(textview_output_messages, f"Temporary results for '{media_file_display_name}' :\n"))
                        for result in results:
                            print(f"{result}")
                            activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))
                            activity.runOnUiThread(appendText(textview_output_messages, f"{result}\n"))
                        print("")
                        #activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))

                        # remove media_filepath from transcribe processed_list
                        if force_recognize == False:
                            if media_filepath not in removed_media_filepaths:
                                removed_media_filepaths.append(media_filepath)

                    if embed_src == True:
                        print(f"No need to embed '{ffmpeg_src_language_code}' subtitles because it's already existed")
                        activity.runOnUiThread(appendText(textview_output_messages, f"No need to embed '{ffmpeg_src_language_code}' subtitles because it's already existed\n"))

                else:
                    print(f"Is '{ffmpeg_src_language_code}' subtitle stream exist : No\n")
                    activity.runOnUiThread(appendText(textview_output_messages, f"Is '{ffmpeg_src_language_code}' subtitle stream exist : No\n"))

                    if os.path.isfile(cancel_file):
                        os.remove(cancel_file)
                        return

            if os.path.isfile(cancel_file):
                os.remove(cancel_file)
                return

        # DO TRANSLATE (src != dst)
        # CHECKING ffmpeg_src_language_code AND ffmpeg_dst_language_code SUBTITLE STREAMS, IF EXISTS WE PRINT IT AND EXTRACT IT
        # IF ONE OF THEM (ffmpeg_src_language_code OR ffmpeg_dst_language_code) NOT EXIST, WE TRANSLATE IT,
        # AND IF BOOLEAN VALUE FOR EMBED (FOR SRC OR DST LANGUAGE) IS TRUE THEN WE EMBED IT
        elif not is_same_language(src, dst):

            if os.path.isfile(cancel_file):
                os.remove(cancel_file)
                return

            print(f"Checking subtitles streams...")
            activity.runOnUiThread(appendText(textview_output_messages, f"Checking subtitles streams...\n"))

            ffmpeg_src_language_code = language.ffmpeg_code_of_code[src]
            ffmpeg_dst_language_code = language.ffmpeg_code_of_code[dst]

            subtitle_stream_parser = SubtitleStreamParser()
            subtitle_streams_data = subtitle_stream_parser(media_filepath)
            print(f"subtitle_streams_data = {subtitle_streams_data}")

            if os.path.isfile(cancel_file):
                os.remove(cancel_file)
                return

            if subtitle_streams_data and subtitle_streams_data != []:

                if os.path.isfile(cancel_file):
                    os.remove(cancel_file)
                    return

                src_subtitle_stream_timed_subtitles = subtitle_stream_parser.timed_subtitles_of_language(ffmpeg_src_language_code)
                dst_subtitle_stream_timed_subtitles = subtitle_stream_parser.timed_subtitles_of_language(ffmpeg_dst_language_code)

                # ffmpeg_src_language_code subtitle stream exist, we print it and extract it
                if ffmpeg_src_language_code in subtitle_stream_parser.languages():

                    if os.path.isfile(cancel_file):
                        os.remove(cancel_file)
                        return

                    print(f"Is '{ffmpeg_src_language_code}' subtitle stream exist : Yes")
                    activity.runOnUiThread(appendText(textview_output_messages, f"Is '{ffmpeg_src_language_code}' subtitle stream exist : Yes\n"))

                    subtitle_stream_regions = []
                    subtitle_stream_transcripts = []
                    for entry in src_subtitle_stream_timed_subtitles:
                        subtitle_stream_regions.append(entry[0])
                        subtitle_stream_transcripts.append(entry[1])
                        if os.path.isfile(cancel_file): return

                    files_dir = str(context.getExternalFilesDir(None))
                    subtitle_folder_name = join(files_dir, media_file_display_name[:-len(media_file_format)-1])
                    if not os.path.isdir(subtitle_folder_name):
                        os.mkdir(subtitle_folder_name)

                    src_subtitle_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.{src}.{subtitle_format}"
                    src_subtitle_file_display_name = os.path.basename(src_subtitle_filepath).split('/')[-1]

                    writer = SubtitleWriter(subtitle_stream_regions, subtitle_stream_transcripts, subtitle_format)
                    writer.write(src_subtitle_filepath)

                    if os.path.isfile(src_subtitle_filepath) and src_subtitle_filepath not in results:
                        results.append(src_subtitle_filepath)

                    print(f"Extracting '{ffmpeg_src_language_code}' subtitle stream as : '{src_subtitle_filepath}'")
                    activity.runOnUiThread(appendText(textview_output_messages, f"Extracting '{ffmpeg_src_language_code}' subtitle stream as :\n'{src_subtitle_filepath}'\n"))

                    if os.path.isfile(cancel_file):
                        os.remove(cancel_file)
                        return

                    if embed_src == True:
                        print(f"No need to embed '{ffmpeg_src_language_code}' subtitle because it's already existed")
                        activity.runOnUiThread(appendText(textview_output_messages, f"No need to embed '{ffmpeg_src_language_code}' subtitles because it's already existed\n"))

                # ffmpeg_src_language_code subtitle stream not exist, just print it
                else:
                    print(f"Is '{ffmpeg_src_language_code}' subtitle stream exist : No")
                    activity.runOnUiThread(appendText(textview_output_messages, f"Is '{ffmpeg_src_language_code}' subtitle stream exist : No\n"))

                    if os.path.isfile(cancel_file):
                        os.remove(cancel_file)
                        return

                # ffmpeg_dst_language_code subtitle stream exist, so we print it and extract it
                if ffmpeg_dst_language_code in subtitle_stream_parser.languages():

                    if os.path.isfile(cancel_file):
                        os.remove(cancel_file)
                        return

                    print(f"Is '{ffmpeg_dst_language_code}' subtitle stream exist : Yes")
                    activity.runOnUiThread(appendText(textview_output_messages, f"Is '{ffmpeg_dst_language_code}' subtitle stream exist : Yes\n"))

                    subtitle_stream_regions = []
                    subtitle_stream_transcripts = []
                    for entry in dst_subtitle_stream_timed_subtitles:
                        subtitle_stream_regions.append(entry[0])
                        subtitle_stream_transcripts.append(entry[1])

                        if os.path.isfile(cancel_file):
                            os.remove(cancel_file)
                            return

                    files_dir = str(context.getExternalFilesDir(None))
                    subtitle_folder_name = join(files_dir, media_file_display_name[:-len(media_file_format)-1])
                    if not os.path.isdir(subtitle_folder_name):
                        os.mkdir(subtitle_folder_name)

                    dst_subtitle_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.{dst}.{subtitle_format}"
                    dst_subtitle_file_display_name = os.path.basename(dst_subtitle_filepath).split('/')[-1]

                    writer = SubtitleWriter(subtitle_stream_regions, subtitle_stream_transcripts, subtitle_format)
                    writer.write(dst_subtitle_filepath)

                    if os.path.isfile(dst_subtitle_filepath) and dst_subtitle_filepath not in results:
                        results.append(dst_subtitle_filepath)

                    if os.path.isfile(cancel_file):
                        os.remove(cancel_file)
                        return

                    print(f"Extracting '{ffmpeg_dst_language_code}' subtitle stream as : '{dst_subtitle_filepath}'")
                    activity.runOnUiThread(appendText(textview_output_messages, f"Extracting '{ffmpeg_dst_language_code}' subtitle stream as :\n'{dst_subtitle_filepath}'\n"))

                    if embed_dst == True:
                        print(f"No need to embed '{ffmpeg_dst_language_code}' subtitles because it's already existed")
                        activity.runOnUiThread(appendText(textview_output_messages, f"No need to embed '{ffmpeg_dst_language_code}' subtitles because it's already existed\n"))

                    if os.path.isfile(cancel_file):
                        os.remove(cancel_file)
                        return

                # ffmpeg_dst_language_code subtitle stream not exist, just print it
                else:
                    print(f"Is '{ffmpeg_dst_language_code}' subtitle stream exist : No")
                    activity.runOnUiThread(appendText(textview_output_messages, f"Is '{ffmpeg_dst_language_code}' subtitle stream exist : No\n"))

                    if os.path.isfile(cancel_file):
                        os.remove(cancel_file)
                        return

                # ffmpeg_src_language_code subtitle stream = not exist,
                # ffmpeg_dst_language_code subtitle stream = exist
                # so we translate it from 'dst' to 'src'
                if ffmpeg_src_language_code not in subtitle_stream_parser.languages() and ffmpeg_dst_language_code in subtitle_stream_parser.languages():

                    if dst_subtitle_stream_timed_subtitles and dst_subtitle_stream_timed_subtitles != []:

                        if os.path.isfile(cancel_file):
                            os.remove(cancel_file)
                            return

                        print(f"Translating subtitles from '{dst}' to '{src}'...")
                        activity.runOnUiThread(appendText(textview_output_messages, f"Translating subtitles from '{dst}' to '{src}'...\n"))

                        translate_start_time = time.time()

                        transcript_translator = SentenceTranslator(src=dst, dst=src)

                        if os.path.isfile(cancel_file):
                            os.remove(cancel_file)
                            return

                        translated_subtitle_stream_transcripts = []

                        activity.runOnUiThread(setVisibility(textview_progress, progress_bar, textview_percentage, textview_time, View.VISIBLE))

                        for i, translated_subtitle_stream_transcript in enumerate(pool.imap(transcript_translator, subtitle_stream_transcripts)):

                            if os.path.isfile(cancel_file):
                                if pool:
                                    pool.terminate()
                                    pool.close()
                                    pool.join()
                                    pool = None
                                return

                            translated_subtitle_stream_transcripts.append(translated_subtitle_stream_transcript)

                            progress = int(i*100/len(dst_subtitle_stream_timed_subtitles))

                            pbar(progress, translate_start_time, 100, f"Translating subtitles from '{dst}' to '{src}'", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                        pbar(100, translate_start_time, 100, f"Translating subtitles from '{dst}' to '{src}'", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                        time.sleep(1)

                        activity.runOnUiThread(setVisibility(textview_progress, progress_bar, textview_percentage, textview_time, View.INVISIBLE))

                        if os.path.isfile(cancel_file):
                            if pool:
                                pool.terminate()
                                pool.close()
                                pool.join()
                                pool = None
                            return

                        print(f"Writing '{src}' subtitles file...")
                        activity.runOnUiThread(appendText(textview_output_messages, f"Writing '{src}' subtitles file...\n"))

                        files_dir = str(context.getExternalFilesDir(None))
                        subtitle_folder_name = join(files_dir, media_file_display_name[:-len(media_file_format)-1])
                        if not os.path.isdir(subtitle_folder_name):
                            os.mkdir(subtitle_folder_name)

                        src_subtitle_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.{src}.{subtitle_format}"
                        src_subtitle_file_display_name = os.path.basename(src_subtitle_filepath).split('/')[-1]

                        translation_writer = SubtitleWriter(subtitle_stream_regions, translated_subtitle_stream_transcripts, subtitle_format)
                        translation_writer.write(src_subtitle_filepath)

                        if os.path.isfile(src_subtitle_filepath) and src_subtitle_filepath not in results:
                            results.append(src_subtitle_filepath)

                        if os.path.isfile(cancel_file):
                            if pool:
                                pool.terminate()
                                pool.close()
                                pool.join()
                                pool = None
                            return

                        print(f"Temporary '{src}' subtitles file saved as : '{src_subtitle_filepath}'")
                        activity.runOnUiThread(appendText(textview_output_messages, f"Temporary '{src}' subtitles file saved as :\n'{src_subtitle_filepath}'\n"))

                        # if embed_src is True then we embed that translated srt (from dst to src) above into media_filepath
                        if embed_src == True:

                            if os.path.isfile(cancel_file):
                                if pool:
                                    pool.terminate()
                                    pool.close()
                                    pool.join()
                                    pool = None
                                return

                            ffmpeg_src_language_code = language.ffmpeg_code_of_code[src]

                            files_dir = str(context.getExternalFilesDir(None))
                            subtitle_folder_name = join(files_dir, media_file_display_name[:-len(media_file_format)-1])
                            if not os.path.isdir(subtitle_folder_name):
                                os.mkdir(subtitle_folder_name)

                            if ext[1:] == "ts":
                                media_file_format = "mp4"
                            else:
                                media_file_format = ext[1:]

                            src_tmp_embedded_media_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.{ffmpeg_src_language_code}.tmp.embedded.{media_file_format}"
                            src_tmp_embedded_media_file_display_name = os.path.basename(src_tmp_embedded_media_filepath).split('/')[-1]

                            src_embedded_media_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.{ffmpeg_src_language_code}.embedded.{media_file_format}"
                            src_embedded_media_file_display_name = os.path.basename(src_embedded_media_filepath).split('/')[-1]

                            if os.path.isfile(cancel_file):
                                if pool:
                                    pool.terminate()
                                    pool.close()
                                    pool.join()
                                    pool = None
                                return

                            try:
                                activity.runOnUiThread(setVisibility(textview_progress, progress_bar, textview_percentage, textview_time, View.VISIBLE))
                                print(f"Embedding '{ffmpeg_src_language_code}' subtitles...")
                                activity.runOnUiThread(appendText(textview_output_messages, f"Embedding '{ffmpeg_src_language_code}' subtitles...\n"))
                                embed_src_start_time = time.time()
                                pbar(0, embed_src_start_time, 100, f"Embedding '{ffmpeg_src_language_code}' subtitles", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                                Config.enableRedirection()

                                subtitle_embedder = MediaSubtitleEmbedder(subtitle_path=src_subtitle_filepath, language=ffmpeg_src_language_code, output_path=src_tmp_embedded_media_filepath, start_time=embed_src_start_time, activity=activity, textview_progress=textview_progress, progress_bar=progress_bar, textview_percentage=textview_percentage, textview_time=textview_time)
                                src_tmp_output = subtitle_embedder(media_filepath)

                                Config.disableRedirection()
                                pbar(100, embed_src_start_time, 100, f"Embedding '{ffmpeg_src_language_code}' subtitles", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                                time.sleep(1)
                                activity.runOnUiThread(setVisibility(textview_progress, progress_bar, textview_percentage, textview_time, View.INVISIBLE))

                            except Exception as e:
                                print(e)
                                return

                            if os.path.isfile(cancel_file):
                                if pool:
                                    pool.terminate()
                                    pool.close()
                                    pool.join()
                                    pool = None
                                return

                            if os.path.isfile(src_tmp_output):
                                shutil.copy(src_tmp_output, src_embedded_media_filepath)
                                os.remove(src_tmp_output)

                                if src_embedded_media_filepath not in results:
                                    results.append(src_embedded_media_filepath)

                            if os.path.isfile(src_embedded_media_filepath):
                                print(f"'{ffmpeg_src_language_code}' subtitles embedded media file saved as : '{src_embedded_media_filepath}'")
                                activity.runOnUiThread(appendText(textview_output_messages, f"'{ffmpeg_src_language_code}' subtitles embedded media file saved as :\n'{src_embedded_media_filepath}'\n"))

                            else:
                                print("Unknown error")
                                activity.runOnUiThread(appendText(textview_output_messages, "Unknown error\n"))

                        # if args.embed_dst is True we can't embed it because dst subtitle stream already exist
                        if embed_dst == True:
                            print(f"No need to embed '{ffmpeg_dst_language_code}' subtitles because it's already existed")
                            activity.runOnUiThread(appendText(textview_output_messages, f"No need to embed '{ffmpeg_dst_language_code}' subtitles because it's already existed\n"))

                        if os.path.isfile(cancel_file):
                            if pool:
                                pool.terminate()
                                pool.close()
                                pool.join()
                                pool = None
                            return

                        if force_recognize == False:
                            if media_filepath not in removed_media_filepaths:
                                removed_media_filepaths.append(media_filepath)


                # ffmpeg_src_language_code subtitle stream = exist,
                # ffmpeg_dst_language_code subtitle stream = not exist
                # so we translate it from 'src' to 'dst'
                elif ffmpeg_src_language_code in subtitle_stream_parser.languages() and ffmpeg_dst_language_code not in subtitle_stream_parser.languages():

                    if src_subtitle_stream_timed_subtitles and src_subtitle_stream_timed_subtitles != []:

                        if os.path.isfile(cancel_file):
                            os.remove(cancel_file)
                            return

                        print(f"Translating subtitles from '{src}' to '{dst}'...")
                        activity.runOnUiThread(appendText(textview_output_messages, f"Translating subtitles from '{src}' to '{dst}'...\n"))

                        translate_start_time = time.time()

                        transcript_translator = SentenceTranslator(src=src, dst=dst)

                        if os.path.isfile(cancel_file):
                            os.remove(cancel_file)
                            return

                        translated_subtitle_stream_transcripts = []

                        activity.runOnUiThread(setVisibility(textview_progress, progress_bar, textview_percentage, textview_time, View.VISIBLE))

                        for i, translated_subtitle_stream_transcript in enumerate(pool.imap(transcript_translator, subtitle_stream_transcripts)):

                            if os.path.isfile(cancel_file):
                                if pool:
                                    pool.terminate()
                                    pool.close()
                                    pool.join()
                                    pool = None
                                return

                            translated_subtitle_stream_transcripts.append(translated_subtitle_stream_transcript)

                            progress = int(i*100/len(src_subtitle_stream_timed_subtitles))

                            pbar(progress, translate_start_time, 100, f"Translating subtitles from '{src}' to '{dst}'", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                        pbar(100, translate_start_time, 100, f"Translating subtitles from '{src}' to '{dst}'", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                        time.sleep(1)

                        activity.runOnUiThread(setVisibility(textview_progress, progress_bar, textview_percentage, textview_time, View.INVISIBLE))

                        if os.path.isfile(cancel_file):
                            if pool:
                                pool.terminate()
                                pool.close()
                                pool.join()
                                pool = None
                            return

                        print(f"Writing '{dst}' subtitles file...")
                        activity.runOnUiThread(appendText(textview_output_messages, f"Writing '{dst}' subtitles file...\n"))

                        files_dir = str(context.getExternalFilesDir(None))
                        subtitle_folder_name = join(files_dir, media_file_display_name[:-len(media_file_format)-1])
                        if not os.path.isdir(subtitle_folder_name):
                            os.mkdir(subtitle_folder_name)

                        dst_subtitle_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.{dst}.{subtitle_format}"
                        dst_subtitle_file_display_name = os.path.basename(dst_subtitle_filepath).split('/')[-1]

                        translation_writer = SubtitleWriter(subtitle_stream_regions, translated_subtitle_stream_transcripts, subtitle_format)
                        translation_writer.write(dst_subtitle_filepath)

                        if os.path.isfile(dst_subtitle_filepath) and dst_subtitle_filepath not in results:
                            results.append(dst_subtitle_filepath)

                        print(f"Temporary '{dst}' subtitles file saved as : '{dst_subtitle_filepath}'")
                        activity.runOnUiThread(appendText(textview_output_messages, f"Temporary '{dst}' subtitles file saved as :\n'{dst_subtitle_filepath}'\n"))

                        if force_recognize == False:
                            if media_filepath not in removed_media_filepaths:
                                removed_media_filepaths.append(media_filepath)

                        # if args.embed_src is True we can't embed it because src subtitle stream already exist
                        if embed_src == True:
                            print(f"No need to embed '{ffmpeg_src_language_code}' subtitles because it's already existed")
                            activity.runOnUiThread(appendText(textview_output_messages, f"No need to embed '{ffmpeg_src_language_code}' subtitles because it's already existed\n"))

                        # if embed_dst is True we embed the translated srt (from src to dst) above into media_filepath
                        if embed_dst == True and src_subtitle_stream_timed_subtitles and src_subtitle_stream_timed_subtitles != []:

                            if os.path.isfile(cancel_file):
                                if pool:
                                    pool.terminate()
                                    pool.close()
                                    pool.join()
                                    pool = None
                                return

                            ffmpeg_dst_language_code = language.ffmpeg_code_of_code[dst]

                            files_dir = str(context.getExternalFilesDir(None))
                            subtitle_folder_name = join(files_dir, media_file_display_name[:-len(media_file_format)-1])
                            if not os.path.isdir(subtitle_folder_name):
                                os.mkdir(subtitle_folder_name)

                            if ext[1:] == "ts":
                                media_file_format = "mp4"
                            else:
                                media_file_format = ext[1:]

                            dst_tmp_embedded_media_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.{ffmpeg_dst_language_code}.tmp.embedded.{media_file_format}"
                            dst_tmp_embedded_media_file_display_name = os.path.basename(dst_tmp_embedded_media_filepath).split('/')[-1]

                            dst_embedded_media_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.{ffmpeg_dst_language_code}.embedded.{media_file_format}"
                            dst_embedded_media_file_display_name = os.path.basename(dst_embedded_media_filepath).split('/')[-1]

                            if os.path.isfile(cancel_file):
                                if pool:
                                    pool.terminate()
                                    pool.close()
                                    pool.join()
                                    pool = None
                                return

                            try:
                                activity.runOnUiThread(setVisibility(textview_progress, progress_bar, textview_percentage, textview_time, View.VISIBLE))
                                print(f"Embedding '{ffmpeg_dst_language_code}' subtitles...")
                                activity.runOnUiThread(appendText(textview_output_messages, f"Embedding '{ffmpeg_dst_language_code}' subtitles...\n"))
                                embed_dst_start_time = time.time()
                                pbar(0, embed_dst_start_time, 100, f"Embedding '{ffmpeg_dst_language_code}' subtitles", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                                Config.enableRedirection()

                                subtitle_embedder = MediaSubtitleEmbedder(subtitle_path=dst_subtitle_filepath, language=ffmpeg_dst_language_code, output_path=dst_tmp_embedded_media_filepath, start_time=embed_dst_start_time, activity=activity, textview_progress=textview_progress, progress_bar=progress_bar, textview_percentage=textview_percentage, textview_time=textview_time)
                                dst_tmp_output = subtitle_embedder(media_filepath)

                                Config.disableRedirection()
                                pbar(100, embed_dst_start_time, 100, f"Embedding '{ffmpeg_dst_language_code}' subtitles", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                                time.sleep(1)
                                activity.runOnUiThread(setVisibility(textview_progress, progress_bar, textview_percentage, textview_time, View.INVISIBLE))

                            except Exception as e:
                                print(e)
                                return

                            if os.path.isfile(cancel_file):
                                if pool:
                                    pool.terminate()
                                    pool.close()
                                    pool.join()
                                    pool = None
                                return

                            if os.path.isfile(dst_tmp_output):
                                shutil.copy(dst_tmp_output, dst_embedded_media_filepath)
                                os.remove(dst_tmp_output)

                            if os.path.isfile(dst_embedded_media_filepath):
                                print(f"'{ffmpeg_dst_language_code}' subtitles embedded media file saved as : '{dst_embedded_media_filepath}'")
                                activity.runOnUiThread(appendText(textview_output_messages, f"'{ffmpeg_dst_language_code}' subtitles embedded media file saved as :\n'{dst_embedded_media_filepath}'\n"))

                                if dst_embedded_media_filepath not in results:
                                    results.append(dst_embedded_media_filepath)

                            else:
                                print("Unknown error")
                                activity.runOnUiThread(appendText(textview_output_messages, "Unknown error\n"))

                if os.path.isfile(cancel_file):
                    if pool:
                        pool.terminate()
                        pool.close()
                        pool.join()
                        pool = None
                    return

                # print overall results
                if (src_subtitle_filepath and os.path.isfile(src_subtitle_filepath)) or (dst_subtitle_filepath and os.path.isfile(dst_subtitle_filepath)):
                    print(f"\nTemporary results for '{media_file_display_name}' :")
                    activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))
                    activity.runOnUiThread(appendText(textview_output_messages, f"Temporary results for '{media_file_display_name}' :\n"))
                    for result in results:
                        print(f"{result}")
                        activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))
                        activity.runOnUiThread(appendText(textview_output_messages, f"{result}\n"))
                    #activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))

                    if force_recognize == False:
                        if media_filepath not in removed_media_filepaths:
                            removed_media_filepaths.append(media_filepath)

            if os.path.isfile(cancel_file):
                os.remove(cancel_file)
                return
                if pool:
                    pool.terminate()
                    pool.close()
                    pool.join()
                    pool = None
                return

    else:
        files_dir = str(context.getExternalFilesDir(None))
        subtitle_folder_name = join(files_dir, media_file_display_name[:-len(media_file_format)-1])
        if not os.path.isdir(subtitle_folder_name):
            os.mkdir(subtitle_folder_name)

        base, ext = os.path.splitext(media_filepath)

        if ext[1:] == "ts":
            media_file_format = "mp4"
        else:
            media_file_format = ext[1:]

        tmp_force_recognize_media_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.tmp.force.recognize.{media_file_format}"

        activity.runOnUiThread(setVisibility(textview_progress, progress_bar, textview_percentage, textview_time, View.VISIBLE))
        print("Removing subtitle streams...")
        activity.runOnUiThread(appendText(textview_output_messages, "Removing subtitle streams...\n"))
        remove_subtitle_streams_start_time = time.time()
        pbar(0, remove_subtitle_streams_start_time, 100, "Removing subtitle streams", activity, textview_progress, progress_bar, textview_percentage, textview_time)
        Config.enableRedirection()
        
        subtitle_remover = MediaSubtitleRemover(output_path=tmp_force_recognize_media_filepath, start_time=remove_subtitle_streams_start_time, activity=activity, textview_progress=textview_progress, progress_bar=progress_bar, textview_percentage=textview_percentage, textview_time=textview_time)
        tmp_output = subtitle_remover(media_filepath)

        Config.disableRedirection()
        pbar(100, remove_subtitle_streams_start_time, 100, "Removing subtitle streams", activity, textview_progress, progress_bar, textview_percentage, textview_time)
        time.sleep(1)

        print(f"Subtitle streams removed")
        activity.runOnUiThread(appendText(textview_output_messages, "Subtitle streams removed\n"))
        activity.runOnUiThread(setVisibility(textview_progress, progress_bar, textview_percentage, textview_time, View.INVISIBLE))

        if os.path.isfile(tmp_output):
            shutil.copy(tmp_output, media_filepath)
            os.remove(tmp_output)


    # TRANSCRIBE PART

    #print(f"removed_media_filepaths = {removed_media_filepaths}")
    #print(f"media_filepath not in removed_media_filepaths = {media_filepath not in removed_media_filepaths }")

    if media_filepath not in removed_media_filepaths:

        if os.path.isfile(cancel_file):
            os.remove(cancel_file)
            return

        src_subtitle_filepath = None
        dst_subtitle_filepath = None

        if os.path.isfile(cancel_file):
            os.remove(cancel_file)
            return

        activity.runOnUiThread(setVisibility(textview_progress, progress_bar, textview_percentage, textview_time, View.VISIBLE))
        print("Converting to WAV file...")
        activity.runOnUiThread(appendText(textview_output_messages, "Converting to WAV file...\n"))
        convert_to_wav_start_time = time.time()
        pbar(0, convert_to_wav_start_time, 100, "Converting to WAV file", activity, textview_progress, progress_bar, textview_percentage, textview_time)
        Config.enableRedirection()

        wav_converter = WavConverter(channels=1, rate=16000, start_time=convert_to_wav_start_time, activity=activity, textview_progress=textview_progress, progress_bar=progress_bar, textview_percentage=textview_percentage, textview_time=textview_time)
        wav_filepath, sample_rate = wav_converter(media_filepath)

        Config.disableRedirection()
        pbar(100, convert_to_wav_start_time, 100, "Converting to WAV file", activity, textview_progress, progress_bar, textview_percentage, textview_time)
        time.sleep(1)
        print(f"Converted WAV file is : {wav_filepath}")
        activity.runOnUiThread(appendText(textview_output_messages, f"Converted WAV file created\n"))
        activity.runOnUiThread(setVisibility(textview_progress, progress_bar, textview_percentage, textview_time, View.INVISIBLE))

        sample_rate = 16000

        if os.path.isfile(cancel_file):
            os.remove(cancel_file)
            return

        print("Finding speech regions of WAV file...")
        activity.runOnUiThread(appendText(textview_output_messages, "Finding speech regions of WAV file...\n"))

        region_finder = SpeechRegionFinder(frame_width=4096, min_region_size=0.5, max_region_size=6)
        regions = region_finder(wav_filepath)

        activity.runOnUiThread(appendText(textview_output_messages, "Speech regions found = " + str(len(regions)) + "\n"))
        time.sleep(1)
        print(f"Speech regions found = {str(len(regions))}")

        if os.path.isfile(cancel_file):
            os.remove(cancel_file)
            return

        converter = FLACConverter(wav_filepath=wav_filepath)
        recognizer = SpeechRecognizer(language=src, rate=sample_rate)

        src_transcriptions = []

        if os.path.isfile(cancel_file):
            os.remove(cancel_file)
            if pool:
                pool.terminate()
                pool.close()
                pool.join()
            return

        if regions:
            print("Converting to FLAC files...")
            activity.runOnUiThread(setVisibility(textview_progress, progress_bar, textview_percentage, textview_time, View.VISIBLE))
            activity.runOnUiThread(appendText(textview_output_messages, "Converting to FLAC files...\n"))
            convert_to_flac_start_time = time.time()
            pbar(0, convert_to_flac_start_time, 100, "Converting to FLAC files", activity, textview_progress, progress_bar, textview_percentage, textview_time)
            extracted_regions = []
            for i, extracted_region in enumerate(pool.imap(converter, regions)):

                if os.path.isfile(cancel_file):
                    os.remove(cancel_file)
                    if pool:
                        pool.terminate()
                        pool.close()
                        pool.join()
                    return

                extracted_regions.append(extracted_region)

                progress = int(i*100/len(regions))

                pbar(progress, convert_to_flac_start_time, 100, "Converting to FLAC files", activity, textview_progress, progress_bar, textview_percentage, textview_time)
            pbar(100, convert_to_flac_start_time, 100, "Converting to FLAC files", activity, textview_progress, progress_bar, textview_percentage, textview_time)

            activity.runOnUiThread(appendText(textview_output_messages, "FLAC files created\n"))

            if os.path.isfile(cancel_file):
                os.remove(cancel_file)
                if pool:
                    pool.terminate()
                    pool.close()
                    pool.join()
                return

            print(f"Creating '{src}' transcriptions...")
            activity.runOnUiThread(appendText(textview_output_messages, f"Creating '{src}' transcriptions...\n"))
            create_transcription_start_time = time.time()
            for i, src_transcription in enumerate(pool.imap(recognizer, extracted_regions)):

                if os.path.isfile(cancel_file):
                    os.remove(cancel_file)
                    if pool:
                        pool.terminate()
                        pool.close()
                        pool.join()
                    return

                src_transcriptions.append(src_transcription)

                progress = int(i*100/len(regions))

                pbar(progress, create_transcription_start_time, 100, f"Creating '{src}' transcriptions", activity, textview_progress, progress_bar, textview_percentage, textview_time)
            pbar(100, create_transcription_start_time, 100, f"Creating '{src}' transcriptions", activity, textview_progress, progress_bar, textview_percentage, textview_time)

            activity.runOnUiThread(appendText(textview_output_messages, f"'{src}' transcriptions created\n"))
            #print(f"src_transcriptions = {src_transcriptions}")

            if os.path.isfile(cancel_file):
                os.remove(cancel_file)
                if pool:
                    pool.terminate()
                    pool.close()
                    pool.join()
                return

            activity.runOnUiThread(appendText(textview_output_messages, f"Writing temporary '{src}' subtitle file\n"))

            files_dir = str(context.getExternalFilesDir(None))
            subtitle_folder_name = join(files_dir, media_file_display_name[:-len(media_file_format)-1])
            if not os.path.isdir(subtitle_folder_name):
                os.mkdir(subtitle_folder_name)

            src_subtitle_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.{src}.{subtitle_format}"
            src_subtitle_file_display_name = os.path.basename(src_subtitle_filepath).split('/')[-1]

            writer = SubtitleWriter(regions, src_transcriptions, subtitle_format)
            writer.write(src_subtitle_filepath)

            if os.path.isfile(src_subtitle_filepath) and src_subtitle_filepath not in results:
                results.append(src_subtitle_filepath)

                print(f"Temporary '{src}' subtitles file saved as : '{src_subtitle_filepath}'")
                activity.runOnUiThread(appendText(textview_output_messages, f"Temporary '{src}' subtitles file saved as :\n'{src_subtitle_filepath}'\n"))

            if os.path.isfile(cancel_file):
                os.remove(cancel_file)
                if pool:
                    pool.terminate()
                    pool.close()
                    pool.join()
                return

            if (not is_same_language(src, dst)) and (os.path.isfile(src_subtitle_filepath)) and (not os.path.isfile(cancel_file)):

                if os.path.isfile(cancel_file):
                    os.remove(cancel_file)
                    if pool:
                        pool.terminate()
                        pool.close()
                        pool.join()
                    return

                dst_subtitle_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.{dst}.{subtitle_format}"
                dst_subtitle_file_display_name = os.path.basename(dst_subtitle_filepath).split('/')[-1]

                created_regions = []
                created_subtitles = []
                timed_subtitles = writer.timed_subtitles
                for entry in timed_subtitles:
                    created_regions.append(entry[0])
                    created_subtitles.append(entry[1])

                transcription_translator = SentenceTranslator(src=src, dst=dst)
                dst_transcriptions = []

                print(f"Translating subtitles from '{src}' to '{dst}'...")
                activity.runOnUiThread(appendText(textview_output_messages, f"Translating subtitles from '{src}' to '{dst}'...\n"))
                translate_start_time = time.time()
                for i, dst_transcription in enumerate(pool.imap(transcription_translator, created_subtitles)):

                    if os.path.isfile(cancel_file):
                        os.remove(cancel_file)
                        pool.terminate()
                        pool.close()
                        return

                    dst_transcriptions.append(dst_transcription)

                    progress = int(i*100/len(created_subtitles))

                    pbar(progress, translate_start_time, 100, f"Translating subtitles from '{src}' to '{dst}'", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                pbar(100, translate_start_time, 100, f"Translating subtitles from '{src}' to '{dst}'", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                time.sleep(1)

                if os.path.isfile(cancel_file):
                    os.remove(cancel_file)
                    if pool:
                        pool.terminate()
                        pool.close()
                        pool.join()
                    return

                activity.runOnUiThread(appendText(textview_output_messages, f"Writing temporary '{dst}' subtitle file\n"))

                translation_writer = SubtitleWriter(created_regions, dst_transcriptions, subtitle_format)
                translation_writer.write(dst_subtitle_filepath)

                if os.path.isfile(dst_subtitle_filepath) and dst_subtitle_filepath not in results:
                    results.append(dst_subtitle_filepath)

                if os.path.isfile(cancel_file):
                    os.remove(cancel_file)
                    if pool:
                        pool.terminate()
                        pool.close()
                        pool.join()
                    return

                print(f"Temporary '{src}' subtitles file saved as : '{src_subtitle_filepath}'")
                print(f"Temporary '{dst}' subtitles file saved as : '{dst_subtitle_filepath}'")

                #activity.runOnUiThread(setVisibility(textview_progress, progress_bar, textview_percentage, textview_time, View.INVISIBLE))
                activity.runOnUiThread(appendText(textview_output_messages, f"Temporary '{src}' subtitles file saved as :\n'{src_subtitle_filepath}'\n"))
                activity.runOnUiThread(appendText(textview_output_messages, f"Temporary '{dst}' subtitles file saved as :\n'{dst_subtitle_filepath}'\n"))

                if os.path.isfile(cancel_file):
                    os.remove(cancel_file)
                    if pool:
                        pool.terminate()
                        pool.close()
                        pool.join()
                    return


            # EMBEDDING subtitles file
            ffmpeg_src_language_code = language.ffmpeg_code_of_code[src]
            ffmpeg_dst_language_code = language.ffmpeg_code_of_code[dst]

            base, ext = os.path.splitext(media_filepath)

            files_dir = str(context.getExternalFilesDir(None))
            subtitle_folder_name = join(files_dir, media_file_display_name[:-len(media_file_format)-1])
            if not os.path.isdir(subtitle_folder_name):
                os.mkdir(subtitle_folder_name)

            if ext[1:] == "ts":
                media_file_format = "mp4"
            else:
                media_file_format = ext[1:]

            src_tmp_embedded_media_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.{ffmpeg_src_language_code}.tmp.embedded.{media_file_format}"
            src_tmp_embedded_media_file_display_name = os.path.basename(src_tmp_embedded_media_filepath).split('/')[-1]

            dst_tmp_embedded_media_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.{ffmpeg_dst_language_code}.tmp.embedded.{media_file_format}"
            dst_tmp_embedded_media_file_display_name = os.path.basename(dst_tmp_embedded_media_filepath).split('/')[-1]

            src_dst_tmp_embedded_media_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.{ffmpeg_src_language_code}.{ffmpeg_dst_language_code}.tmp.embedded.{media_file_format}"
            src_dst_tmp_embedded_media_file_display_name = os.path.basename(src_dst_tmp_embedded_media_filepath).split('/')[-1]

            src_embedded_media_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.{ffmpeg_src_language_code}.embedded.{media_file_format}"
            src_embedded_media_file_display_name = os.path.basename(src_embedded_media_filepath).split('/')[-1]

            dst_embedded_media_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.{ffmpeg_dst_language_code}.embedded.{media_file_format}"
            dst_embedded_media_file_display_name = os.path.basename(dst_embedded_media_filepath).split('/')[-1]

            src_dst_embedded_media_filepath = f"{subtitle_folder_name + os.sep + media_file_display_name[:-len(media_file_format)-1]}.{ffmpeg_src_language_code}.{ffmpeg_dst_language_code}.embedded.{media_file_format}"
            src_dst_embedded_media_file_display_name = os.path.basename(src_dst_embedded_media_filepath).split('/')[-1]
                
            #activity.runOnUiThread(setVisibility(textview_progress, progress_bar, textview_percentage, textview_time, View.VISIBLE))

            if is_same_language(src, dst):

                if embed_src == True:
                    try:
                        print(f"Embedding '{ffmpeg_src_language_code}' subtitles...")
                        activity.runOnUiThread(appendText(textview_output_messages, f"Embedding '{ffmpeg_src_language_code}' subtitles...\n"))
                        embed_src_start_time = time.time()
                        pbar(0, embed_src_start_time, 100, f"Embedding '{ffmpeg_src_language_code}' subtitles", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                        Config.enableRedirection()

                        subtitle_embedder = MediaSubtitleEmbedder(subtitle_path=src_subtitle_filepath, language=ffmpeg_src_language_code, output_path=src_tmp_embedded_media_filepath, start_time=embed_src_start_time, activity=activity, textview_progress=textview_progress, progress_bar=progress_bar, textview_percentage=textview_percentage, textview_time=textview_time)
                        src_tmp_output = subtitle_embedder(media_filepath)

                        Config.disableRedirection()
                        pbar(100, embed_src_start_time, 100, f"Embedding '{ffmpeg_src_language_code}' subtitles", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                        time.sleep(1)

                        if os.path.isfile(src_tmp_output):
                            shutil.copy(src_tmp_output, src_embedded_media_filepath)
                            os.remove(src_tmp_output)

                            if src_embedded_media_filepath not in results:
                                results.append(src_embedded_media_filepath)

                        if os.path.isfile(src_embedded_media_filepath):
                            activity.runOnUiThread(appendText(textview_output_messages, f"Subtitles embedded media file saved as :\n'{src_embedded_media_filepath}'\n"))

                            print(f"\nTemporary results for '{media_file_display_name}' :")
                            activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))
                            activity.runOnUiThread(appendText(textview_output_messages, f"Temporary results for '{media_file_display_name}' :\n"))
                            for result in results:
                                print(f"{result}")
                                activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))
                                activity.runOnUiThread(appendText(textview_output_messages, f"{result}\n"))
                            #activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))

                        else:
                            print("Unknown error")
                            activity.runOnUiThread(appendText(textview_output_messages, "Unknown error\n"))

                    except Exception as e:
                        print(e)
                        return

            elif not is_same_language(src, dst):

                if embed_src == True and embed_dst == True:
                    try:
                        print(f"Embedding '{ffmpeg_src_language_code}' subtitles...")
                        activity.runOnUiThread(appendText(textview_output_messages, f"Embedding '{ffmpeg_src_language_code}' subtitles...\n"))
                        embed_src_start_time = time.time()
                        pbar(0, embed_src_start_time, 100, f"Embedding '{ffmpeg_src_language_code}' subtitles", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                        Config.resetStatistics()
                        Config.enableRedirection()

                        src_subtitle_embedder = MediaSubtitleEmbedder(subtitle_path=src_subtitle_filepath, language=ffmpeg_src_language_code, output_path=src_tmp_embedded_media_filepath, start_time=embed_src_start_time, activity=activity, textview_progress=textview_progress, progress_bar=progress_bar, textview_percentage=textview_percentage, textview_time=textview_time)
                        src_tmp_output = src_subtitle_embedder(media_filepath)

                        Config.disableRedirection()
                        pbar(100, embed_src_start_time, 100, f"Embedding '{ffmpeg_src_language_code}' subtitles", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                        time.sleep(1)

                        if os.path.isfile(src_tmp_output) and os.path.isfile(dst_subtitle_filepath):
                            print(f"Embedding '{ffmpeg_dst_language_code}' subtitles...")
                            activity.runOnUiThread(appendText(textview_output_messages, f"Embedding '{ffmpeg_dst_language_code}' subtitles...\n"))
                            embed_dst_start_time = time.time()
                            pbar(0, embed_dst_start_time, 100, f"Embedding '{ffmpeg_dst_language_code}' subtitles", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                            Config.enableRedirection()

                            src_dst_subtitle_embedder = MediaSubtitleEmbedder(subtitle_path=dst_subtitle_filepath, language=ffmpeg_dst_language_code, output_path=src_dst_tmp_embedded_media_filepath, start_time=embed_dst_start_time, activity=activity, textview_progress=textview_progress, progress_bar=progress_bar, textview_percentage=textview_percentage, textview_time=textview_time)
                            src_dst_tmp_output = src_dst_subtitle_embedder(src_tmp_output)

                            Config.disableRedirection()
                            pbar(100, embed_dst_start_time, 100, f"Embedding '{ffmpeg_dst_language_code}' subtitles", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                            time.sleep(1)

                        if os.path.isfile(src_dst_tmp_output):
                            shutil.copy(src_dst_tmp_output, src_dst_embedded_media_filepath)

                            if os.path.isfile(src_dst_tmp_output):
                                os.remove(src_dst_tmp_output)
                            if os.path.isfile(src_tmp_output):
                                os.remove(src_tmp_output)

                            if src_dst_embedded_media_filepath not in results:
                                results.append(src_dst_embedded_media_filepath)

                        if os.path.isfile(src_dst_embedded_media_filepath):
                            activity.runOnUiThread(appendText(textview_output_messages, f"Subtitles embedded media file saved as :\n'{src_dst_embedded_media_filepath}'\n"))

                            print(f"\nTemporary results for '{media_file_display_name}' :")
                            activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))
                            activity.runOnUiThread(appendText(textview_output_messages, f"Temporary results for '{media_file_display_name}' :\n"))
                            for result in results:
                                print(f"{result}")
                                activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))
                                activity.runOnUiThread(appendText(textview_output_messages, f"{result}\n"))
                            #activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))

                        else:
                            print("Unknown error")
                            activity.runOnUiThread(appendText(textview_output_messages, "Unknown error\n"))

                    except Exception as e:
                        print(e)
                        return

                    if os.path.isfile(cancel_file):
                        os.remove(cancel_file)
                        if pool:
                            pool.terminate()
                            pool.close()
                            pool.join()
                        return

                elif embed_src == True and embed_dst == False:
                    try:

                        print(f"Embedding '{ffmpeg_src_language_code}' subtitles...")
                        activity.runOnUiThread(appendText(textview_output_messages, f"Embedding '{ffmpeg_src_language_code}' subtitles...\n"))
                        embed_src_start_time = time.time()
                        pbar(0, embed_src_start_time, 100, f"Embedding '{ffmpeg_src_language_code}' subtitles", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                        Config.enableRedirection()

                        src_subtitle_embedder = MediaSubtitleEmbedder(subtitle_path=src_subtitle_filepath, language=ffmpeg_src_language_code, output_path=src_tmp_embedded_media_filepath, start_time=embed_src_start_time, activity=activity, textview_progress=textview_progress, progress_bar=progress_bar, textview_percentage=textview_percentage, textview_time=textview_time)
                        src_tmp_output = src_subtitle_embedder(media_filepath)

                        Config.disableRedirection()
                        pbar(100, embed_src_start_time, 100, f"Embedding '{ffmpeg_src_language_code}' subtitles", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                        time.sleep(1)

                        if os.path.isfile(src_tmp_output):
                            shutil.copy(src_tmp_output, src_embedded_media_filepath)
                            os.remove(src_tmp_output)

                            if src_embedded_media_filepath not in results:
                                results.append(src_embedded_media_filepath)

                        if os.path.isfile(src_embedded_media_filepath):
                            activity.runOnUiThread(appendText(textview_output_messages, f"Subtitles embedded media file saved as :\n'{src_embedded_media_filepath}'\n"))

                            print(f"\nTemporary results for '{media_file_display_name}' :")
                            activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))
                            activity.runOnUiThread(appendText(textview_output_messages, f"Temporary results for '{media_file_display_name}' :\n"))
                            for result in results:
                                print(f"{result}")
                                activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))
                                activity.runOnUiThread(appendText(textview_output_messages, f"{result}\n"))
                            #activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))

                        else:
                            print("Unknown error")
                            activity.runOnUiThread(appendText(textview_output_messages, "Unknown error\n"))

                    except Exception as e:
                        print(e)
                        return

                    if os.path.isfile(cancel_file):
                        os.remove(cancel_file)
                        if pool:
                            pool.terminate()
                            pool.close()
                            pool.join()
                        return

                elif embed_src == False and embed_dst == True:
                    try:

                        print(f"Embedding '{ffmpeg_dst_language_code}' subtitles...")
                        activity.runOnUiThread(appendText(textview_output_messages, f"Embedding '{ffmpeg_dst_language_code}' subtitles...\n"))
                        embed_dst_start_time = time.time()
                        pbar(0, embed_dst_start_time, 100, f"Embedding '{ffmpeg_dst_language_code}' subtitles", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                        Config.enableRedirection()

                        dst_subtitle_embedder = MediaSubtitleEmbedder(subtitle_path=dst_subtitle_filepath, language=ffmpeg_dst_language_code, output_path=src_tmp_embedded_media_filepath, start_time=embed_dst_start_time, activity=activity, textview_progress=textview_progress, progress_bar=progress_bar, textview_percentage=textview_percentage, textview_time=textview_time)
                        dst_tmp_output = dst_subtitle_embedder(media_filepath)

                        Config.disableRedirection()
                        pbar(100, embed_dst_start_time, 100, f"Embedding '{ffmpeg_dst_language_code}' subtitles", activity, textview_progress, progress_bar, textview_percentage, textview_time)
                        time.sleep(1)

                        if os.path.isfile(dst_tmp_output):
                            shutil.copy(dst_tmp_output, dst_embedded_media_filepath)
                            os.remove(dst_tmp_output)

                            if dst_embedded_media_filepath not in results:
                                results.append(dst_embedded_media_filepath)

                        if os.path.isfile(dst_embedded_media_filepath):
                            activity.runOnUiThread(appendText(textview_output_messages, f"Subtitles embedded media file saved as :\n'{dst_embedded_media_filepath}'\n"))

                            print(f"\nTemporary results for '{media_file_display_name}' :")
                            activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))
                            activity.runOnUiThread(appendText(textview_output_messages, f"Temporary results for '{media_file_display_name}' :\n"))
                            for result in results:
                                print(f"{result}")
                                activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))
                                activity.runOnUiThread(appendText(textview_output_messages, f"{result}\n"))
                            #activity.runOnUiThread(appendText(textview_output_messages, f"{dashChars}\n"))

                        else:
                            print("Unknown error")
                            activity.runOnUiThread(appendText(textview_output_messages, "Unknown error\n"))

                    except Exception as e:
                        print(e)
                        return

                    if os.path.isfile(cancel_file):
                        os.remove(cancel_file)
                        if pool:
                            pool.terminate()
                            pool.close()
                            pool.join()
                        return

            activity.runOnUiThread(setVisibility(textview_progress, progress_bar, textview_percentage, textview_time, View.INVISIBLE))


        pool.close()
        pool.join()
        pool = None
        os.remove(wav_filepath)
        tmpdir = os.path.split(wav_filepath)[0]
        for file in os.listdir(tmpdir):
            file_path = os.path.join(tmpdir, file)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)

    return results


class setText(static_proxy(None, Runnable)):
    def __init__(self, textview_output_messages, strings):
        super(setText, self).__init__()
        self.textview_output_messages = textview_output_messages
        self.strings = strings

    @Override(jvoid, [])
    def run(self):
        self.textview_output_messages.setText(self.strings)


class appendText(static_proxy(None, Runnable)):
    def __init__(self, textview_output_messages, strings):
        super(appendText, self).__init__()
        self.textview_output_messages = textview_output_messages
        self.strings = strings

    @Override(jvoid, [])
    def run(self):
        height = self.textview_output_messages.getHeight()
        lineHeight = self.textview_output_messages.getLineHeight()
        lines = self.textview_output_messages.getLineCount()
        maxLinesOfOutputMessages = height/lineHeight
        if lines >= maxLinesOfOutputMessages:
            self.textview_output_messages.setGravity(Gravity.BOTTOM)
        self.textview_output_messages.append(self.strings)


class setVisibility(static_proxy(None, Runnable)):
    def __init__(self, textview_progress, progress_bar, textview_percentage, textview_time, view):
        super(setVisibility, self).__init__()
        self.textview_progress = textview_progress
        self.progress_bar = progress_bar
        self.textview_percentage = textview_percentage
        self.textview_time = textview_time
        self.view = view

    @Override(jvoid, [])
    def run(self):
        self.textview_progress.setVisibility(self.view)
        self.progress_bar.setVisibility(self.view)
        self.textview_percentage.setVisibility(self.view)
        self.textview_time.setVisibility(self.view)

