import logging
import tempfile

import moviepy.editor as mp
import requests
import whisper

from src.config import Settings

logger = logging.getLogger(__name__)

def extract_shortcode(url: str) -> str:
    logger.debug(f"Extracting shortcode from URL: {url}")
    try:
        url = str(url)  # Convertir a cadena explícitamente
        shortcode = url.split('https://www.instagram.com/reel/')[1].split('/')[0]
        logger.debug(f"Extracted shortcode: {shortcode}")
        return shortcode
    except Exception as e:
        logger.error(f"Error extracting shortcode: {e}")
        raise e

def fetch_video_url(shortcode: str) -> str or None:
    logger.debug(f"Fetching video URL for shortcode: {shortcode}")
    api_url = f"https://instagram-bulk-scraper-latest.p.rapidapi.com/media_download_by_shortcode/{shortcode}"
    headers = {
        'x-rapidapi-host': 'instagram-bulk-scraper-latest.p.rapidapi.com',
        'x-rapidapi-key': Settings().RAPID_API_KEY  # Asegúrate de que RAPID_API_KEY esté configurado correctamente en Settings
    }
    try:
        response = requests.get(api_url, headers=headers)
        logger.debug(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            media_data = data.get("data")
            if media_data:
                video_url = media_data.get("main_media_hd")
                logger.debug(f"Fetched video URL: {video_url}")
                return video_url
        else:
            logger.error(f"Error fetching video URL: {response.status_code}")
    except Exception as e:
        logger.error(f"Error fetching video URL: {e}")
    return None

def process_video(video_url):
    logger.debug(f"Processing video URL: {video_url}")
    if video_url:
        try:
            video_response = requests.get(video_url)
            if video_response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
                    temp_video.write(video_response.content)
                    temp_video_path = temp_video.name

                video_clip = mp.VideoFileClip(temp_video_path)
                audio_path = tempfile.mktemp(suffix=".wav")
                video_clip.audio.write_audiofile(audio_path)
                video_clip.close()
                logger.debug(f"Processed video and extracted audio to: {audio_path}")
                return audio_path
        except Exception as e:
            logger.error(f"Error processing video: {e}")
    return None

def transcribe_audio(audio_path):
    logger.debug(f"Transcribing audio from path: {audio_path}")
    if audio_path:
        try:
            model = whisper.load_model("base")
            result = model.transcribe(audio_path)
            logger.debug(f"Transcription result: {result['text']}")
            return result["text"]
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
    return None

def transcribe_video_from_instagram(instagram_url: str) -> str:
    logger.debug(f"Starting transcription for Instagram URL: {instagram_url}")
    shortcode = extract_shortcode(instagram_url)
    if shortcode is None:
        logger.error("Failed to extract shortcode from URL.")
        raise ValueError("Invalid Instagram URL.")

    try:
        video_url = fetch_video_url(shortcode)
        if not video_url:
            logger.error("Failed to fetch video URL.")
            raise ValueError("Failed to fetch video URL.")

        audio_path = process_video(video_url)
        if not audio_path:
            logger.error("Failed to process video.")
            raise ValueError("Failed to process video.")

        transcription = transcribe_audio(audio_path)
        if not transcription:
            logger.error("Failed to transcribe audio.")
            raise ValueError("Failed to transcribe audio.")

        logger.debug(f"Final transcription: {transcription}")
        return transcription
    except Exception as e:
        logger.error(f"Error in transcription process: {e}")
        raise e
