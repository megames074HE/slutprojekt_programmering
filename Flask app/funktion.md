# Hur Flask app är byggd

Programmet är flask baserad och hämtar och visar tv program information från NPO på en webbsida. Den funkar som en gui.

## Innehåll

* [def index()](#def-index)
* [def search_results()](#def-search_results)
* [def programs()](#def-programs)
* [def season_data_api](#def-season_data_api)
* [def file_api()](#def-file_api)



### def index()

Varje gång en användare besöker startsidan av webbsidan får användaren 5 slumpvisa bilder som recomendations. Dessa hämtas från Npo's recomendations api.

Programmet börjar med att skapa en dictionary som heter "post_data". Denna använd som huvudbehållaren för all data som ska skickas till html sidan.
```
    post_data = {"items": {"trending_programs": {"image": [],
                                                 "text_image": [],
                                                 "slug": []},
                           "new_programs": {"image": [],
                                            "text_image": [],
                                            "slug": []}}}

```

Programet gör get requests till 2 apier. En för trending program och en för nya program. Data blir sparad i 2 variabler "trending_new_programs_url" och "new_programs_url". Dessa apier går att byta ut mot andra kategorier.
```
    trending_programs_data = requests.get(trending_programs_url).json()
    new_programs_data = requests.get(new_programs_url).json()
```

Efter det kör programmet 2 loops. En som upprepar 2 gånger för trending data och en som upprepar 3 gånger för nya program. Allt data som bilder och länkar blir addat till post_data. Om det händer en error för att där kanske inte finns en bild, upprepa loopen en gång till.
```
    while i < 2:
        random_trending_program = random.choice(trending_programs_data["items"])

        try:
            post_data["items"]["trending_programs"]["text_image"].append(random_trending_program["images"][1]['url'])
            post_data["items"]["trending_programs"]["slug"].append(random_trending_program["slug"])
            post_data["items"]["trending_programs"]["image"].append(random_trending_program["images"][0]['url'])
        except:
            i = -1

        i += 1
    i = 0

    while i < 3:
        random_new_programs = random.choice(new_programs_data["items"])
        try:
            post_data["items"]["new_programs"]["text_image"].append(random_new_programs["images"][1]['url'])
            post_data["items"]["new_programs"]["slug"].append(random_new_programs["slug"])
            post_data["items"]["new_programs"]["image"].append(random_new_programs["images"][0]['url'])
        except:
            i = -1

        i += 1
```

Till slut öppnar flask templaten "index.html" och fyller den med post_data. Efter visar html datan på webbläsaren.
```return render_template("index.html", post_data=post_data)```

### def search_results()

Programmet kontrollerar om requesten är POST. Om det är post ska den hämta datan från formulär som är skickad vid post. 
```
    if request.method == 'POST':

        search_term = request.form['search-term']
```

Efter det skapa programmet en payload för sökresultat apien från NPO. Sökresultater är filtrerad på serier och innehåller NPO plus serier.
```
        payload = {"searchQuery": search_term,
                   "searchType": "series",
                   "subscriptionType": "anonymous",
                   "includePremiumContent": "true"}
```

Programmet gör en get request till sökresultat apien med "payload" och får max 24 sökresultat. Sökresultat är sparad i variabeln "search_results_api".
```
        search_results_api = requests.get("https://npo.nl/start/api/domain/search-collection-items", params=payload).json()[
            'items'][:24]
```

Programmet skapar en dictionary som används för html filen senare. Den innehåller bilder och länkar. 
```
        post_data = {"items": {"image_url": [],
                               "title_image": [],
                               "series_slug": []}}
```

Mängd sökresultater blir sparad i en variabel "len_list"
```len_list = len(search_results_api)```

Programmet ska nu loopar genom alla sökresultater och spara bilder och länkar i "post_data". Programmet kontrollerar om där finns bilder och länkar för varje sökresultat. Om det inte är så hoppa den över den sökresultaten eller väljer den en annan bild. 
```
        for i in range(len(search_results_api)):
            image_url = None
            image_text_url = None


            for image in search_results_api[i]['images']:
                if image['role'] == "title":
                    image_text_url = image['url']
                    post_data['items']['title_image'].append(image_text_url)

            if not image_text_url:
                len_list -= 1
                continue


            for image in search_results_api[i]['images']:
                if image['role'] == "collection_item":
                    image_url = image['url']
                    post_data['items']['image_url'].append(image_url)

            if not image_url:
                for image in search_results_api[i]['images']:
                    if image['role'] == "default":
                        image_url = image['url']
                        post_data['items']['image_url'].append(image_url)
            
            post_data['items']['series_slug'].append(search_results_api[i]['slug'])
```

Programmet kontrollerar om där finns 0 sökresultater. Om det är så får användaren en error sida. Om där finns sökresultater får användaren sidan med alla resultater.
```
        if len_list == 0:
            return render_template("error.html")
        else:
            print(post_data)
            return render_template("search_results.html", post_data=post_data, len=len_list)
```

### def programs()

På den här sidan får användaren information om valt program. Användaren får information som Bild, sammanfattning och alla säsonger och avsnittet.

Programmet börjar med att hämta en parameter från urlen. Parameter är en slug som används för att få data från NPO apier. Sluggen blir sparad i variabeln "program_slug".
```program_slug = request.args.get('slug')```

Efter det skapar programmet en payload för att göra en get request till NPO program data api. Payloaden byggs med sluggen från användarens valt program.
```    
payload = {
        'seriesSlug': program_slug,
        'tab': 'afleveringen'
    }

    program_data = requests.get(f"https://npo.nl/start/_next/data/{api_url_data_string}/serie/{program_slug}/afleveringen.json", params=payload).json()['pageProps']['dehydratedState']['queries']
```

Programmet skapar en dictionary med variabeln "post_data" som innehåller allt data för användaren.
```    
post_data = {"items": {"image_url": "",
                        "title_image": "",
                        "program_title": "",
                        "program_summary": "",
                        "program_genre": "",
                        'season_title': [],
                        'season_guid': []}}
```

Programmet parsar titeln och sammanfattning från "program_data" och sparar den i "post_data".
```
    program_title = program_data[0]['state']['data']['title']
    post_data['items']['program_title'] = program_title

    program_summary = program_data[0]['state']['data']['synopsis']
    post_data['items']['program_summary'] = program_summary
```

Nu kontrollerar programmet om där finns en genre i programdata. Om det inte är så blir genren "Informatief". Genren blir sparad i post_data.
```
   try:
        program_genre = program_data[0]['state']['data']['genres'][0]['name']
    except:
        program_genre = "Informatief"

    post_data['items']['program_genre'] = program_genre
```

Efter det kontrollerar om "program_data" har bilder. Cover art bilder kan va två typer i "program_data" en som har en key "collection_item" och en "default". Programmet kontrollerar så att en av de finns. 
```
    for image_text in program_data[0]['state']['data']['images']:
        if image_text['role'] == "title":
            image_text_url = image_text['url']
            post_data['items']['title_image'] = image_text_url

    for image in program_data[0]['state']['data']['images']:
        if image['role'] == "collection_item":
            image_url = image['url']
            post_data['items']['image_url'] = image_url
            
    if not image_url:
        for image in program_data[0]['state']['data']['images']:
            if image['role'] == "default":
                image_url = image['url']
                post_data['items']['image_url'] = image_url
```

Programmer loopar för alla säsonger i serien. Den kontrollerar om säsong har en "label". Om det finns sparar programmet den i variabeln "program_season_label". Om "program_season_label" är None
hämtar programmet säsong nummer från key "seasonKey". Efter det sparar programmet säsongslabel i "post_data".

Om där inte finns en "label" för säsongen betyder det att det finns bara 1 säsong. Programmet använder då serie titel som säsongsnamn. Om ordet "nos" finns i serie titeln är det en nyhet program. De använder en annan api för avsnitt och har bara 1 säsong.
```

    for program_seasons in program_data[3]['state']['data']:
        print(program_seasons)
        try:
            program_season_label = program_seasons['label']
            print(program_season_label)
        except:
            program_season_label = program_seasons['slug'].replace("-", " ")

            ## fix as nos programs doesn't have seasons.

            if "nos" in program_season_label:
                program_season_label = 1
                post_data['items']['season_title'].append(program_season_label)

                ## another fix as nos programs does not use the same api for episode as series.

                program_seasons_nos = requests.get(
                    f"https://npo.nl/start/_next/data/84pYDQb1urckQuRTnDy1_/serie/{program_slug}/afleveringen.json",
                    params=payload).json()['pageProps']['dehydratedState']['queries'][0]['state']['data']

                # print(program_seasons_nos['guid'])
                program_season_guid = "nos" + program_seasons_nos['guid']
                print(program_season_guid)
                post_data['items']['season_guid'].append(program_season_guid)
                return render_template('program_info.html', post_data=post_data,
                                       len=len(post_data['items']['season_title']))

        if program_season_label == None:
            program_season_label =  f"Seizoen {program_seasons['seasonKey']}"

            
        post_data['items']['season_title'].append(program_season_label)
```

Till slut sparar programmet säsongens GUID i "post_data". Den används senare för att få avsnitt information. Och till slut får användaren html filen i webbläsaren med allt data. 
```
        program_season_guid = program_seasons['guid']
        print(program_season_guid)
        post_data['items']['season_guid'].append(program_season_guid)
        
    return render_template('program_info.html', post_data=post_data, len=len(post_data['items']['season_title']))
```

### def season_data_api()

Den här sidan används som en proxy. Det är gjort för att Npo start api har inte CORS. Javascript koden på "program_info.html" fungerar inte utan CORS. Den här api sparar datan från Npo's api i variabeln "cors_data" och skicka det som JSON.

Programmet kontrollerar också om "season-slug" innehåller ordet "nos". Om det är så använder den en annan api, för att alla nos program använder en anna api.
```
    season_guid = request.args.get('season-slug')
    print('slug '+season_guid)

    if "nos" in season_guid:
        print('nos program found!')
        print(f'https://npo.nl/start/api/domain/programs-by-series?includePremiumContent=true&seriesGuid={season_guid.replace("nos", "")}&limit=20&sort=-firstBroadcastDate')
        cors_data = requests.get(f'https://npo.nl/start/api/domain/programs-by-series?includePremiumContent=true&seriesGuid={season_guid.replace("nos", "")}&limit=20&sort=-firstBroadcastDate').json()
    else:
        cors_data = requests.get(f'https://npo.nl/start/api/domain/programs-by-season?ageRestriction=undefined&guid={season_guid}&type=timebound_series&includePremiumContent=true').json()

    return cors_data
```

### def file_api()

Den här apin används för att skicka filer till användaren. Justnu skicker den samma fil som är en video om anti piracy. Men om man ha Drm downloader här istället får användaren en avsnitt istället. 

Programmet hämtar sluggen från urlen som. Och programmet hämtar valt säsong och avsnitt av skickat formulär data. 

Till slut skicker programmet videon till användaren med filnamn som har följande struktur: ```<slug>-S-0-E-0```
```

        program_slug = request.args.get('slug')

        selected_season = request.form['selected-season']
        selected_episode = request.form['selected-episode']

        return send_file("video.mp4", as_attachment=True, download_name=f'{program_slug + "-S-" + selected_season + "-E-" + selected_episode}.mp4')
```
