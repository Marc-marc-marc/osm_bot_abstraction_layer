import requests
import requests.exceptions
import time
from tqdm import tqdm
import random

def sleep(time_in_s):
    for i in tqdm(range(time_in_s*10), ascii=True):
        time.sleep(0.1)

def download_overpass_query(query, filepath, timeout=1500, user_agent='overpass downloader for OSM bot (if it is overusing resources, please block it and contact matkoniecz@gmail.com)'):
    # see https://github.com/westnordost/StreetComplete/blob/6740a0b03996b929f9cf74ddb0e6afac7e3fc48e/app/src/main/res/xml/preferences.xml#L99
    faster_server ="https://lz4.overpass-api.de/api/interpreter"
    alt_server = "http://z.overpass-api.de/api/interpreter"
    server = random.choice([faster_server, alt_server])
    with open(filepath, 'w+') as file:
        file.write(get_response_from_overpass_server(server, query, timeout, user_agent))

def sleep_before_retry(error_summary):
    print("sleeping before retry due to", error_summary)
    sleep(100)
    print("retrying")

def get_response_from_overpass_server(api_url, query, timeout, user_agent):
    #print("sleeping before download")
    #sleep(20)
    while True:
        try:
            response = single_query_run(api_url, query, timeout, user_agent)
            if response.status_code != 429 and response.status_code != 503:
                return response.content.decode('utf-8')
            sleep_before_retry(str(response.status_code) + " error code (response received)")
            continue
        except requests.exceptions.ConnectionError as e:
            print(e)
            sleep_before_retry("requests.exceptions.ConnectionError")
            continue
        except requests.exceptions.HTTPError as e:
            print(e.response.status_code)
            if e.response.status_code == 429 or e.response.status_code == 503:
                sleep_before_retry(e.response.status_code + " error code (HTTPError thrown)")
                continue
            raise e
        except requests.exceptions.ReadTimeout as e:
            sleep_before_retry("timeout")
            continue
    print("overpass query failed!")

def single_query_run(api_url, query, timeout, user_agent):
    print("downloading " + query)
    response = requests.post(
        api_url,
        data={'data': query},
        timeout=timeout,
        headers={'User-Agent': user_agent}
    )
    print("completed with", response.status_code, "http code")
    return response
