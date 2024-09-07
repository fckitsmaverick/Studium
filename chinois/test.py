import io

filename = "cedict_ts.u8"
with io.open(filename,'r',encoding='utf8') as f:
    text = f.read()

print(text)