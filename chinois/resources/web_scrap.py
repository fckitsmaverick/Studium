import pandas as pd

from termcolor import cprint

l = ["1-1000", "1001-2000", "2001-3000", "3001-4000", "4001-5000", "5001-6000", "6001-7000", "7001-8000", "8001-9000", "9001-10000"]

for i in l:
    df = pd.read_html(f'https://en.wiktionary.org/wiki/Appendix:Mandarin_Frequency_lists/{i}')

    dic_1000 = {

    }

    # remove null values
    df_simp = df[0]["Simplified"] = df[0]["Simplified"].dropna()
    df_pin = df[0]["Pinyin"] = df[0]["Pinyin"].dropna()
    df_m = df[0]["Meaning"] = df[0]["Meaning"].dropna()

    # turn df into dictionnaries
    dic_1000["Simplified"] = df_simp.to_dict()
    dic_1000["Pinyin"] = df_pin.to_dict()
    dic_1000["Meaning"] = df_m.to_dict()

    final_dic = {
        "Simplified": dic_1000["Simplified"],
        "Pinyin": {},
        "Meaning": {}
    }

    #clear the pinyin part of inccorect values
    for key, value in dic_1000["Pinyin"].items():
        if value != "(file)":
            final_dic["Pinyin"][key] = value

    for key, value in dic_1000["Meaning"].items():
        value = value.replace(':(file)', '')
        value = value.replace(dic_1000["Pinyin"][key], "")
        final_dic["Meaning"][key] = value

    print(final_dic["Simplified"][546], final_dic["Pinyin"][546], final_dic["Meaning"][546])
    df = pd.DataFrame.from_dict(final_dic)
    df.to_csv(f"{i}Mandarin.csv")
#print(df)

#cprint(f'{final_dic["Simplified"][982]},\n{final_dic["Pinyin"][982]},\n{final_dic["Meaning"][982]}', "light_magenta")

#print(len(final_dic["Simplified"]), len(final_dic["Pinyin"]), len(final_dic["Meaning"]))

#print(df[0]["Simplified"].dropna())
#print(df[0]["Pinyin"].dropna().drop())

#print(df[0]["Simplified"][0])
#print(df[0]["Simplified"][1])


