# Meflix Drm downloader och Flask app

Med Meflix Drm downloader kan man ladda ner tv program från NPO start. 

## Innehåll

* [Ladda ner och installera Meflix](#Ladda-ner-och-installera-Meflix)
* [Hur ska man använda programmet](#Hur-ska-man-använda-programmet)
* [Felhantering](#Felhantering)
* [Hur är programmet byggd](#hur-är-programmet-byggd)


## Ladda ner och installera Meflix

1. Man börjar med att ladda ner alla filer från GitHub. 
    Det gör man genom att klicka på knappen "Code" och sedan välja "Download zip". 
    ![code_button](/readme_images/code_button.png)
    ![download_button](/readme_images/download_button.png)

2. Man öppnar filen med ett valfritt zip-program och extraherar filerna till en valfri plats. 


3. Man ska installera alla dependencies, och det gör man med kommandot: ```pip install -r requirements.txt``` Där finns två requirements.txt filer: En i /flask app och en i /Drm downloader. 


## Hur ska man använda programmet 

### Innehåll

* [Användning av Drm Downloader](#Användning-av-Drm-Downloader)
* [Användning av Flask app](#Användning-av-Flask-app)
* [Ändra Flask konfiguration](#Ändra-Flask-konfiguration)
* [Konfigurera NPO plus cookie](#Konfigurera-NPO-plus-cookie)
* [Konfigurera för nedladdning](#Konfigurera-för-nedladdning)


### Användning av Drm Downloader

Där finns två typer av Drm Downloader:

* [En för att ladda ner ett avsnitt](#Ladda-ner-ett-avsnitt)
* [En för att ladda ner en hel säsong](#Ladda-ner-en-säsong)


#### Ladda ner ett avsnitt

Info: Filen är nu konfigurerad för att hämta dekrypteringsnycklar. Den laddar inte ner något nu. Se [Konfigurera för nedladdning](#Konfigurera-för-nedladdning)

1. Kör python filen "NPO_downloader.py". Då visas följande output:
    ![output1](/readme_images/output1.png)
2. Man klistrar in länken till programmet som man vill ladda ner. 
   Länken måste ha följande struktur: "https://npo.nl/start/afspelen/de-slimste-mens_1240"
3. Då visas följande output. Här ska man klistra in sin NPO start plus cookie. se [Konfigurera NPO plus cookie](#Konfigurera-NPO-plus-cookie).
För att hoppa över detta klickar man bara på Enter.
    ![output2](/readme_images/output2.png)
4. Man får fram följande output. Detta är dekrypteringsnyckel och videoströmmen som man behöver för att ladda ner videon.
    ![output3](/readme_images/output3.png) Om man fick en error se då [Felhantering](#Felhantering)


#### Ladda ner en säsong

Info: Filen är nu konfigurerad för att hämta dekrypteringsnycklar. Den laddar inte ner något nu. Se [Konfigurera för nedladdning](#Konfigurera-för-nedladdning)

1. kör python filen "NPO_season_downloader.py". Då visas följande output:
    ![output4](/readme_images/output4.png)
2. Man klistrar in länken till programmet som man vill ladda ner.
    länken måste ha följande struktur: "https://npo.nl/start/serie/de-slimste-mens/afleveringen". Du kan också klistrar in en länk som redan innehåller säsong som man ska ladda ner "https://npo.nl/start/serie/de-slimste-mens/afleveringen/seizoen-29".
3. Då visas följande output. Här ska man klistra in sin NPO start plus cookie. se [Konfigurera NPO plus cookie](#Konfigurera-NPO-plus-cookie).
För att hoppa över detta klickar man bara på Enter.
    ![output2](/readme_images/output2.png)
4. Nu ska man välja en säsong. Det visas en lista med alla säsongsnummer.
    ![output5](/readme_images/output5.png)
5. Efter att man har valt en säsong kommer programmet att skriva ut alla avsnitt i säsongen.
    ![output6](/readme_images/output6.png) Om man fick en error se då [Felhantering](#Felhantering)


### Användning av Flask app

Info: Flask appen är konfigurerad för att inte ladda ner videor just nu. Den laddar istället ner en testvideo. Flask appen är hostad på "https://slutprojekt.megames.se" som en WSGI app.

1. kör python filen "app.py". Då visas följande output:![output7](/readme_images/output7.png)
2. Öppna IP adressen i webbläsaren. Gröna pilen visar en lokal ip-adress som alla apparater inom huset kan öppna.
    Röda pilen visar datorns loopback ip, som endast fungerar på din egen dator.
3. Om man vill ändra porten, debug-läge eller något annat se [Ändra Flask konfiguration](#Ändra-Flask-konfiguration)


### Ändra Flask konfiguration

För att ändra konfiguration i Flask öppnar man filen "app.py" i en text eller kod editor.

* [Ändra port på webbsidan](#Ändra-port-på-webbsidan)
* [Debug-läge](#Debug-läge)


#### Ändra port på webbsidan

För att ändra porten på webbsidan ska man gå till rad 254. Där ser man följande kod snippet: ```app.run(host='0.0.0.0')``` 
För att ändra porten anger man ```port=<port>```. Exempel: ```app.run(host='0.0.0.0', port=8000)```


#### Debug-läge

Om man vill ändra koden i "app.py" kan det vara användbart att ha debug-läge på. Det gör att sidan laddas om automatisk när man ändrar nått i koden.
För att ändra debug-läge går man till rad 254 i koden. Där ser man följande kod snippet: ```app.run(host='0.0.0.0')``` 
För att ändra debug-läge anger man ```debug=True```. Exempel: ```app.run(host='0.0.0.0', debug=True)```


### Konfigurera NPO plus cookie

Om man ska ladda ner NPO Plus content eller vill ta bort geo restriction måste man ange en NPO Plus cookie. 

1. Man loggar in på NPO start med sitt NPO plus konto. Därefter öppnar man inspector element och går till fliken "Application". 
![inspector_element](/readme_images/inspector_element.png)
2. I Application ska man välja Cookies. Därefter ska man leta efter cookien som heter "__Secure-next-auth.session-token".
![about_cookie](/readme_images/about_cookie.png)
3. kopiera cookien och klistra in den. Programmet frågar om man vill spara cookien. Skriv "Y" om du vill.
![output8](/readme_images/output8.png)

Nu har du sparat cookie. Vill du ändra cookie? Gör så här.

1. När man kör koden "NPO_downloader.py" eller "NPO_season_downloader.py" frågar programmet dig om du vill ändra eller använda sparad cookie. Skriv "E" för att ändra cookien. 
![output9](/readme_images/output9.png)
2. Följ de föregående stegen igen för att uppdatera cookien.


### Konfigurera för nedladdning

Om man vill ladda ner med programmet måste man ta bort vissa kommentarer i python koden. Man ska också ha programmen "N_m3u8DL-RE.exe", "packager-win-x64.exe" och "ffmpeg.exe" i samma directory som python filen.

#### NPO_downloader.py

1. Gå till rad 7 och ange en download location: ```download_path = "C:\\Path\\To\\Media\\location\\"```

2. Gå till rad 52 och ta bort "#"

#### NPO_season_downloader.py

1. Gå till rad 7 och ange en download location: ```download_path = "C:\\Path\\To\\Media\\location\\"```

2. Gå till rad 93 och 94 och ta bort "#". 


## Felhantering

Gå till instruktioner för Felhantering: [Felhantering](/felhantering.md)

## Hur är programmet byggd

Gå till funktion av Drm downloader: [Hur är Drm Downloader byggd](/Drm%20downloader/funktion.md)

Gå till funktion av Flask app: [Hur är Flask app byggd](/Flask%20app/funktion.md)