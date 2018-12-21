import requests
import json
import sys

url = "http://webtris.highwaysengland.co.uk/api/v1/reports/16032016/to/17032016/daily?sites=    "
params ="&page=1&page_size=200"

def make_request(url):
    return requests.get(url)

def print_data(id, json):
    rows = json["Rows"]
    for row in rows:
        print(str(id) +  "|" + row["Site Name"] + "|" + row["Report Date"] + "|" + row["Time Period Ending"]  + "|" + row["Time Interval"]
         + "|" + row["0 - 520 cm"]  + "|" + row["521 - 660 cm"]  + "|" + row["661 - 1160 cm"]  + "|" + row["1160+ cm"]
          + "|" + row["0 - 10 mph"]  + "|" + row["11 - 15 mph"]  + "|" + row["16 - 20 mph"] + "|" + row["21 - 25 mph"]  + "|" + row["26 - 30 mph"]  + "|" + row["31 - 35 mph"]
           + "|" + row["36 - 40 mph"]  + "|" + row["41 - 45 mph"]  + "|" + row["46 - 50 mph"]  + "|" + row["51 - 55 mph"]
            + "|" + row["56 - 60 mph"]  + "|" + row["61 - 70 mph"]  + "|" + row["71 - 80 mph"]  + "|" + row["80+ mph"]
             + "|" + row["Avg mph"]  + "|" + row["Total Volume"])

def iterate_over_links(id, json_links):
    for link in json_links:
        if link["nextPage"]:
            response = make_request(link["href"])
            if response.status_code==200:
                json_data = response.json()
                # print (json_data)
                print_data(id, json_data)
                if json_data["Header"]['links']:
                    iterate_over_links(json_data["Header"]['links'])


print("Id|Name|Report Date|Time Period Ending|Time Interval|0 - 520 cm|521 - 660 cm|661 - 1160 cm|1160+ cm|0 - 10 mph|11 - 15 mph|16 - 20 mph|" +
"21 - 25 mph| 26 - 30 mph|31 - 35 mph|36 - 40 mph|41 - 45 mph|46 - 50mph|51 - 55 mph|56 - 60 mph|61 - 70 mph|71 - 80 mph|80+ mph|Avg mph|Total volume")
for id in range(1, 17367):
    response =  make_request(url + str(id) + params)
    if response.status_code==200:
        json_data = response.json()
        print_data(id, json_data)
        if json_data["Header"]['links']:
            iterate_over_links(json_data["Header"]["links"])

    else:
        sys.stderr.write(str(id) + "\t" + response.text + "\n")
        sys.stderr.flush()
