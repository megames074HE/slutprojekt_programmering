from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine.pssh import PSSH
import requests
import re



## Main function to crack the keys for NPO Start
# TODO: Fix that non DRM content can also download
def npo_widevine(slug, cookie):

    stream_season_number = 0

    ## Gets all the data about the video like: metadata, video id and episode number
    stream_id_metadata = requests.get(f"https://npo.nl/start/api/domain/program-detail?ageRestriction=undefined&includePremiumContent=true&slug={slug}").json()

    try:
        stream_episode_title = stream_id_metadata['title']
        #print(stream_episode_title)
    except (TypeError, KeyError):
        print("\n[ERROR] Provided URL does not work. Try again or try another video. Make sure it uses this structure: https://npo.nl/start/afspelen/de-slimste-mens_1240")
        exit()

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
    #print(stream_id)

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


    headers_token = {"cookie": f"__Secure-next-auth.session-token={cookie}"}


    ## Authorization token
    token = requests.get(f'https://npo.nl/start/api/domain/player-token?productId={stream_id}', headers=headers_token).json()['jwt']



    payload = {"profileName":"dash","drmType":"widevine","referrerUrl":f"https://npo.nl/start/afspelen/{slug}","ster":{"identifier":"npo-app-desktop","deviceType":4,"player":"web"}}


    headers = {"Content-Type":"application/json",
               "Authorization": f"{token}",
               "referer": "https://npo.nl/",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
               "origin": "https://npo.nl",}

    ## Tries getting stream information like headers and dash stream
    # TODO: add more error support such as an fix to download from another location
    # TODO: add support to download NPO plus
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


    mpd_url = stream_data_url['streamURL']

    ## Dash stream needed for getting PSSH
    dash_contents = requests.get(mpd_url).text
    http_token = stream_data_url['drm']['httpHeaders']['X-Custom-Data']

    ## Gets PSSH from dash stream
    pssh_data = re.findall(r"<cenc:pssh>(.*?)</cenc:pssh>", dash_contents)[1]
    #print(f"PSSH: {pssh_data}")

    pssh = PSSH(pssh_data)

    ## Loads wvd. Create an wvd with this command: "pywidevine create-device -k <device_private_key> -c <device_client_id_blob> -t "ANDROID" -l 3"
    device = Device.load("cdm.wvd")

    cdm = Cdm.from_device(device)

    session_id = cdm.open()

    challenge = cdm.get_license_challenge(session_id, pssh)

    headers = {"X-Custom-Data": http_token}

    licence = requests.post("https://npo-drm-gateway.samgcloud.nepworldwide.nl/authentication", data=challenge,
                            headers=headers)
    licence.raise_for_status()

    cdm.parse_license(session_id, licence.content)

    ## Get decryption key for video
    for key in cdm.get_keys(session_id):
        if key.type == "CONTENT":
            #print(f"KEY FOUND: {key.kid.hex}:{key.key.hex()}")
            stream_widevine_key = f"{key.kid.hex}:{key.key.hex()}"
            cdm.close(session_id)
            return(mpd_url, stream_widevine_key, media_name, stream_season_number, stream_title)


