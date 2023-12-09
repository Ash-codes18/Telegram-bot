from pyrogram import Client, filters
from pyrogram.types import Message
from anime_api.apis import NekosAPI
from urllib.parse import urljoin
from bardapi import BardCookies
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tpblite import TPB
from io import BytesIO
import asyncio
import subprocess
import random
import redgifs
import time
import yt_dlp
import os
import subprocess
import requests

#Enter your bot credentials
api_id = 123456
api_hash = 'your-api-hash'
bot_token = 'your-bot-token'

#YouTube Data API v3 key
api_key = 'your-yt-api-key'

#Spotify API credentials
client_id = 'your-client=id'
client_secret = 'your-client-secret'

#Unsplash API access key
UNSPLASH_ACCESS_KEY = 'your-unsplash-api-key'


#Pexels API key
PEXELS_API_KEY = 'your-pexels-api-key'

api = NekosAPI()
BASE_URL = "https://api.waifu.pics"


ANIME_COMMANDS = [
    "waifu", "neko", "shinobu", "megumin", "bully", "cuddle", "cry", "hug", "awoo", "kiss",
    "lick", "pat", "smug", "bonk", "yeet", "blush", "smile", "wave", "highfive", "handhold",
    "nom", "bite", "glomp", "slap", "kill", "kick", "happy", "wink", "poke", "dance", "cringe"
]


# You can use any domain of the piratebay
tpb = TPB('https://tpb.party')



# Replace with your Google Custom Search Engine API key
GAPI_KEY = "your-api-key"

# Replace with your Google Custom Search Engine ID
SEARCH_ENGINE_ID = "your-search-engine-id"
BING_ENGINE_ID = "your-search-engine-id"
YANDEX_ENGINE_ID="your-search-engine-id"
DDG_ENGINE_ID="your-search-engine-id"
WEB_ENGINE_ID="your-search-engine-id"


#BARD MODULE NOT WORKING FOR MOST CASES

#Enter Any cookie values you want to pass to the session object.
# COOKIE_DICT = {
#     "__Secure-1PSID": "",
#     "__Secure-1PSIDTS": "",
#     "__Secure-1PSIDCC": "",
# }

# bard = BardCookies(cookie_dict=COOKIE_DICT)


app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)



KEYWORD = 0
user_states = {}


audio_ydl = yt_dlp.YoutubeDL({
    "format": "bestaudio/best",
    "outtmpl": "%(title)s.mp3",
    "extract_flat": True,
    "youtube_api_key": api_key,
    "noplaylist": False
})


video_ydl = yt_dlp.YoutubeDL({
    "format": "best",
    "outtmpl": "%(title)s.%(ext)s",
    "allow_playlist_files": True
})


def send_message(chat_id, message):
    app.send_message(chat_id, message)


def send_upload_progress(chat_id, message_id):
    async def callback(current, total):
        progress = (current / total) * 100
        await app.edit_message_text(chat_id, message_id, text=f"File Upload Progress: {progress:.2f}%")

    return callback


def download_audio(url,chat_id):
    send_message(chat_id, "Audio download started...")
    with audio_ydl as ydl:
        info = ydl.extract_info(url)
        filename = ydl.prepare_filename(info)
        send_message(chat_id, "Audio download finished!")
        return filename


def download_video(url,chat_id):
    send_message(chat_id, "Video download started...")
    with video_ydl as ydl:
        info = ydl.extract_info(url)
        filename = ydl.prepare_filename(info)
        send_message(chat_id, "Video download finished!")
        return filename


# Not used but kept here for future purposes
def convert_to_mp3(filename,chat_id):
    if filename.endswith('.mp3'):
        return filename

    output_filename = f"{os.path.splitext(filename)[0]}.mp3"
    subprocess.run(['ffmpeg', '-i', filename, '-codec:a', 'libmp3lame', '-q:a', '2', output_filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if os.path.exists(output_filename):
        send_message(chat_id, "Audio conversion finished!")
        return output_filename
    else:
        return None


def search_youtube(query):
    results = audio_ydl.extract_info(f"ytsearch5:{query}", download=False)
    return results.get("entries", [])


def get_random_image(category, image_type):
    url = f"{BASE_URL}/{image_type}/{category}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "url" in data:
            return data["url"]
        elif "files" in data and len(data["files"]) > 0:
            return data["files"][0]
    return None


def fetch_image(category, image_type):
    image_url = get_random_image(category, image_type)
    return image_url


def extract_youtube_music_url(output):
    lines = output.split('\n')  
    youtube_music_url = None

    for line in lines:
        if line.startswith('Downloaded') and 'music.youtube.com' in line:
            parts = line.split(': ')
            if len(parts) > 1:
                youtube_music_url = parts[-1].strip()  
                break

    return youtube_music_url





@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text('**Hello, I am a bot that can perform various tasks. Use these commands to know my functionalities**:\n\n/general - __To get the most useful commands__\n/anime - __To get all anime related commands__\n/subreddit - __to get all reddit related commands__\n/browse - __To get all the web searching commands__')


@app.on_message(filters.command("general"))
async def start_command(client, message):
    await message.reply_text('**Audio** :\n/audio <url>  - Download an audio from the given URL\n/song <song-name> - Downloads the song from YouTube and sends it.\n/spotdl <spotify-url>  - searches spotify song on yt music and sends it.\n/spotify <query> - Searches spotify and returns top 10 results\n/search <query>  - Search YouTube and return the top 5 results\n\n**Video** :\n/vid <url>  - Download a video from the given URL\n/vpex <query> - sends 5 stocks vids/gifs from vimeo based on query\n/search <query> - Search YouTube and return the top 5 results\n\n**Images** :\n/unsplash <keywords>  - Searches Unsplash for an image based on the query\n/ipex <query>  - sends 5 stock images based on query\n\n**Github** :\n/clone <github-repo-url>  - Clones a github repo and sends it.\n/repo <query> - Searches github and return top 10 repos based on query.\n\n**Torrents** :\n/pbay <query>  - Searches the piratebay and returns torrents.')



@app.on_message(filters.command("subreddit"))
async def start_command(client, message):
    await message.reply_text('/meme - Fetches a random meme from a random subreddit\n/manymeme - An extension of `/meme` that fetches 10 memes at once.\n/reddit - fetches random (mostly nsfw) things from reddit.\n/mreddit - An extension of `/reddit` for fetching 10 results at once.')


@app.on_message(filters.command("browse"))
async def start_command(client, message):
    await message.reply_text('/web <query> - Searches the entire web and returns top 10 results\n/google <query> - Searches Google and returns top 10 results\n/bing <query> - Searches Bing and returns top 10 results\n/yandex <query> - Searches Yandex and returns top 10 results\n/ddg <query> - Searches Duck Duck Go and returns top 10 results\n/img <query> - Searches the entire web and returns top 10 images.\n/gimg <query> - Searches Google and returns top 10 images\n/bimg <query> - Searches Bing and returns top 10 images\n/yimg <query> - Searches Yandex and returns top 10 images\n/dimg <query> - Searches Duck DUck Go and returns top 10 images\n')




@app.on_message(filters.command("audio"))
def handle_audio_command(client, message):
    url = message.text.split(" ", 1)[1]
    chat_id = message.chat.id

    
    audio_filename = download_audio(url, chat_id)

    # mp3_filename = convert_to_mp3(audio_filename, chat_id)

    send_message(chat_id, "Uploading audio...")
    app.send_audio(chat_id, audio_filename)
    send_message(chat_id, "Audio upload finished!")
    os.remove(audio_filename)  
    # os.remove(mp3_filename)



@app.on_message(filters.command("vid"))
def handle_video_command(client, message):
    url = message.text.split(" ", 1)[1]
    chat_id = message.chat.id

    video_filename = download_video(url, chat_id)

    send_message(chat_id, "Uploading video...")
    app.send_video(chat_id, video_filename)
    send_message(chat_id, "Video upload finished!")
    os.remove(video_filename)



@app.on_message(filters.command("search"))
async def search_command(client, message):
    try:
        query = message.text.split(" ", 1)[1]
        results = search_youtube(query)

        for idx, result in enumerate(results, start=1):
            title = result.get("title")
            url = result.get("url")  
            if url:  
                await message.reply_text(f"{idx}. {title}\n{url}")
            else:
                await message.reply_text(f"{idx}. {title}\nURL not found")

    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")
        
        


async def send_status(chat_id, status):
    await app.send_message(chat_id, status)


@app.on_message(filters.command("song"))
async def song_command(client, message):
    try:
        chat_id = message.chat.id
        await send_status(chat_id, "Searching for the song...")
        query = message.text.split(" ", 1)[1]
        results = search_youtube(query)

        if results:
            top_result = results[0]
            audio_url = top_result["url"]

            try:
                await send_status(chat_id, "Song Found! Starting download...")
                filename = download_audio(audio_url, chat_id)

                if filename:
                    # await send_status(chat_id, "Download complete. Converting to MP3...")

                    # mp3_filename = convert_to_mp3(filename,chat_id)

                    # if mp3_filename:
                    chat_id = message.chat.id
                    await send_status(chat_id, "Uploading audio...")

                    await app.send_audio(chat_id, filename)

                    await send_status(chat_id, "Audio upload finished!")
                    os.remove(filename)
                        # os.remove(mp3_filename)
                    # else:
                    #     await send_status(chat_id, "Error: Unsupported file format")
                else:
                    await send_status(chat_id, "Error: Unsupported file format")
            except Exception as e:
                await send_status(chat_id, f"Error: {str(e)}")
        else:
            await send_status(chat_id, "No results found for the provided query.")
    except Exception as e:
        await send_status(chat_id, f"Error: {str(e)}")



@app.on_message(filters.command("spotdl"))
async def spotdl_command(client, message):
    try:
        query = " ".join(message.command[1:])
        if not query:
            await message.reply("Please provide a Spotify or YouTube link.")
            return

        await app.send_message(message.chat.id, "Downloading...")

        process = subprocess.Popen(
            f"python -m spotdl {query}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        output, error = process.communicate()

        if error:
            await app.send_message(message.chat.id, f"Error: {error}")
        else:
            file_name = ""
            for filename in os.listdir("."):
                if filename.endswith(".mp3"):
                    file_name = filename
                    break

            if file_name:
                await app.send_message(message.chat.id, "Download Finished!, Uploading...")
                with open(file_name, "rb") as file:
                    await app.send_audio(message.chat.id, file)
                os.remove(file_name)  # Delete the file after sending
                await app.send_message(message.chat.id, "Downloaded and sent!")

    except Exception as e:
        await send_status(message.chat.id, f"Error: {str(e)}")


@app.on_message(filters.command("spotify"))
async def spotify_search(client, message):
    
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    try:
        query = " ".join(message.command[1:])
        if not query:
            await message.reply("Please provide a search query for Spotify.")
            return

        await app.send_message(message.chat.id, "Searching on Spotify...")

        
        results = sp.search(q=query, limit=10)  

        if results:
            await app.send_message(message.chat.id, "Search Results from Spotify:")
            for idx, item in enumerate(results['tracks']['items'], start=1):
                await app.send_message(
                    message.chat.id,
                    f"{idx}. **Name**: `{item['name']}`\n **Artists**: `{', '.join([artist['name'] for artist in item['artists']])}`\n**Album**: `{item['album']['name']}`\n**URL**: {item['external_urls']['spotify']}"
                )
        else:
            await app.send_message(message.chat.id, "No results found on Spotify.")
    except Exception as e:
        await app.send_message(message.chat.id, f'An error occurred: {str(e)}')

        



@app.on_message(filters.command("anime"))
def anime_commands_handler(client, message):
    
    sfw_description = "/cat: Sends a random catgirl image.\n"
    for command in ANIME_COMMANDS:
        sfw_description += f"/{command}: sends a random {command} image.\n"
    sfw_description += "\nUsage: Type any of the above commands to get a random image of that category."


    quotes_description = "Quote Commands:\n\n"
    quotes_description += "/quote: Sends a random anime quote.\n"
    quotes_description += "/mquote: Sends multiple anime quotes."

    text = f"{sfw_description}\n\n{quotes_description}"
    client.send_message(message.chat.id, text)



@app.on_message(filters.command("quote"))
def get_random_quote(client, message):
    try:
        response = requests.get("https://animechan.xyz/api/random")
        if response.status_code == 200:
            quote = response.json()
            formatted_quote = f"**Anime**: `{quote['anime']}`\n**Character**: `{quote['character']}`\n**Quote**: __\"{quote['quote']}\"__"
            app.send_message(message.chat.id, formatted_quote)
        else:
            app.send_message(message.chat.id, "Failed to fetch a quote. Try again later.")
    except Exception as e:
        app.send_message(message.chat.id, f"An error occurred: {str(e)}")



@app.on_message(filters.command("mquote"))
def get_many_quotes(client, message):
    try:
        response = requests.get("https://animechan.xyz/api/quotes")
        if response.status_code == 200:
            quotes = response.json()
            formatted_quotes = "\n\n".join([f"**Anime**: `{quote['anime']}`\n**Character**: `{quote['character']}`\n**Quote**: __\"{quote['quote']}\"__" for quote in quotes])
            app.send_message(message.chat.id, formatted_quotes)
        else:
            app.send_message(message.chat.id, "Failed to fetch quotes. Try again later.")
    except Exception as e:
        app.send_message(message.chat.id, f"An error occurred: {str(e)}")
        


@app.on_message(filters.command(ANIME_COMMANDS))
def image_fetch_handler(client, message):
    command = message.command[0]
    image_url = fetch_image(command, "sfw") 
    if image_url:
        client.send_photo(message.chat.id, photo=image_url)
    else:
        client.send_message(message.chat.id, "Failed to fetch the image.")




@app.on_message(filters.command("cat"))
async def catgirl_command(client, message):
    try:
        
        image = api.get_random_image(categories=["catgirl"])

        await app.send_photo(message.chat.id, photo=image.url)
    except Exception as e:
        await app.send_message(message.chat.id, f'An error occurred: {str(e)}')




@app.on_message(filters.command("meme"))
def handle_meme_command(client, message):
    api_url = "https://meme-api.com/gimme"

    response = requests.get(api_url)

    if response.status_code == 200:
        meme_data = response.json()

        title = meme_data['title']
        meme_url = meme_data['url']

        meme_file = requests.get(meme_url)

        if meme_file.status_code == 200:
            file_extension = meme_url.split('.')[-1]
            file_name = f"{title}.{file_extension}"

            with open(file_name, 'wb') as file:
                file.write(meme_file.content)

            # send_message(message.chat.id, "Uploading meme...")
            if file_extension in ['png', 'jpg', 'gif']:
                app.send_photo(message.chat.id, file_name, caption=title)
            elif file_extension in ['mp4', 'gifv']:
                app.send_video(message.chat.id, file_name, caption=title)
            # send_message(message.chat.id, "Meme upload finished!")

            os.remove(file_name)

        else:
            send_message(message.chat.id, "Failed to download the meme.")
    else:
        send_message(message.chat.id, "Failed to fetch the meme from the API.")





@app.on_message(filters.command("manymeme"))
def handle_many_meme_command(client, message):

    api_url = "https://meme-api.com/gimme/5"

    response = requests.get(api_url)

    if response.status_code == 200:
        memes_data = response.json()

        memes_list = memes_data['memes']

        for meme in memes_list:
            title = meme['title']
            meme_url = meme['url']

  
            meme_file = requests.get(meme_url)

            if meme_file.status_code == 200:
                
                file_extension = meme_url.split('.')[-1]
                file_name = f"{title}.{file_extension}"

                with open(file_name, 'wb') as file:
                    file.write(meme_file.content)

                # send_message(message.chat.id, "Uploading meme...")
                if file_extension in ['png', 'jpg', 'gif']:
                    app.send_photo(message.chat.id, file_name, caption=title)
                elif file_extension in ['mp4', 'gifv']:
                    app.send_video(message.chat.id, file_name, caption=title)
                # send_message(message.chat.id, "Meme upload finished!")
                os.remove(file_name)

            else:
                send_message(message.chat.id, f"Failed to download the meme '{title}'.")

    else:
        send_message(message.chat.id, "Failed to fetch memes from the API.")




@app.on_message(filters.command("reddit"))
def handle_reddit_command(client, message):

    # Specify any subreddits of your choice
    subreddits = ["wholesomememes", "memes", "funny", "aww"] 


    selected_subreddit = random.choice(subreddits)

    api_url = f"https://meme-api.com/gimme/{selected_subreddit}"

    response = requests.get(api_url)

    if response.status_code == 200:
        meme_data = response.json()

        title = meme_data['title']
        meme_url = meme_data['url']

        meme_file = requests.get(meme_url)

        if meme_file.status_code == 200:
            file_extension = meme_url.split('.')[-1]
            file_name = f"{title}.{file_extension}"

            with open(file_name, 'wb') as file:
                file.write(meme_file.content)

            # send_message(message.chat.id, "Uploading meme...")
            if file_extension in ['png', 'jpg', 'gif']:
                app.send_photo(message.chat.id, file_name, caption=title)
            elif file_extension in ['mp4', 'gifv']:
                app.send_video(message.chat.id, file_name, caption=title)
            # send_message(message.chat.id, "Meme upload finished!")

            os.remove(file_name)

        else:
            send_message(message.chat.id, "Failed to download the meme.")
    else:
        send_message(message.chat.id, "Failed to fetch the meme from the API.")





@app.on_message(filters.command("mreddit"))
def handle_multiple_reddit_command(client, message):
    # Specify any subreddits you want
    subreddits = ["wholesomememes", "memes", "funny", "aww"]  

    memes_to_fetch = 5 #change according to your needs

    all_memes = []

    for _ in range(memes_to_fetch):

        selected_subreddit = random.choice(subreddits)
        api_url = f"https://meme-api.com/gimme/{selected_subreddit}"

        response = requests.get(api_url)

        if response.status_code == 200:
            meme_data = response.json()
            all_memes.append(meme_data)
        else:
            send_message(message.chat.id, f"Failed to fetch meme from {selected_subreddit}.")

    for meme_data in all_memes:
        title = meme_data['title']
        meme_url = meme_data['url']

        meme_file = requests.get(meme_url)

        if meme_file.status_code == 200:
            file_extension = meme_url.split('.')[-1]
            file_name = f"{title}.{file_extension}"

            with open(file_name, 'wb') as file:
                file.write(meme_file.content)

            # send_message(message.chat.id, "Uploading meme...")
            if file_extension in ['png', 'jpg', 'gif']:
                app.send_photo(message.chat.id, file_name, caption=title)
            elif file_extension in ['mp4', 'gifv']:
                app.send_video(message.chat.id, file_name, caption=title)
            send_message(message.chat.id, "Meme upload finished!")

            os.remove(file_name)

        else:
            send_message(message.chat.id, "Failed to download the meme.")





@app.on_message(filters.command("unsplash"))
async def unsplash_command(client, message):
    try:
        query = " ".join(message.command[1:])
        if query:
            response = requests.get(f'https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_ACCESS_KEY}')
            data = response.json()

            if 'results' in data:
                await app.send_message(message.chat.id, "Searching for images...")
                photos = data['results']
                if photos:
                    await app.send_message(message.chat.id, "Images found!, Uploading...")
                    for index, photo in enumerate(photos[:10], start=1):  # Send the first 5 images
                        image_url = photo['urls']['regular']
                        image_file = requests.get(image_url)
                        if image_file.status_code == 200:

                            await app.send_photo(message.chat.id, photo=image_url)
                        else:
                            await app.send_message(message.chat.id, "Failed to fetch image.")
                else:
                    await app.send_message(message.chat.id, "Can't find images for that keyword.")
            else:
                await app.send_message(message.chat.id, "Failed to get images.")
        else:
            await app.send_message(message.chat.id, "Please provide a keyword to search for images.")

    except Exception as e:
        await app.send_message(message.chat.id, f'An error occurred: {str(e)}')
        
        

@app.on_message(filters.command("ipex"))
async def ipex_command(client, message):
    try:
        keyword = " ".join(message.command[1:])
        if keyword:
            headers = {
                'Authorization': PEXELS_API_KEY,
            }
            params = {
                'query': keyword,
                'per_page': 5,
            }
            await app.send_message(message.chat.id, "Fetching Images...")
            response = requests.get('https://api.pexels.com/v1/search', headers=headers, params=params)
            data = response.json()
            photos = data.get('photos')
            if photos:
                await app.send_message(message.chat.id, "Images Found!, Uploading...")
                for photo in photos:
                    image_url = photo['src']['medium']
                    await app.send_photo(message.chat.id, photo=image_url)
            else:
                await app.send_message(message.chat.id, "No images found for the keyword.")
        else:
            await app.send_message(message.chat.id, "Please provide a keyword to search for images.")
    except Exception as e:
        await app.send_message(message.chat.id, f'An error occurred: {str(e)}')



@app.on_message(filters.command("vpex"))
async def vpex_command(client, message):
    try:
        keyword = " ".join(message.command[1:])
        if keyword:
            headers = {
                'Authorization': PEXELS_API_KEY,
            }
            params = {
                'query': keyword,
                'per_page': 5,
            }
            await app.send_message(message.chat.id, "Fetching Videos...")
            response = requests.get('https://api.pexels.com/videos/search', headers=headers, params=params)
            data = response.json()
            videos = data.get('videos')
            if videos:
                await app.send_message(message.chat.id, "Videos Found!, Uploading...")
                for video in videos:
                    video_url = video['video_files'][0]['link']
                    await app.send_video(message.chat.id, video_url)
            else:
                await app.send_message(message.chat.id, "No videos found for the keyword.")
        else:
            await app.send_message(message.chat.id, "Please provide a keyword to search for videos.")
    except Exception as e:
        await app.send_message(message.chat.id, f'An error occurred: {str(e)}')        



@app.on_message(filters.command("pbay"))
async def pirate_bay_command(client, message):
    try:
        search_query = " ".join(message.command[1:])
        if search_query:
            await app.send_message(message.chat.id, "Searching for torrents...")
            torrents = tpb.search(search_query)

            if torrents:
                await app.send_message(message.chat.id, f"Found {len(torrents)} torrents:")
                for torrent in torrents:
                    magnet_link = torrent.magnetlink  # Retrieve magnet link
                    info = (
                        f"**Title**: {torrent.title}\n"
                        f"**Uploader**: {torrent.uploader}\n"
                        f"**Category**: {torrent.category}\n"
                        f"**Seeders**: {torrent.seeds}\n"
                        f"**Leechers**: {torrent.leeches}\n"
                        f"**Upload Date**: {torrent.upload_date}\n"
                        f"**Filesize**: {torrent.filesize}\n"
                        f"**Magnet Link**: `{magnet_link}`\n"  # Send magnet link
                    )
                    await app.send_message(message.chat.id, info)
            else:
                await app.send_message(message.chat.id, "No torrents found for the keyword.")
        else:
            await app.send_message(message.chat.id, "Please provide a keyword to search for torrents.")
    except Exception as e:
        await app.send_message(message.chat.id, f'An error occurred: {str(e)}')




@app.on_message(filters.command("clone"))
async def clone_repo(client, message):
    try:
        
        url = " ".join(message.command[1:])
        

        if not url:
            await message.reply("Please provide a valid GitHub repository URL.")
            return

        
        zip_url = f"{url.rstrip('/')}/archive/refs/heads/main.zip"  # Assuming 'main' branch, adjust as needed
        

        response = requests.get(zip_url)
        
        if response.status_code == 200:
            
            await app.send_document(message.chat.id, document=response.content, file_name="repository.zip")
            await message.reply("Repository zip file sent!")
        else:
            await message.reply("Failed to fetch the repository zip file.")
            
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")
        
        
        

@app.on_message(filters.command("repo"))
async def search_github_repos(client, message):
    try:
        query = " ".join(message.command[1:])
        if not query:
            await message.reply("Please provide a search query for repositories.")
            return

        await app.send_message(message.chat.id, "Searching for GitHub repositories...")

        # GitHub API search request
        response = requests.get(f"https://api.github.com/search/repositories?q={query}&per_page=10")
        if response.status_code == 200:
            data = response.json()
            repos = data.get('items', [])

            if repos:
                await app.send_message(message.chat.id, "Top 10 GitHub Repositories:")
                for index, repo in enumerate(repos[:10], start=1):
                    repo_name = repo.get('full_name')
                    stars = repo.get('stargazers_count')
                    forks = repo.get('forks_count')
                    repo_url = repo.get('html_url')

                    await app.send_message(
                        message.chat.id,
                        f"{index}.  **Name**: `{repo_name}`\n **Stars**: `{stars}`\n**Forks**: `{forks}`\n**URL**: {repo_url}"
                    )
            else:
                await app.send_message(message.chat.id, "No repositories found for the query.")
        else:
            await app.send_message(message.chat.id, "Failed to fetch repositories.")
    except Exception as e:
        await app.send_message(message.chat.id, f'An error occurred: {str(e)}')




@app.on_message(filters.command("google"))
async def google_search(client, message):
    try:
        query = " ".join(message.command[1:])
        if not query:
            await message.reply("Please provide a search query.")
            return

        await app.send_message(message.chat.id, "Searching on Google...")

        response = requests.get(f"https://www.googleapis.com/customsearch/v1?key={GAPI_KEY}&cx={SEARCH_ENGINE_ID}&q={query}")
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])

            if items:
                await app.send_message(message.chat.id, "Top search results:")
                for index, item in enumerate(items[:10], start=1):
                    title = f"[{item.get('title')}]({item.get('link')})"
                    snippet = item.get('snippet')


                    await app.send_message(
                        message.chat.id,
                        f"{index}. {title}\n\n{snippet}",
                        disable_web_page_preview=False
                    )
            else:
                await app.send_message(message.chat.id, "No search results found.")
        else:
            await app.send_message(message.chat.id, "Failed to fetch search results.")
            
    except Exception as e:
        await app.send_message(message.chat.id, f"An error occurred: {str(e)}")
        
        

@app.on_message(filters.command("bing"))
async def bing_search(client, message):
    try:
        query = " ".join(message.command[1:])
        if not query:
            await message.reply("Please provide a search query.")
            return

        await app.send_message(message.chat.id, "Searching on Bing...")

        response = requests.get(f"https://www.googleapis.com/customsearch/v1?key={GAPI_KEY}&cx={BING_ENGINE_ID}&q={query}")
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])

            if items:
                await app.send_message(message.chat.id, "Top search results:")
                for index, item in enumerate(items[:10], start=1):
                    title = f"[{item.get('title')}]({item.get('link')})"
                    snippet = item.get('snippet')

                    await app.send_message(
                        message.chat.id,
                        f"{index}. {title}\n\n{snippet}",
                        disable_web_page_preview=False
                    )
            else:
                await app.send_message(message.chat.id, "No search results found.")
        else:
            await app.send_message(message.chat.id, "Failed to fetch search results.")
            
    except Exception as e:
        await app.send_message(message.chat.id, f"An error occurred: {str(e)}")
        
        
        
@app.on_message(filters.command("yandex"))
async def yandex_search(client, message):
    try:
        query = " ".join(message.command[1:])
        if not query:
            await message.reply("Please provide a search query.")
            return

        await app.send_message(message.chat.id, "Searching on Yandex...")

        response = requests.get(f"https://www.googleapis.com/customsearch/v1?key={GAPI_KEY}&cx={YANDEX_ENGINE_ID}&q={query}")
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])

            if items:
                await app.send_message(message.chat.id, "Top search results:")
                for index, item in enumerate(items[:10], start=1):
                    title = f"[{item.get('title')}]({item.get('link')})"
                    snippet = item.get('snippet')

                    await app.send_message(
                        message.chat.id,
                        f"{index}. {title}\n\n{snippet}",
                        disable_web_page_preview=False
                    )
            else:
                await app.send_message(message.chat.id, "No search results found.")
        else:
            await app.send_message(message.chat.id, "Failed to fetch search results.")
            
    except Exception as e:
        await app.send_message(message.chat.id, f"An error occurred: {str(e)}")


@app.on_message(filters.command("ddg"))
async def ddg_search(client, message):
    try:
        query = " ".join(message.command[1:])
        if not query:
            await message.reply("Please provide a search query.")
            return

        await app.send_message(message.chat.id, "Searching on DuckDuckGo...")

        response = requests.get(f"https://www.googleapis.com/customsearch/v1?key={GAPI_KEY}&cx={DDG_ENGINE_ID}&q={query}")
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])

            if items:
                await app.send_message(message.chat.id, "Top search results:")
                for index, item in enumerate(items[:10], start=1):
                    title = f"[{item.get('title')}]({item.get('link')})"
                    snippet = item.get('snippet')

                    await app.send_message(
                        message.chat.id,
                        f"{index}. {title}\n\n{snippet}",
                        disable_web_page_preview=False
                    )
            else:
                await app.send_message(message.chat.id, "No search results found.")
        else:
            await app.send_message(message.chat.id, "Failed to fetch search results.")
            
    except Exception as e:
        await app.send_message(message.chat.id, f"An error occurred: {str(e)}")

        

@app.on_message(filters.command("web"))
async def web_search(client, message):
    try:
        query = " ".join(message.command[1:])
        if not query:
            await message.reply("Please provide a search query.")
            return

        await app.send_message(message.chat.id, "Searching the web...")

        response = requests.get(f"https://www.googleapis.com/customsearch/v1?key={GAPI_KEY}&cx={WEB_ENGINE_ID}&q={query}")
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])

            if items:
                await app.send_message(message.chat.id, "Top search results:")
                for index, item in enumerate(items[:10], start=1):
                    title = f"[{item.get('title')}]({item.get('link')})"
                    snippet = item.get('snippet')

                    await app.send_message(
                        message.chat.id,
                        f"{index}. {title}\n\n{snippet}",
                        disable_web_page_preview=False
                    )
            else:
                await app.send_message(message.chat.id, "No search results found.")
        else:
            await app.send_message(message.chat.id, "Failed to fetch search results.")
            
    except Exception as e:
        await app.send_message(message.chat.id, f"An error occurred: {str(e)}")



        
        
@app.on_message(filters.command("img"))
async def image_search(client, message):
    try:
        query = " ".join(message.command[1:])
        if not query:
            await message.reply("Please provide a search query for images.")
            return

        await app.send_message(message.chat.id, "Searching for images...")

        response = requests.get(f"https://www.googleapis.com/customsearch/v1?key={GAPI_KEY}&cx={WEB_ENGINE_ID}&q={query}&searchType=image&num=10")
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])

            if items:
                await app.send_message(message.chat.id, "Top 10 image results:")
                for index, item in enumerate(items[:10], start=1):
                    image_url = item.get('link')

                    await app.send_photo(message.chat.id, photo=image_url)
            else:
                await app.send_message(message.chat.id, "No image results found.")
        else:
            await app.send_message(message.chat.id, "Failed to fetch image results.")
            
    except Exception as e:
        await app.send_message(message.chat.id, f"An error occurred: {str(e)}")


        
        
@app.on_message(filters.command("gimg"))
async def image_search(client, message):
    try:
        query = " ".join(message.command[1:])
        if not query:
            await message.reply("Please provide a search query for images.")
            return

        await app.send_message(message.chat.id, "Searching for images...")

        response = requests.get(f"https://www.googleapis.com/customsearch/v1?key={GAPI_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&searchType=image&num=10")
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])

            if items:
                await app.send_message(message.chat.id, "Top 10 image results:")
                for index, item in enumerate(items[:10], start=1):
                    image_url = item.get('link')

                    await app.send_photo(message.chat.id, photo=image_url)
            else:
                await app.send_message(message.chat.id, "No image results found.")
        else:
            await app.send_message(message.chat.id, "Failed to fetch image results.")
            
    except Exception as e:
        await app.send_message(message.chat.id, f"An error occurred: {str(e)}")
        
        
        
        
@app.on_message(filters.command("bimg"))
async def image_search(client, message):
    try:
        query = " ".join(message.command[1:])
        if not query:
            await message.reply("Please provide a search query for images.")
            return

        await app.send_message(message.chat.id, "Searching for images...")

        response = requests.get(f"https://www.googleapis.com/customsearch/v1?key={GAPI_KEY}&cx={BING_ENGINE_ID}&q={query}&searchType=image&num=10")
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])

            if items:
                await app.send_message(message.chat.id, "Top 10 image results:")
                for index, item in enumerate(items[:10], start=1):
                    image_url = item.get('link')

                    await app.send_photo(message.chat.id, photo=image_url)
            else:
                await app.send_message(message.chat.id, "No image results found.")
        else:
            await app.send_message(message.chat.id, "Failed to fetch image results.")
            
    except Exception as e:
        await app.send_message(message.chat.id, f"An error occurred: {str(e)}")


        
        
@app.on_message(filters.command("yimg"))
async def image_search(client, message):
    try:
        query = " ".join(message.command[1:])
        if not query:
            await message.reply("Please provide a search query for images.")
            return

        await app.send_message(message.chat.id, "Searching for images...")

        response = requests.get(f"https://www.googleapis.com/customsearch/v1?key={GAPI_KEY}&cx={YANDEX_ENGINE_ID}&q={query}&searchType=image&num=10")
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])

            if items:
                await app.send_message(message.chat.id, "Top 10 image results:")
                for index, item in enumerate(items[:10], start=1):
                    image_url = item.get('link')

                    await app.send_photo(message.chat.id, photo=image_url)
            else:
                await app.send_message(message.chat.id, "No image results found.")
        else:
            await app.send_message(message.chat.id, "Failed to fetch image results.")
            
    except Exception as e:
        await app.send_message(message.chat.id, f"An error occurred: {str(e)}")


        
        
@app.on_message(filters.command("dimg"))
async def image_search(client, message):
    try:
        query = " ".join(message.command[1:])
        if not query:
            await message.reply("Please provide a search query for images.")
            return

        await app.send_message(message.chat.id, "Searching for images...")

        response = requests.get(f"https://www.googleapis.com/customsearch/v1?key={GAPI_KEY}&cx={DDG_ENGINE_ID}&q={query}&searchType=image&num=10")
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])

            if items:
                await app.send_message(message.chat.id, "Top 10 image results:")
                for index, item in enumerate(items[:10], start=1):
                    image_url = item.get('link')

                    await app.send_photo(message.chat.id, photo=image_url)
            else:
                await app.send_message(message.chat.id, "No image results found.")
        else:
            await app.send_message(message.chat.id, "Failed to fetch image results.")
            
    except Exception as e:
        await app.send_message(message.chat.id, f"An error occurred: {str(e)}")


        

# Handler for /bard command
# @app.on_message(filters.command("bard"))
# async def bard_command(client, message):

#     try:
#         query = " ".join(message.command[1:])
#         if query:
#             await app.send_message(message.chat.id, "Creating Response...")
#             # Use Bard API to get an answer based on the user's query
#             answer = bard.get_answer(query)['content']
#             await app.send_message(message.chat.id, answer)
#         else:
#             await app.send_message(message.chat.id, "Please provide a query to get an answer.")
#     except Exception as e:
#         await app.send_message(message.chat.id, f'An error occurred: {str(e)}')



@app.on_message(filters.command("ping"))
async def handle_ping_command(client, message):
    start_time = time.time() 


    sent_message = await app.send_message(message.chat.id, "Pong! I'm alive and responsive.")

    end_time = time.time()  
    elapsed_time = round((end_time - start_time) * 1000, 2)  

    response_message = f"Pong! Response time: {elapsed_time} ms"
    await app.edit_message_text(message.chat.id, sent_message.id, response_message)





app.run()