from npo_widevine import *
import subprocess
import os
import json

## Download location for downloaded media. Format: "C:\\Path\\To\\Media\\location\\"
download_path = "C:\\Path\\To\\Media\\location\\"
season_guid = ""
seasons = []
season = 0

# TODO: add some kind of simple search engine to make downloading easier
show_url = input("Enter NPO Start Season URL Like: ['https://npo.nl/start/serie/de-slimste-mens/afleveringen'] : ")

with open("cookie.json", "r") as data:
    cookie_data = json.load(data)

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

slug = show_url.split("serie/")[1].split("/afleveringen")[0]

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



for i in range(len(all_seasons)):
    if all_seasons[i]['seasonKey'] == str(season):
        season_guid = all_seasons[i]['guid']

## Gets information about all the episodes of one season
try:
    all_season_episodes = requests.get(f"https://npo.nl/start/api/domain/programs-by-season?ageRestriction=undefined&guid={season_guid}&type=timebound_series&includePremiumContent=true").json()[::-1]
except KeyError:
    print("\n[ERROR] Provided URL does not work. Try again or try another series. Make sure it uses this structure: https://npo.nl/start/serie/de-slimste-mens/afleveringen OR https://npo.nl/start/serie/de-slimste-mens/afleveringen/seizoen-29")
    exit()

print(f"\n[INFO] season {season} has {len(all_season_episodes)} episodes")

for i in range(len(all_season_episodes)):
    slug = all_season_episodes[i]['slug']

    ## Gets all the data needed for downloading from npo_widevine.py
    mpd_url, stream_widevine_key, media_name, stream_season_number, stream_title = npo_widevine(slug, cookie)
    print(media_name)
    ## Makes a folder for the downloaded show. Format: "*\\series\\SHOW_NAME\\SEASON_X"
    try:
        os.makedirs(f'{download_path}series\\{stream_title.replace(" ", "_")}\\Season_{stream_season_number}')
    except FileExistsError:
        pass

    download_location = f'{download_path}series\\{stream_title.replace(" ", "_")}\\Season_{stream_season_number}'

    ## Downloads at highest quality and decrypts automatically
    #subprocess.run(
    #f'N_m3u8DL-RE "{mpd_url}" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36" -H "Accept: */*" -H "Origin: https://npo.nl" -H "Referer: https://npo.nl/" --key {stream_widevine_key} --use-shaka-packager -M format=mkv --auto-select --save-dir {download_location} --save-name {media_name}')
