import requests
import random

i = 0

post_data = {"items": {"trending_programs": {"image": [],
                                             "text_image": [],
                                             "slug": []},
                       "new_programs": {"image": [],
                                        "text_image": [],
                                        "slug": []}}}

## URLS can basically be changed to everything you want. Did these one because my layout has trending and new programs. But you can have programs from an category displayed as well.
trending_programs_url = "https://npo.nl/start/api/domain/recommendation-collection?collectionId=trending-anonymous-v0&collectionIndex=1&collectionType=SERIES&includePremiumContent=true&layoutType=RECOMMENDATION&partyId=1%3Amjue2oeb%3A16f959774071426fb880d64700be8000"

new_programs_url = "https://npo.nl/start/api/domain/recommendation-collection?collectionId=recent-free-v0&collectionIndex=4&collectionType=SERIES&includePremiumContent=true&layoutType=RECOMMENDATION&partyId=1%3Amjue2oeb%3A16f959774071426fb880d64700be8000"



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
    print(i)
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
    print(i)

print(post_data)
