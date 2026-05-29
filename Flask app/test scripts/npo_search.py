import requests


payload = {"searchQuery": "de mol",
            "searchType": "series",
            "subscriptionType": "anonymous",
            "includePremiumContent": "true"}

search_results_api = requests.get("https://npo.nl/start/api/domain/search-collection-items", params=payload).json()[
    'items'][:24]


post_data = {"items": {"image_url": [],
                       "title_image": [],
                       "series_slug": []}}



for i in range(len(search_results_api)):
    image_url = None


    post_data['items']['series_slug'].append(search_results_api[i]['slug'])


    for image in search_results_api[i]['images']:
        if image['role'] == "title":
            image_url = image['url']
            post_data['items']['title_image'].append(image_url)

    for image in search_results_api[i]['images']:
        if image['role'] == "collection_item":
            image_url = image['url']
            post_data['items']['image_url'].append(image_url)
            
    if not image_url:
        for image in search_results_api[i]['images']:
            if image['role'] == "default":
                image_url = image['url']
                post_data['items']['image_url'].append(image_url)


print(post_data)

    




#    for images in range(len(search_results_api[i]['images'])):
#        if search_results_api[i]['images'][images]['role'] == "collection_item":
# #            print(search_results_api[i]['title'])


