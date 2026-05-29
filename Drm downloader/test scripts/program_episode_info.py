import requests

api = requests.get('https://npo.nl/start/api/domain/programs-by-season?ageRestriction=undefined&guid=7a3b8637-f23d-492f-a4bd-28a17ee68a88&type=timebound_series&includePremiumContent=true').json()

print(api[0]['programKey'])