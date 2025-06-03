import os
from typing import Optional
import openai  # Requires: pip install openai
import base64
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import requests
import gtts  # Requires: pip install gTTS

YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = "client_secrets.json"
TOKEN_PICKLE_FILE = "token.pickle"

def get_topic() -> str:
    """Prompt user for a video topic, with input validation and optional default."""
    topic = input("Enter the topic for the AI video (or press Enter for a random topic): ").strip()
    if not topic:
        # Optionally, you can use a random topic or a default
        import random
        default_topics = [
            "The future of artificial intelligence",
            "How electric cars work",
            "The history of the internet",
            "Tips for healthy living",
            "Space exploration milestones"
        ]
        topic = random.choice(default_topics)
        print(f"No topic entered. Using random topic: {topic}")
    return topic

def generate_script(topic: str) -> str:
    """Generate a script for the given topic using Hugging Face Inference API and an open-source LLM."""
    api_token = os.getenv("HF_API_TOKEN")
    if not api_token:
        raise EnvironmentError("HF_API_TOKEN environment variable not set.")
    endpoint = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {api_token}"}
    prompt = f"Write a detailed, engaging, and informative script for a YouTube video about: {topic}\n\nScript:"
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 400}}
    print(f"Generating script for topic: {topic}")
    response = requests.post(endpoint, headers=headers, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Hugging Face API error: {response.status_code} {response.text}")
    result = response.json()
    # The output may be a list of dicts or a dict with 'generated_text'
    if isinstance(result, list) and 'generated_text' in result[0]:
        script = result[0]['generated_text']
    elif isinstance(result, dict) and 'generated_text' in result:
        script = result['generated_text']
    else:
        script = str(result)
    print("Script generated.")
    return script

def text_to_speech(script: str, audio_path: str) -> None:
    """Convert script to speech and save as an MP3 audio file using gTTS."""
    tts = gtts.gTTS(script)
    tts.save(audio_path)
    print(f"Audio saved to {audio_path}")

def generate_visuals(topic: str, visuals_path: str) -> None:
    """Generate visuals for the topic using OpenAI DALL-E API and save as PNG."""
    # Set your OpenAI API key as an environment variable: OPENAI_API_KEY
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set.")
    openai.api_key = api_key
    
    print(f"Generating image for topic: {topic}")
    response = openai.images.generate(
        model="dall-e-3",
        prompt=topic,
        n=1,
        size="1024x1024",
        response_format="b64_json"
    )
    image_b64 = response.data[0].b64_json
    with open(visuals_path, "wb") as f:
        f.write(base64.b64decode(image_b64))
    print(f"Visuals saved to {visuals_path}")

def combine_audio_visuals(audio_path: str, visuals_path: str, video_path: str) -> None:
    """Combine audio and visuals into a video (placeholder)."""
    # TODO: Use ffmpeg or moviepy for real implementation
    with open(video_path, 'w') as f:
        f.write("VIDEO_PLACEHOLDER")
    print(f"Video saved to {video_path}")

def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, YOUTUBE_SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return build('youtube', 'v3', credentials=creds)

def upload_to_youtube(video_path: str, title: str, description: Optional[str] = None) -> None:
    """Upload the video to YouTube using YouTube Data API v3."""
    youtube = get_authenticated_service()
    body = {
        'snippet': {
            'title': title,
            'description': description or '',
            'tags': [],
            'categoryId': '22'  # 'People & Blogs' category
        },
        'status': {
            'privacyStatus': 'private',  # Change to 'public' if desired
        }
    }
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/*')
    print(f"Uploading {video_path} to YouTube...")
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")
    print(f"Upload complete! Video ID: {response['id']}")

def main() -> None:
    topic = get_topic()
    script = generate_script(topic)
    audio_path = "audio.mp3"
    visuals_path = "visuals.png"
    video_path = "output_video.mp4"

    text_to_speech(script, audio_path)
    generate_visuals(topic, visuals_path)
    combine_audio_visuals(audio_path, visuals_path, video_path)
    upload_to_youtube(video_path, topic, script)

if __name__ == "__main__":
    main()