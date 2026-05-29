from flask import Flask, render_template, request, send_file
from flask_cors import CORS
import requests
import random


app = Flask(__name__)
CORS(app)


## URLS can basically be changed to everything you want. Did these one because my layout has trending and new programs. But you can have programs from an category displayed as well.
trending_programs_url = "https://npo.nl/start/api/domain/recommendation-collection?collectionId=trending-anonymous-v0&collectionIndex=1&collectionType=SERIES&includePremiumContent=true&layoutType=RECOMMENDATION&partyId=1%3Amjue2oeb%3A16f959774071426fb880d64700be8000"

new_programs_url = "https://npo.nl/start/api/domain/recommendation-collection?collectionId=recent-free-v0&collectionIndex=4&collectionType=SERIES&includePremiumContent=true&layoutType=RECOMMENDATION&partyId=1%3Amjue2oeb%3A16f959774071426fb880d64700be8000"

## String for the data apis. Needs to be changed every month. Going to be automatic
api_url_data_string = "84pYDQb1urckQuRTnDy1_"

@app.route('/')
def index():
    i = 0
    post_data = {"items": {"trending_programs": {"image": [],
                                                 "text_image": [],
                                                 "slug": []},
                           "new_programs": {"image": [],
                                            "text_image": [],
                                            "slug": []}}}

    trending_programs_data = requests.get(trending_programs_url).json()
    new_programs_data = requests.get(new_programs_url).json()

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

    return render_template("index.html", post_data=post_data)

@app.route('/search_results', methods=['POST'])
def search_results():

    if request.method == 'POST':

        search_term = request.form['search-term']

        payload = {"searchQuery": search_term,
                   "searchType": "series",
                   "subscriptionType": "anonymous",
                   "includePremiumContent": "true"}

        search_results_api = requests.get("https://npo.nl/start/api/domain/search-collection-items", params=payload).json()[
            'items'][:24]

        post_data = {"items": {"image_url": [],
                               "title_image": [],
                               "series_slug": []}}


        len_list = len(search_results_api)

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

        if len_list == 0:
            return render_template("error.html")
        else:
            print(post_data)
            return render_template("search_results.html", post_data=post_data, len=len_list)

@app.route('/programs')
def programs():
    program_slug = request.args.get('slug')

    image_url = None

    payload = {
        'seriesSlug': program_slug,
        'tab': 'afleveringen'
    }

    program_data = requests.get(f"https://npo.nl/start/_next/data/{api_url_data_string}/serie/{program_slug}/afleveringen.json", params=payload).json()['pageProps']['dehydratedState']['queries']



    post_data = {"items": {"image_url": "",
                        "title_image": "",
                        "program_title": "",
                        "program_summary": "",
                        "program_genre": "",
                        'season_title': [],
                        'season_guid': []}}

    program_title = program_data[0]['state']['data']['title']
    post_data['items']['program_title'] = program_title

    program_summary = program_data[0]['state']['data']['synopsis']
    post_data['items']['program_summary'] = program_summary

    ## Fix for genres not showing up or causing errors. This happens because the program doesn't have a genre.
    try:
        program_genre = program_data[0]['state']['data']['genres'][0]['name']
    except:
        program_genre = "Informatief"

    post_data['items']['program_genre'] = program_genre

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

        program_season_guid = program_seasons['guid']
        print(program_season_guid)
        post_data['items']['season_guid'].append(program_season_guid)
    
    

    return render_template('program_info.html', post_data=post_data, len=len(post_data['items']['season_title']))


@app.route('/login')
def login():
    return render_template('error.html')


@app.route('/about')
def about():
    return render_template('about.html')


# Made a proxy right here below as it was too slow to make javascript fetch data for each season. Every season has an own api link.
# the api below gets an request from the javascript for the selected season. This makes it faster and doesnt result in a timeout from the npo api. 

@app.route("/season-data-api")
def season_data_api():
    
    season_guid = request.args.get('season-slug')
    print('slug '+season_guid)

    if "nos" in season_guid:
        print('nos program found!')
        print(f'https://npo.nl/start/api/domain/programs-by-series?includePremiumContent=true&seriesGuid={season_guid.replace("nos", "")}&limit=20&sort=-firstBroadcastDate')
        cors_data = requests.get(f'https://npo.nl/start/api/domain/programs-by-series?includePremiumContent=true&seriesGuid={season_guid.replace("nos", "")}&limit=20&sort=-firstBroadcastDate').json()
    else:
        cors_data = requests.get(f'https://npo.nl/start/api/domain/programs-by-season?ageRestriction=undefined&guid={season_guid}&type=timebound_series&includePremiumContent=true').json()

    return cors_data


@app.route("/file-api", methods=["GET", "POST"])
def file_api():
    if request.method == 'POST':

        program_slug = request.args.get('slug')

        selected_season = request.form['selected-season']
        selected_episode = request.form['selected-episode']

        return send_file("video.mp4", as_attachment=True, download_name=f'{program_slug + "-S-" + selected_season + "-E-" + selected_episode}.mp4')




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
