import requests
import json
import sys
import os
import datetime
urlStartDate = '01022016'
urlFinishDate = '31032016'

startDate =   datetime.date(2016,2,1)
finishDate =  datetime.date(2016,3,31)


url = "http://webtris.highwaysengland.co.uk/api/v1/reports/{}/to/{}/daily?sites=".format(urlStartDate, urlFinishDate)
params ="&page=1&page_size=200"
current_path=os.path.dirname(os.path.abspath(__file__)) + "/reportsv2"

# radom initialization
actualDate = datetime.date(1900,1,1)
actualFile = None

def createDirectoryHierarchy(startDate, finishDate):
    print(current_path)
    pathWhereFileAreDownloaded = current_path
    if not os.path.isdir(pathWhereFileAreDownloaded):
        os.makedirs(pathWhereFileAreDownloaded)
    # for year in range (startDate.year, finishDate.year +1):
    #     yearDirectory = pathWhereFileAreDownloaded +"/"+ str(year)
    #     if not os.path.isdir(yearDirectory):        
    #         os.makedirs(yearDirectory)
    #     for month in range(1, 13):
    #         monthDirectory = yearDirectory + "/" + str(month)
    #         if not os.path.isdir(monthDirectory):        
    #             os.makedirs(monthDirectory)   
    #         for day in range(1,32):
    #             dayReportFile = monthDirectory +"/" + str(day) +".csv"        
    #             file =open(dayReportFile, 'w')
    #             file.write("Id|Name|Report Date|Time Period Ending|Time Interval|Avg mph|Total volume\n")
    #             file.close()

def make_request(url):
    return requests.get(url)

def print_data(id, json):
    global actualFile
    rows = json["Rows"]
    for row in rows:
        actualFile.write(str(id) +  "|" + row["Site Name"] + "|" + row["Report Date"].replace('00:00:00', row["Time Period Ending"]) +  "|" + row["Avg mph"]  + "|" + row["Total Volume"] + "\n")


def iterate_over_links(id, json_links):
    for link in json_links:
        if link["rel"] == "nextPage" :
            response = make_request(link["href"])
            if response.status_code==200:
                json_data = response.json()
                # print (json_data)
                print_data(id, json_data)
                if json_data["Header"]['links']:
                    iterate_over_links(id, json_data["Header"]['links'])


createDirectoryHierarchy(startDate, finishDate)
for id in range(1, 17367):
    try:
        response =  make_request(url + str(id) + params)
        if response.status_code==200:
            actualFile =open(current_path + "/{}.csv".format(id) , 'w')
            actualFile.write("Id|Name|Report Date|Avg mph|Total volume\n")

            json_data = response.json()
            print_data(id, json_data)
            if json_data["Header"]["links"]:
                iterate_over_links(id, json_data["Header"]["links"])
            actualFile.close()
        else:
            sys.stderr.write(str(id) + "\t" + response.text + "\n")
            sys.stderr.flush()
    except KeyboardInterrupt:
        sys.exit()
    except:
        sys.stderr.write("Unexpected error:" +  str(sys.exc_info()[0]))
    