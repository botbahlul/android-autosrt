package com.android.autosrt;

import static android.os.Environment.DIRECTORY_DOCUMENTS;
import static android.os.Environment.getExternalStorageDirectory;
import static android.text.TextUtils.substring;
import static com.arthenica.mobileffmpeg.Config.TAG;
import static java.lang.Math.round;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.Looper;
import android.provider.DocumentsContract;
import android.provider.MediaStore;
import android.provider.OpenableColumns;
import android.provider.Settings;
import android.text.method.ScrollingMovementMethod;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.Spinner;
import android.widget.TextView;

import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import org.apache.commons.lang3.StringUtils;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;


public class MainActivity extends AppCompatActivity {
    ArrayList<String> arraylist_src_code = new ArrayList<>();
    ArrayList<String> arraylist_dst_code = new ArrayList<>();
    ArrayList<String> arraylist_src_languages = new ArrayList<>();
    ArrayList<String> arraylist_dst_languages = new ArrayList<>();
    Map<String, String> map_src_country = new HashMap<>();
    Map<String, String> map_dst_country = new HashMap<>();
    public static String src_language, dst_language, src_code, dst_code;
    ArrayList<String> arraylist_subtitle_format = new ArrayList<>();

    CheckBox checkbox_debug_mode;

    Spinner spinner_src_languages;
    TextView textview_src_code;

    CheckBox checkbox_create_translation;

    TextView textview_text2;
    Spinner spinner_dst_languages;
    TextView textview_dst_code;

    Spinner spinner_subtitle_format;
    TextView textview_subtitle_format;

    TextView textview_fileURI;
    TextView textview_filePath;
    TextView textview_fileDisplayName;
    TextView textview_isTranscribing;
    Button button_browse, button_start;
    TextView textview_debug;

    Python py;
    PyObject pyObjSubtitleFilePath;
    PyObject pyObjWavTempName;
    PyObject pyObjRegions;

    public static boolean isTranscribing = false;
    public static boolean canceled = true;
    public static Thread runpy;
    public static String cancelFile = null;
    public static String copiedPath = null;
    public static String wavTempName = null;
    public static String regions = null;
    public static String subtitleFilePath = null;
    public static Uri fileURI;
    public static String filePath;
    public static String fileDisplayName;
    public static String subtitleFormat;
    public static String subtitleFilePathPath;
    public static String subtitleTranslatedFilePath;
    public static String subtitleFolderName;
    int STORAGE_PERMISSION_CODE = 101;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        arraylist_src_code.add("af");
        arraylist_src_code.add("sq");
        arraylist_src_code.add("am");
        arraylist_src_code.add("ar");
        arraylist_src_code.add("hy");
        arraylist_src_code.add("as");
        arraylist_src_code.add("ay");
        arraylist_src_code.add("az");
        arraylist_src_code.add("bm");
        arraylist_src_code.add("eu");
        arraylist_src_code.add("be");
        arraylist_src_code.add("bn");
        arraylist_src_code.add("bho");
        arraylist_src_code.add("bs");
        arraylist_src_code.add("bg");
        arraylist_src_code.add("ca");
        arraylist_src_code.add("ceb");
        arraylist_src_code.add("ny");
        arraylist_src_code.add("zh-CN");
        arraylist_src_code.add("zh-TW");
        arraylist_src_code.add("co");
        arraylist_src_code.add("hr");
        arraylist_src_code.add("cs");
        arraylist_src_code.add("da");
        arraylist_src_code.add("dv");
        arraylist_src_code.add("doi");
        arraylist_src_code.add("nl");
        arraylist_src_code.add("en");
        arraylist_src_code.add("eo");
        arraylist_src_code.add("et");
        arraylist_src_code.add("ee");
        arraylist_src_code.add("fil");
        arraylist_src_code.add("fi");
        arraylist_src_code.add("fr");
        arraylist_src_code.add("fy");
        arraylist_src_code.add("gl");
        arraylist_src_code.add("ka");
        arraylist_src_code.add("de");
        arraylist_src_code.add("el");
        arraylist_src_code.add("gn");
        arraylist_src_code.add("gu");
        arraylist_src_code.add("ht");
        arraylist_src_code.add("ha");
        arraylist_src_code.add("haw");
        arraylist_src_code.add("he");
        arraylist_src_code.add("hi");
        arraylist_src_code.add("hmn");
        arraylist_src_code.add("hu");
        arraylist_src_code.add("is");
        arraylist_src_code.add("ig");
        arraylist_src_code.add("ilo");
        arraylist_src_code.add("id");
        arraylist_src_code.add("ga");
        arraylist_src_code.add("it");
        arraylist_src_code.add("ja");
        arraylist_src_code.add("jv");
        arraylist_src_code.add("kn");
        arraylist_src_code.add("kk");
        arraylist_src_code.add("km");
        arraylist_src_code.add("rw");
        arraylist_src_code.add("gom");
        arraylist_src_code.add("ko");
        arraylist_src_code.add("kri");
        arraylist_src_code.add("kmr");
        arraylist_src_code.add("ckb");
        arraylist_src_code.add("ky");
        arraylist_src_code.add("lo");
        arraylist_src_code.add("la");
        arraylist_src_code.add("lv");
        arraylist_src_code.add("ln");
        arraylist_src_code.add("lt");
        arraylist_src_code.add("lg");
        arraylist_src_code.add("lb");
        arraylist_src_code.add("mk");
        arraylist_src_code.add("mg");
        arraylist_src_code.add("ms");
        arraylist_src_code.add("ml");
        arraylist_src_code.add("mt");
        arraylist_src_code.add("mi");
        arraylist_src_code.add("mr");
        arraylist_src_code.add("mni-Mtei");
        arraylist_src_code.add("lus");
        arraylist_src_code.add("mn");
        arraylist_src_code.add("my");
        arraylist_src_code.add("ne");
        arraylist_src_code.add("no");
        arraylist_src_code.add("or");
        arraylist_src_code.add("om");
        arraylist_src_code.add("ps");
        arraylist_src_code.add("fa");
        arraylist_src_code.add("pl");
        arraylist_src_code.add("pt");
        arraylist_src_code.add("pa");
        arraylist_src_code.add("qu");
        arraylist_src_code.add("ro");
        arraylist_src_code.add("ru");
        arraylist_src_code.add("sm");
        arraylist_src_code.add("sa");
        arraylist_src_code.add("gd");
        arraylist_src_code.add("nso");
        arraylist_src_code.add("sr");
        arraylist_src_code.add("st");
        arraylist_src_code.add("sn");
        arraylist_src_code.add("sd");
        arraylist_src_code.add("si");
        arraylist_src_code.add("sk");
        arraylist_src_code.add("sl");
        arraylist_src_code.add("so");
        arraylist_src_code.add("es");
        arraylist_src_code.add("su");
        arraylist_src_code.add("sw");
        arraylist_src_code.add("sv");
        arraylist_src_code.add("tg");
        arraylist_src_code.add("ta");
        arraylist_src_code.add("tt");
        arraylist_src_code.add("te");
        arraylist_src_code.add("th");
        arraylist_src_code.add("ti");
        arraylist_src_code.add("ts");
        arraylist_src_code.add("tr");
        arraylist_src_code.add("tk");
        arraylist_src_code.add("tw");
        arraylist_src_code.add("uk");
        arraylist_src_code.add("ur");
        arraylist_src_code.add("ug");
        arraylist_src_code.add("uz");
        arraylist_src_code.add("vi");
        arraylist_src_code.add("cy");
        arraylist_src_code.add("xh");
        arraylist_src_code.add("yi");
        arraylist_src_code.add("yo");
        arraylist_src_code.add("zu");

        arraylist_src_languages.add("Afrikaans");
        arraylist_src_languages.add("Albanian");
        arraylist_src_languages.add("Amharic");
        arraylist_src_languages.add("Arabic");
        arraylist_src_languages.add("Armenian");
        arraylist_src_languages.add("Assamese");
        arraylist_src_languages.add("Aymara");
        arraylist_src_languages.add("Azerbaijani");
        arraylist_src_languages.add("Bambara");
        arraylist_src_languages.add("Basque");
        arraylist_src_languages.add("Belarusian");
        arraylist_src_languages.add("Bengali");
        arraylist_src_languages.add("Bhojpuri");
        arraylist_src_languages.add("Bosnian");
        arraylist_src_languages.add("Bulgarian");
        arraylist_src_languages.add("Catalan");
        arraylist_src_languages.add("Cebuano");
        arraylist_src_languages.add("Chichewa");
        arraylist_src_languages.add("Chinese (Simplified)");
        arraylist_src_languages.add("Chinese (Traditional)");
        arraylist_src_languages.add("Corsican");
        arraylist_src_languages.add("Croatian");
        arraylist_src_languages.add("Czech");
        arraylist_src_languages.add("Danish");
        arraylist_src_languages.add("Dhivehi");
        arraylist_src_languages.add("Dogri");
        arraylist_src_languages.add("Dutch");
        arraylist_src_languages.add("English");
        arraylist_src_languages.add("Esperanto");
        arraylist_src_languages.add("Estonian");
        arraylist_src_languages.add("Ewe");
        arraylist_src_languages.add("Filipino");
        arraylist_src_languages.add("Finnish");
        arraylist_src_languages.add("French");
        arraylist_src_languages.add("Frisian");
        arraylist_src_languages.add("Galician");
        arraylist_src_languages.add("Georgian");
        arraylist_src_languages.add("German");
        arraylist_src_languages.add("Greek");
        arraylist_src_languages.add("Guarani");
        arraylist_src_languages.add("Gujarati");
        arraylist_src_languages.add("Haitian Creole");
        arraylist_src_languages.add("Hausa");
        arraylist_src_languages.add("Hawaiian");
        arraylist_src_languages.add("Hebrew");
        arraylist_src_languages.add("Hindi");
        arraylist_src_languages.add("Hmong");
        arraylist_src_languages.add("Hungarian");
        arraylist_src_languages.add("Icelandic");
        arraylist_src_languages.add("Igbo");
        arraylist_src_languages.add("Ilocano");
        arraylist_src_languages.add("Indonesian");
        arraylist_src_languages.add("Irish");
        arraylist_src_languages.add("Italian");
        arraylist_src_languages.add("Japanese");
        arraylist_src_languages.add("Javanese");
        arraylist_src_languages.add("Kannada");
        arraylist_src_languages.add("Kazakh");
        arraylist_src_languages.add("Khmer");
        arraylist_src_languages.add("Kinyarwanda");
        arraylist_src_languages.add("Konkani");
        arraylist_src_languages.add("Korean");
        arraylist_src_languages.add("Krio");
        arraylist_src_languages.add("Kurdish (Kurmanji)");
        arraylist_src_languages.add("Kurdish (Sorani)");
        arraylist_src_languages.add("Kyrgyz");
        arraylist_src_languages.add("Lao");
        arraylist_src_languages.add("Latin");
        arraylist_src_languages.add("Latvian");
        arraylist_src_languages.add("Lingala");
        arraylist_src_languages.add("Lithuanian");
        arraylist_src_languages.add("Luganda");
        arraylist_src_languages.add("Luxembourgish");
        arraylist_src_languages.add("Macedonian");
        arraylist_src_languages.add("Malagasy");
        arraylist_src_languages.add("Malay");
        arraylist_src_languages.add("Malayalam");
        arraylist_src_languages.add("Maltese");
        arraylist_src_languages.add("Maori");
        arraylist_src_languages.add("Marathi");
        arraylist_src_languages.add("Meiteilon (Manipuri)");
        arraylist_src_languages.add("Mizo");
        arraylist_src_languages.add("Mongolian");
        arraylist_src_languages.add("Myanmar (Burmese)");
        arraylist_src_languages.add("Nepali");
        arraylist_src_languages.add("Norwegian");
        arraylist_src_languages.add("Odiya (Oriya)");
        arraylist_src_languages.add("Oromo");
        arraylist_src_languages.add("Pashto");
        arraylist_src_languages.add("Persian");
        arraylist_src_languages.add("Polish");
        arraylist_src_languages.add("Portuguese");
        arraylist_src_languages.add("Punjabi");
        arraylist_src_languages.add("Quechua");
        arraylist_src_languages.add("Romanian");
        arraylist_src_languages.add("Russian");
        arraylist_src_languages.add("Samoan");
        arraylist_src_languages.add("Sanskrit");
        arraylist_src_languages.add("Scots Gaelic");
        arraylist_src_languages.add("Sepedi");
        arraylist_src_languages.add("Serbian");
        arraylist_src_languages.add("Sesotho");
        arraylist_src_languages.add("Shona");
        arraylist_src_languages.add("Sindhi");
        arraylist_src_languages.add("Sinhala");
        arraylist_src_languages.add("Slovak");
        arraylist_src_languages.add("Slovenian");
        arraylist_src_languages.add("Somali");
        arraylist_src_languages.add("Spanish");
        arraylist_src_languages.add("Sundanese");
        arraylist_src_languages.add("Swahili");
        arraylist_src_languages.add("Swedish");
        arraylist_src_languages.add("Tajik");
        arraylist_src_languages.add("Tamil");
        arraylist_src_languages.add("Tatar");
        arraylist_src_languages.add("Telugu");
        arraylist_src_languages.add("Thai");
        arraylist_src_languages.add("Tigrinya");
        arraylist_src_languages.add("Tsonga");
        arraylist_src_languages.add("Turkish");
        arraylist_src_languages.add("Turkmen");
        arraylist_src_languages.add("Twi (Akan)");
        arraylist_src_languages.add("Ukrainian");
        arraylist_src_languages.add("Urdu");
        arraylist_src_languages.add("Uyghur");
        arraylist_src_languages.add("Uzbek");
        arraylist_src_languages.add("Vietnamese");
        arraylist_src_languages.add("Welsh");
        arraylist_src_languages.add("Xhosa");
        arraylist_src_languages.add("Yiddish");
        arraylist_src_languages.add("Yoruba");
        arraylist_src_languages.add("Zulu");

        for (int i = 0; i < arraylist_src_languages.size(); i++) {
            map_src_country.put(arraylist_src_languages.get(i), arraylist_src_code.get(i));
        }

        arraylist_dst_code.add("af");
        arraylist_dst_code.add("sq");
        arraylist_dst_code.add("am");
        arraylist_dst_code.add("ar");
        arraylist_dst_code.add("hy");
        arraylist_dst_code.add("as");
        arraylist_dst_code.add("ay");
        arraylist_dst_code.add("az");
        arraylist_dst_code.add("bm");
        arraylist_dst_code.add("eu");
        arraylist_dst_code.add("be");
        arraylist_dst_code.add("bn");
        arraylist_dst_code.add("bho");
        arraylist_dst_code.add("bs");
        arraylist_dst_code.add("bg");
        arraylist_dst_code.add("ca");
        arraylist_dst_code.add("ceb");
        arraylist_dst_code.add("ny");
        arraylist_dst_code.add("zh-CN");
        arraylist_dst_code.add("zh-TW");
        arraylist_dst_code.add("co");
        arraylist_dst_code.add("hr");
        arraylist_dst_code.add("cs");
        arraylist_dst_code.add("da");
        arraylist_dst_code.add("dv");
        arraylist_dst_code.add("doi");
        arraylist_dst_code.add("nl");
        arraylist_dst_code.add("en");
        arraylist_dst_code.add("eo");
        arraylist_dst_code.add("et");
        arraylist_dst_code.add("ee");
        arraylist_dst_code.add("fil");
        arraylist_dst_code.add("fi");
        arraylist_dst_code.add("fr");
        arraylist_dst_code.add("fy");
        arraylist_dst_code.add("gl");
        arraylist_dst_code.add("ka");
        arraylist_dst_code.add("de");
        arraylist_dst_code.add("el");
        arraylist_dst_code.add("gn");
        arraylist_dst_code.add("gu");
        arraylist_dst_code.add("ht");
        arraylist_dst_code.add("ha");
        arraylist_dst_code.add("haw");
        arraylist_dst_code.add("he");
        arraylist_dst_code.add("hi");
        arraylist_dst_code.add("hmn");
        arraylist_dst_code.add("hu");
        arraylist_dst_code.add("is");
        arraylist_dst_code.add("ig");
        arraylist_dst_code.add("ilo");
        arraylist_dst_code.add("id");
        arraylist_dst_code.add("ga");
        arraylist_dst_code.add("it");
        arraylist_dst_code.add("ja");
        arraylist_dst_code.add("jv");
        arraylist_dst_code.add("kn");
        arraylist_dst_code.add("kk");
        arraylist_dst_code.add("km");
        arraylist_dst_code.add("rw");
        arraylist_dst_code.add("gom");
        arraylist_dst_code.add("ko");
        arraylist_dst_code.add("kri");
        arraylist_dst_code.add("kmr");
        arraylist_dst_code.add("ckb");
        arraylist_dst_code.add("ky");
        arraylist_dst_code.add("lo");
        arraylist_dst_code.add("la");
        arraylist_dst_code.add("lv");
        arraylist_dst_code.add("ln");
        arraylist_dst_code.add("lt");
        arraylist_dst_code.add("lg");
        arraylist_dst_code.add("lb");
        arraylist_dst_code.add("mk");
        arraylist_dst_code.add("mg");
        arraylist_dst_code.add("ms");
        arraylist_dst_code.add("ml");
        arraylist_dst_code.add("mt");
        arraylist_dst_code.add("mi");
        arraylist_dst_code.add("mr");
        arraylist_dst_code.add("mni-Mtei");
        arraylist_dst_code.add("lus");
        arraylist_dst_code.add("mn");
        arraylist_dst_code.add("my");
        arraylist_dst_code.add("ne");
        arraylist_dst_code.add("no");
        arraylist_dst_code.add("or");
        arraylist_dst_code.add("om");
        arraylist_dst_code.add("ps");
        arraylist_dst_code.add("fa");
        arraylist_dst_code.add("pl");
        arraylist_dst_code.add("pt");
        arraylist_dst_code.add("pa");
        arraylist_dst_code.add("qu");
        arraylist_dst_code.add("ro");
        arraylist_dst_code.add("ru");
        arraylist_dst_code.add("sm");
        arraylist_dst_code.add("sa");
        arraylist_dst_code.add("gd");
        arraylist_dst_code.add("nso");
        arraylist_dst_code.add("sr");
        arraylist_dst_code.add("st");
        arraylist_dst_code.add("sn");
        arraylist_dst_code.add("sd");
        arraylist_dst_code.add("si");
        arraylist_dst_code.add("sk");
        arraylist_dst_code.add("sl");
        arraylist_dst_code.add("so");
        arraylist_dst_code.add("es");
        arraylist_dst_code.add("su");
        arraylist_dst_code.add("sw");
        arraylist_dst_code.add("sv");
        arraylist_dst_code.add("tg");
        arraylist_dst_code.add("ta");
        arraylist_dst_code.add("tt");
        arraylist_dst_code.add("te");
        arraylist_dst_code.add("th");
        arraylist_dst_code.add("ti");
        arraylist_dst_code.add("ts");
        arraylist_dst_code.add("tr");
        arraylist_dst_code.add("tk");
        arraylist_dst_code.add("tw");
        arraylist_dst_code.add("uk");
        arraylist_dst_code.add("ur");
        arraylist_dst_code.add("ug");
        arraylist_dst_code.add("uz");
        arraylist_dst_code.add("vi");
        arraylist_dst_code.add("cy");
        arraylist_dst_code.add("xh");
        arraylist_dst_code.add("yi");
        arraylist_dst_code.add("yo");
        arraylist_dst_code.add("zu");

        arraylist_dst_languages.add("Afrikaans");
        arraylist_dst_languages.add("Albanian");
        arraylist_dst_languages.add("Amharic");
        arraylist_dst_languages.add("Arabic");
        arraylist_dst_languages.add("Armenian");
        arraylist_dst_languages.add("Assamese");
        arraylist_dst_languages.add("Aymara");
        arraylist_dst_languages.add("Azerbaijani");
        arraylist_dst_languages.add("Bambara");
        arraylist_dst_languages.add("Basque");
        arraylist_dst_languages.add("Belarusian");
        arraylist_dst_languages.add("Bengali");
        arraylist_dst_languages.add("Bhojpuri");
        arraylist_dst_languages.add("Bosnian");
        arraylist_dst_languages.add("Bulgarian");
        arraylist_dst_languages.add("Catalan");
        arraylist_dst_languages.add("Cebuano");
        arraylist_dst_languages.add("Chichewa");
        arraylist_dst_languages.add("Chinese (Simplified)");
        arraylist_dst_languages.add("Chinese (Traditional)");
        arraylist_dst_languages.add("Corsican");
        arraylist_dst_languages.add("Croatian");
        arraylist_dst_languages.add("Czech");
        arraylist_dst_languages.add("Danish");
        arraylist_dst_languages.add("Dhivehi");
        arraylist_dst_languages.add("Dogri");
        arraylist_dst_languages.add("Dutch");
        arraylist_dst_languages.add("English");
        arraylist_dst_languages.add("Esperanto");
        arraylist_dst_languages.add("Estonian");
        arraylist_dst_languages.add("Ewe");
        arraylist_dst_languages.add("Filipino");
        arraylist_dst_languages.add("Finnish");
        arraylist_dst_languages.add("French");
        arraylist_dst_languages.add("Frisian");
        arraylist_dst_languages.add("Galician");
        arraylist_dst_languages.add("Georgian");
        arraylist_dst_languages.add("German");
        arraylist_dst_languages.add("Greek");
        arraylist_dst_languages.add("Guarani");
        arraylist_dst_languages.add("Gujarati");
        arraylist_dst_languages.add("Haitian Creole");
        arraylist_dst_languages.add("Hausa");
        arraylist_dst_languages.add("Hawaiian");
        arraylist_dst_languages.add("Hebrew");
        arraylist_dst_languages.add("Hindi");
        arraylist_dst_languages.add("Hmong");
        arraylist_dst_languages.add("Hungarian");
        arraylist_dst_languages.add("Icelandic");
        arraylist_dst_languages.add("Igbo");
        arraylist_dst_languages.add("Ilocano");
        arraylist_dst_languages.add("Indonesian");
        arraylist_dst_languages.add("Irish");
        arraylist_dst_languages.add("Italian");
        arraylist_dst_languages.add("Japanese");
        arraylist_dst_languages.add("Javanese");
        arraylist_dst_languages.add("Kannada");
        arraylist_dst_languages.add("Kazakh");
        arraylist_dst_languages.add("Khmer");
        arraylist_dst_languages.add("Kinyarwanda");
        arraylist_dst_languages.add("Konkani");
        arraylist_dst_languages.add("Korean");
        arraylist_dst_languages.add("Krio");
        arraylist_dst_languages.add("Kurdish (Kurmanji)");
        arraylist_dst_languages.add("Kurdish (Sorani)");
        arraylist_dst_languages.add("Kyrgyz");
        arraylist_dst_languages.add("Lao");
        arraylist_dst_languages.add("Latin");
        arraylist_dst_languages.add("Latvian");
        arraylist_dst_languages.add("Lingala");
        arraylist_dst_languages.add("Lithuanian");
        arraylist_dst_languages.add("Luganda");
        arraylist_dst_languages.add("Luxembourgish");
        arraylist_dst_languages.add("Macedonian");
        arraylist_dst_languages.add("Malagasy");
        arraylist_dst_languages.add("Malay");
        arraylist_dst_languages.add("Malayalam");
        arraylist_dst_languages.add("Maltese");
        arraylist_dst_languages.add("Maori");
        arraylist_dst_languages.add("Marathi");
        arraylist_dst_languages.add("Meiteilon (Manipuri)");
        arraylist_dst_languages.add("Mizo");
        arraylist_dst_languages.add("Mongolian");
        arraylist_dst_languages.add("Myanmar (Burmese)");
        arraylist_dst_languages.add("Nepali");
        arraylist_dst_languages.add("Norwegian");
        arraylist_dst_languages.add("Odiya (Oriya)");
        arraylist_dst_languages.add("Oromo");
        arraylist_dst_languages.add("Pashto");
        arraylist_dst_languages.add("Persian");
        arraylist_dst_languages.add("Polish");
        arraylist_dst_languages.add("Portuguese");
        arraylist_dst_languages.add("Punjabi");
        arraylist_dst_languages.add("Quechua");
        arraylist_dst_languages.add("Romanian");
        arraylist_dst_languages.add("Russian");
        arraylist_dst_languages.add("Samoan");
        arraylist_dst_languages.add("Sanskrit");
        arraylist_dst_languages.add("Scots Gaelic");
        arraylist_dst_languages.add("Sepedi");
        arraylist_dst_languages.add("Serbian");
        arraylist_dst_languages.add("Sesotho");
        arraylist_dst_languages.add("Shona");
        arraylist_dst_languages.add("Sindhi");
        arraylist_dst_languages.add("Sinhala");
        arraylist_dst_languages.add("Slovak");
        arraylist_dst_languages.add("Slovenian");
        arraylist_dst_languages.add("Somali");
        arraylist_dst_languages.add("Spanish");
        arraylist_dst_languages.add("Sundanese");
        arraylist_dst_languages.add("Swahili");
        arraylist_dst_languages.add("Swedish");
        arraylist_dst_languages.add("Tajik");
        arraylist_dst_languages.add("Tamil");
        arraylist_dst_languages.add("Tatar");
        arraylist_dst_languages.add("Telugu");
        arraylist_dst_languages.add("Thai");
        arraylist_dst_languages.add("Tigrinya");
        arraylist_dst_languages.add("Tsonga");
        arraylist_dst_languages.add("Turkish");
        arraylist_dst_languages.add("Turkmen");
        arraylist_dst_languages.add("Twi (Akan)");
        arraylist_dst_languages.add("Ukrainian");
        arraylist_dst_languages.add("Urdu");
        arraylist_dst_languages.add("Uyghur");
        arraylist_dst_languages.add("Uzbek");
        arraylist_dst_languages.add("Vietnamese");
        arraylist_dst_languages.add("Welsh");
        arraylist_dst_languages.add("Xhosa");
        arraylist_dst_languages.add("Yiddish");
        arraylist_dst_languages.add("Yoruba");
        arraylist_dst_languages.add("Zulu");

        for (int i = 0; i < arraylist_dst_languages.size(); i++) {
            map_dst_country.put(arraylist_dst_languages.get(i), arraylist_dst_code.get(i));
        }

        arraylist_subtitle_format.add("srt");
        arraylist_subtitle_format.add("vtt");
        arraylist_subtitle_format.add("json");
        arraylist_subtitle_format.add("raw");

        setContentView(R.layout.activity_main);

        checkbox_debug_mode = findViewById(R.id.checkbox_debug_mode);
        spinner_src_languages = findViewById(R.id.spinner_src_languages);
        setup_src_spinner(arraylist_src_languages);
        textview_src_code = findViewById(R.id.textview_src_code);

        checkbox_create_translation = findViewById(R.id.checkbox_create_translation);

        textview_text2 = findViewById(R.id.textview_text2);
        spinner_dst_languages = findViewById(R.id.spinner_dst_languages);
        setup_dst_spinner(arraylist_dst_languages);
        textview_dst_code = findViewById(R.id.textview_dst_code);

        spinner_subtitle_format = findViewById(R.id.spinner_subtitle_format);
        setup_subtitle_format(arraylist_subtitle_format);
        textview_subtitle_format = findViewById(R.id.textview_subtitle_format);

        textview_fileURI = findViewById(R.id.textview_fileURI);
        textview_filePath = findViewById(R.id.textview_filePath);
        textview_fileDisplayName = findViewById(R.id.textview_fileDisplayName);

        button_browse = findViewById(R.id.button_browse);
        button_start = findViewById(R.id.button_start);
        textview_isTranscribing = findViewById(R.id.textview_isTranscribing);
        textview_debug = findViewById(R.id.textview_debug);

        textview_debug.setSelected(true);

        spinner_src_languages.setFocusable(true);
        spinner_src_languages.requestFocus();

        textview_fileURI.setMovementMethod(new ScrollingMovementMethod());
        textview_debug.setMovementMethod(new ScrollingMovementMethod());

        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayOptions(ActionBar.DISPLAY_SHOW_CUSTOM);
            getSupportActionBar().setCustomView(R.layout.actionbar_layout);
        }

        cancelFile = getApplicationContext().getExternalFilesDir(null) + File.separator + "cancel.txt";
        File f = new File(cancelFile);
        if (f.exists()) {
            f.delete();
        }

        String t1 = "isTranscribing = " + isTranscribing;
        textview_isTranscribing.setText(t1);

        checkbox_debug_mode.setOnClickListener(view -> {
            if(((CompoundButton) view).isChecked()){
                textview_src_code.setVisibility(View.VISIBLE);
                textview_dst_code.setVisibility(View.VISIBLE);
                textview_subtitle_format.setVisibility(View.VISIBLE);
                textview_fileURI.setVisibility(View.VISIBLE);
                textview_fileDisplayName.setVisibility(View.VISIBLE);
                textview_isTranscribing.setVisibility(View.VISIBLE);
            }
            else {
                textview_src_code.setVisibility(View.GONE);
                textview_dst_code.setVisibility(View.GONE);
                textview_subtitle_format.setVisibility(View.GONE);
                textview_fileURI.setVisibility(View.GONE);
                textview_fileDisplayName.setVisibility(View.GONE);
                textview_isTranscribing.setVisibility(View.GONE);
            }
        });

        spinner_src_languages.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                src_language = spinner_src_languages.getSelectedItem().toString();
                //dst_language = spinner_dst_languages.getSelectedItem().toString();
                src_code = map_src_country.get(src_language);
                //dst_code = map_dst_country.get(dst_language);
                runOnUiThread(() -> {
                    String lsrc = "src_code = " + src_code;
                    textview_src_code.setText(lsrc);
                });
            }
            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {
                src_language = spinner_src_languages.getSelectedItem().toString();
                //dst_language = spinner_dst_languages.getSelectedItem().toString();
                src_code = map_src_country.get(src_language);
                //dst_code = map_dst_country.get(dst_language);
                runOnUiThread(() -> {
                    String lsrc = "src_code = " + src_code;
                    textview_src_code.setText(lsrc);
                });
            }
        });

        spinner_dst_languages.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                //src_language = spinner_src_languages.getSelectedItem().toString();
                dst_language = spinner_dst_languages.getSelectedItem().toString();
                //src_code = map_src_country.get(src_language);
                dst_code = map_dst_country.get(dst_language);
                runOnUiThread(() -> {
                    String ldst = "dst_code = " + dst_code;
                    textview_dst_code.setText(ldst);
                });
            }
            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {
                //src_language = spinner_src_languages.getSelectedItem().toString();
                dst_language = spinner_dst_languages.getSelectedItem().toString();
                //src_code = map_src_country.get(src_language);
                dst_code = map_dst_country.get(dst_language);
                runOnUiThread(() -> {
                    String ldst = "dst_code = " + dst_code;
                    textview_dst_code.setText(ldst);
                });
            }
        });

        checkbox_create_translation.setOnClickListener(view -> {
            if(((CompoundButton) view).isChecked()){
                textview_text2.setVisibility(View.VISIBLE);
                spinner_dst_languages.setVisibility(View.VISIBLE);
                textview_dst_code.setVisibility(View.VISIBLE);

                spinner_dst_languages.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
                    @Override
                    public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                        src_language = spinner_src_languages.getSelectedItem().toString();
                        dst_language = spinner_dst_languages.getSelectedItem().toString();
                        src_code = map_src_country.get(src_language);
                        dst_code = map_dst_country.get(dst_language);
                        runOnUiThread(() -> {
                            String ldst = "dst_code = " + dst_code;
                            textview_dst_code.setText(ldst);
                        });
                    }
                    @Override
                    public void onNothingSelected(AdapterView<?> adapterView) {
                        src_language = spinner_src_languages.getSelectedItem().toString();
                        dst_language = spinner_dst_languages.getSelectedItem().toString();
                        src_code = map_src_country.get(src_language);
                        dst_code = map_dst_country.get(dst_language);
                        runOnUiThread(() -> {
                            String ldst = "dst_code = " + dst_code;
                            textview_dst_code.setText(ldst);
                        });
                    }
                });

            }
            else {
                textview_text2.setVisibility(View.GONE);
                spinner_dst_languages.setVisibility(View.GONE);
                textview_dst_code.setVisibility(View.GONE);

                dst_language = src_language;
                spinner_dst_languages.setSelection(arraylist_dst_languages.indexOf(dst_language));
                dst_code = map_dst_country.get(dst_language);
            }
        });

        spinner_subtitle_format.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                subtitleFormat = spinner_subtitle_format.getSelectedItem().toString();
                String sf = "subtitleFormat = " + subtitleFormat;
                textview_subtitle_format.setText(sf);
            }
            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {
                subtitleFormat = spinner_subtitle_format.getSelectedItem().toString();
                String sf = "subtitleFormat = " + subtitleFormat;
                textview_subtitle_format.setText(sf);
            }
        });

        button_browse.setOnClickListener(view -> {
            textview_debug.setText("");
            fileURI = null;
            Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            String[] mimeTypes = {"video/*", "audio/*"};
            intent.setType("*/*");
            intent.putExtra(Intent.EXTRA_MIME_TYPES, mimeTypes);
            mStartForActivity.launch(intent);
        });

        button_start.setOnClickListener(view -> {
            textview_debug.setText("");
            subtitleFilePath = null;
            if (runpy != null) {
                runpy.interrupt();
                runpy = null;
            }
            cancelFile = getApplicationContext().getExternalFilesDir(null) + File.separator + "cancel.txt";
            if (new File(cancelFile).exists()) {
                new File(cancelFile).delete();
            }
            File frs = new File(getApplicationContext().getExternalCacheDir().getAbsoluteFile() + File.separator + "region_start.txt");
            File fet = new File(getApplicationContext().getExternalCacheDir().getAbsoluteFile() + File.separator + "elapsed_time.txt");
            if (frs.exists()) {
                frs.delete();
            }
            if (fet.exists()) {
                fet.delete();
            }
            isTranscribing = !isTranscribing;
            if (fileURI != null) canceled = !canceled;

            if (isTranscribing) {
                runOnUiThread(() -> {
                    String ts = "isTranscribing = " + isTranscribing;
                    textview_isTranscribing.setText(ts);
                    String t = "Cancel";
                    button_start.setText(t);
                    transcribe();
                });
            }

            else {
                canceled = true;
                runOnUiThread(() -> {
                    String ts = "isTranscribing = " + isTranscribing;
                    textview_isTranscribing.setText(ts);
                    String t = "Start Transcribe";
                    button_start.setText(t);
                });
                File fc = new File(cancelFile);
                try {
                    FileWriter out = new FileWriter(fc);
                    out.write("");
                    out.close();
                } catch (IOException e) {
                    Log.e("Error: ", Objects.requireNonNull(e.getMessage()));
                    e.printStackTrace();
                }

                if (subtitleFilePath != null) {
                    File sf = new File(subtitleFilePath).getAbsoluteFile();
                    if(sf.exists() && sf.delete()){
                        System.out.println(new File(subtitleFilePath).getAbsoluteFile() + " deleted");
                    }
                }
                if (subtitleFilePath != null) {
                    File stf = new File(subtitleFilePath).getAbsoluteFile();
                    if(stf.exists() && stf.delete()){
                        System.out.println(new File(subtitleFilePath).getAbsoluteFile() + " deleted");
                    }
                }

                if (runpy != null) {
                    runpy.interrupt();
                    runpy = null;
                }
                isTranscribing = false;
            }
        });

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q && !Environment.isExternalStorageLegacy()) {
            Uri uri = Uri.parse("package:" + MainActivity.this.getPackageName());
            startActivity(new Intent(Settings.ACTION_MANAGE_WRITE_SETTINGS, uri));
        } else {
            checkPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE, STORAGE_PERMISSION_CODE);
        }

    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == STORAGE_PERMISSION_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                //Toast.makeText(MainActivity.this, "Storage Permission Granted", Toast.LENGTH_SHORT).show();
                String m = "Storage permission granted";
                textview_debug.setText(m);
            } else {
                //Toast.makeText(MainActivity.this, "Storage Permission Denied", Toast.LENGTH_SHORT).show();
                String m = "Storage permission denied";
                textview_debug.setText(m);
            }
        }
    }

    public void checkPermission(String permission, int requestCode) {
        if (ContextCompat.checkSelfPermission(MainActivity.this, permission) == PackageManager.PERMISSION_DENIED) {
            ActivityCompat.requestPermissions(MainActivity.this, new String[] { permission }, requestCode);
        }
    }

    public void setup_src_spinner(ArrayList<String> supported_languages) {
        Collections.sort(supported_languages);
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, R.layout.spinner_textview_align, supported_languages);
        adapter.setDropDownViewResource(R.layout.spinner_textview_align);
        spinner_src_languages.setAdapter(adapter);
        spinner_src_languages.setSelection(supported_languages.indexOf("English"));
    }

    public void setup_dst_spinner(ArrayList<String> supported_languages) {
        Collections.sort(supported_languages);
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, R.layout.spinner_textview_align, supported_languages);
        adapter.setDropDownViewResource(R.layout.spinner_textview_align);
        spinner_dst_languages.setAdapter(adapter);
        spinner_dst_languages.setSelection(supported_languages.indexOf("Indonesian"));
    }

    public void setup_subtitle_format(ArrayList<String> supported_formats) {
        Collections.sort(supported_formats);
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, R.layout.spinner_textview_align, supported_formats);
        adapter.setDropDownViewResource(R.layout.spinner_textview_align);
        spinner_subtitle_format.setAdapter(adapter);
        spinner_subtitle_format.setSelection(supported_formats.indexOf("srt"));
    }

    ActivityResultLauncher<Intent> mStartForActivity = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            new ActivityResultCallback<ActivityResult>() {
                @Override
                public void onActivityResult(ActivityResult result) {
                    if (result.getResultCode() == Activity.RESULT_OK) {
                        Intent intent = result.getData();
                        if (intent != null) {
                            fileURI = intent.getData();
                        }
                        filePath = Uri2Path(getApplicationContext(), fileURI);
                        fileDisplayName = queryName(getApplicationContext(), fileURI);
                        subtitleFilePathPath = substring(filePath,0,filePath.length()-4) + "." + subtitleFormat;
                        subtitleTranslatedFilePath = substring(filePath,0,filePath.length()-4) + "_translated." + subtitleFormat;
                        runOnUiThread(() -> {
                            String t1 = "fileURI = " + fileURI;
                            textview_fileURI.setText(t1);
                            String t2 = "filePath = " + filePath;
                            textview_filePath.setText(t2);
                            String t3 = "fileDisplayName = " + fileDisplayName;
                            textview_fileDisplayName.setText(t3);
                        });
                    }
                }
            });

    private static String queryName(Context context, Uri uri) {
        Cursor returnCursor = context.getContentResolver().query(uri, null, null, null, null);
        assert returnCursor != null;
        int nameIndex = returnCursor.getColumnIndex(OpenableColumns.DISPLAY_NAME);
        returnCursor.moveToFirst();
        String name = returnCursor.getString(nameIndex);
        returnCursor.close();
        return name;
    }

    /*public byte[] getBytes(InputStream inputStream) throws IOException {
        ByteArrayOutputStream byteBuffer = new ByteArrayOutputStream();
        int bufferSize = 1024;
        byte[] buffer = new byte[bufferSize];

        int len;
        while ((len = inputStream.read(buffer)) != -1) {
            byteBuffer.write(buffer, 0, len);
        }
        return byteBuffer.toByteArray();
    }*/

    private void transcribe() {
        runpy = null;
        runpy = new Thread(() -> {
            if (Looper.myLooper() == null) {
                Looper.prepare();
            }

            if (fileURI != null) {
                if (!canceled) {
                    Log.d("Current Thread", "Running");
                    try {
                        if (!Python.isStarted()) {
                            Python.start(new AndroidPlatform(MainActivity.this));
                            py = Python.getInstance();
                        }
                        // DUE TO SCOPED STORAGE RESTRICTION THERE ARE 2 OPTIONS TO PROCEED USERS PICKED FILE
                        // OPTION 1 : CREATE A COPY OF USERS PICKED FILE TO ExternalFilesDir/subtitleFolderName
                        // THEN PROCEED IT IN PYTHON SCRIPT (copiedPath AS filePath IN PYTHON SCRIPT)
                        // SO USERS CAN DIRECTLY WATCH THEIR MOVIES WITH SUBTITLES IN ExternalFilesDir/subtitleFolderName
                        // AFTER APP EXECUTION

                        // OPTION 2 : DIRECTLY USE filePath TO REDUCE EXECUTION TIME

                        // ALL SUBTITLE FILES WILL BE CREATED AT externalFilesDir/subtitleFolderName
                        // SO USERS SHOULD MOVE SUBTITLE FILES THEMSELF TO THEIR DESIRED FOLDER

                        // BUT externalFilesDir/subtitleFolderName IS NOT A SAFE FOLDER TO STORE SUBTITLE FILE
                        // BECAUSE IF USER UNINSTALL APP, ALL SUBTITLE FILES WILL BE GONE TOO
                        // SO WE SHOULD COPY THEM TO A SAFE FOLDER
                        // IN THIS CASE WE CAN SAVE THEM TO Environment.getExternalStorageDirectory().DIRECTORY_DOCUMENTS

                        // subtitleFolderName AND SUBTITLE FILES NAME WILL BE CREATED BASED ON fileDisplayName

                        // WE SHOULD USE time.sleep(seconds) WHEN CALL dinamic_proxy FUNCTIONS
                        // IN PYTHON SCRIPT TO AVOID CRASH

                        // USING OPTION 1 : CREATE A COPY
                        /*subtitleFolderName = substring(fileDisplayName, 0, fileDisplayName.length() - 4);
                        String prefix = "Creating a copy of " + fileDisplayName + " : ";
                        String copyPath = copyFileToExternalFilesDir(fileURI, subtitleFolderName, prefix);
                        if (copyPath != null) {
                            copiedPath = copyPath;
                        }
                        else {
                            runpy.interrupt();
                            runpy = null;
                            transcribe();
                        }*/

                        // USING OPTION 2 : : DIRECTLY USING filePath
                        if (filePath == null) {
                            runpy.interrupt();
                            runpy = null;
                            transcribe();
                        }

                        // THERE ARE 2 ALTERNATIVE TO RUN PYTHON SCRIPT
                        // ALTERNATIVE 1 : RUN A SINGLE FUNCTION transcribe() IN autosrt.py
                        // ALTERNATIVE 2 : RUN SPLIT FUNCTIONS OF transcibe() IN autosrt.py

                        // USING ALTERNATIVE 1 OPTION 1 :
                        // RUN A SINGLE FUNCTION transcribe() and USING copiedPath
                        /*pyObjSubtitleFilePath = py.getModule("autosrt").callAttr(
                                "transcribe",
                                src_code, dst_code, filePath, fileDisplayName, subtitleFormat, MainActivity.this, textview_debug);
                        if (pyObjSubtitleFilePath != null) {
                            subtitleFilePath = pyObjSubtitleFilePath.toString();
                        }*/

                        // USING ALTERNATIVE 1 OPTION 2 : 
                        // RUN A SINGLE FUNCTION transcribe() and DIRECTLY USE filePath
                        pyObjSubtitleFilePath = py.getModule("autosrt").callAttr(
                                "transcribe",
                                src_code, dst_code, filePath, fileDisplayName, subtitleFormat, MainActivity.this, textview_debug);
                        if (pyObjSubtitleFilePath != null) {
                            subtitleFilePath = pyObjSubtitleFilePath.toString();
                            // ALL FILES IN externalFilesDir() WILL BE DELETED IF USER UNINSTALL APP
                            // SO WE NEED TO COPY IT TO SAVE FOLDER LIKE Environment.getExternalStorageDirectory().DIRECTORY_DOCUMENTS
                            saveSubtitleFileToDocumentsDir();
                        }

                        // USING ALTERNATIVE 2 OPTION 1 :
                        // RUN SPLIT FUNCTIONS OF transcibe() and USING copiedPath AS filePath
                        /*if (!canceled && fileURI != null && copiedPath != null) {
                            try (pyObjWavTempName = py.getModule("autosrt").callAttr(
                                    "convert_to_wav",
                                    copiedPath, 1, 16000, MainActivity.this, textview_debug)) {
                                if (pyObjWavTempName != null) wavTempName = pyObjWavTempName.toString();
                            }
                        }
                        if (!canceled && fileURI != null && wavTempName != null) {
                            try (pyObjRegions = py.getModule("autosrt").callAttr(
                                    "find_audio_regions",
                                    wavTempName, 4096, 0.3, 8, MainActivity.this, textview_debug)) {
                                if (pyObjRegions != null) regions = pyObjRegions.toString();
                            }
                        }
                        if (!canceled && fileURI != null && copiedPath != null && wavTempName != null) {
                            try (PyObject pyObjSubtitleFilePath = py.getModule("autosrt").callAttr(
                                    "perform_speech_recognition",
                                    filePath, fileDisplayName, wavTempName, subtitleFormat, src_code, MainActivity.this, textview_debug)) {
                                if (pyObjSubtitleFilePath != null) {
                                    subtitleFilePath = pyObjSubtitleFilePath.toString();
                                    if (Objects.equals(src_code, dst_code)) {
                                        saveSubtitleFileToDocumentsDir();
                                    }
                                }
                            }
                        }

                        if (!canceled && fileURI != null && subtitleFilePath != null && Objects.equals(src_code, dst_code)) {
                            if (runpy != null) {
                                runpy.interrupt();
                                runpy = null;
                            }
                            isTranscribing = false;
                            canceled = true;
                            runOnUiThread(() -> {
                                String ts = "isTranscribing = " + isTranscribing;
                                textview_isTranscribing.setText(ts);
                                String t1 = "Start Transcribe";
                                button_start.setText(t1);
                            });
                        }

                        if (!canceled && fileURI != null && subtitleFilePath != null && !Objects.equals(src_code, dst_code)) {
                            try (pyObjSubtitleFilePath = py.getModule("autosrt").callAttr(
                                    "perform_translation",
                                    subtitleFilePath, subtitleFormat, src_code, dst_code, MainActivity.this, textview_debug)) {
                                if (pyObjSubtitleFilePath != null) {
                                    subtitleFilePath = pyObjSubtitleFilePath.toString();
                                    saveSubtitleFileToDocumentsDir();
                                }
                            }
                        }*/
                        // END OF ALTERNATIVE 2 OPTION 1


                        // USING ALTERNATIVE 2 OPTION 2 :
                        // RUN SPLIT FUNCTIONS OF transcibe() and DIRECTLY USING filePath
                        /*if (filePath == null) {
                            runpy.interrupt();
                            runpy = null;
                            transcribe();
                        }
                        if (!canceled && fileURI != null && filePath != null) {
                            try (pyObjWavTempName = py.getModule("autosrt").callAttr(
                                    "convert_to_wav",
                                    filePath, 1, 16000, MainActivity.this, textview_debug)) {
                                if (pyObjWavTempName != null) wavTempName = pyObjWavTempName.toString();
                            }
                        }
                        if (!canceled && fileURI != null && wavTempName != null) {
                            try (pyObjRegions = py.getModule("autosrt").callAttr(
                                    "find_audio_regions",
                                    wavTempName, 4096, 0.3, 8, MainActivity.this, textview_debug)) {
                                if (pyObjRegions != null) regions = pyObjRegions.toString();
                            }
                        }
                        if (!canceled && fileURI != null && filePath != null && wavTempName != null) {
                            try (pyObjSubtitleFilePath = py.getModule("autosrt").callAttr(
                                    "perform_speech_recognition",
                                    filePath, fileDisplayName, wavTempName, subtitleFormat, src_code, MainActivity.this, textview_debug)) {
                                if (pyObjSubtitleFilePath != null) {
                                    subtitleFilePath = pyObjSubtitleFilePath.toString();
                                    if (Objects.equals(src_code, dst_code)) {
                                        saveSubtitleFileToDocumentsDir();
                                    }
                                }
                            }
                        }

                        if (!canceled && fileURI != null && subtitleFilePath != null && Objects.equals(src_code, dst_code)) {
                            if (runpy != null) {
                                runpy.interrupt();
                                runpy = null;
                            }
                            isTranscribing = false;
                            canceled = true;
                            runOnUiThread(() -> {
                                String ts = "isTranscribing = " + isTranscribing;
                                textview_isTranscribing.setText(ts);
                                String t1 = "Start Transcribe";
                                button_start.setText(t1);
                            });
                        }

                        if (!canceled && fileURI != null && subtitleFilePath != null && !Objects.equals(src_code, dst_code)) {
                            try (pyObjSubtitleFilePath = py.getModule("autosrt").callAttr(
                                    "perform_translation",
                                    subtitleFilePath, subtitleFormat, src_code, dst_code, MainActivity.this, textview_debug)) {
                                if (pyObjSubtitleFilePath != null) {
                                    subtitleFilePath = pyObjSubtitleFilePath.toString();
                                    saveSubtitleFileToDocumentsDir();
                                }
                            }
                        }*/
                        // END OF ALTERNATIVE 2 OPTION 2


                        // FINISHING
                        if (!canceled && fileURI != null && subtitleFilePath != null) {
                            if (runpy != null) {
                                runpy.interrupt();
                                runpy = null;
                            }
                            isTranscribing = false;
                            canceled = true;
                            runOnUiThread(() -> {
                                String ts = "isTranscribing = " + isTranscribing;
                                textview_isTranscribing.setText(ts);
                                String t1 = "Start Transcribe";
                                button_start.setText(t1);
                            });
                        }
                    }
                    catch (Exception e) {
                        Log.e("Error: ", Objects.requireNonNull(e.getMessage()));
                        e.printStackTrace();
                    }
                }

                else {
                    if (runpy != null) {
                        runpy.interrupt();
                        runpy = null;
                    }
                    isTranscribing = false;
                }

            }
            else {
                if (runpy != null) {
                    runpy.interrupt();
                    runpy = null;
                }
                isTranscribing = false;
                runOnUiThread(() -> {
                    String t1 = "Start Transcribe";
                    button_start.setText(t1);
                    String m = "You should browse a file first\n";
                    textview_debug.setText(m);
                });
            }
        });
        runpy.start();
        runOnUiThread(() -> {

        });
    }

    /*SimpleDateFormat tf = new SimpleDateFormat("HH:mm:ss");
    Date startTime=null, nowTime=null;
    String str_nowTime, str_startTime, str_remainingTime;
    long long_elapsedTime, long_remainingTime;*/
    @SuppressLint({"SetTextI18n", "SimpleDateFormat"})
    private String copyFileToExternalFilesDir(Uri uri, String newDirName, String prefix) {
        File output = null;
        int nameIndex;
        int sizeIndex;
        @SuppressLint("Recycle") Cursor returnCursor = getApplicationContext().getContentResolver().query(uri, new String[]{
                OpenableColumns.DISPLAY_NAME, OpenableColumns.SIZE
        }, null, null, null);
        //*
        //* Get the column indexes of the data in the Cursor,
        //*     * move to the first row in the Cursor, get the data,
        //*     * and display it.
        //*
        if (canceled) {
            if (runpy != null) {
                runpy.interrupt();
                runpy = null;
            }
            isTranscribing = false;
        } else {
            nameIndex = returnCursor.getColumnIndex(OpenableColumns.DISPLAY_NAME);
            sizeIndex = returnCursor.getColumnIndex(OpenableColumns.SIZE);
            returnCursor.moveToFirst();
            String name = (returnCursor.getString(nameIndex));
            String size = (Long.toString(returnCursor.getLong(sizeIndex)));

            if (!newDirName.equals("")) {
                File dir = new File(getApplicationContext().getExternalFilesDir(null) + "/" + newDirName);
                if (!dir.exists()) {
                    dir.mkdir();
                }
                output = new File(getApplicationContext().getExternalFilesDir(null) + "/" + newDirName + "/" + name);
            } else {
                output = new File(getApplicationContext().getExternalFilesDir(null) + "/" + name);
            }
            try {
                InputStream inputStream = getApplicationContext().getContentResolver().openInputStream(uri);
                FileOutputStream outputStream = new FileOutputStream(output);
                long length = Long.parseLong(size);
                long counter = 0;
                int read;
                int bufferSize = 1024;
                final byte[] buffers = new byte[bufferSize];

                //if (counter == 0) {
                //    startTime = new java.util.Date(System.currentTimeMillis());
                //    str_startTime = new SimpleDateFormat("HH:mm:ss").format(startTime);
                //    try {
                //        startTime = tf.parse(str_startTime);
                //    } catch (ParseException e) {
                //        throw new RuntimeException(e);
                //    }
                //}

                while ((read = inputStream.read(buffers)) != -1) {
                    if (canceled) {
                        if (runpy != null) {
                            runpy.interrupt();
                            runpy = null;
                        }
                        isTranscribing = false;
                    } else {
                        counter += read;
                        outputStream.write(buffers, 0, read);
                        //pBar(counter, length, prefix);

                        //nowTime = new java.util.Date(System.currentTimeMillis());
                        //str_nowTime = new SimpleDateFormat("HH:mm:ss").format(nowTime);
                        //try {
                        //    nowTime = tf.parse(str_nowTime);
                        //} catch (ParseException e) {
                        //    throw new RuntimeException(e);
                        //}
                        //long_elapsedTime = Objects.requireNonNull(nowTime).getTime() - Objects.requireNonNull(startTime).getTime();
                        //long_remainingTime = long_elapsedTime * (long) (length / counter);
                        //str_remainingTime = millisecondToDate(long_remainingTime);

                        int bar_length = 10;
                        float percentage = round(100.0 * counter / (float) (length));
                        String pounds = StringUtils.repeat('#', round(bar_length * counter / (float) (length)));
                        String equals = StringUtils.repeat('=', (bar_length - round(bar_length * counter / (float) (length))));
                        String bar = pounds + equals;
                        if ((int)(percentage) % 10 == 0){
                            runOnUiThread(() -> {
                                textview_debug.setText(prefix + " [" + bar + "] " + percentage + '%');
                                //textview_debug.setText(prefix + " [" + bar + "] " + percentage + "% " + str_remainingTime);
                            });
                        }
                    }
                }
                inputStream.close();
                outputStream.close();
                runOnUiThread(() -> textview_debug.append("\n"));

            } catch (Exception e) {
                Log.e("Exception", Objects.requireNonNull(e.getMessage()));
            }
        }
        return Objects.requireNonNull(output).getPath();
    }

    /*public static String millisecondToDate(long t) {
        long i = t;
        i /= 1000;  //from www.java2s.com
        long minute = i / 60;
        long hour = minute / 60;
        long second = i % 60;
        minute %= 60;
        if (hour <= 0) {
            return String.format(Locale.getDefault(), "%02d:%02d", minute, second);
        } else {
            return String.format(Locale.getDefault(), "%02d:%02d:%02d", hour, minute, second);
        }
    }*/

    public String Uri2Path(Context context, Uri uri) {
        if (uri == null) {
            return null;
        }

        if(ContentResolver.SCHEME_FILE.equals(uri.getScheme())) {
            System.out.println("uri.getPath() = " + uri.getPath());
            return uri.getPath();
        }

        else if(ContentResolver.SCHEME_CONTENT.equals(uri.getScheme())) {
            String authority = uri.getAuthority();
            String idStr = "";

            if(authority.startsWith("com.android.externalstorage")) {
                String docId = DocumentsContract.getDocumentId(uri);
                String[] split = docId.split(":");
                String type = split[0];
                String fullPath = getPathFromExtSD(split);
                if (!fullPath.equals("")) {
                    System.out.println("fullPath = " + fullPath);
                    return fullPath;
                } else {
                    return null;
                }
            }

            else {
                if(authority.equals("media")) {
                    idStr = uri.toString().substring(uri.toString().lastIndexOf('/') + 1);
                    System.out.println("media idStr = " + idStr);
                }
                else if(authority.startsWith("com.android.providers")) {
                    idStr = DocumentsContract.getDocumentId(uri).split(":")[1];
                    System.out.println("providers idStr = " + idStr);
                }

                ContentResolver contentResolver = context.getContentResolver();
                Cursor cursor = contentResolver.query(MediaStore.Files.getContentUri("external"),
                        new String[] {MediaStore.Files.FileColumns.DATA},
                        "_id=?",
                        new String[]{idStr}, null);
                if (cursor != null) {
                    cursor.moveToFirst();
                    try {
                        int idx = cursor.getColumnIndex(MediaStore.Files.FileColumns.DATA);
                        System.out.println("cursor.getString(idx) = " + cursor.getString(idx));
                        return cursor.getString(idx);
                    } catch (Exception e) {
                        e.printStackTrace();
                    } finally {
                        cursor.close();
                    }
                }
            }
        }
        return null;
    }

    private String getPathFromExtSD(String[] pathData) {
        final String type = pathData[0];
        final String relativePath = File.separator + pathData[1];
        String fullPath;

        if ("primary".equalsIgnoreCase(type)) {
            System.out.println("PRIMARY");
            System.out.println("type = " + type);
            fullPath = Environment.getExternalStorageDirectory() + relativePath;
            if (fileExists(fullPath)) {
                return fullPath;
            }
        }
        // CHECK SECONDARY STORAGE
        else {
            fullPath = "/storage/" + type + File.separator + relativePath;
            if (fileExists(fullPath)) {
                return fullPath;
            }
        }
        return fullPath;
    }

    private static boolean fileExists(String filePath) {
        File file = new File(filePath);
        return file.exists();
    }

    private void saveSubtitleFileToDocumentsDir() {
        OutputStream outputStream;
        String subtitleFolder = StringUtils.substring(fileDisplayName,0,fileDisplayName.length()-4);
        String savedSubtitleFilePath = StringUtils.substring(fileDisplayName,0,fileDisplayName.length()-4) + "." + subtitleFormat;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            ContentValues values = new ContentValues();
            values.put(MediaStore.MediaColumns.DISPLAY_NAME, savedSubtitleFilePath); // file name savedSubtitleFilePath required to contain extension file mime
            values.put(MediaStore.MediaColumns.MIME_TYPE, "text/plain");
            values.put(MediaStore.MediaColumns.RELATIVE_PATH, DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator + subtitleFolder);
            Uri extVolumeUri = MediaStore.Files.getContentUri("external");
            Uri fileUri = getApplicationContext().getContentResolver().insert(extVolumeUri, values);
            try {
                outputStream = getApplicationContext().getContentResolver().openOutputStream(fileUri);
            } catch (FileNotFoundException e) {
                throw new RuntimeException(e);
            }
        }
        else {
            File root = new File(Environment.getExternalStorageDirectory() + File.separator + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator + subtitleFolder);
            if (!root.exists()) {
                root.mkdirs();
            }
            File file = new File(root, savedSubtitleFilePath );
            Log.d(TAG, "saveFile: file path - " + file.getAbsolutePath());
            try {
                outputStream = new FileOutputStream(file);
            } catch (FileNotFoundException e) {
                throw new RuntimeException(e);
            }
        }
        Uri uri = Uri.fromFile(new File(subtitleFilePath));
        InputStream inputStream;
        try {
            inputStream = getApplicationContext().getContentResolver().openInputStream(uri);
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        }
        byte[] bytes = new byte[1024];
        int length;
        while (true) {
            try {
                if (!((length = inputStream.read(bytes)) > 0)) break;
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            try {
                outputStream.write(bytes, 0, length);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
        try {
            outputStream.close();
            inputStream.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        String savedTanslatedsubtitleFilePath = StringUtils.substring(fileDisplayName, 0, fileDisplayName.length() - 4) + "_translated." + subtitleFormat;
        if (!Objects.equals(src_code, dst_code)) {
            OutputStream outputStreamTranslated;
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                ContentValues values = new ContentValues();
                values.put(MediaStore.MediaColumns.DISPLAY_NAME, savedTanslatedsubtitleFilePath); // file name avedTanslatedsubtitleFilePath required to contain extension file mime
                values.put(MediaStore.MediaColumns.MIME_TYPE, "text/plain");
                values.put(MediaStore.MediaColumns.RELATIVE_PATH, DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator + subtitleFolder);
                Uri extVolumeUri = MediaStore.Files.getContentUri("external");
                Uri fileUri = getApplicationContext().getContentResolver().insert(extVolumeUri, values);
                try {
                    outputStreamTranslated = getApplicationContext().getContentResolver().openOutputStream(fileUri);
                } catch (FileNotFoundException e) {
                    throw new RuntimeException(e);
                }
            } else {
                File root = new File(Environment.getExternalStorageDirectory() + File.separator + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator + subtitleFolder);
                if (!root.exists()) {
                    root.mkdirs();
                }
                File file = new File(root, savedTanslatedsubtitleFilePath);
                Log.d(TAG, "saveFile: file path - " + file.getAbsolutePath());
                try {
                    outputStreamTranslated = new FileOutputStream(file);
                } catch (FileNotFoundException e) {
                    throw new RuntimeException(e);
                }
            }

            String translatedsubtitleFilePath = StringUtils.substring(subtitleFilePath, 0, subtitleFilePath.length() - 4) + "_translated." + subtitleFormat;
            Uri uriTranslated = Uri.fromFile(new File(translatedsubtitleFilePath));
            InputStream inputStreamTranslated;
            try {
                inputStreamTranslated = getApplicationContext().getContentResolver().openInputStream(uriTranslated);
            } catch (FileNotFoundException e) {
                throw new RuntimeException(e);
            }
            byte[] bytesTranslated = new byte[1024];
            int lengthTranslated;
            while (true) {
                try {
                    if (!((lengthTranslated = inputStreamTranslated.read(bytesTranslated)) > 0))
                        break;
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
                try {
                    outputStreamTranslated.write(bytesTranslated, 0, lengthTranslated);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
            try {
                outputStreamTranslated.close();
                inputStreamTranslated.close();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
        runOnUiThread(() -> {
            textview_debug.setText("");
            String savedFolderPath = getExternalStorageDirectory() + File.separator + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator + subtitleFolder;
            String sf = "Subtitle file saved at : \n" + savedFolderPath + File.separator + savedSubtitleFilePath + "\n\n";
            textview_debug.append(sf);
            if (!Objects.equals(src_code, dst_code)) {
                String tsf = "Translated subtitle file saved at : \n" + savedFolderPath + File.separator + savedTanslatedsubtitleFilePath + "\n\n";
                textview_debug.append(tsf);
            }
            String d = "Done.";
            textview_debug.append(d);
        });
    }

    /*@SuppressLint("SetTextI18n")
    public void pBar(long counter, long total, String prefix) {
        int bar_length = 10;
        int rounded = round(bar_length * counter/(float)(total));
        int filled_up_Length = (int)(rounded);
        float percentage = round(100.0 * counter /(float)(total));
        String pounds = StringUtils.repeat('#', filled_up_Length);
        String equals = StringUtils.repeat('=', (bar_length - filled_up_Length));
        String bar = pounds + equals;
        textview_debug.setText(prefix + " [" + bar + "] " + percentage + '%');
    }*/

}

