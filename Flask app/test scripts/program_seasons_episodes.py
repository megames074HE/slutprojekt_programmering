import requests

search_slug = "nos-jeugdjournaal"

payload = {
    'seriesSlug': search_slug,
    'tab': 'afleveringen'
}


program_data = requests.get(f"https://npo.nl/start/_next/data/84pYDQb1urckQuRTnDy1_/serie/{search_slug}/afleveringen.json", params=payload).json()['pageProps']['dehydratedState']['queries'][3]['state']['data']

for program_seasons in program_data:

    try:
        program_season_label = program_seasons['label']
        print(program_season_label)
    except:
        program_season_label = program_seasons['slug'].replace("-", " ")

        ## fix as nos programs doesn't have seasons.

        if "nos" in program_season_label:
            program_season_label = 1
            program_seasons_nos = requests.get(f"https://npo.nl/start/_next/data/84pYDQb1urckQuRTnDy1_/serie/{search_slug}/afleveringen.json",params=payload).json()['pageProps']['dehydratedState']['queries'][0]['state']['data']

            #print(program_seasons_nos['guid'])
            program_season_guid = "nos" + program_seasons_nos['guid']
            print(program_season_guid)
            break

        print(program_season_label)


    program_season_guid = program_seasons['guid']
    print(program_season_guid)

