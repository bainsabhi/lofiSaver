import requests
import csv
import os
from dotenv import load_dotenv
from apiclient.discovery import build
import re
from datetime import datetime, date, timedelta
import googleapiclient.discovery
from flask import Flask, request
from flask_cors import CORS

load_dotenv()
api_key = os.environ.get("API_KEY")
api_service_name = "youtube"
api_version = "v3"

app = Flask(__name__)
CORS(app)

global trackIndex
trackIndex = []


@app.route("/lofiBackend")
def processRequest():
    trackIndex.clear()
    videoUrlId = request.args.get("videoId")
    userTimeStamp = request.args.get("timestamp", type=(float))
    userTimeStamp = int(userTimeStamp)
    userTimeStamp = str(timedelta(seconds=userTimeStamp))
    video_info = get_vidDesc(videoUrlId)
    parentVideoTitle = video_info[0]
    parentVideoDesc = video_info[1]
    parsedDesc = desc_parser(parentVideoDesc)
    if bool(parsedDesc) == False:
        # description is empty and we are returning early
        return "No description with timestamps"
    returnTimeStamp = click_track_picker(userTimeStamp)
    val = returnTimeStamp[1]
    # returnTimeStamp[0] is timestamp and [1] is title
    url = fetch_url_from_youtube(val)
    if not url:
        return "No results were found for your track, sowwi :("
    export_to_csv(parentVideoTitle, returnTimeStamp, url)
    return "Your song was logged to database :)"


def export_to_csv(parentTitle, userTime, link):
    filePath = os.environ.get("FILE_PATH")
    fileExists = os.path.exists(filePath)
    today = str(date.today())
    # incase we only find just one result ( rare but possible, specially when descriptions have artifacts )
    link2 = "MISSING SECOND LINK, SOWWI"
    if len(link) > 1:
        link2 = link[1]
    data = [parentTitle, userTime, link[0], link2, today]
    if fileExists:
        with open(filePath, mode="r+") as csvfile:
            isLinkPresent = False
            reader = csv.reader(csvfile)
            writer = csv.writer(csvfile)
            for content in reader:
                if content[2] == link[0]:
                    isLinkPresent = True
            if not isLinkPresent:
                writer.writerow(data)

    if not fileExists:
        with open(filePath, "a+", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ["Parent Vid Title", "UserStamp", "Link", "Backup Link, Date added"]
            )
            writer.writerow(data)


def fetch_url_from_youtube(trackName):
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key
    )

    request = youtube.search().list(
        part="snippet",
        maxResults=3,
        q=trackName,
        type="video",
        regionCode="CA",
        order="relevance",
        relevanceLanguage="en",  # Prioritizes English results.
        safeSearch="none",  # Adjust safe search settings if needed.
        videoDefinition="any",  # Optionally restrict to HD or any quality.
    )

    fetchedLinks = []
    response_data = request.execute()
    totalResults = response_data["pageInfo"]["totalResults"]
    totalResults = min(totalResults, 2)
    if not totalResults:
        return fetchedLinks
    for i in range(totalResults):
        videoUrlId = response_data["items"][i]["id"]["videoId"]
        fetchedLinks.append(f"https://www.youtube.com/watch?v={videoUrlId}")
    return fetchedLinks


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

    video_title = data["items"][0]["snippet"]["title"]
    video_description = data["items"][0]["snippet"]["description"]
    # obtains the description from the key snippet
    # json response layout here : https://developers.google.com/youtube/v3/docs/videos#resource-representation
    return video_title, video_description


def desc_parser(video_description):
    # regex the entire description line by line
    # look for [HH]:[MM]:[SS] or [MM]:[SS]

    pattern = re.compile("(\d{1,2}:\d{2}(?::\d{2})?)")
    video_description = re.sub(r"\r\n?", "", video_description)
    lines = video_description.splitlines()

    # inefficient because we are going to search for each timestamp in all the lines, makes i O(n^2)
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        match = pattern.search(line)

        if match:
            timestamp = match.group(1)
            trackExtract = line[match.end() :].strip()
            if not trackExtract:
                # try the end of the string because the match could be placed at the end.
                trackExtract = line[: match.start()].strip()
                # try the end of the string because the match could be placed at the end.
            if trackExtract == "":
                # clean it and use it otherwise move to the next line and skip this i, assuming next line has track info only
                if i < len(lines) - 1:
                    # it could literally be the last line
                    line = lines[i + 1]
                    trackExtract = line.strip()
            trackClean = re.sub(r"^\W+|\W+$", "", trackExtract)
            # to clean any artifacts before the actual track info such as "-", "*", or whitespace, anything that was used as a separator in the description
            trackIndex.append((timestamp, trackClean))
        i += 1
    return trackIndex


def convert_to_time_obj(timeStr):
    try:
        trackStamp = datetime.strptime(timeStr, "%H:%M:%S")
    except ValueError:
        trackStamp = datetime.strptime(timeStr, "%M:%S")
    return trackStamp


def click_track_picker(userStampStr):
    userStamp = convert_to_time_obj(userStampStr)
    isLastTrack = True
    for index, timestamp_iter in enumerate(trackIndex):
        trackStamp = convert_to_time_obj(timestamp_iter[0])
        # if bool stays true that means we never had timestamp greater than userstamp
        # this means the userStamp was from the last track
        # otherwise this bool changes to false if we find something
        if userStamp < trackStamp:
            isLastTrack = False
            return trackIndex[index - 1]
    if isLastTrack == True:
        return trackIndex[-1]


if __name__ == "__main__":
    # run app in debug mode on port 8080
    app.run(debug=False, port=8080)
