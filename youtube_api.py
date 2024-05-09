from googleapiclient.discovery import build
from settings import API_KEY,DEFAULT_COUNTRY

def build_youtube_client():
    return build('youtube', 'v3', developerKey=API_KEY)

def search_videos(query, max_results=50, page_token=None):
    """Searches for videos on YouTube based on a query.

    Args:
        query (str): The search query.
        max_results (int): Maximum number of results to retrieve.
        page_token (str): Token for page of results to retrieve.

    Returns:
        dict: A dictionary containing the items and the next page token.
    """
    youtube = build_youtube_client()
    response = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results,
        pageToken=page_token
    ).execute()
    return {
        'items': response.get('items', []),
        'nextPageToken': response.get('nextPageToken')
    }

def get_channel_details(channel_id):
    """Retrieves details about a specific YouTube channel.
    
    Args:
        channel_id (str): The ID of the channel to retrieve details for.
    
    Returns:
        dict: A dictionary containing channel details.
    """
    youtube = build_youtube_client()
    response = youtube.channels().list(
        part='snippet,statistics,brandingSettings',
        id=channel_id
    ).execute()
    if response['items']:
        item = response['items'][0]
        return {
            'username': item['snippet']['title'],
            'subscribers': item['statistics'].get('subscriberCount', 'N/A'),
            'views': item['statistics'].get('viewCount', 'N/A'),
            'videoCount': item['statistics'].get('videoCount', 'N/A'),
            'link': f'https://www.youtube.com/channel/{channel_id}',
            'country': item['brandingSettings']['channel'].get('country', 'N/A')
        }
    return None

