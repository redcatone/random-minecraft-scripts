import os, json, csv
import translators as ts

def json_generator(language_list):
    script_dir = os.path.dirname(__file__) # get path to script
    with open(f"{script_dir}/en_us.json", "r") as main_data_file: # convert main json to python dictionary
        main_data_dict = json.loads(main_data_file.read()) # main_data_file == en_us.json

    for language in language_list:
        final_data_dict = main_data_dict.copy() # main_data_file used as base for other languages

        rel_path = f"lang/{language}.json"
        abs_file_path = os.path.join(script_dir, rel_path)

        try:
            with open(abs_file_path, "r") as f: # read old file
                _old_data_dict = json.loads(f.read())

                for key in final_data_dict:
                    if key not in _old_data_dict: # translate if not already translated
                        translated_value = translate(final_data_dict[key], language)
                        if translated_value == "No translation available":
                            continue
                        else:
                            final_data_dict[key] = translated_value
                    elif final_data_dict[key] != _old_data_dict[key]: # copy old translation if it exists
                        final_data_dict[key] = _old_data_dict[key]
        except FileNotFoundError: # if file doesn't exist, translate all
            for key in final_data_dict:
                translated_value = translate(final_data_dict[key], language)
                if translated_value == "No translation available":
                    continue
                else:
                    final_data_dict[key] = translated_value
        finally:
            with open(abs_file_path, "w") as fw:
                fw.write(json.dumps(final_data_dict, indent=4, separators=(",", ": "), sort_keys=True))
                fw.write("\n")

with open("locale_code_mc_google.csv", mode='r') as locale_codes: # create dict to convert from mc locale to google translate locale
    reader = csv.reader(locale_codes)
    mc_to_google_locale_dict = {rows[0]:rows[1] for rows in reader}

def translate(text, mc_locale):
    locale_code = mc_to_google_locale_dict[mc_locale]
    if locale_code == "":
        return "No translation available"
    else:
        translated_text = ts.google(text, from_language="en", to_language=locale_code)
        return translated_text

if __name__ == "__main__":
    # locale codes from minecraft wiki
    languages = ["af_za", "ar_sa", "ast_es", "az_az", "ba_ru", "bar", "be_by", "bg_bg", "br_fr", "brb", "bs_ba", "ca_es", "cs_cz", "cy_gb", "da_dk", "de_at", "de_ch", "de_de", "el_gr", "en_au", "en_ca", "en_gb", "en_nz", "en_pt", "en_ud", "en_us", "enp", "enws", "eo_uy", "es_ar", "es_cl", "es_ec", "es_es", "es_mx", "es_uy", "es_ve", "esan", "et_ee", "eu_es", "fa_ir", "fi_fi", "fil_ph", "fo_fo", "fr_ca", "fr_fr", "fra_de", "fy_nl", "ga_ie", "gd_gb", "gl_es", "got_de", "gv_im", "haw_us", "he_il", "hi_in", "hr_hr", "hu_hu", "hy_am", "id_id", "ig_ng", "io_en", "is_is", "isv", "it_it", "ja_jp", "jbo_en", "ka_ge", "kab_kab", "kk_kz", "kn_in", "ko_kr", "ksh", "kw_gb", "la_la", "lb_lu", "li_li", "lol_us", "lt_lt", "lv_lv", "mi_nz", "mk_mk", "mn_mn", "moh_ca", "ms_my", "mt_mt", "nb_no", "nds_de", "nl_be", "nl_nl", "nn_no", "nuk", "oc_fr", "oj_ca", "ovd", "pl_pl", "pt_br", "pt_pt", "qya_aa", "ro_ro", "ru_ru", "scn", "sk_sk", "sl_si", "sme", "so_so", "sq_al", "sr_sp", "sv_se", "swg", "sxu", "szl", "ta_in", "th_th", "tlh_aa", "tr_tr", "tt_ru", "tzl_tzl", "uk_ua", "val_es", "vec_it", "vi_vn", "yi_de", "yo_ng", "zh_cn", "zh_tw"]
    json_generator(languages)
