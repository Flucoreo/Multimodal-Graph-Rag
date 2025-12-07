from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript(url: str):
    """
    Extract the transcript from a youtube video
    """

    ytt_api = YouTubeTranscriptApi()

    # extract the video ID from url
    video_id = ""
    for i in range(len(url)-1,0,-1):
        if url[i] == "=":
            break

        video_id += url[i]
    video_id = video_id[::-1]

    try:
        fetched_transcript = ytt_api.fetch(video_id)
    except Exception:
        print("Invalid video URL")
        return

    return fetched_transcript


def main():

    # get the video url from the user
    video_url = input("Youtube Video URL: ")
    if not video_url.startswith("https://www.youtube.com/watch?v="):
        print("Invalid url")
        return

    transcript = get_transcript(video_url)
    for snippet in transcript:
        print(snippet.text)

    #https://www.youtube.com/watch?v=yqrp2uK9LY4

if __name__ == "__main__":
    main()
