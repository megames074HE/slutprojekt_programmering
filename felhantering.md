# Felhantering av Drm downloader och Flask app

## innehåll

* [Drm downloader](#Drm-downloader)
* [Flask app](#Flask-app)

## Drm downloader

### Kända fel:

* [ModuleNotFounderror](#modulenotfounderror)
* [Provided URL does not work](#provided-url-does-not-work)
* [Dit programma mag niet bekeken worden vanaf jouw locatie](#dit-programma-mag-niet-bekeken-worden-vanaf-jouw-locatie)
* [Dit programma is alleen te zien met een plus abonnement.](#dit-programma-is-alleen-te-zien-met-een-plus-abonnement)
* [Provided URL does not work. Try again or try another series](#provided-url-does-not-work-try-again-or-try-another-series)

### ModuleNotFounderror

Händer när inte alla dependencies är installerat. Gå till [readme.md](/readme.md) och följ instruktioner om hur man ska installera programmet.

### Provided URL does not work

Det händer när man har matat in fel url struktur. Använd alltid en sånt här struktur "https://npo.nl/start/afspelen/de-slimste-mens_1240" när man ska ladda ner en avsnitt.

### Dit programma mag niet bekeken worden vanaf jouw locatie

Det händer när programmet har en geo restriction. Det innebär att programmet inte kan visas i landet man befinner sig i. Ange en NPO Plus cookie för att fixa det här.

### Dit programma is alleen te zien met een plus abonnement.

Det händer när programmet är bara för Plus medlemmar. Ange en NPO Plus cookie för att fixa det här.

### Provided URL does not work. Try again or try another series

Det händer när man har matat in fel url struktur för en säsong. Använd alltid en sånt här struktur "https://npo.nl/start/serie/de-slimste-mens/afleveringen Eller https://npo.nl/start/serie/de-slimste-mens/afleveringen/seizoen-29" när man ska ladda ner en säsong med säsongsnummer i url.

## Flask app

### Kända fel:

* [ModuleNotFounderror](#modulenotfounderror)
* [Login sida fungerar inte](#login-sida-fungerar-inte)
* [No programs found or random error occurred!](#no-programs-found-or-random-error-occurred)

### ModuleNotFounderror

Händer när inte alla dependencies är installerat. Gå till [readme.md](/readme.md) och följ instruktioner om hur man ska installera programmet.

### Login sida fungerar inte

Den fungerar inte för att den inte finns :)

### No programs found or random error occurred!

Händer när man har skrivit programnamnet fel eller om programmet inte finns. Försok igen genom att klicka på "Go Back" knappen.

