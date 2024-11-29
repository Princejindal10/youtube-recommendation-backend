from flask import Flask, jsonify
from flask_cors import CORS
from authenticator import authenticate_user
from googleapiclient.discovery import build

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow all cross-origin requests

def get_recommendations(credentials):
    youtube = build('youtube', 'v3', credentials=credentials)

    # Step 1: Get recent activities (videos the user interacted with)
    activities = youtube.activities().list(
        part='snippet,contentDetails',
        mine=True,
        maxResults=15  # Increased to 15 recommendations
    ).execute()

    recommendations = []

    # Fetch activities-based recommendations (actual videos the user interacted with)
    for item in activities['items']:
        title = item['snippet']['title']
        # Check if it's an upload activity (e.g., video uploaded by the user, video watched, liked, etc.)
        if 'upload' in item['contentDetails']:
            video_id = item['contentDetails']['upload']['videoId']
            thumbnail_url = item['snippet']['thumbnails']['high']['url']  # Get high-quality thumbnail
            recommendations.append({
                'title': title,
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'thumbnail': thumbnail_url
            })

    # If activities don't provide enough recommendations, use subscriptions
    if len(recommendations) < 15:
        # Step 2: Get user's subscriptions and recommend recent videos from those channels
        subscriptions = youtube.subscriptions().list(
            part='snippet',
            mine=True,
            maxResults=20  # Increased to 20 subscriptions
        ).execute()

        # Fetch video recommendations from the subscriptions' channels
        for item in subscriptions['items']:
            channel_id = item['snippet']['resourceId']['channelId']
            # Fetch videos from the subscription's channel
            channel_videos = youtube.search().list(
                part='snippet',
                channelId=channel_id,
                order='date',  # To get the latest videos
                maxResults=5  # Increased to 5 latest videos from the channel
            ).execute()

            for video_item in channel_videos['items']:
                # Check if it's a video item (could also be a playlist or other type)
                if 'videoId' in video_item['id']:
                    video_title = video_item['snippet']['title']
                    video_id = video_item['id']['videoId']
                    thumbnail_url = video_item['snippet']['thumbnails']['high']['url']  # Get high-quality thumbnail
                    recommendations.append({
                        'title': video_title,
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'thumbnail': thumbnail_url
                    })

            # Stop if enough recommendations are found
            if len(recommendations) >= 15:
                break
    
    return recommendations

@app.route('/api/recommendations', methods=['GET'])
def recommendations():
    print("Authenticating user...")  # Debug statement
    credentials = authenticate_user()
    print("User authenticated.")  # Debug statement
    
    recommendations = get_recommendations(credentials)
    
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))