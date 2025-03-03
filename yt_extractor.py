import yt_dlp

ydl = yt_dlp.YoutubeDL()

def get_video_infos(url):
    with ydl:
        results = ydl.extract_info(url, download=False)
        
    if 'entries' in results:
        return results['entries'][0]
    return results

def get_audio_url(video_info):
    for f in video_info['formats']:
        if f['ext'] == 'm4a':
            return f['url']
    
if __name__ == '__main__':
    url = 'https://youtu.be/eu9krITz6NQ?si=isWFmr7Fz5GzG-S5'
    video_info = get_video_infos(url)
    audio_url = get_audio_url(video_info)
    print(audio_url)
    