import requests
import json
from ratelimit import limits, RateLimitException, sleep_and_retry

ONE_MINUTE = 60
MAX_CALLS_PER_MINUTE = 30

'''
DESCRIPTION:
retrieves map from goalpoint endpoint of crossmint's API and returns the goal state
PARAMETERS:
url: string, endpoint url for request
RETURNS:
2d python array containing goal endpoint of the crosspoint challenge
'''
def get_map(url):
    response = requests.get(url)
    json_data = json.loads(response.text)
    return json_data["goal"]
    
'''
DESCRIPTION:
goes through the desired map and makes the corresponding API calls to crossmint's API, 
rate limiter applied to combat API throttling
PARAMETERS:
N/A
RETURNS:
N/A
'''
@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def parse():
    map = get_map("http://challenge.crossmint.io/api/map/f893d337-ad78-4f9f-bb9d-905662ff7e38/goal")
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] == "POLYANET":
                obj = {
                    "candidateId" : "f893d337-ad78-4f9f-bb9d-905662ff7e38",
                    "row" : x,
                    "column" : y
                }
                url = "http://challenge.crossmint.io/api/polyanets"
                response = requests.post(url, data=obj)
            else: 
                if map[x][y] != "SPACE":
                    hyphen = map[x][y].index("_")
                    if map[x][y][hyphen + 1:] == "SOLOON":
                        obj = {
                            "candidateId" : "f893d337-ad78-4f9f-bb9d-905662ff7e38",
                            "row" : x,
                            "column" : y,
                            "color" : map[x][y][:hyphen].lower().strip()
                        }
                        url = "http://challenge.crossmint.io/api/soloons"
                        response = requests.post(url, data=obj)
                    else:
                        obj = {
                            "candidateId" : "f893d337-ad78-4f9f-bb9d-905662ff7e38",
                            "row" : x,
                            "column" : y,
                            "direction" : map[x][y][:hyphen].lower().strip()
                        }
                        url = "http://challenge.crossmint.io/api/comeths"
                        response = requests.post(url, data=obj)          

parse()                