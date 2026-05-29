# Meflix Drm downloader och Flask app

Med Meflix Drm downloader kan man ladda ner tv program från NPO start. 

## Innehåll

* [Ladda ner och installera Meflix](#Ladda-ner-och-installera-Meflix)
* [Hur ska man använda programmet](Hur-ska-man-använda-programmet)
* [Felhantering](#Felhantering)
* [Funktion av programmet](#Funktion-av-programmet)


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
    länken måste ha följande struktur: "https://npo.nl/start/serie/de-slimste-mens/afleveringen"
3. Då visas följande output. Här ska man klistra in sin NPO start plus cookie. se [Konfigurera NPO plus cookie](#Konfigurera-NPO-plus-cookie).
För att hoppa över detta klickar man bara på Enter.
    ![output2](/readme_images/output2.png)
4. Nu ska man välja en säsong. Det visas en lista med alla säsongsnummer.
    ![output5](/readme_images/output5.png)
5. Efter att man har valt en säsong kommer programmet att skriva ut alla avsnitt i säsongen.
    ![output6](/readme_images/output6.png) Om man fick en error se då [Felhantering](#Felhantering)


### Användning av Flask app

Info: Flask appen är konfigurerad för att inte ladda ner videor just nu. Den laddar istället ner en testvideo. Flask appen är hostad på "https://slutprojekt.megames.se" som en WSGI app.



1. kör python filen 