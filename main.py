import os

from urllib import response
from dotenv import load_dotenv
from googleapiclient.discovery import build


from utils.comments import process_comments, make_csv

load_dotenv()
API_KEY = os.getenv("API_KEY")

youtube = build("youtube", "v3", developerKey=API_KEY)

def comment_threads(channelID, to_csv=False):
    
    comments_list = []
    
    request = youtube.commentThreads().list(
        part='id,replies,snippet',
        videoId=channelID,
    )

    response = request.execute()
    comments_list.extend(process_comments(response['items']))

    # if there is nextPageToken, then keep calling the API
    while response.get('nextPageToken', None):
        request = youtube.commentThreads().list(
            part='id,replies,snippet',
            videoId=channelID,
            pageToken=response['nextPageToken']
        )
        response = request.execute()
        comments_list.extend(process_comments(response['items']))
        

    print(f"Finished fetching comments for {channelID}. {len(comments_list)} comments found.")
    
    if to_csv:
        make_csv(comments_list, channelID)
    
    return comments_list

if __name__ == '__main__':
    pyscriptVidId = 'Qo8dXyKXyME'
    channelId = '1fuau2Idip8'
    # channelId = 'dhruvrathee'

    response = comment_threads(channelId, to_csv=True)
    
    print(response)