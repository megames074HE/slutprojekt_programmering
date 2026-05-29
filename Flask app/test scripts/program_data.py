import requests

search_slug = "kunst-in-het-wild"

payload = {
    'seriesSlug': search_slug,
    'tab': 'afleveringen'
}


program_data = requests.get(f"https://npo.nl/start/_next/data/84pYDQb1urckQuRTnDy1_/serie/{search_slug}/afleveringen.json", params=payload).json()['pageProps']['dehydratedState']['queries']


post_data = {"items": {"image_url": "",
                       "title_image": "",
                       "program_title": "",
                       "program_summary": "",
                       "program_genre": ""}}

program_title = program_data[0]['state']['data']['title']
post_data['items']['program_title'] = program_title

program_summary = program_data[0]['state']['data']['synopsis']
post_data['items']['program_summary'] = program_summary

try:
    program_genre = program_data[0]['state']['data']['genres'][0]['name']
except:
    program_genre = program_data[1]['state']['data']
    print(program_genre)

post_data['items']['program_genre'] = program_genre

for image_text in program_data['images']:
    if image_text['role'] == "title":
        image_text_url = image_text['url']
        post_data['items']['title_image'] = image_text_url

for image in program_data['images']:
    if image['role'] == "collection_item":
        image_url = image['url']
        post_data['items']['image_url'] = image_url
        
if not image_url:
    for image in program_data['images']:
        if image['role'] == "default":
            image_url = image['url']
            post_data['items']['image_url'] = image_url


print(post_data)