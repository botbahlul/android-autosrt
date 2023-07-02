package com.android.autosrt;

import static android.os.Environment.DIRECTORY_DOCUMENTS;
import static android.os.Environment.getExternalStorageDirectory;
import static android.provider.DocumentsContract.EXTRA_INITIAL_URI;
import static android.provider.Settings.AUTHORITY;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.ClipData;
import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Paint;
import android.graphics.Rect;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.Looper;
import android.os.ParcelFileDescriptor;
import android.os.storage.StorageManager;
import android.provider.DocumentsContract;
import android.provider.MediaStore;
import android.provider.OpenableColumns;
import android.provider.Settings;
import android.text.method.ScrollingMovementMethod;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.ProgressBar;
import android.widget.RelativeLayout;
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
import androidx.documentfile.provider.DocumentFile;

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
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.Arrays;
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
    String src_language, dst_language, src_code, dst_code;
    ArrayList<String> arraylist_subtitle_format = new ArrayList<>();

    Spinner spinner_src_languages;
    CheckBox checkbox_create_translation;
    TextView textview_text2;
    Spinner spinner_dst_languages;
    Spinner spinner_subtitle_format;
    TextView textview_filePath;
    Button button_browse;
    Button button_grant_storage_permission;
    TextView textview_grant_storage_permission_notes;
    Button button_grant_manage_app_all_files_access_permission;
    TextView textview_grant_manage_app_all_files_access_permission_notes;
    Button button_grant_persisted_tree_uri_permission;
    TextView textview_grant_persisted_tree_uri_permission_notes;
    Button button_start;
    TextView textview_currentFilePathProceed;
    TextView textview_progress;
    ProgressBar progressBar;
    TextView textview_percentage;
    TextView textview_time;
    TextView textview_output_messages;

    Python py;
    PyObject pyObjTmpSubtitleFilePath;

    boolean isTranscribing = false;
    Thread threadTranscriber;
    String cancelFilePath;

    ArrayList<Uri> selectedFilesUri;
    ArrayList<String> selectedFilesPath;
    ArrayList<String> selectedFilesDisplayName;
    String subtitleFormat;
    ArrayList<String> tmpSubtitleFilesPath;
    ArrayList<String> tmpTranslatedSubtitleFilesPath;
    File[] savedSubtitleFile;

    String selectedFolderPath;
    Uri selectedFolderUri;
    ArrayList<Uri> savedTreesUri;

    int heightOfOutputMessages;
    int maxLinesOfOutputMessages;
    int maxChars = 0;
    String equals;
    long transcribeStartTime;
    long transcribeElapsedTime;
    String formattedElapsedTime;


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

        spinner_src_languages = findViewById(R.id.spinner_src_languages);
        setup_src_spinner(arraylist_src_languages);

        checkbox_create_translation = findViewById(R.id.checkbox_create_translation);

        textview_text2 = findViewById(R.id.textview_text2);
        spinner_dst_languages = findViewById(R.id.spinner_dst_languages);
        setup_dst_spinner(arraylist_dst_languages);

        spinner_subtitle_format = findViewById(R.id.spinner_subtitle_format);
        setup_subtitle_format(arraylist_subtitle_format);

        textview_filePath = findViewById(R.id.textview_filePath);
        button_browse = findViewById(R.id.button_browse);

        button_grant_storage_permission = findViewById(R.id.button_grant_storage_permission);
        textview_grant_storage_permission_notes = findViewById(R.id.textview_grant_storage_permission_notes);
        button_grant_manage_app_all_files_access_permission = findViewById(R.id.button_grant_manage_app_all_files_access_permission);
        textview_grant_manage_app_all_files_access_permission_notes = findViewById(R.id.textview_grant_manage_app_all_files_access_permission_notes);
        button_grant_persisted_tree_uri_permission = findViewById(R.id.button_grant_persisted_tree_uri_permission);
        textview_grant_persisted_tree_uri_permission_notes = findViewById(R.id.textview_grant_persisted_tree_uri_permission_notes);

        button_start = findViewById(R.id.button_start);
        textview_currentFilePathProceed = findViewById(R.id.textview_currentFilePathProceed);
        textview_progress = findViewById(R.id.textview_progress);
        progressBar = findViewById(R.id.progressBar);
        textview_percentage = findViewById(R.id.textview_percentage);
        textview_time = findViewById(R.id.textview_time);
        textview_output_messages = findViewById(R.id.textview_output_messages);

        textview_filePath.setTextIsSelectable(true);
        textview_output_messages.setTextIsSelectable(true);

        textview_filePath.setSelected(true);
        textview_output_messages.setSelected(true);

        textview_filePath.setMovementMethod(new ScrollingMovementMethod());
        textview_output_messages.setMovementMethod(new ScrollingMovementMethod());

        spinner_src_languages.setFocusable(true);
        spinner_src_languages.requestFocus();

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            button_grant_manage_app_all_files_access_permission.setVisibility(View.VISIBLE);
            textview_grant_manage_app_all_files_access_permission_notes.setVisibility(View.VISIBLE);
            adjustOutputMessagesHeight();
        }
        else {
            button_grant_manage_app_all_files_access_permission.setVisibility(View.GONE);
            textview_grant_manage_app_all_files_access_permission_notes.setVisibility(View.GONE);
            adjustOutputMessagesHeight();
        }

        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayOptions(ActionBar.DISPLAY_SHOW_CUSTOM);
            getSupportActionBar().setCustomView(R.layout.actionbar_layout);
        }

        cancelFilePath = getApplicationContext().getExternalFilesDir(null) + File.separator + "cancel.txt";
        File f = new File(cancelFilePath);
        if (f.exists() && f.delete()) {
            Log.d("onCreate", f + " deleted");
        }

        textview_currentFilePathProceed.setHint("");
        textview_progress.setHint("");
        textview_percentage.setHint("");
        textview_time.setHint("");
        hideProgressBar();

        spinner_src_languages.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                src_language = spinner_src_languages.getSelectedItem().toString();
                src_code = map_src_country.get(src_language);
            }
            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {
                src_language = spinner_src_languages.getSelectedItem().toString();
                src_code = map_src_country.get(src_language);
            }
        });

        spinner_dst_languages.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                dst_language = spinner_dst_languages.getSelectedItem().toString();
                dst_code = map_dst_country.get(dst_language);
            }
            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {
                dst_language = spinner_dst_languages.getSelectedItem().toString();
                dst_code = map_dst_country.get(dst_language);
            }
        });

        checkbox_create_translation.setOnClickListener(view -> {
            if(((CompoundButton) view).isChecked()){
                textview_text2.setVisibility(View.VISIBLE);
                spinner_dst_languages.setVisibility(View.VISIBLE);
                adjustOutputMessagesHeight();
                spinner_dst_languages.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
                    @Override
                    public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                        src_language = spinner_src_languages.getSelectedItem().toString();
                        dst_language = spinner_dst_languages.getSelectedItem().toString();
                        src_code = map_src_country.get(src_language);
                        dst_code = map_dst_country.get(dst_language);
                    }
                    @Override
                    public void onNothingSelected(AdapterView<?> adapterView) {
                        src_language = spinner_src_languages.getSelectedItem().toString();
                        dst_language = spinner_dst_languages.getSelectedItem().toString();
                        src_code = map_src_country.get(src_language);
                        dst_code = map_dst_country.get(dst_language);
                    }
                });
            }
            else {
                textview_text2.setVisibility(View.GONE);
                spinner_dst_languages.setVisibility(View.GONE);
                adjustOutputMessagesHeight();

                dst_language = src_language;
                spinner_dst_languages.setSelection(arraylist_dst_languages.indexOf(dst_language));
                dst_code = map_dst_country.get(dst_language);
            }
        });

        spinner_subtitle_format.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                subtitleFormat = spinner_subtitle_format.getSelectedItem().toString();
            }
            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {
                subtitleFormat = spinner_subtitle_format.getSelectedItem().toString();
            }
        });

        button_browse.setOnClickListener(view -> {
            setText(textview_output_messages, "");
            runOnUiThread(() -> {
                textview_output_messages.setGravity(Gravity.START);
                textview_output_messages.scrollTo(0,0);
            });
            selectedFilesUri = null;
            selectedFilesUri = new ArrayList<>();
            selectedFilesPath = null;
            selectedFilesPath = new ArrayList<>();
            selectedFilesDisplayName = null;
            selectedFilesDisplayName = new ArrayList<>();
            tmpSubtitleFilesPath = null;
            tmpSubtitleFilesPath = new ArrayList<>();
            tmpTranslatedSubtitleFilesPath = null;
            tmpTranslatedSubtitleFilesPath = new ArrayList<>();
            Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
            String[] mimeTypes = {"video/*", "audio/*"};
            intent.setType("*/*");
            intent.putExtra(Intent.EXTRA_MIME_TYPES, mimeTypes);
            intent.addFlags(
                    Intent.FLAG_GRANT_READ_URI_PERMISSION
                            | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                            | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION
                            | Intent.FLAG_GRANT_PREFIX_URI_PERMISSION);
            startForBrowseFileActivity.launch(intent);
        });

        button_grant_storage_permission.setOnClickListener(view -> {
            if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, STORAGE_PERMISSION_CODE);
            }
        });

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            button_grant_manage_app_all_files_access_permission.setOnClickListener(view -> {
                if (!Environment.isExternalStorageManager()) {
                    try {
                        Uri uri = Uri.parse("package:${BuildConfig.LIBRARY_PACKAGE_NAME}");
                        Intent intent = new Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION, uri);
                        //Intent intent = new Intent(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION, uri);
                        intent.addCategory("android.intent.category.DEFAULT");
                        intent.setData(Uri.parse(String.format("package:%s", getApplicationContext().getPackageName())));
                        //startActivity(intent);
                        startForRequestManageAppAllFileAccessPermissionActivity.launch(intent);
                    } catch (Exception e) {
                        Log.e("Exception: ", Objects.requireNonNull(e.getMessage()));
                        e.printStackTrace();
                        Intent intent = new Intent();
                        intent.setAction(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION);
                        startActivity(intent);
                    }
                }
            });
        }

        button_grant_persisted_tree_uri_permission.setOnClickListener(view -> {
            savedTreesUri = loadSavedTreeUrisFromSharedPreference();
            Log.d("onCreated", "savedTreesUri.size() = " + savedTreesUri.size());
            for (int i=0; i<savedTreesUri.size(); i++) {
                Log.d("onCreated", "savedTreesUri.get(" + i + ") = " + savedTreesUri.get(i));
            }
            requestTreeUriPermissions();
        });

        button_start.setOnClickListener(view -> {
            if (threadTranscriber != null) {
                threadTranscriber.interrupt();
                threadTranscriber = null;
            }

            cancelFilePath = getApplicationContext().getExternalFilesDir(null) + File.separator + "cancel.txt";
            if (new File(cancelFilePath).exists() && new File(cancelFilePath).delete()) {
                Log.d("onCreate", new File(cancelFilePath).getName() + " deleted");
            }

            if (selectedFilesUri != null) isTranscribing = !isTranscribing;

            if (isTranscribing && selectedFilesUri != null) {
                transcribeStartTime = System.currentTimeMillis();
                Log.d("transcribe", "transcribeStartTime = " + transcribeStartTime);
                runOnUiThread(() -> {
                    String t = "Cancel";
                    button_start.setText(t);
                    if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
                        transcribe();
                    }
                    else {
                        if (threadTranscriber != null) {
                            threadTranscriber.interrupt();
                            threadTranscriber = null;
                        }
                        isTranscribing = false;
                        runOnUiThread(() -> {
                            String t1 = "Start Transcribe";
                            button_start.setText(t1);
                            setText(textview_output_messages, "Storage permission is not granted, this app won't work");
                        });
                    }
                });
            }
            else if (!isTranscribing && selectedFilesUri != null) {
                showConfirmationDialogue();
            }
            else if (!isTranscribing && selectedFilesUri == null) {
                if (threadTranscriber != null) {
                    threadTranscriber.interrupt();
                    threadTranscriber = null;
                }
                isTranscribing = false;
                runOnUiThread(() -> {
                    String t1 = "Start Transcribe";
                    button_start.setText(t1);
                    String m = "Please select at least 1 video/audio file\n";
                    textview_output_messages.setText(m);
                });
            }

        });


        // ASK WRITE PERMISSION
        if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, STORAGE_PERMISSION_CODE);
        }

        savedTreesUri = loadSavedTreeUrisFromSharedPreference();
        Log.d("onCreated", "savedTreesUri.size() = " + savedTreesUri.size());
        for (int i=0; i<savedTreesUri.size(); i++) {
            Log.d("onCreated", "savedTreesUri.get(" + i + ") = " + savedTreesUri.get(i));
        }
        if (savedTreesUri.size() == 0) {
            requestTreeUriPermissions();
        }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            if (!Environment.isExternalStorageManager()) {
                try {
                    Uri uri = Uri.parse("package:${BuildConfig.LIBRARY_PACKAGE_NAME}");
                    Intent intent = new Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION, uri);
                    intent.addCategory("android.intent.category.DEFAULT");
                    intent.setData(Uri.parse(String.format("package:%s", getApplicationContext().getPackageName())));
                    startForRequestManageAppAllFileAccessPermissionActivity.launch(intent);
                } catch (Exception e) {
                    Log.e("Exception: ", Objects.requireNonNull(e.getMessage()));
                    e.printStackTrace();
                    Intent intent = new Intent();
                    intent.setAction(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION);
                    startActivity(intent);
                }
            }
        }


        // REMOVE BUTTONS IF PERMISSIONS HAVE ALREADY GRANTED BECAUSE THERE'S NO ANY WAY TO REVOKE PERMISSION PROGRAMMATICALLY
        if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
            button_grant_storage_permission.setVisibility(View.GONE);
            textview_grant_storage_permission_notes.setVisibility(View.GONE);
            adjustOutputMessagesHeight();
        }
        else {
            button_grant_storage_permission.setVisibility(View.VISIBLE);
            textview_grant_storage_permission_notes.setVisibility(View.VISIBLE);
            adjustOutputMessagesHeight();
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            if (Environment.isExternalStorageManager()) {
                button_grant_manage_app_all_files_access_permission.setVisibility(View.GONE);
                textview_grant_manage_app_all_files_access_permission_notes.setVisibility(View.GONE);
                adjustOutputMessagesHeight();
            }
            else {
                button_grant_manage_app_all_files_access_permission.setVisibility(View.VISIBLE);
                textview_grant_manage_app_all_files_access_permission_notes.setVisibility(View.VISIBLE);
                adjustOutputMessagesHeight();
            }
        }
        savedTreesUri = loadSavedTreeUrisFromSharedPreference();
        Log.d("onCreated", "savedTreesUri.size() = " + savedTreesUri.size());
        for (int i=0; i<savedTreesUri.size(); i++) {
            Log.d("onCreated", "savedTreesUri.get(" + i + ") = " + savedTreesUri.get(i));
        }

        if (!isInternetAvailable()) {
            setText(textview_output_messages, "It seems that you're not connected to internet, this app won't work without internet connection.");
        }

        adjustOutputMessagesHeight();

        textview_output_messages.post(() -> {
            equals = StringUtils.repeat('=', 80);
            maxChars = (calculateMaxCharsInTextView(equals, textview_output_messages.getWidth(), (int) textview_output_messages.getTextSize()));
            Log.d("onCreate", "textview_output_messages.getWidth() = " + textview_output_messages.getWidth());
            Log.d("onCreate", "textview_output_messages.getTextSize() = " + textview_output_messages.getTextSize());
            Log.d("onCreate", "maxChars = " + maxChars);
            equals = StringUtils.repeat('=', maxChars - 2);
        });

        try {
            Class.forName("dalvik.system.CloseGuard")
                    .getMethod("setEnabled", boolean.class)
                    .invoke(null, true);
        } catch (ReflectiveOperationException e) {
            throw new RuntimeException(e);
        }

    }


    @Override
    public void onBackPressed() {
        if (isTranscribing) {
            showConfirmationDialogue();
        }
        else {
            finish();
        }
    }


    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == STORAGE_PERMISSION_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Log.v("onRequestPermissionsResult","Permission: " + permissions[0] + " was "+ grantResults[0]);

                button_grant_storage_permission.setVisibility(View.GONE);
                textview_grant_storage_permission_notes.setVisibility(View.GONE);
                adjustOutputMessagesHeight();
                setText(textview_output_messages, "Storage permission is granted\n");

                savedTreesUri = loadSavedTreeUrisFromSharedPreference();
                Log.d("onRequestPermissionsResult", "savedTreesUri.size() = " + savedTreesUri.size());
                if (savedTreesUri.size() > 0) {
                    appendText(textview_output_messages, "Persisted tree uri permission is granted for folders :\n");
                    for (int i=0; i<savedTreesUri.size(); i++) {
                        appendText(textview_output_messages, savedTreesUri.get(i).toString() + "\n");
                        Log.d("onRequestPermissionsResult", "savedTreesUri.get(" + i + ") = " + savedTreesUri.get(i));
                    }
                    if (selectedFilesPath != null && selectedFilesPath.size()>0) {
                        if (isTreeUriPermissionGrantedForDirPathOfFilePath(selectedFilesPath.get(0))) {
                            setText(textview_output_messages, "Persisted tree uri permission is granted for :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                            appendText(textview_output_messages, "All subtitle files will be saved into :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                        }
                        else {
                            setText(textview_output_messages, "Persisted tree uri permission request is not granted for " + new File(selectedFilesPath.get(0)).getParent() + "\n");
                            appendText(textview_output_messages, "All subtitle files will be saved into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator);
                        }
                    }
                    else {
                        appendText(textview_output_messages, "All subtitle files will be saved into your selected folder.");
                    }
                }
                else {
                    appendText(textview_output_messages, "Persisted tree uri permission is not granted for any folders\n");
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                        if (Environment.isExternalStorageManager()) {
                            button_grant_manage_app_all_files_access_permission.setVisibility(View.GONE);
                            textview_grant_manage_app_all_files_access_permission_notes.setVisibility(View.GONE);
                            adjustOutputMessagesHeight();
                            appendText(textview_output_messages, "Manage app all files access permission is granted.\n");
                            appendText(textview_output_messages, "All subtitle files will be saved into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + "/com.android.autosrt/");
                        }
                        else {
                            button_grant_manage_app_all_files_access_permission.setVisibility(View.VISIBLE);
                            textview_grant_manage_app_all_files_access_permission_notes.setVisibility(View.VISIBLE);
                            appendText(textview_output_messages, "Manage app all files access permission is not granted.\n");
                            appendText(textview_output_messages, "All subtitle files will always be saved as new files into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + "/com.android.autosrt/");
                        }
                    }
                    else {
                        button_grant_manage_app_all_files_access_permission.setVisibility(View.GONE);
                        textview_grant_manage_app_all_files_access_permission_notes.setVisibility(View.GONE);
                        adjustOutputMessagesHeight();
                        appendText(textview_output_messages, "All subtitle files will be saved into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + "/com.android.autosrt/");
                    }
                }
            }
            else {
                button_grant_storage_permission.setVisibility(View.VISIBLE);
                textview_grant_storage_permission_notes.setVisibility(View.VISIBLE);
                setText(textview_output_messages, "Storage permission is not granted, this app won't work.");
            }
            //Toast.makeText(MainActivity.this, m1 + m2 + m3, Toast.LENGTH_SHORT).show();
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


    ActivityResultLauncher<Intent> startForRequestManageAppAllFileAccessPermissionActivity = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            new ActivityResultCallback<ActivityResult>() {
                @Override
                public void onActivityResult(ActivityResult result) {
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                        if (Environment.isExternalStorageManager()) {
                            button_grant_manage_app_all_files_access_permission.setVisibility(View.GONE);
                            textview_grant_manage_app_all_files_access_permission_notes.setVisibility(View.GONE);
                            adjustOutputMessagesHeight();
                            setText(textview_output_messages, "Manage app all files access permission is granted.\n");

                            if (ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
                                button_grant_storage_permission.setVisibility(View.GONE);
                                textview_grant_storage_permission_notes.setVisibility(View.GONE);
                                adjustOutputMessagesHeight();
                                appendText(textview_output_messages, "Storage permission is granted.\n");

                                savedTreesUri = loadSavedTreeUrisFromSharedPreference();
                                Log.d("startForRequestManageAppAllFileAccessPermissionActivity", "savedTreesUri.size() = " + savedTreesUri.size());
                                if (savedTreesUri.size() > 0) {
                                    appendText(textview_output_messages, "Persisted tree uri permission is granted for folders :\n");
                                    for (int i=0; i<savedTreesUri.size(); i++) {
                                        appendText(textview_output_messages, savedTreesUri.get(i).toString() + "\n");
                                        Log.d("startForRequestManageAppAllFileAccessPermissionActivity", "savedTreesUri.get(" + i + ") = " + savedTreesUri.get(i));
                                    }
                                    if (selectedFilesPath.size()>0) {
                                        if (isTreeUriPermissionGrantedForDirPathOfFilePath(selectedFilesPath.get(0))) {
                                            setText(textview_output_messages, "Persisted tree uri permission is granted for :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                            appendText(textview_output_messages, "All subtitle files will be saved into :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                        }
                                        else {
                                            setText(textview_output_messages, "Persisted tree uri permission request is not granted for " + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                            appendText(textview_output_messages, "All subtitle files will always be saved as new files into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator);
                                        }
                                    }
                                    else {
                                        appendText(textview_output_messages, "All subtitle files will be saved into your selected folder.");
                                    }

                                }
                                else {
                                    appendText(textview_output_messages, "Persisted tree uri permission is not granted for any folder");
                                    appendText(textview_output_messages, "All subtitle files will be saved into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator);
                                }
                            }
                            else {
                                button_grant_storage_permission.setVisibility(View.VISIBLE);
                                textview_grant_storage_permission_notes.setVisibility(View.VISIBLE);
                                setText(textview_output_messages, "Storage permission is not granted, this app won't work.");
                            }
                        }
                        else {
                            button_grant_manage_app_all_files_access_permission.setVisibility(View.VISIBLE);
                            textview_grant_manage_app_all_files_access_permission_notes.setVisibility(View.VISIBLE);
                            setText(textview_output_messages, "Manage all files permission is not granted.\n");

                            if (ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
                                button_grant_storage_permission.setVisibility(View.GONE);
                                textview_grant_storage_permission_notes.setVisibility(View.GONE);
                                adjustOutputMessagesHeight();
                                appendText(textview_output_messages, "Storage permission is granted.\n");

                                savedTreesUri = loadSavedTreeUrisFromSharedPreference();
                                Log.d("startForRequestManageAppAllFileAccessPermissionActivity", "savedTreesUri.size() = " + savedTreesUri.size());
                                if (savedTreesUri.size() > 0) {
                                    appendText(textview_output_messages, "Persisted tree uri permission is granted for folders :\n");
                                    for (int i=0; i<savedTreesUri.size(); i++) {
                                        appendText(textview_output_messages, savedTreesUri.get(i).toString() + "\n");
                                        Log.d("startForRequestManageAppAllFileAccessPermissionActivity", "savedTreesUri.get(" + i + ") = " + savedTreesUri.get(i));
                                    }
                                    if (selectedFilesPath != null && selectedFilesPath.size()>0) {
                                        if (isTreeUriPermissionGrantedForDirPathOfFilePath(selectedFilesPath.get(0))) {
                                            setText(textview_output_messages, "Persisted tree uri permission is granted for :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                            appendText(textview_output_messages, "All subtitle files will be saved into :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                        }
                                        else {
                                            setText(textview_output_messages, "Persisted tree uri permission request is not granted for " + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                            appendText(textview_output_messages, "All subtitle files will always be saved as new files into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator);
                                        }
                                    }
                                    else {
                                        appendText(textview_output_messages, "All subtitle files will be saved into your selected folder.");
                                    }
                                }
                                else {
                                    appendText(textview_output_messages, "Persisted tree uri permission is not granted for any folder");
                                    appendText(textview_output_messages, "All subtitle files will always be saved as new files into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + "/com.android.autosrt/");
                                }
                            }
                            else {
                                button_grant_storage_permission.setVisibility(View.VISIBLE);
                                textview_grant_storage_permission_notes.setVisibility(View.VISIBLE);
                                setText(textview_output_messages, "Storage permission is not granted, this app won't work");
                            }
                        }
                    }
                }
            });


    ActivityResultLauncher<Intent> startForRequestPersistedTreeUriPermissionActivity = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            new ActivityResultCallback<ActivityResult>() {
                @Override
                public void onActivityResult(ActivityResult result) {
                    if (result.getResultCode() == Activity.RESULT_OK) {
                        Uri treeUri;
                        Intent intent = result.getData();
                        if (intent != null) {
                            treeUri = intent.getData();

                            if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
                                button_grant_storage_permission.setVisibility(View.GONE);
                                textview_grant_storage_permission_notes.setVisibility(View.GONE);
                                adjustOutputMessagesHeight();
                                setText(textview_output_messages, "Storage permission is granted.\n");

                                appendText(textview_output_messages, "Persisted tree uri permission is granted for :\n" + TreeUri2Path(treeUri) + "\n");
                                DocumentFile dfSelectedDir = DocumentFile.fromTreeUri(MainActivity.this, treeUri);
                                DocumentFile dfFile;
                                if (dfSelectedDir != null) {
                                    dfFile = dfSelectedDir.createFile("*/*", "test.txt");
                                    if (dfFile != null && dfFile.canWrite()) {
                                        Uri uriFile = dfFile.getUri();
                                        Log.d("startForRequestPersistedTreeUriPermissionActivity", "uriFile = " + uriFile);
                                        try {
                                            testWrite(uriFile);
                                            if (dfFile.exists() && dfFile.delete()) {
                                                appendText(textview_output_messages, "Write test succeed\n");
                                                appendText(textview_output_messages, "All subtitle files will be saved into :\n" + TreeUri2Path(treeUri));
                                            }
                                        } catch (FileNotFoundException e) {
                                            throw new RuntimeException(e);
                                        }
                                    } else {
                                        Log.d("startForRequestPersistedTreeUriPermissionActivity", "File is not exist or cannot write dfFile");
                                        setText(textview_output_messages, "Write test error!");
                                    }
                                }

                                savedTreesUri = loadSavedTreeUrisFromSharedPreference();
                                boolean alreadySaved = false;
                                for (int i = 0; i < savedTreesUri.size(); i++) {
                                    Log.d("startForRequestPersistedTreeUriPermissionActivity", "savedTreesUri.get(i) = " + savedTreesUri.get(i));
                                    if (savedTreesUri.get(i) == treeUri) {
                                        alreadySaved = true;
                                        Log.d("startForRequestPersistedTreeUriPermissionActivity", "alreadySaved = true");
                                    }
                                }
                                if (!alreadySaved) {
                                    int takeFlags = Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION;
                                    getContentResolver().takePersistableUriPermission(treeUri, takeFlags);
                                    savedTreesUri.add(treeUri);
                                    Log.d("startForRequestPersistedTreeUriPermissionActivity", "alreadySaved = false -> saveTreeUrisToSharedPreference");
                                    saveTreeUrisToSharedPreference(savedTreesUri);
                                }
                            }
                            else {
                                button_grant_storage_permission.setVisibility(View.VISIBLE);
                                textview_grant_storage_permission_notes.setVisibility(View.VISIBLE);
                                setText(textview_output_messages, "Storage permission is not granted, this app won't work");
                                ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, STORAGE_PERMISSION_CODE);
                            }
                        }
                    }
                    else {
                        Log.d("startForRequestPersistedTreeUriPermissionActivity", "result.getResultCode() != Activity.RESULT_OK");
                    }
                }
            });


    ActivityResultLauncher<Intent> startForBrowseFileActivity = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            new ActivityResultCallback<ActivityResult>() {
                @Override
                public void onActivityResult(ActivityResult result) {
                    if (result.getResultCode() == Activity.RESULT_OK) {
                        Intent intent = result.getData();
                        ClipData cd;
                        selectedFilesUri.clear();
                        selectedFilesPath.clear();
                        selectedFilesDisplayName.clear();
                        selectedFolderPath = null;
                        selectedFolderUri = null;

                        // USER SELECT MULTIPLE FILES
                        if (intent != null && intent.getClipData() != null) {
                            Log.d("startForBrowseFileActivity", "intent != null && intent.getClipData() != null");
                            cd = intent.getClipData();

                            for (int i=0; i<cd.getItemCount(); i++) {
                                Uri fileUri = cd.getItemAt(i).getUri();
                                selectedFilesUri.add(fileUri);
                                String filePath = Uri2Path(getApplicationContext(), fileUri);
                                selectedFilesPath.add(filePath);
                                String fileDisplayName = queryName(getApplicationContext(), fileUri);
                                //String fileDisplayName = FilenameUtils.getName(tmpSubtitleFilePath);
                                selectedFilesDisplayName.add(fileDisplayName);
                                selectedFolderPath = new File(selectedFilesPath.get(i)).getParent();

                                boolean alreadySaved = isTreeUriPermissionGrantedForDirPathOfFilePath(selectedFilesPath.get(i));
                                if (!alreadySaved) {
                                    Log.d("startForBrowseFileActivity", "alreadySaved = false -> requestTreeUriPermissions()");
                                    button_grant_persisted_tree_uri_permission.setVisibility(View.VISIBLE);
                                    setText(textview_output_messages, "Folder " + selectedFolderPath + " has not been granted yet for persisted tree uri permission.\n");
                                    if (i==0) requestTreeUriPermissions();
                                }
                                else {
                                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                                        if (Environment.isExternalStorageManager()) {
                                            button_grant_manage_app_all_files_access_permission.setVisibility(View.GONE);
                                            textview_grant_manage_app_all_files_access_permission_notes.setVisibility(View.GONE);
                                            adjustOutputMessagesHeight();
                                            appendText(textview_output_messages, "Manage app all files access permission is granted.\n");

                                            if (ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
                                                button_grant_storage_permission.setVisibility(View.GONE);
                                                textview_grant_storage_permission_notes.setVisibility(View.GONE);
                                                adjustOutputMessagesHeight();
                                                setText(textview_output_messages, "Storage permission is granted.\n");

                                                if (isTreeUriPermissionGrantedForDirPathOfFilePath(selectedFilesPath.get(0))) {
                                                    setText(textview_output_messages, "Persisted tree uri permission is granted for :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                                    appendText(textview_output_messages, "All subtitle files will be saved into :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                                } else {
                                                    setText(textview_output_messages, "Persisted tree uri permission request has not been granted yet for " + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                                    appendText(textview_output_messages, "All subtitle files will always be saved as new files into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator);
                                                }
                                            } else {
                                                ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, STORAGE_PERMISSION_CODE);
                                                requestTreeUriPermissions();
                                                setText(textview_output_messages, "Storage permission is not granted, this app won't work");
                                            }
                                        }
                                        else {
                                            button_grant_manage_app_all_files_access_permission.setVisibility(View.VISIBLE);
                                            textview_grant_manage_app_all_files_access_permission_notes.setVisibility(View.VISIBLE);
                                            appendText(textview_output_messages, "Manage app all files access permission is not granted.\n");

                                            if (ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
                                                button_grant_storage_permission.setVisibility(View.GONE);
                                                textview_grant_storage_permission_notes.setVisibility(View.GONE);
                                                adjustOutputMessagesHeight();
                                                setText(textview_output_messages, "Storage permission is granted.\n");

                                                if (isTreeUriPermissionGrantedForDirPathOfFilePath(selectedFilesPath.get(0))) {
                                                    setText(textview_output_messages, "Persisted tree uri permission is granted for :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                                    appendText(textview_output_messages, "All subtitle files will be saved into :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                                } else {
                                                    setText(textview_output_messages, "Persisted tree uri permission request has not been granted yet for " + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                                    appendText(textview_output_messages, "All subtitle files will always be saved as new files into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + "/com.android.autosrt/");
                                                }
                                            } else {
                                                ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, STORAGE_PERMISSION_CODE);
                                                if (i==0) requestTreeUriPermissions();
                                                setText(textview_output_messages, "Storage permission is not granted, this app won't work");
                                            }
                                        }
                                    }
                                    else {
                                        if (ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
                                            button_grant_storage_permission.setVisibility(View.GONE);
                                            textview_grant_storage_permission_notes.setVisibility(View.GONE);
                                            adjustOutputMessagesHeight();
                                            setText(textview_output_messages, "Storage permission is granted.\n");
                                            if (isTreeUriPermissionGrantedForDirPathOfFilePath(selectedFilesPath.get(0))) {
                                                setText(textview_output_messages, "Persisted tree uri permission is granted for :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                                appendText(textview_output_messages, "All subtitle files will be saved into :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                            } else {
                                                setText(textview_output_messages, "Persisted tree uri permission request has not been granted yet for " + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                                appendText(textview_output_messages, "All subtitle files will always be saved as new files into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator);
                                            }
                                        } else {
                                            ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, STORAGE_PERMISSION_CODE);
                                            if (i==0) requestTreeUriPermissions();
                                            setText(textview_output_messages, "Storage permission is not granted, this app won't work");
                                        }
                                    }
                                }
                            }

                            runOnUiThread(() -> {
                                textview_filePath.setText("");
                                for (int i = 0; i < selectedFilesUri.size(); i++) {
                                    String t2 = selectedFilesPath.get(i);
                                    textview_filePath.append(t2 + "\n");
                                }
                            });

                        }

                        // USER SELECTS ONLY 1 SINGLE FILE
                        if (intent !=null && intent.getClipData() == null) {
                            Log.d("startForBrowseFileActivity", "intent !=null && intent.getClipData() == null");
                            Uri fileUri = intent.getData();
                            selectedFilesUri.add(fileUri);
                            String selectedFilePath = Uri2Path(getApplicationContext(), fileUri);
                            selectedFilesPath.add(selectedFilePath);
                            String fileDisplayName = queryName(getApplicationContext(), fileUri);
                            selectedFilesDisplayName.add(fileDisplayName);
                            selectedFolderPath = new File(selectedFilePath).getParent();

                            boolean alreadySaved = isTreeUriPermissionGrantedForDirPathOfFilePath(selectedFilePath);
                            if (!alreadySaved) {
                                Log.d("startForBrowseFileActivity", "alreadySaved = false -> requestTreeUriPermissions()");
                                requestTreeUriPermissions();
                            }

                            else {
                                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                                    if (Environment.isExternalStorageManager()) {
                                        button_grant_manage_app_all_files_access_permission.setVisibility(View.GONE);
                                        textview_grant_manage_app_all_files_access_permission_notes.setVisibility(View.GONE);
                                        adjustOutputMessagesHeight();
                                        appendText(textview_output_messages, "Manage app all files access permission is granted.\n");
                                        if (ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
                                            if (isTreeUriPermissionGrantedForDirPathOfFilePath(selectedFilesPath.get(0))) {
                                                setText(textview_output_messages, "Persisted tree uri permission is granted for :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                                appendText(textview_output_messages, "All subtitle files will be saved into :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                            } else {
                                                setText(textview_output_messages, "Persisted tree uri permission request is not granted for " + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                                appendText(textview_output_messages, "All subtitle files will always be saved as new files into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator);
                                            }
                                        }
                                        else {
                                            ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, STORAGE_PERMISSION_CODE);
                                            requestTreeUriPermissions();
                                            setText(textview_output_messages, "Storage permission is not granted, this app won't work");
                                        }
                                    }
                                    else {
                                        if (ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
                                            if (isTreeUriPermissionGrantedForDirPathOfFilePath(selectedFilesPath.get(0))) {
                                                setText(textview_output_messages, "Persisted tree uri permission is granted for :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                                appendText(textview_output_messages, "All subtitle files will always be saved as new files into " + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                            } else {
                                                setText(textview_output_messages, "Persisted tree uri permission request is not granted for " + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                                appendText(textview_output_messages, "All subtitle files will always be saved as new files into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator);
                                            }
                                        }
                                        else {
                                            ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, STORAGE_PERMISSION_CODE);
                                            requestTreeUriPermissions();
                                            setText(textview_output_messages, "Storage permission is not granted, this app won't work");
                                        }
                                    }
                                }
                                else {
                                    if (ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
                                        if (isTreeUriPermissionGrantedForDirPathOfFilePath(selectedFilesPath.get(0))) {
                                            setText(textview_output_messages, "Persisted tree uri permission is granted for :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                            appendText(textview_output_messages, "All subtitle files will be saved into :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                        } else {
                                            setText(textview_output_messages, "Persisted tree uri permission request is not granted for " + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                            appendText(textview_output_messages, "All subtitle files will be saved into :\n" + Environment.getExternalStoragePublicDirectory(DIRECTORY_DOCUMENTS).toString() + ".");
                                        }
                                    }
                                    else {
                                        ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, STORAGE_PERMISSION_CODE);
                                        requestTreeUriPermissions();
                                        setText(textview_output_messages, "Storage permission is not granted, this app won't work");
                                    }
                                }
                            }

                            runOnUiThread(() -> {
                                textview_filePath.setText("");
                                for (int i = 0; i < selectedFilesUri.size(); i++) {
                                    String t2 = selectedFilesPath.get(i);
                                    textview_filePath.append(t2 + "\n");
                                }
                            });
                        }
                        else if (intent == null) {
                            runOnUiThread(() -> {
                                String msg = "Please select at least 1 video/audio file";
                                textview_output_messages.setText(msg);
                            });
                        }
                    }
                }
            });


    @SuppressLint("DefaultLocale")
    private void transcribe() {
        setText(textview_output_messages, "");
        runOnUiThread(() -> {
            textview_output_messages.setGravity(Gravity.START);
            textview_output_messages.scrollTo(0,0);
        });

        if (threadTranscriber != null && threadTranscriber.isAlive()) threadTranscriber.interrupt();
        threadTranscriber = null;
        threadTranscriber = new Thread(() -> {
            if (Looper.myLooper() == null) {
                Looper.prepare();
            }

            if (selectedFilesUri != null) {
                if (isTranscribing) {
                    Log.d("transcribe", "Running");
                    try {
                        if (!Python.isStarted()) {
                            Python.start(new AndroidPlatform(MainActivity.this));
                            py = Python.getInstance();
                        }

                        if (selectedFilesPath == null) {
                            threadTranscriber.interrupt();
                            threadTranscriber = null;
                            setText(textview_output_messages, "");
                            transcribe();
                        }

                        savedSubtitleFile = new File[selectedFilesUri.size()];

                        for (int i=0; i<selectedFilesUri.size(); i++) {
                            if (!isTranscribing) return;

                            setText(textview_currentFilePathProceed, "Processing file : " + selectedFilesDisplayName.get(i));
                            int finalI = i;
                            textview_output_messages.post(() -> {
                                appendText(textview_output_messages, equals + "\n");
                                appendText(textview_output_messages, "Processing file : " + selectedFilesDisplayName.get(finalI) + "\n");
                                appendText(textview_output_messages, equals + "\n");
                            });

                            if (!Python.isStarted()) {
                                Python.start(new AndroidPlatform(MainActivity.this));
                                py = Python.getInstance();
                            }

                            String tmpSubtitleFilePath;
                            String tmpTranslatedSubtitleFilePath;

                            pyObjTmpSubtitleFilePath = py.getModule("autosrt").callAttr(
                                    "transcribe",
                                    src_code,
                                    dst_code,
                                    selectedFilesPath.get(i),
                                    selectedFilesDisplayName.get(i),
                                    subtitleFormat,
                                    MainActivity.this,
                                    textview_output_messages,
                                    textview_progress,
                                    progressBar,
                                    textview_percentage,
                                    textview_time
                            );

                            if (pyObjTmpSubtitleFilePath != null) {
                                tmpSubtitleFilePath = pyObjTmpSubtitleFilePath.toString();
                                tmpSubtitleFilesPath.add(tmpSubtitleFilePath);
                                tmpTranslatedSubtitleFilePath = StringUtils.substring(tmpSubtitleFilePath, 0, tmpSubtitleFilePath.length() - 4) + ".translated." + subtitleFormat;
                                tmpTranslatedSubtitleFilesPath.add(tmpTranslatedSubtitleFilePath);

                                if (new File(tmpSubtitleFilePath).exists() && new File(tmpSubtitleFilePath).length() > 1) {
                                    savedTreesUri = loadSavedTreeUrisFromSharedPreference();
                                    if (savedTreesUri.size() == 0) {

                                        Log.d("transcribe", "Saving subtitle file using saveSubtitleFileToDocumentsDir()");
                                        savedSubtitleFile[i] = saveSubtitleFileToDocumentsDir(tmpSubtitleFilePath);
                                        Log.d("transcribe", "savedSubtitleFile[" + i + "] = " + savedSubtitleFile[i]);

                                        if (savedSubtitleFile[i].exists() && savedSubtitleFile[i].length() > 1) {
                                            Log.d("transcribe", savedSubtitleFile[i] + " created");
                                            appendText(textview_output_messages, equals + "\n");
                                            appendText(textview_output_messages, "Saved subtitle files for " + selectedFilesDisplayName.get(i) + " : \n");
                                            appendText(textview_output_messages, savedSubtitleFile[i] + "\n");

                                            if (!Objects.equals(src_code, dst_code)) {
                                                String savedTranslatedSubtitleFilePath = StringUtils.replace(savedSubtitleFile[i].toString(), ".srt", ".translated.srt");
                                                Log.d("transcribe", "savedTranslatedSubtitleFilePath = " + savedTranslatedSubtitleFilePath);
                                                if (new File(savedTranslatedSubtitleFilePath).exists() && new File(savedTranslatedSubtitleFilePath).length() > 1) {
                                                    appendText(textview_output_messages, savedTranslatedSubtitleFilePath + "\n");
                                                }
                                            }
                                            appendText(textview_output_messages, equals + "\n");
                                        }

                                    }
                                    else {
                                        Log.d("transcribe", "savedTreesUri.size() = " + savedTreesUri.size());
                                        Uri dirUri = getFolderUri(selectedFolderPath);
                                        Log.d("transcribe", "dirUri = " + dirUri);

                                        int j=0;
                                        for (Uri savedTreeUri : savedTreesUri) {
                                            Log.d("transcribe", "savedTreeUri[" + j + "] = " + savedTreeUri);
                                            if (dirUri.getLastPathSegment().contains(savedTreeUri.getLastPathSegment())) {
                                                selectedFolderUri = savedTreeUri;
                                                Log.d("transcribe", "selectedFolderUri = " + selectedFolderUri);
                                            }
                                            j+=1;
                                        }

                                        boolean alreadySaved = isTreeUriPermissionGrantedForDirPathOfFilePath(selectedFilesPath.get(i));
                                        if (alreadySaved) {

                                            Log.d("transcribe", "Saving subtitle file using saveSubtitleFileToSelectedDir()");
                                            Log.d("transcribe", "selectedFolderUri = " + selectedFolderUri);
                                            savedSubtitleFile[i] = saveSubtitleFileToSelectedDir(tmpSubtitleFilePath, selectedFolderUri);

                                            if (savedSubtitleFile[i].exists() && savedSubtitleFile[i].length() > 1) {
                                                Log.d("transcribe", savedSubtitleFile[i].toString() + " created");
                                                appendText(textview_output_messages, equals + "\n");
                                                appendText(textview_output_messages, "Saved subtitle files for " + selectedFilesDisplayName.get(i) + " : \n");
                                                appendText(textview_output_messages, savedSubtitleFile[i].toString() + "\n");

                                                if (!Objects.equals(src_code, dst_code)) {
                                                    String savedTranslatedSubtitleFilePath = StringUtils.replace(savedSubtitleFile[i].toString(), ".srt", ".translated.srt");
                                                    Log.d("transcribe", "savedTranslatedSubtitleFilePath = " + savedTranslatedSubtitleFilePath);
                                                    if (new File(savedTranslatedSubtitleFilePath).exists() && new File(savedTranslatedSubtitleFilePath).length() > 1) {
                                                        appendText(textview_output_messages, savedTranslatedSubtitleFilePath + "\n");
                                                    }
                                                }
                                                appendText(textview_output_messages, equals + "\n");
                                            }

                                        }
                                        else {

                                            Log.d("transcribe", "Saving subtitle file using saveSubtitleFileToDocumentsDir()");
                                            savedSubtitleFile[i] = saveSubtitleFileToDocumentsDir(tmpSubtitleFilePath);
                                            Log.d("transcribe", "savedSubtitleFile[" + i + "] = " + savedSubtitleFile[i]);

                                            if (new File(savedSubtitleFile[i].toString()).exists() && new File(savedSubtitleFile[i].toString()).length() > 1) {
                                                Log.d("transcribe", savedSubtitleFile[i] + " created");
                                                appendText(textview_output_messages, equals + "\n");
                                                appendText(textview_output_messages, "Saved subtitle files for " + selectedFilesDisplayName.get(i) + " : \n");
                                                appendText(textview_output_messages, savedSubtitleFile[i] + "\n");

                                                if (!Objects.equals(src_code, dst_code)) {
                                                    String savedTranslatedSubtitleFilePath = StringUtils.replace(savedSubtitleFile[i].toString(), ".srt", ".translated.srt");
                                                    Log.d("transcribe", "savedTranslatedSubtitleFilePath = " + savedTranslatedSubtitleFilePath);
                                                    if (new File(savedTranslatedSubtitleFilePath).exists() && new File(savedTranslatedSubtitleFilePath).length() > 1) {
                                                        appendText(textview_output_messages, savedTranslatedSubtitleFilePath + "\n");
                                                    }
                                                }
                                                appendText(textview_output_messages, equals + "\n");
                                            }

                                        }
                                    }
                                }
                            }
                        }
                        setText(textview_currentFilePathProceed, "");

                        if (isTranscribing && selectedFilesUri != null) {
                            if (threadTranscriber != null) {
                                threadTranscriber.interrupt();
                                threadTranscriber = null;
                            }
                            isTranscribing = false;
                            runOnUiThread(() -> {
                                String t1 = "Start Transcribe";
                                button_start.setText(t1);
                                Log.d("transcribe", "transcribeStartTime = " + transcribeStartTime);
                                Log.d("transcribe", "transcribeEndTime = " + System.currentTimeMillis());
                                transcribeElapsedTime = System.currentTimeMillis() - transcribeStartTime;
                                Log.d("transcribe", "transcribeElapsedTime = " + transcribeElapsedTime);
                                long totalSeconds = transcribeElapsedTime / 1000;
                                Log.d("transcribe", "totalSeconds = " + totalSeconds);
                                long hours = totalSeconds / 3600;
                                long minutes = (totalSeconds % 3600) / 60;
                                long seconds = totalSeconds % 60;
                                formattedElapsedTime = String.format("%02d:%02d:%02d", hours, minutes, seconds);
                                appendText(textview_output_messages, "Transcribe total time : " + formattedElapsedTime + "\n");
                                appendText(textview_output_messages, equals + "\n");
                            });
                        }

                    }
                    catch (Exception e) {
                        Log.e("Exception: ", Objects.requireNonNull(e.getMessage()));
                        e.printStackTrace();
                    }

                }
                else {
                    if (threadTranscriber != null) {
                        threadTranscriber.interrupt();
                        threadTranscriber = null;
                    }
                    isTranscribing = false;
                }

            }
            else {
                if (threadTranscriber != null) {
                    threadTranscriber.interrupt();
                    threadTranscriber = null;
                }
                isTranscribing = false;
                runOnUiThread(() -> {
                    String t1 = "Start Transcribe";
                    button_start.setText(t1);
                    String m = "Please select at least 1 video/audio file\n";
                    textview_output_messages.setText(m);
                });
            }

        });
        threadTranscriber.start();
    }


    private static String queryName(Context context, Uri uri) {
        Cursor returnCursor = context.getContentResolver().query(uri, null, null, null, null);
        assert returnCursor != null;
        int nameIndex = returnCursor.getColumnIndex(OpenableColumns.DISPLAY_NAME);
        returnCursor.moveToFirst();
        String name = returnCursor.getString(nameIndex);
        returnCursor.close();
        return name;
    }


    public static Uri getFolderUri(String folderPath) {
        File folder = new File(folderPath);
        Uri uri;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            uri = DocumentsContract.buildDocumentUri(
                    "com.android.externalstorage.documents",
                    folder.getAbsolutePath().substring(1));
        } else {
            uri = Uri.fromFile(folder);
        }
        return uri;
    }


    private String TreeUri2Path(Uri uri) {
        if (uri == null) {
            return null;
        }
        String docId = DocumentsContract.getTreeDocumentId(uri);
        Log.d("TreeUri2Path", "docId = " + docId);
        String[] split = docId.split(":");
        Log.d("TreeUri2Path", "split = " + Arrays.toString(split));
        String fullPath = getPathFromExtSD(split);
        if (!fullPath.equals("")) {
            Log.d("TreeUri2Path", "fullPath = " + fullPath);
            return fullPath;
        } else {
            return null;
        }
    }


    private String Uri2Path(Context context, Uri uri) {
        if (uri == null) {
            return null;
        }

        if(ContentResolver.SCHEME_FILE.equals(uri.getScheme())) {
            Log.d("Uri2Path", "uri.getPath() = " + uri.getPath());
            return uri.getPath();
        }

        else if(ContentResolver.SCHEME_CONTENT.equals(uri.getScheme())) {
            String authority = uri.getAuthority();
            Log.d("Uri2Path", "authority = " + authority);
            String idStr = "";

            if(authority.startsWith("com.android.externalstorage")) {
                String docId = DocumentsContract.getDocumentId(uri);
                String[] split = docId.split(":");
                String fullPath = getPathFromExtSD(split);
                if (!fullPath.equals("")) {
                    Log.d("Uri2Path", "fullPath = " + fullPath);
                    return fullPath;
                } else {
                    return null;
                }
            }

            else {
                if(authority.equals("media")) {
                    idStr = uri.toString().substring(uri.toString().lastIndexOf('/') + 1);
                    Log.d("Uri2Path", "media idStr = " + idStr);
                }
                else if(authority.startsWith("com.android.providers")) {
                    idStr = DocumentsContract.getDocumentId(uri).split(":")[1];
                    Log.d("Uri2Path", "providers idStr = " + idStr);
                }

                ContentResolver contentResolver = context.getContentResolver();
                Cursor cursor = contentResolver.query(MediaStore.Files.getContentUri("external"),
                        new String[] {MediaStore.Files.FileColumns.DATA},
                        "_id=?",
                        new String[]{idStr}, null);
                if (cursor != null && cursor.getCount()>0 && cursor.moveToFirst()) {
                    cursor.moveToFirst();
                    try {
                        int idx = cursor.getColumnIndex(MediaStore.Files.FileColumns.DATA);
                        Log.d("Uri2Path", "cursor.getString(idx) = " + cursor.getString(idx));
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
        String fullPath = null;

        if ("primary".equalsIgnoreCase(type)) {
            Log.d("getPathFromExtSD", "PRIMARY");
            Log.d("getPathFromExtSD", "type = " + type);
            if (new File(Environment.getExternalStorageDirectory() + relativePath).exists()) {
                fullPath = Environment.getExternalStorageDirectory() + relativePath;
            }
        }
        // CHECK SECONDARY STORAGE
        else {
            if (new File("/storage/" + type + relativePath).exists()) {
                fullPath = "/storage/" + type + relativePath;
            }
        }
        Log.d("getPathFromExtSD", "fullPath = " + fullPath);
        return fullPath;
    }


    @SuppressLint("Recycle")
    private File saveSubtitleFileToDocumentsDir(String tmpSubtitleFilePath) {
        InputStream tmpSubtitleInputStream;
        Uri tmpSubtitleUri = Uri.fromFile(new File(tmpSubtitleFilePath));
        try {
            tmpSubtitleInputStream = getApplicationContext().getContentResolver().openInputStream(tmpSubtitleUri);
        } catch (FileNotFoundException e) {
            Log.e("FileNotFoundException: ", e.getMessage());
            e.printStackTrace();
            throw new RuntimeException(e);
        }

        String subtitleFileDisplayName = tmpSubtitleFilePath.substring(tmpSubtitleFilePath.lastIndexOf("/") + 1);
        Log.d("saveSubtitleFileToDocumentsDir", "subtitleFileDisplayName = " + subtitleFileDisplayName);
        String subtitleFolderDisplayName = StringUtils.substring(subtitleFileDisplayName, 0, subtitleFileDisplayName.length() - 4);
        String savedFolderPath = getExternalStorageDirectory() + File.separator + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator + subtitleFolderDisplayName;
        OutputStream savedSubtitleFileOutputStream;
        Uri savedSubtitleUri = null;
        Uri savedTranslatedSubtitleUri = null;

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            MainActivity.this.getActivityResultRegistry().register("key", new ActivityResultContracts.OpenDocument(), result -> MainActivity.this.getApplicationContext().getContentResolver().takePersistableUriPermission(result, Intent.FLAG_GRANT_READ_URI_PERMISSION));
            ContentValues values = new ContentValues();
            values.put(MediaStore.MediaColumns.DISPLAY_NAME, subtitleFileDisplayName); // savedFile name subtitleFileDisplayName required to contain extension savedFile mime
            values.put(MediaStore.MediaColumns.MIME_TYPE, "*/*");
            values.put(MediaStore.MediaColumns.RELATIVE_PATH, DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator + subtitleFolderDisplayName);
            Uri extVolumeUri = MediaStore.Files.getContentUri("external");
            Log.d("saveSubtitleFileToDocumentsDir", "extVolumeUri = " + extVolumeUri);

            if (Environment.isExternalStorageManager()) {
                String selection = MediaStore.MediaColumns.RELATIVE_PATH + "=?";
                String[] selectionArgs = new String[]{DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator + subtitleFolderDisplayName + File.separator};    //must include "/" in front and end
                Cursor cursor = getApplicationContext().getContentResolver().query(extVolumeUri, null, selection, selectionArgs, null);

                Log.d("saveSubtitleFileToDocumentsDir", "cursor.getCount() = " + cursor.getCount());
                if (cursor.getCount() == 0) {
                    savedSubtitleUri = getApplicationContext().getContentResolver().insert(extVolumeUri, values);
                } else {
                    while (cursor.moveToNext()) {
                        String fileName = cursor.getString(cursor.getColumnIndex(MediaStore.MediaColumns.DISPLAY_NAME));
                        Log.d("saveSubtitleFileToDocumentsDir", "fileName = " + fileName);
                        if (fileName.equals(subtitleFileDisplayName)) {
                            long id = cursor.getLong(cursor.getColumnIndex(MediaStore.MediaColumns._ID));
                            savedSubtitleUri = ContentUris.withAppendedId(extVolumeUri, id);
                            break;
                        }
                    }
                    if (savedSubtitleUri == null) {
                        savedSubtitleUri = getApplicationContext().getContentResolver().insert(extVolumeUri, values);
                    }
                }
                cursor.close();
            }
            else {
                savedSubtitleUri = getApplicationContext().getContentResolver().insert(extVolumeUri, values);                
            }
            try {
                savedSubtitleFileOutputStream = getApplicationContext().getContentResolver().openOutputStream(savedSubtitleUri);
            } catch (FileNotFoundException e) {
                Log.e("FileNotFoundException: ", e.getMessage());
                e.printStackTrace();
                throw new RuntimeException(e);
            }

        }
        else {
            File root = new File(getExternalStorageDirectory() + File.separator + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator + subtitleFolderDisplayName);
            if (!root.exists() && root.mkdirs()) {
                Log.d("saveSubtitleFileToDocumentsDir", root + " created");
            }
            File savedSubtitleFile = new File(root, subtitleFileDisplayName);
            Log.d("saveSubtitleFileToDocumentsDir", "savedSubtitleFile.getAbsolutePath() = " + savedSubtitleFile.getAbsolutePath());
            try {
                savedSubtitleFileOutputStream = new FileOutputStream(savedSubtitleFile);
            } catch (FileNotFoundException e) {
                Log.e("FileNotFoundException: ", e.getMessage());
                e.printStackTrace();
                throw new RuntimeException(e);
            }
        }

        byte[] bytes = new byte[1024];
        int length;
        while (true) {
            try {
                if (!((length = tmpSubtitleInputStream.read(bytes)) > 0)) break;
            } catch (IOException e) {
                Log.e("IOException: ", e.getMessage());
                e.printStackTrace();
                throw new RuntimeException(e);
            }
            try {
                savedSubtitleFileOutputStream.write(bytes, 0, length);
            } catch (IOException e) {
                Log.e("IOException: ", e.getMessage());
                e.printStackTrace();
                throw new RuntimeException(e);
            }
        }
        try {
            savedSubtitleFileOutputStream.close();
            tmpSubtitleInputStream.close();
        } catch (IOException e) {
            Log.e("IOException: ", e.getMessage());
            e.printStackTrace();
            throw new RuntimeException(e);
        }


        if (!Objects.equals(src_code, dst_code)) {
            InputStream tmpTranslatedSubtitleInputStream;
            String translatedSubtitleFileDisplayName = StringUtils.substring(subtitleFileDisplayName, 0, subtitleFileDisplayName.length() - 4) + ".translated." + subtitleFormat;
            String tmpTranslatedSubtitleFilePath = StringUtils.substring(tmpSubtitleFilePath, 0, tmpSubtitleFilePath.length() - 4) + ".translated." + subtitleFormat;
            Uri tmpTranslatedSubtitleUri = Uri.fromFile(new File(tmpTranslatedSubtitleFilePath));
            OutputStream savedTranslatedSubtitleFileOutputStream;

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                ContentValues savedTranslatedSubtitleValues = new ContentValues();
                savedTranslatedSubtitleValues.put(MediaStore.MediaColumns.DISPLAY_NAME, translatedSubtitleFileDisplayName); // savedFile name translatedSubtitleFileDisplayName required to contain extension savedFile mime
                savedTranslatedSubtitleValues.put(MediaStore.MediaColumns.MIME_TYPE, "*/*");
                savedTranslatedSubtitleValues.put(MediaStore.MediaColumns.RELATIVE_PATH, DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator + subtitleFolderDisplayName);
                Uri extVolumeUri = MediaStore.Files.getContentUri("external");

                if (Environment.isExternalStorageManager()) {
                    String selection = MediaStore.MediaColumns.RELATIVE_PATH + "=?";
                    String[] selectionArgs = new String[]{DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator + subtitleFolderDisplayName + File.separator};
                    @SuppressLint("Recycle")
                    Cursor cursor = getContentResolver().query(extVolumeUri, null, selection, selectionArgs, null);

                    if (cursor.getCount() == 0) {
                        savedTranslatedSubtitleUri = getApplicationContext().getContentResolver().insert(extVolumeUri, savedTranslatedSubtitleValues);
                    } else {
                        while (cursor.moveToNext()) {
                            String fileName = cursor.getString(cursor.getColumnIndex(MediaStore.MediaColumns.DISPLAY_NAME));
                            if (fileName.equals(translatedSubtitleFileDisplayName)) {
                                long id = cursor.getLong(cursor.getColumnIndex(MediaStore.MediaColumns._ID));
                                savedTranslatedSubtitleUri = ContentUris.withAppendedId(extVolumeUri, id);
                                break;
                            }
                        }
                        if (savedTranslatedSubtitleUri == null) {
                            savedTranslatedSubtitleUri = getApplicationContext().getContentResolver().insert(extVolumeUri, savedTranslatedSubtitleValues);
                        }
                    }
                    cursor.close();
                }
                else {
                    savedTranslatedSubtitleUri = getApplicationContext().getContentResolver().insert(extVolumeUri, savedTranslatedSubtitleValues);
                }
                try {
                    savedTranslatedSubtitleFileOutputStream = getApplicationContext().getContentResolver().openOutputStream(savedTranslatedSubtitleUri);
                } catch (FileNotFoundException e) {
                    Log.e("FileNotFoundException: ", e.getMessage());
                    e.printStackTrace();
                    throw new RuntimeException(e);
                }

            } else {
                File root = new File(getExternalStorageDirectory() + File.separator + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator + subtitleFolderDisplayName);
                if (!root.exists() && root.mkdirs()) {
                    Log.d("saveSubtitleFileToDocumentsDir", root + " created");
                }
                File savedTranslatedSubtitleFile = new File(root, translatedSubtitleFileDisplayName);
                Log.d("saveSubtitleFileToDocumentsDir", "savedTranslatedSubtitleFile.getAbsolutePath() = " + savedTranslatedSubtitleFile.getAbsolutePath());
                try {
                    savedTranslatedSubtitleFileOutputStream = new FileOutputStream(savedTranslatedSubtitleFile);
                } catch (FileNotFoundException e) {
                    Log.e("FileNotFoundException: ", e.getMessage());
                    e.printStackTrace();
                    throw new RuntimeException(e);
                }
            }

            try {
                tmpTranslatedSubtitleInputStream = getApplicationContext().getContentResolver().openInputStream(tmpTranslatedSubtitleUri);
            } catch (FileNotFoundException e) {
                Log.e("FileNotFoundException: ", e.getMessage());
                e.printStackTrace();
                throw new RuntimeException(e);
            }

            byte[] tmpTranslatedSubtitleBytes = new byte[1024];
            int tmpTranslatedSubtitleLength;
            while (true) {
                try {
                    if (!((tmpTranslatedSubtitleLength = tmpTranslatedSubtitleInputStream.read(tmpTranslatedSubtitleBytes)) > 0))
                        break;
                } catch (IOException e) {
                    Log.e("IOException: ", e.getMessage());
                    e.printStackTrace();
                    throw new RuntimeException(e);
                }
                try {
                    savedTranslatedSubtitleFileOutputStream.write(tmpTranslatedSubtitleBytes, 0, tmpTranslatedSubtitleLength);
                } catch (IOException e) {
                    Log.e("IOException: ", e.getMessage());
                    e.printStackTrace();
                    throw new RuntimeException(e);
                }
            }
            try {
                savedTranslatedSubtitleFileOutputStream.close();
                tmpTranslatedSubtitleInputStream.close();
            } catch (IOException e) {
                Log.e("IOException: ", e.getMessage());
                e.printStackTrace();
                throw new RuntimeException(e);
            }
        }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            return new File(Uri2Path(getApplicationContext(), savedSubtitleUri));
        }
        else {
            return new File(savedFolderPath + File.separator + subtitleFileDisplayName);
        }
    }


    @SuppressLint("Recycle")
    private File saveSubtitleFileToSelectedDir(String tmpSubtitleFilePath, Uri selectedDirUri) {
        Uri tmpSubtitleUri = Uri.fromFile(new File(tmpSubtitleFilePath));
        String tmpTranslatedSubtitleFilePath = StringUtils.substring(tmpSubtitleFilePath, 0, tmpSubtitleFilePath.length() - 4) + ".translated." + subtitleFormat;
        Uri tmpTranslatedSubtitleUri = Uri.fromFile(new File(tmpTranslatedSubtitleFilePath));

        InputStream tmpSubtitleInputStream;
        InputStream tmpTranslatedSubtitleInputStream;

        OutputStream savedSubtitleOutputStream = null;
        OutputStream savedTranslatedSubtitleOutputStream = null;

        Uri savedSubtitleUri;
        Uri savedTranslatedSubtitleUri;

        String subtitleFileDisplayName = tmpSubtitleFilePath.substring(tmpSubtitleFilePath.lastIndexOf("/") + 1);
        Log.d("saveSubtitleFileToSelectedDir", "subtitleFileDisplayName = " + subtitleFileDisplayName);
        String translatedSubtitleFileDisplayName = StringUtils.substring(subtitleFileDisplayName, 0, subtitleFileDisplayName.length() - 4) + ".translated." + subtitleFormat;
        Log.d("saveSubtitleFileToSelectedDir", "translatedSubtitleFileDisplayName = " + translatedSubtitleFileDisplayName);

        DocumentFile selectedDirDocumentFile = DocumentFile.fromTreeUri(MainActivity.this, selectedDirUri);
        DocumentFile savedSubtitleDocumentFile;
        DocumentFile savedTranslatedSubtitleDocumentFile;

        String savedSubtitleFilePath = null;

        ParcelFileDescriptor subtitleParcelFileDescriptor = null;

        try {
            tmpSubtitleInputStream = getApplicationContext().getContentResolver().openInputStream(tmpSubtitleUri);
        } catch (FileNotFoundException e) {
            Log.e("FileNotFoundException: ", e.getMessage());
            e.printStackTrace();
            throw new RuntimeException(e);
        }

        if (selectedDirDocumentFile != null) {
            if (!selectedDirDocumentFile.exists()) {
                Log.e("saveSubtitleFileToSelectedDir", selectedDirDocumentFile +  " is not exists");
                releasePermissions(selectedDirUri);
                setText(textview_output_messages, selectedDirDocumentFile + " is not exist!");
                return null;
            }
            else {
                savedSubtitleDocumentFile = selectedDirDocumentFile.findFile(subtitleFileDisplayName);
                Log.d("saveSubtitleFileToSelectedDir", "savedSubtitleDocumentFile = " + savedSubtitleDocumentFile);
                if (savedSubtitleDocumentFile == null) savedSubtitleDocumentFile = selectedDirDocumentFile.createFile("*/*", subtitleFileDisplayName);
                if (savedSubtitleDocumentFile != null && savedSubtitleDocumentFile.canWrite()) {
                    savedSubtitleUri = savedSubtitleDocumentFile.getUri();
                    Log.d("saveSubtitleFileToSelectedDir", "subtitleFile.getUri() = " + savedSubtitleDocumentFile.getUri());
                    savedSubtitleFilePath = Uri2Path(getApplicationContext(), savedSubtitleUri);
                    Log.d("saveSubtitleFileToSelectedDir", "savedSubtitleFilePath = " + savedSubtitleFilePath);
                    try {
                        subtitleParcelFileDescriptor = getContentResolver().openFileDescriptor(savedSubtitleUri, "w");
                        savedSubtitleOutputStream = new FileOutputStream(subtitleParcelFileDescriptor.getFileDescriptor());
                    } catch (FileNotFoundException e) {
                        throw new RuntimeException(e);
                    }
                }
                else {
                    Log.d("saveSubtitleFileToSelectedDir", subtitleFileDisplayName + " is not exist or cannot write");
                    setText(textview_output_messages, "Write error!");
                }
            }
        }

        byte[] bytes = new byte[1024];
        int length;
        while (true) {
            try {
                if (!((length = tmpSubtitleInputStream.read(bytes)) > 0)) break;
            } catch (IOException e) {
                Log.e("IOException: ", e.getMessage());
                e.printStackTrace();
                throw new RuntimeException(e);
            }
            try {
                if (savedSubtitleOutputStream != null) {
                    savedSubtitleOutputStream.write(bytes, 0, length);
                }
            } catch (IOException e) {
                Log.e("IOException: ", e.getMessage());
                e.printStackTrace();
                throw new RuntimeException(e);
            }

        }

        try {
            if (savedSubtitleOutputStream != null) {
                savedSubtitleOutputStream.close();
            }
            tmpSubtitleInputStream.close();
        } catch (IOException e) {
            Log.e("IOException: ", e.getMessage());
            e.printStackTrace();
            throw new RuntimeException(e);
        }

        try {
            if (subtitleParcelFileDescriptor != null) {
                subtitleParcelFileDescriptor.close();
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        ParcelFileDescriptor translatedSubtitleParcelFileDescriptor = null;

        if (!Objects.equals(src_code, dst_code)) {
            if (selectedDirDocumentFile == null || !selectedDirDocumentFile.exists()) {
                Log.e("saveSubtitleFileToSelectedDir", selectedDirDocumentFile +  " not exists");
                releasePermissions(selectedDirUri);
                setText(textview_output_messages, selectedDirDocumentFile + " not exist!");
                return null;
            }
            else {
                savedTranslatedSubtitleDocumentFile = selectedDirDocumentFile.findFile(translatedSubtitleFileDisplayName);
                if (savedTranslatedSubtitleDocumentFile == null) savedTranslatedSubtitleDocumentFile = selectedDirDocumentFile.createFile("*/*", translatedSubtitleFileDisplayName);
                if (savedTranslatedSubtitleDocumentFile != null && savedTranslatedSubtitleDocumentFile.canWrite()) {
                    savedTranslatedSubtitleUri = savedTranslatedSubtitleDocumentFile.getUri();
                    Log.d("saveSubtitleFileToSelectedDir", "savedTranslatedSubtitleDocumentFile.getUri() = " + savedTranslatedSubtitleDocumentFile.getUri());
                    String savedTranslatedSubtitleFile = Uri2Path(getApplicationContext(), savedTranslatedSubtitleUri);
                    Log.d("saveSubtitleFileToSelectedDir", "savedTranslatedSubtitleFile = " + savedTranslatedSubtitleFile);
                    try {
                        translatedSubtitleParcelFileDescriptor = getContentResolver().openFileDescriptor(savedTranslatedSubtitleUri, "w");
                        savedTranslatedSubtitleOutputStream = new FileOutputStream(translatedSubtitleParcelFileDescriptor.getFileDescriptor());
                    } catch (FileNotFoundException e) {
                        throw new RuntimeException(e);
                    }
                }
                else {
                    Log.d("saveSubtitleFileToSelectedDir", subtitleFileDisplayName + " is not exist or cannot write");
                    setText(textview_output_messages, "Write error!");
                }
            }

            try {
                tmpTranslatedSubtitleInputStream = getApplicationContext().getContentResolver().openInputStream(tmpTranslatedSubtitleUri);
            } catch (FileNotFoundException e) {
                Log.e("FileNotFoundException: ", e.getMessage());
                e.printStackTrace();
                throw new RuntimeException(e);
            }
            byte[] bytesTranslated = new byte[1024];
            int lengthTranslated;
            while (true) {
                try {
                    if (!((lengthTranslated = tmpTranslatedSubtitleInputStream.read(bytesTranslated)) > 0))
                        break;
                } catch (IOException e) {
                    Log.e("IOException: ", e.getMessage());
                    e.printStackTrace();
                    throw new RuntimeException(e);
                }
                try {
                    if (savedTranslatedSubtitleOutputStream != null) {
                        savedTranslatedSubtitleOutputStream.write(bytesTranslated, 0, lengthTranslated);
                    }
                } catch (IOException e) {
                    Log.e("IOException: ", e.getMessage());
                    e.printStackTrace();
                    throw new RuntimeException(e);
                }
            }
            try {
                if (savedTranslatedSubtitleOutputStream != null) {
                    savedTranslatedSubtitleOutputStream.close();
                }
                tmpTranslatedSubtitleInputStream.close();
            } catch (IOException e) {
                Log.e("IOException: ", e.getMessage());
                e.printStackTrace();
                throw new RuntimeException(e);
            }

            try {
                if (translatedSubtitleParcelFileDescriptor != null) {
                    translatedSubtitleParcelFileDescriptor.close();
                }
            } catch (IOException e) {
                throw new RuntimeException(e);
            }

        }

        if (savedSubtitleFilePath != null) {
            Log.d("saveSubtitleFileToSelectedDir", "Succesed! Returned savedSubtitleFilePath = " + savedSubtitleFilePath);
            return new File(savedSubtitleFilePath);
        }
        else {
            Log.d("saveSubtitleFileToSelectedDir", "Failed! Returned null!");
            return null;
        }
    }


    private void showConfirmationDialogue() {
        AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
        builder.setTitle("Confirm");
        builder.setMessage("Are you sure?");

        builder.setPositiveButton("YES", (dialog, which) -> runOnUiThread(() -> {
            String t = "Start Transcribe";
            button_start.setText(t);

            File fc = new File(cancelFilePath);
            try {
                FileWriter out = new FileWriter(fc);
                out.write("");
                Log.i("showConfirmationDialogue", "cancelFile created");
                out.close();
            } catch (IOException e) {
                Log.e("showConfirmationDialogue", e.getMessage());
                e.printStackTrace();
            }

            if (fc.exists()) {
                Log.i("showConfirmationDialogue", "cancelFile exists");
            }
            else {
                Log.i("showConfirmationDialogue", "cancelFile is not exist");
            }

            if (tmpSubtitleFilesPath != null) {
                for (int i=0; i<tmpSubtitleFilesPath.size(); i++) {
                    File sf = new File(tmpSubtitleFilesPath.get(i)).getAbsoluteFile();
                    if (sf.exists() && sf.delete()) {
                        Log.i("showConfirmationDialogue", new File(tmpSubtitleFilesPath.get(i)).getAbsoluteFile() + " deleted");
                    }
                }
            }
            if (tmpTranslatedSubtitleFilesPath != null) {
                for (int i=0; i<tmpTranslatedSubtitleFilesPath.size(); i++) {
                    File stf = new File(tmpTranslatedSubtitleFilesPath.get(i)).getAbsoluteFile();
                    if (stf.exists() && stf.delete()) {
                        Log.i("showConfirmationDialogue", new File(tmpTranslatedSubtitleFilesPath.get(i)).getAbsoluteFile() + " deleted");
                    }
                }
            }

            if (threadTranscriber != null) {
                threadTranscriber.interrupt();
                threadTranscriber = null;
            }
            isTranscribing = false;
            dialog.dismiss();
            setText(textview_output_messages, "Process has been canceled");
            hideProgressBar();
        }));

        builder.setNegativeButton("NO", (dialog, which) -> {
            // Do nothing
            dialog.dismiss();
        });

        AlertDialog alert = builder.create();
        alert.show();
    }


    private void requestTreeUriPermissions() {
        // Choose a directory using the system's file picker.
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            new AlertDialog.Builder(this)
                    .setMessage("Please select folder of your audio/video files so this app can write subtitle files on same folder")
                    .setNegativeButton("Cancel", (dialog, which) -> {
                        setText(textview_output_messages, "Persisted tree uri permission request is canceled.\n");

                        if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
                            button_grant_storage_permission.setVisibility(View.GONE);
                            textview_grant_storage_permission_notes.setVisibility(View.GONE);
                            adjustOutputMessagesHeight();
                            setText(textview_output_messages, "Storage permission is granted.\n");

                            savedTreesUri = loadSavedTreeUrisFromSharedPreference();
                            Log.d("requestTreeUriPermissions", "savedTreesUri.size() = " + savedTreesUri.size());
                            if (savedTreesUri.size() > 0) {
                                appendText(textview_output_messages, "Persisted tree uri permission is granted for folders :\n");
                                for (int i=0; i<savedTreesUri.size(); i++) {
                                    appendText(textview_output_messages, savedTreesUri.get(i).toString() + "\n");
                                    Log.d("requestTreeUriPermissions", "savedTreesUri.get(" + i + ") = " + savedTreesUri.get(i));
                                }
                                if (selectedFilesPath != null && selectedFilesPath.size()>0) {
                                    if (isTreeUriPermissionGrantedForDirPathOfFilePath(selectedFilesPath.get(0))) {
                                        setText(textview_output_messages, "Persisted tree uri permission is granted for :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                        appendText(textview_output_messages, "All subtitle files will be saved into :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                    }
                                    else {
                                        setText(textview_output_messages, "Persisted tree uri permission request is not granted for " + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                        appendText(textview_output_messages, "All subtitle files will always be saved as new files into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator);
                                    }
                                }
                                else {
                                    appendText(textview_output_messages, "All subtitle files will be saved into your selected folder.");
                                }
                            }
                            else {
                                appendText(textview_output_messages, "Persisted tree uri permission is not granted for any folders\n");
                                if (Environment.isExternalStorageManager()) {
                                    button_grant_manage_app_all_files_access_permission.setVisibility(View.GONE);
                                    textview_grant_manage_app_all_files_access_permission_notes.setVisibility(View.GONE);
                                    adjustOutputMessagesHeight();
                                    appendText(textview_output_messages, "Manage app all files access permission is granted.\n");
                                    appendText(textview_output_messages, "All subtitle files will always be saved as new files into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator);
                                }
                                else {
                                    button_grant_manage_app_all_files_access_permission.setVisibility(View.VISIBLE);
                                    textview_grant_manage_app_all_files_access_permission_notes.setVisibility(View.VISIBLE);
                                    appendText(textview_output_messages, "Manage app all files access permission is not granted.\n");
                                    appendText(textview_output_messages, "All subtitle files will always be saved as new files into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + "/com.android.autosrt/");
                                }
                            }
                        }

                        else {
                            button_grant_storage_permission.setVisibility(View.VISIBLE);
                            textview_grant_storage_permission_notes.setVisibility(View.VISIBLE);
                            setText(textview_output_messages, "Storage permission is not granted, this app won't work");
                        }
                    })
                    .setPositiveButton("Ok", (dialog, which) -> {
                        StorageManager sm = (StorageManager) getSystemService(Context.STORAGE_SERVICE);
                        Intent intent = sm.getPrimaryStorageVolume().createOpenDocumentTreeIntent();
                        String startDir = "Documents";
                        Uri uri;
                        if (intent != null) {
                            uri = intent.getParcelableExtra("android.provider.extra.INITIAL_URI");
                            String scheme;
                            if (uri != null) {
                                scheme = uri.toString().replace("/root/", "/document/");
                                scheme += "%3A" + startDir;
                                uri = Uri.parse(scheme);
                                Uri rootUri = DocumentsContract.buildDocumentUri(AUTHORITY, uri.toString());
                                sm.getPrimaryStorageVolume().createOpenDocumentTreeIntent().putExtra(EXTRA_INITIAL_URI, rootUri);

                                // Optionally, specify a URI for the directory that should be opened in
                                // the system file picker when it loads.
                                Intent intent2 = new Intent(Intent.ACTION_OPEN_DOCUMENT_TREE);
                                intent2.addFlags(
                                        Intent.FLAG_GRANT_READ_URI_PERMISSION
                                                | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                                                | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION
                                                | Intent.FLAG_GRANT_PREFIX_URI_PERMISSION);
                                intent2.putExtra(EXTRA_INITIAL_URI, rootUri);
                                //startActivity(intent2);
                                startForRequestPersistedTreeUriPermissionActivity.launch(intent2);
                            }
                        }
                    })
                    .setCancelable(false)
                    .show();
        }
        else {
            new AlertDialog.Builder(this)
                    .setMessage("Please select folder of your audio/video files so this app can write subtitle files on same folder")
                    .setNegativeButton("Cancel", (dialog, which) -> {
                        setText(textview_output_messages, "Persisted tree uri permission request is canceled.\n");

                        if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
                            button_grant_storage_permission.setVisibility(View.GONE);
                            textview_grant_storage_permission_notes.setVisibility(View.GONE);
                            adjustOutputMessagesHeight();
                            setText(textview_output_messages, "Storage permission is granted.\n");

                            savedTreesUri = loadSavedTreeUrisFromSharedPreference();
                            Log.d("requestTreeUriPermissions", "savedTreesUri.size() = " + savedTreesUri.size());
                            if (savedTreesUri.size() > 0) {
                                appendText(textview_output_messages, "Persisted tree uri permission is granted for folders :\n");
                                for (int i=0; i<savedTreesUri.size(); i++) {
                                    appendText(textview_output_messages, savedTreesUri.get(i).toString() + "\n");
                                    Log.d("requestTreeUriPermissions", "savedTreesUri.get(" + i + ") = " + savedTreesUri.get(i));
                                }
                                if (selectedFilesPath != null && selectedFilesPath.size()>0) {
                                    if (isTreeUriPermissionGrantedForDirPathOfFilePath(selectedFilesPath.get(0))) {
                                        setText(textview_output_messages, "Persisted tree uri permission is granted for :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                        appendText(textview_output_messages, "All subtitle files will be saved into :\n" + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                    }
                                    else {
                                        setText(textview_output_messages, "Persisted tree uri permission request is not granted for " + new File(selectedFilesPath.get(0)).getParent() + "\n");
                                        appendText(textview_output_messages, "All subtitle files will always be saved as new files into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator);
                                    }
                                }
                                else {
                                    appendText(textview_output_messages, "All subtitle files will be saved into your selected folder.");
                                }
                            }
                            else {
                                appendText(textview_output_messages, "Persisted tree uri permission is not granted for any folders\n");
                                appendText(textview_output_messages, "All subtitle files will be saved into :\n/storage/emulated/0/" + DIRECTORY_DOCUMENTS + File.separator + getPackageName() + File.separator);
                            }
                        }

                        else {
                            setText(textview_output_messages, "Storage permission is not granted, this app won't work");
                        }
                    })
                    .setPositiveButton("Ok", (dialog, which) -> {
                        //Intent intent = sm.getPrimaryStorageVolume().createAccessIntent(DIRECTORY_DOCUMENTS);
                        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT_TREE);
                        intent.addFlags(
                                Intent.FLAG_GRANT_READ_URI_PERMISSION
                                        | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                                        | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION
                                        | Intent.FLAG_GRANT_PREFIX_URI_PERMISSION);

                        //startActivity(intent);
                        startForRequestPersistedTreeUriPermissionActivity.launch(intent);
                    })
                    .setCancelable(false)
                    .show();
        }
    }


    @SuppressLint("Recycle")
    private void testWrite(Uri uri) throws FileNotFoundException {
        @SuppressLint("Recycle")
        ParcelFileDescriptor parcelFileDescriptor;
        parcelFileDescriptor = getContentResolver().openFileDescriptor(uri, "w");
        try (FileOutputStream fos = new FileOutputStream(parcelFileDescriptor.getFileDescriptor())) {
            long currentTimeMillis = System.currentTimeMillis();
            fos.write(("String written at " + currentTimeMillis + "\n").getBytes());
            //Log.d("testWrite", "Write test succeed");
        }
        catch (IOException e) {
            Log.e("IOException: ", e.getMessage());
            e.printStackTrace();
            throw new RuntimeException(e);
        }
        try {
            parcelFileDescriptor.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }


    private void releasePermissions(Uri uri) {
        int takeFlags = Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION;
        getContentResolver().releasePersistableUriPermission(uri,takeFlags);
    }


    private InetAddress[] checkGoogleHost() {
        final InetAddress[] ipAddr = new InetAddress[1];
        Thread netThread = new Thread(() -> {
            try {
                ipAddr[0] = InetAddress.getByName("www.google.com");
            } catch (UnknownHostException e) {
                throw new RuntimeException(e);
            }
            Log.d("isInternetAvailable", "ipAddr = " + ipAddr[0]);
        });
        netThread.start();
        return ipAddr;
    }


    private boolean isInternetAvailable() {
        try {
            InetAddress[] ipAddr = checkGoogleHost();
            return !Arrays.toString(ipAddr).equals("");
        } catch (Exception e) {
            return false;
        }
    }


    private void saveTreeUrisToSharedPreference(ArrayList<Uri> savedTreesUri) {
        SharedPreferences sp = getSharedPreferences("com.android.autosubtitle.prefs", 0);
        SharedPreferences.Editor mEdit1 = sp.edit();
        mEdit1.putInt("arrayListSize", savedTreesUri.size());
        for(int i=0;i<savedTreesUri.size();i++) {
            mEdit1.remove("arrayList_" + i);
            mEdit1.putString("arrayList_" + i, savedTreesUri.get(i).toString());
            Log.d("saveTreeUrisToSharedPreference", "arrayList_" + i + " = " + savedTreesUri.get(i).toString());
        }
        mEdit1.apply();
    }


    private ArrayList<Uri> loadSavedTreeUrisFromSharedPreference() {
        ArrayList<Uri> savedTreesUri = new ArrayList<>();
        SharedPreferences sp = getSharedPreferences("com.android.autosubtitle.prefs", 0);
        int size = sp.getInt("arrayListSize", 0);
        for(int i=0;i<size;i++) {
            Uri uri = Uri.parse(sp.getString("arrayList_" + i, null));
            savedTreesUri.add(uri);
        }
        return savedTreesUri;
    }


    private boolean isTreeUriPermissionGrantedForDirPathOfFilePath(String filePath) {
        Log.d("isTreeUriPermissionGrantedForDirPathOfFilePath", "filePath = " + filePath);
        String dirName = Objects.requireNonNull(new File(filePath).getParentFile()).getName();
        Log.d("isTreeUriPermissionGrantedForDirPathOfFilePath", "dirName = " + dirName);
        Uri dirUri = getFolderUri(dirName);

        savedTreesUri = loadSavedTreeUrisFromSharedPreference();
        if (savedTreesUri.size() > 0) {
            for (int j=0; j<savedTreesUri.size(); j++) {
                Uri savedTreeUri = Uri.parse(savedTreesUri.get(j).toString());

                Log.d("isTreeUriPermissionGrantedForFilePath", "savedTreeUri = " + savedTreeUri);
                Log.d("isTreeUriPermissionGrantedForFilePath", "savedTreeUri.getLastPathSegment() = " + savedTreeUri.getLastPathSegment());
                Log.d("isTreeUriPermissionGrantedForFilePath", "dirUri = " + dirUri);
                Log.d("isTreeUriPermissionGrantedForFilePath", "dirUri.getLastPathSegment() = " + dirUri.getLastPathSegment());

                if (savedTreeUri.getLastPathSegment().contains(dirUri.getLastPathSegment())) {
                    selectedFolderUri = savedTreeUri;
                    Log.d("isTreeUriPermissionGrantedForDirPathOfFilePath", "selectedFolderUri = " + selectedFolderUri);
                    Log.d("isTreeUriPermissionGrantedForDirPathOfFilePath", "alreadySaved = true");
                    return true;
                }
                else {
                    Log.d("isTreeUriPermissionGrantedForDirPathOfFilePath", "alreadySaved = false");
                }
            }
        }
        return false;
    }


    private void hideProgressBar() {
        runOnUiThread(() -> {
            textview_progress.setVisibility(View.INVISIBLE);
            progressBar.setVisibility(View.INVISIBLE);
            textview_percentage.setVisibility(View.INVISIBLE);
            textview_time.setVisibility(View.INVISIBLE);
        });
    }


    public int calculateMaxCharsInTextView(String text, int viewWidth, int textSize) {
        Paint paint = new Paint();
        paint.setTextSize(textSize);
        Rect bounds = new Rect();
        paint.getTextBounds(text, 0, text.length(), bounds);
        int textWidth = bounds.width();
        return (int) Math.floor((double) viewWidth / (double) textWidth * text.length());
    }


    private void adjustOutputMessagesHeight() {
        textview_output_messages.post(() -> {
            DisplayMetrics display = new DisplayMetrics();
            getWindowManager().getDefaultDisplay().getMetrics(display);
            int displayheightPixels = display.heightPixels;
            Log.d("adjustOutputMessagesHeight", "displayheightPixels = " + displayheightPixels);
            int[] location = new int[2];
            textview_output_messages.getLocationOnScreen(location);
            int top = location[1];
            Log.d("adjustOutputMessagesHeight", "top = " + top);
            int height = textview_output_messages.getHeight();
            Log.d("adjustOutputMessagesHeight", "height = " + height);
            int emptySpace = displayheightPixels - (top + height);
            Log.d("adjustOutputMessagesHeight", "emptySpace = " + emptySpace);
            int newHeight = height + emptySpace - 24;
            Log.d("adjustOutputMessagesHeight", "newHeight = " + (height + emptySpace));

            RelativeLayout.LayoutParams params = (RelativeLayout.LayoutParams) textview_output_messages.getLayoutParams();
            params.height = newHeight;
            textview_output_messages.setLayoutParams(params);
            heightOfOutputMessages = newHeight;

            int lineHeight = textview_output_messages.getLineHeight();
            maxLinesOfOutputMessages = heightOfOutputMessages / lineHeight;
            Log.d("adjustOutputMessagesHeight", "maxLinesOfOutputMessages = " + maxLinesOfOutputMessages);

        });

    }


    private void setText(final TextView tv, final String text){
        runOnUiThread(() -> tv.setText(text));
    }

    private void appendText(final TextView tv, final String text){
        runOnUiThread(() -> {
            int lines = textview_output_messages.getLineCount();
            if (lines >= maxLinesOfOutputMessages) textview_output_messages.setGravity(Gravity.BOTTOM);
            tv.append(text);
        });
    }

}
