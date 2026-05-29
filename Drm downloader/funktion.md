# Hur Drm downloader är byggd

## Innehåll

* [NPO_downloader.py](#npo_downloader)
* NPO_season_downloader.py
* [npo_widevine.py](#Npo_widevine)
* Flödesschema


## NPO_downloader

Programmet börjar med att tilldelar en download path till variabeln download_path. ```download_path = "C:\\Path\\To\\Media\\location\\"```

Programmet skriver ut frågan "Enter NPO Start Video URL Like: ['https://npo.nl/start/afspelen/de-slimste-mens_1240'] : " och sen matas in avsnitt länken av användaren som en sträng i variabeln Video url. ```video_url = input("Enter NPO Start Video URL Like: ['https://npo.nl/start/afspelen/de-slimste-mens_1240'] : ")```

Sen öppnar programmet en JSON fil "cookie.json" och sparar cookien som en sträng i variabeln cookie_data. ```with open("cookie.json", "r") as data:
    cookie_data = json.load(data)```

Efter det kollar programmet om det redan finns en sparad cookie. Om det är så skriver den ut en fråga om användaren vill använda eller uppdatera cookien.

Om användaren vill ändra cookien fråga programmet om en ny cookie. När användaren har matat in cookien sparar den i JSON filen "cookie.json" i en key som heter "cookie". Om användaren inte vill ändra cookie använder programmet samma cookien som redan finns i json filen. 

Om där inte finns en cookie fråga programmet om man vill skriva in en cookie. Om man vill, öppnar programmet samma JSON fil "cookie.json" och sparar cookie i en key kallad "cookie". Om man inte ska skriva in en cookie fortsätter programmet. 

```
if cookie_data['cookie']:
    if input("\nSaved cookie for NPO Plus found. To edit this cookie press 'E'. To use the saved cookie press ENTER: "):
        new_cookie = input("\nEnter new '__Secure-next-auth.session-token' cookie: ")
        cookie_data['cookie'] = new_cookie
        with open("cookie.json", "w") as f:
            json.dump(cookie_data, f)
            print("\nNew cookie saved!")
        cookie = cookie_data['cookie']

    else:
        cookie = cookie_data['cookie']


else:
    cookie = input("\nEnter '__Secure-next-auth.session-token' cookie for downloading NPO plus content. To skip press ENTER: ")
    if cookie:
        if input("\nSave this cookie for future use? [Y/N]: ").lower() == "y":
            cookie_data['cookie'] = cookie
            with open("cookie.json", "w") as f:
                json.dump(cookie_data, f)
                print("\nCookie saved!")
```

Nu ska programmet tilldelas en värde till variabeln "slug". Npo använder "slugs" för alla apier. en slug ser ut så här: "over-mijn-lijk".
Programmet får sluggen genom att den plockar ut sista delen av värdet av variabeln "video_url". Alltså den url som användaren har matat in. ```slug = video_url.split("/")[-1]```

Nu anropar programmet en funktion i filen "npo_widevine.py" se [hur npo_widevine.py är byggd](#Npo_widevine). Programmet gör en anropen till funktionen med variabeln "slug" och "cookie".
Funktionen returnerar flera värden samtidigt "mpd_url", "stream_widevine_key", "media_name", "stream_season_number" och "stream_title". Allt data som behövs för att ladda ner en avsnitt.
Sen skriver programmer ut "media_name", "stream_widevine_key", "mpd_url". 
```
mpd_url, stream_widevine_key, media_name, stream_season_number, stream_title = npo_widevine(slug, cookie)
print(f"[INFO] Media name: {media_name}, Media decryption key: {stream_widevine_key}, MPD stream: {mpd_url}")
```

Efter det försöker programmet skapa en mappstruktur för serien med download_path som rotkatalog. Programmet ersätter alla mellanslag i series namn med "_".
Om mappen redan finns ska den inte skapa en.
```
try:
    os.makedirs(f'{download_path}series\\{stream_title.replace(" ", "_")}\\Season_{stream_season_number}')
except FileExistsError:
    pass
```




## Npo_widevine

