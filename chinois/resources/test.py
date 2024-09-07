import pandas as pd

from termcolor import cprint

df = pd.read_csv("1-1000Mandarin.csv")
dic = {}
dic = df.to_dict()
dic["Done"] = {}

for key, value in dic["Simplified"].items():
    cprint(dic["Meaning"][key], "light_magenta")
    ans = input()
    if ans == dic["Simplified"][key]:
        cprint(dic["Pinyin"][key], "green")
        cprint("Good Answer", "green")
    else:
        cprint("Wrong Answer", "light_red")
        cprint(f'{dic["Simplified"][key]} {dic["Pinyin"][key]}', "light_red")
    