import requests
import bs4
import csv
import os
import urllib
import json
from dotenv import load_dotenv
from apiclient.discovery import build

from bs4 import BeautifulSoup
import re
from datetime import datetime, date, timedelta
import json
import googleapiclient.discovery
from flask import Flask, request
from flask_cors import CORS


load_dotenv()
api_key = os.environ.get("API_KEY")
api_service_name = "youtube"
api_version = "v3"

app = Flask(__name__)
CORS(app)


@app.route("/lofiBackend")
def processRequest():
    print("Receive info here and run, running")
    videoId = request.args.get("videoId")
    userTimeStamp = request.args.get("timestamp", type=(float))
    userTimeStamp = int(userTimeStamp)
    userTimeStamp = str(timedelta(seconds=userTimeStamp))
    video_info = get_vidDesc(videoId)
    parentVideoTitle = video_info[0]
    parentVideoDesc = video_info[1]
    print(f"inside flask printing --- title ----{parentVideoTitle}")
    print()
    parsedDesc = desc_parser(parentVideoDesc)
    if bool(parsedDesc) == False:
        print("Empty MFING description")
        return "<h1>Returning EARLY</h1>"
    # userTimeStamp = "00:24:20"
    returnTimeStamp = clickTrackPicker(userTimeStamp)
    print(f" printing time stamp from user parsing return {returnTimeStamp}")

    val = returnTimeStamp[1]
    print(val)
    # returnTimeStamp[0] is timestamp and [1] is title
    # url is where it exists
    # parent video title :
    url = fectchUrlfromYoutube(val)
    print("Running in /lofiBackend route flask")
    export_to_csv(parentVideoTitle, returnTimeStamp, url)
    return "Your song was logged to database :)"


def export_to_csv(parentTitle, userTime, link):
    filePath = os.environ.get("FILE_PATH")
    file_exists = os.path.exists(filePath)
    today = str(date.today())
    data = [parentTitle, userTime, link[0], link[1], today]
    if file_exists:
        with open(filePath, mode="r+") as csvfile:
            isLinkPresent = False
            reader = csv.reader(csvfile)
            writer = csv.writer(csvfile)
            for content in reader:
                if content[2] == link[0]:
                    isLinkPresent = True
                    # with open(filePath, "a+", newline="", encoding="utf-8") as csvfile:
                    print("Track already exists from a previous entry")
            if not isLinkPresent:
                print("Track info not present so printing it ")
                writer.writerow(data)

    if not file_exists:
        with open(filePath, "a+", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ["Parent Vid Title", "UserStamp", "Link", "Backup Link, Date added"]
            )
            writer.writerow(data)


def possibleMissingTrackInfo(matchStr):
    return not matchStr.strip() or not any(matchStr.isalnum() for iter in matchStr)
    # return true is it's empty or there are no alpha bumeric characters because, iter has to be false for all of them


def fetchYoutubeUrl(trackName):
    customHeaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82"
    }

    url = "https://www.google.com/search"

    parameters = {
        "q": "lofi " + trackName,
        "tbm": "vid",  # This tells Google to search for videos
    }

    resultPage = requests.get(url, headers=customHeaders, params=parameters)
    # print(resultPage.url)
    resultPage.raise_for_status()
    # resultPage.encoding = "utf-8"
    soup = BeautifulSoup(resultPage.text, "html.parser")
    search_result = soup.find(id="search")
    print("was")
    if not search_result:
        print("No results or video links found")
        # video_links.append("No link found :(")
    video_links = search_result.find_all("a")
    for link in video_links:
        print(link.get("href", ""))
        # if "https://soundcloud.com/" in link.get("href", ""):
        #   return link.get("href", "")


def fectchUrlfromYoutube(trackName):
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key
    )

    request = youtube.search().list(
        part="snippet",
        maxResults=3,
        q="lofi " + trackName,
        type="video",
        regionCode="CA",
        order="relevance",
        relevanceLanguage="en",  # Prioritizes English results.
        safeSearch="none",  # Adjust safe search settings if needed.
        videoDefinition="any",  # Optionally restrict to HD or any quality.
    )

    response_data = request.execute()
    fetchedLinks = []
    for i in range(2):
        videoId = response_data["items"][i]["id"]["videoId"]
        # print(f"Link is https://www.youtube.com/watch?v={videoId}")
        fetchedLinks.append(f"https://www.youtube.com/watch?v={videoId}")
    return fetchedLinks
    # print((response_data))

    # for url in response_data:
    #    print(response_data[items][id][videoId])


def get_vidDesc(video_id_value):
    api_url = (
        "https://www.googleapis.com/youtube/v3/videos?"
        "part=snippet&id={video_id}&key={api_key}"
    ).format(video_id=video_id_value, api_key=api_key)
    try:
        response = requests.get(api_url, timeout=1)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")

    data = response.json()
    # print(data)
    # print(type(data))
    # data mirrors the dict from response json
    video_title = data["items"][0]["snippet"]["title"]
    video_description = data["items"][0]["snippet"]["description"]
    # obtains the description from the key snippet
    # json response layout here : https://developers.google.com/youtube/v3/docs/videos#resource-representation
    return video_title, video_description


trackIndex = []


def desc_parser(video_description):
    # regex the entire description line by line
    # look for [HH]:[MM]:[SS] or [MM]:[SS]
    # export the line name of the title right next it.
    print("parser functions")
    pattern = re.compile("(\d{1,2}:\d{2}(?::\d{2})?)")
    video_description = re.sub(r"\r\n?", "", video_description)
    # =lines = [line.strip() for line in video_description.splitlines()]
    lines = video_description.splitlines()
    # BUG https://www.youtube.com/watch?v=j4Zxq6hwAfo, inconsistent new lines
    # for i in lines:
    #   print(f"new line<->{i}")
    # print(lines)

    # inefficient because we are going to search for each timestamp in all the lines, makes i O(n^2)
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # if line == "":
        #   i += 1
        #   continue|

        # print(f"New line after strip ---- {line}")
        match = pattern.search(line)

        if match:
            timestamp = match.group(1)
            trackExtract = line[match.end() :].strip()
            # print(f"extract line--- {trackExtract}")
            if trackExtract == "":
                # clean it and use it other wise move to the next line and skip this i, assuming next line has track info only
                if i < len(lines) - 1:
                    # it could quit literally be the last line -- https://www.youtube.com/watch?v=SXQeyudFe-g&t=1s
                    line = lines[i + 1]
                    trackExtract = line.strip()
            print(f"final line--- {trackExtract}")
            trackClean = re.sub(r"^\W+|\W+$", "", trackExtract)
            # print(f"clean line--- {trackClean}")
            # to clean any artifacts before the actual track info such as "-", "*", or whitespace, anything that was used as a separator in the description
            trackIndex.append((timestamp, trackClean))
        i += 1
    return trackIndex
    # print(bool(trackIndex))
    # print(type(trackIndex[0][1]))


def convertToTimeObj(timeStr):
    try:
        trackStamp = datetime.strptime(timeStr, "%H:%M:%S")
    except ValueError:
        trackStamp = datetime.strptime(timeStr, "%M:%S")
    print(trackStamp)
    return trackStamp
    # print(f"timestamp hours {trackStamp.minute} and mins {trackStamp.second} ")


def clickTrackPicker(userStampStr):
    userStamp = convertToTimeObj(userStampStr)
    isLastTrack = True
    for index, timestamp_iter in enumerate(trackIndex):
        trackStamp = convertToTimeObj(timestamp_iter[0])
        # if bool stays true that means we never had timestamp greater than userstamp
        # this means the userStamp was from the last track
        # otherwise this bool changes to false if we find something
        if userStamp < trackStamp:
            isLastTrack = False
            return trackIndex[index - 1]
    if isLastTrack == True:
        return trackIndex[-1]


# I am posting the links and now need to grab it from the webpage and post the link for the py server  at the back

if __name__ == "__main__":
    # run app in debug mode on port 8080
    print("Running before flask")
    app.run(debug=True, port=8080)
