from youtube_api import search_videos, get_channel_details
from settings import DEFAULT_COUNTRY, DEFAULT_QUERY
import pandas as pd
import datetime
from slugify import slugify
import sys
import io

# Thay đổi mã hóa toàn cục cho stdout để hỗ trợ UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', errors='ignore')

def main():
    country = DEFAULT_COUNTRY
    query = DEFAULT_QUERY
    full_query = f"{query} {country}"
    channels = {}
    page_token = None

    try:
        while True:
            result = search_videos(full_query, max_results=50, page_token=page_token)
            videos = result['items']
            if not videos:
                print("No more videos found.", file=sys.stdout)
                break

            for video in videos:
                channel_id = video['snippet']['channelId']
                if channel_id not in channels:
                    details = get_channel_details(channel_id)
                    if details:
                        channels[channel_id] = details
                        print(f"Added channel: {details}", file=sys.stdout)
                    else:
                        print(f"Details not found for channel ID {channel_id}", file=sys.stdout)

            page_token = result.get('nextPageToken')
            if not page_token:
                print("No more pages to fetch.", file=sys.stdout)
                break

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

    if channels:
        df = pd.DataFrame.from_dict(channels, orient='index')
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{slugify(query)}_{slugify(country)}_{timestamp}.xlsx"
        df.to_excel(filename, index=False)
        print(f"Channels have been saved to '{filename}'.", file=sys.stdout)
    else:
        print("No channels were added, thus no Excel file was created.", file=sys.stdout)

if __name__ == '__main__':
    main()