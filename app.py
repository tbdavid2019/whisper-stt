import gradio as gr
import whisper
import os
import requests
from pydub import AudioSegment
import os
from yt_dlp import YoutubeDL

# 載入模型，預設為 small
MODEL_OPTIONS = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
DEFAULT_MODEL = "small"
DEFAULT_PROMPT = "請轉錄以下內容為繁體中文"

# 使用 Cookies 支援 YouTube 下載
COOKIES_FILE = "cookies.txt"  # 上傳 cookies.txt 文件至同一目錄

def download_audio_from_youtube(youtube_url):
    try:
        # 使用 yt-dlp 下載音訊，附帶 cookies
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'temp_audio.%(ext)s',
            'quiet': True,
            'cookiefile': COOKIES_FILE,  # 使用 cookies.txt
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        
        # 查找轉換後的音訊檔案
        for file in os.listdir():
            if file.endswith(".wav"):
                return file, None
        return None, "音訊下載失敗"
    except Exception as e:
        return None, f"下載音訊失敗: {str(e)}"

# 建立語音轉錄功能
def transcribe_audio(audio, model_size, prompt, use_openai, openai_api_key, youtube_url):
    # 如果提供了 YouTube URL，先下載音訊
    if youtube_url:
        audio, error = download_audio_from_youtube(youtube_url)
        if error:
            return error
    if not audio:
        return "請上傳音訊文件或提供有效的 YouTube URL"
    
    # 使用 OpenAI Whisper API
    if use_openai:
        if not openai_api_key:
            return "請輸入 OpenAI API Key"
        headers = {
            "Authorization": f"Bearer {openai_api_key}"
        }
        files = {
            "file": (os.path.basename(audio), open(audio, "rb")),
            "model": (None, "whisper-1"),
            "prompt": (None, prompt)
        }
        response = requests.post("https://api.openai.com/v1/audio/transcriptions", headers=headers, files=files)
        if response.status_code == 200:
            return response.json().get("text", "轉錄失敗")
        else:
            return f"轉錄失敗: {response.status_code} - {response.text}"
    else:
        # 使用本地模型
        model = whisper.load_model(model_size)
        result = model.transcribe(audio, language="zh", task="transcribe", initial_prompt=prompt)
        return result["text"]

# 使用 Gradio 構建介面
audio_input = gr.Audio(type="filepath", label="上傳音頻")
youtube_url_input = gr.Textbox(label="YouTube URL", placeholder="輸入 YouTube 影片網址")
model_input = gr.Dropdown(choices=MODEL_OPTIONS, value=DEFAULT_MODEL, label="選擇 Whisper 模型")
prompt_input = gr.Textbox(value=DEFAULT_PROMPT, label="轉錄用戶定製的例句")
use_openai_input = gr.Checkbox(label="使用 OpenAI Whisper", value=False)
openai_key_input = gr.Textbox(label="OpenAI API Key", type="password", placeholder="請輸入您的 OpenAI API Key")
text_output = gr.Textbox(label="轉錄結果")

description = "上傳音頻文件或提供 YouTube 影片網址，選擇 Whisper 模型來轉錄音頻內容。您可以使用 (1) 免費本機模型  或  (2)付費的 OpenAI API Whisper 服務。"

demo = gr.Interface(
    fn=transcribe_audio, 
    inputs=[audio_input, model_input, prompt_input, use_openai_input, openai_key_input, youtube_url_input], 
    outputs=text_output, 
    description=description,
    title="Whisper 語音轉錄應用"
)

demo.launch()