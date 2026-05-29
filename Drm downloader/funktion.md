# Hur Drm downloader är byggd

## Innehåll

* [NPO_downloader.py](#npo_downloader)
* [NPO_season_downloader.py](#npo_season_downloader)
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

Programmet tilldelar download location som än sträng till variabeln "download_location". ```download_location = f'{download_path}series\\{stream_title.replace(" ", "_")}\\Season_{stream_season_number}'```

Till slut använder programmet subprocess.run() för att köra ett extern program som laddar och sparar videostreamen. Programmet är "N_m3u8DL-RE" 
och det används för att ladda ner och dekryptera videoinnehåll. Videon laddas ner med mpd streamen, dekrypterings nyckel, download location och fil namnet.
Den använder googles shaka packager för dekryptering av streamen. Den skickar också http headers för att efterlikna en webbsida. Fil namnet har följande strukturen: ```<programnamn>-S00E00-<avsnittnamn>.mkv ```
```
subprocess.run(f'N_m3u8DL-RE "{mpd_url}" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36" -H "Accept: */*" -H "Origin: https://npo.nl" -H "Referer: https://npo.nl/" --key {stream_widevine_key} --use-shaka-packager -M format=mkv --auto-select --save-dir {download_location} --save-name {media_name}')
```


## NPO_season_downloader

Programmet börjar med att tilldelar en download path till variabeln download_path. ```download_path = "C:\\Path\\To\\Media\\location\\"```

Programmet skriver ut frågan "Enter NPO Start Season URL Like: ['https://npo.nl/start/serie/de-slimste-mens/afleveringen'] : " och sen matas in säsong länken av användaren som en sträng i variabeln show url. ```show_url = input("Enter NPO Start Season URL Like: ['https://npo.nl/start/serie/de-slimste-mens/afleveringen'] : ")```

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
Programmet delar upp urlen i flera steg då kan den plocka ut en del mellan /serie och /afleveringen. Alltså den url som användaren har matat in. ```slug = show_url.split("serie/")[1].split("/afleveringen")[0]```

Efter det ska programmet kontrollerar först om urlen innehåller en säsong. Om den har en säsong hämta den säsongens slug med split(). Efter det skickar programmet en http get request till npos api för att hämta information om alla säsonger.
Den ska loopa igenom alla säsonger och kontrollerar vilken säsong har samma slug som sluggen i urlen. Då hämta den säsongnumret och sparar den i en variabel "season"

Om urlen inte innehåller en säsong hämta programmet först alla säsonger från apiet och spara det i en variabeln "all_seasons" som en lista. 
Den ska gå genom varje säsong och spara säsongsnummer i en lista med variabeln "seasons" och skriver ut alla säsonger. Till slut frågar programmet användaren vilken säsong som ska laddas ner
```
if show_url.split("afleveringen")[1].split("-")[0] == "/seizoen":

    season_slug = show_url.split("afleveringen/")[1]
    all_seasons = requests.get(f"https://npo.nl/start/api/domain/series-seasons?includePremiumContent=true&slug={slug}&type=timebound_series").json()
    for i in range(len(all_seasons)):
        if all_seasons[i]['slug'] == str(season_slug):
            season = all_seasons[i]['seasonKey']

else:

    ## Gets information about all the seasons
    all_seasons = requests.get(f"https://npo.nl/start/api/domain/series-seasons?includePremiumContent=true&slug={slug}&type=timebound_series").json()

    for i in range(len(all_seasons)):
        seasons.append(all_seasons[i]['seasonKey'])

    print(", ".join(seasons))
    season = int(input("\nEnter Season Number To Download: "))
```

Efter det ska programmet loopar genom alla säsonger och matcha vald säsong som användaren har matas in. När den är hittad hämta programmet GUID och sparar den som en sträng i variabeln "season_guid". GUID används som en identifierare för säsongens api.
```
for i in range(len(all_seasons)):
    if all_seasons[i]['seasonKey'] == str(season):
        season_guid = all_seasons[i]['guid']
```

Programmet ska nu skickar en get request till npo's api med variabeln "season_guid" för att hämta alla avsnitt for säsongen det blir sparad i variabeln "all_seasons_episodes" som en lista. Den använder [::-1] för att vända listan. Det är gjort för att annars börja den ladda ner nyaste avsnitt. 
Där finns felhantering som skriver ut och avslutar programmet när användaren har använd fel url. Efter programmer hat fått alla avsnitt av en säsong, skriver den ut hur många avsnitt där finns i en säsong.
```
try:
    all_season_episodes = requests.get(f"https://npo.nl/start/api/domain/programs-by-season?ageRestriction=undefined&guid={season_guid}&type=timebound_series&includePremiumContent=true").json()[::-1]
except KeyError:
    print("\n[ERROR] Provided URL does not work. Try again or try another series. Make sure it uses this structure: https://npo.nl/start/serie/de-slimste-mens/afleveringen OR https://npo.nl/start/serie/de-slimste-mens/afleveringen/seizoen-29")
    exit()

print(f"\n[INFO] season {season} has {len(all_season_episodes)} episodes")
```

Nu ska programmet loopa genom alla avsnitt och hämta guid från json datan "all_seasons_episodes" som tillhör till avsnitten. Efter det ska den hämta allt information den behöver för nedladdningen. Nu anropar programmet en funktion i filen "npo_widevine.py" se [hur npo_widevine.py är byggd](#Npo_widevine). Programmet gör en anropen till funktionen med variabeln "slug" och "cookie".
Funktionen returnerar flera värden samtidigt "mpd_url", "stream_widevine_key", "media_name", "stream_season_number" och "stream_title". Allt data som behövs för att ladda ner en avsnitt.
Sen skriver programmer ut "media_name", "stream_widevine_key", "mpd_url". Programmet upprepar loopen tills alla avsnittet har laddats ner. 
```
for i in range(len(all_season_episodes)):
    slug = all_season_episodes[i]['slug']

    
    mpd_url, stream_widevine_key, media_name, stream_season_number, stream_title = npo_widevine(slug, cookie)
```


Efter det försöker programmet skapa en mappstruktur för serien med download_path som rotkatalog. Programmet ersätter alla mellanslag i series namn med "_".
Om mappen redan finns ska den inte skapa en.
```
    try:
        os.makedirs(f'{download_path}series\\{stream_title.replace(" ", "_")}\\Season_{stream_season_number}')
    except FileExistsError:
        pass
```

Programmet tilldelar download location som än sträng till variabeln "download_location". ```download_location = f'{download_path}series\\{stream_title.replace(" ", "_")}\\Season_{stream_season_number}'```

Till slut använder programmet subprocess.run() för att köra ett extern program som laddar och sparar videostreamen. Programmet är "N_m3u8DL-RE" 
och det används för att ladda ner och dekryptera videoinnehåll. Videon laddas ner med mpd streamen, dekrypterings nyckel, download location och fil namnet.
Den använder googles shaka packager för dekryptering av streamen. Den skickar också http headers för att efterlikna en webbsida. Fil namnet har följande strukturen: ```<programnamn>-S00E00-<avsnittnamn>.mkv ```
```
   #subprocess.run(
   #f'N_m3u8DL-RE "{mpd_url}" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36" -H "Accept: */*" -H "Origin: https://npo.nl" -H "Referer: https://npo.nl/" --key {stream_widevine_key} --use-shaka-packager -M format=mkv --auto-select --save-dir {download_location} --save-name {media_name}')
```



## Npo_widevine

Den här filen används som en modul med funktionen ```npo_widevine``` som används av huvudprogrammet. Funktionen tar emot variablerna slug och cookie. 
```def npo_widevine(slug, cookie):```

Programmet börjar med att skicka en http get request tipp npo api för att hämta metadata, video id och avsnittsnummer. Den använder en avsnitt slug från "NPO_downloader.py" eller "NPO_season_downloader.py" för att göra en api request. Sedan blir det sparad i variabeln "stream_id_metadata" som en lista. 
```stream_id_metadata = requests.get(f"https://npo.nl/start/api/domain/program-detail?ageRestriction=undefined&includePremiumContent=true&slug={slug}").json()```

Efter det försöker programmet får titeln av avsnittet och sparar den som en sträng i variabeln "stream_episode_title". Om där inte finns en titel i datan händer där en error. Men istället för att crasha skriver proggrammet ut "[ERROR] Provided URL does not work. Try again or try another video. Make sure it uses this structure: https://npo.nl/start/afspelen/de-slimste-mens_1240" och avslutar programmet. 
```
try:
    stream_episode_title = stream_id_metadata['title']
    #print(stream_episode_title)
except (TypeError, KeyError):
    print("\n[ERROR] Provided URL does not work. Try again or try another video. Make sure it uses this structure: https://npo.nl/start/afspelen/de-slimste-mens_1240")
    exit()
```

Nu kontrollerar programmet om vald avsnitt är del av en serie eller är en film/dokumentär. 
Om det inte är en serie får variabeln "serie" en boolean värde som är "False". Då blir namnet av videon samma som säsongnamnet och det sparas is en sträng i variabeln "stream_title".
variabeln "stream_episode_number" får en integer värde av 0 för att där finns bar 1 avsnitt. 

Om det är en serie får variabeln "serie" en boolean värde som är "True". Då hämtas namnet för avsnitten från listan med variabeln "stream_id_metadata". Samma för "series_slug", "stream_episode_nuber", "stream_seasonKey".

Och efter programmet har kontrollerat om det är en serie eller inte får variabeln "stream_id" en sträng värde som är video id'n. Id ser så här ut "KN_1737346". Den där id'n behövs för att hämta en authorization token. 
```
if stream_id_metadata['series'] is None:
    series = False
    stream_title = stream_episode_title
    stream_episode_number = 0
    stream_seasonKey = ""
    series_slug = ""
else:
    series = True
    stream_title = stream_id_metadata['series']['title']
    series_slug = stream_id_metadata['series']['slug']
    stream_episode_number = stream_id_metadata['programKey']
    stream_seasonKey = stream_id_metadata['season']['seasonKey']
stream_id = stream_id_metadata['productId']
```

Om variabeln "series" är True hämtar programmet säsongsinformation. Den skicker en get request till npo's api och det blir sparad in en lista med variabeln "current_series_seasons".
Nu ska den loopa igenom alla säsonger av vald serie. Den ska matcha rätt säsong och kontrollera om säsongen har en "label" för att få säsongtiteln. Men om label inte innehåller ordet "Seizoen" är det en specielt säsong då används labeln som säsongsnamn. 
Om label saknas används "seasonKey" istället. 

Nu ska den extrahera säsongsnummer och det görs med .split(). Då blir det från det här "Seizoen 1" till det här "1". Säsongsnummer blir sparad i variabeln "stream_season_number".

Efter det ska programmet skapa filnamn. Det görs enligt följande formatet: ```<programnamn>-S00E00-<avsnittnamn>```. Mellanslag ersätts med "_". Variabeln "media_name" får filnamnen som en sträng. 

Om variabeln "series" är False blir "media_name" namnet av vald säsong.
```
    if series:
        ## gets season number or name for the current video
        current_series_seasons = requests.get(f"https://npo.nl/start/api/domain/series-seasons?includePremiumContent=true&slug={series_slug}&type=timebound_series").json()

        for i in range(len(current_series_seasons)):
            if current_series_seasons[i]['seasonKey'] == stream_seasonKey:
                if current_series_seasons[i]['label'] is not None and "Seizoen" not in current_series_seasons[i]['label']:
                    stream_season_number = f"_{current_series_seasons[i]['label']}_"
                else:
                    if current_series_seasons[i]['label'] is None:
                        stream_season_number = current_series_seasons[i]['seasonKey']
                    else:
                        stream_season_number = current_series_seasons[i]['label'].split(" ")[1]


        #print(f"S{stream_season_number}E{stream_episode_number}, N:{stream_title} NT:{stream_episode_title}")

        ## Final name that the downloaded file will get. Format: "SHOW_NAME-S00E00-EPISODE_NAME"
        media_name = f"{stream_title.replace(' ','_')}-S{stream_season_number}E{stream_episode_number}-{stream_episode_title.replace(' ', '_')}"
    else:
        media_name = stream_episode_title.replace(" ", "_")
```

Följande delen av koden används för att auktoriserar senare mot npo's api. 

Den börjar med att skapa en cookie header och sparar det i en dict "headers_token" som innehåller användarens sessionscookie. Cookien som används här är det som användaren har angett.
```headers_token = {"cookie": f"__Secure-next-auth.session-token={cookie}"}```

Programmet gör nu en get request till NPO's api för att hämta JWT token som behövs för auktorisering senare. Requesten görs med headers som är användarens sessionscookie. Token blir sparad i variabeln "token".
``` token = requests.get(f'https://npo.nl/start/api/domain/player-token?productId={stream_id}', headers=headers_token).json()['jwt']```

Nu ska programmet skapa en payload som ska skickas till NPO's stream api. Som använder användarens slug. 
```payload = {"profileName":"dash","drmType":"widevine","referrerUrl":f"https://npo.nl/start/afspelen/{slug}","ster":{"identifier":"npo-app-desktop","deviceType":4,"player":"web"}}```

Programmet skapa headers för post requesten. Den innehåller JWT authorization token och används för att autentisera requesten.
```
    headers = {"Content-Type":"application/json",
               "Authorization": f"{token}",
               "referer": "https://npo.nl/",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
               "origin": "https://npo.nl",}
```

Nu ska programmet hämta stream information med en post request. Post request görs med en payload och headers. Payloaden innehåller avsnitts länken. Datan blir sparat som en lista i variabeln "stream_data_url"

Om datan av requesten inte innehåller key "stream" skriver programmet ut vad error kan va och avslutar programmet. 
```
    try:
        stream_data_url = requests.post("https://prod.npoplayer.nl/stream-link", json=payload, headers=headers).json()['stream']
    except KeyError:
        error_data = requests.post("https://prod.npoplayer.nl/stream-link", json=payload, headers=headers).json()
        if error_data['status'] == 402:
            print(f"\n[ERROR] {error_data['body']} Try adding NPO Plus cookie or edit the cookie.")
            exit()
        else:
            print(f"\n[ERROR] {error_data}")
            exit()
```

Programmet hämta MPD urlen från "stream_data_url". 
```mpd_url = stream_data_url['streamURL']```

Programmet hämtar DASH manifestet som innehåller information om video, ljud och DRM data. Det görs med en get request till MPD urlen. Innehållet är hämtat som text.
```dash_contents = requests.get(mpd_url).text```

Efter det ska programmet hämta en DRM relaterade header från Dash manifestet