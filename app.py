import gradio as gr
import whisper
import os
import openai

# 載入模型，預設為 small
MODEL_OPTIONS = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
DEFAULT_MODEL = "small"
DEFAULT_PROMPT = "請轉錄以下內容為繁體中文"

# 建立語音轉錄功能
def transcribe_audio(audio, model_size, prompt, use_openai, openai_api_key):
    if use_openai:
        if not openai_api_key:
            return "請輸入 OpenAI API Key"
        openai.api_key = openai_api_key
        with open(audio, "rb") as audio_file:
            response = openai.Audio.transcribe("whisper-1", audio_file, prompt=prompt)
        return response["text"]
    else:
        model = whisper.load_model(model_size)
        result = model.transcribe(audio, prompt=prompt)
        return result["text"]

# 使用 Gradio 構建介面
audio_input = gr.Audio(type="filepath", label="上傳音頻")
model_input = gr.Dropdown(choices=MODEL_OPTIONS, value=DEFAULT_MODEL, label="選擇 Whisper 模型")
prompt_input = gr.Textbox(value=DEFAULT_PROMPT, label="轉錄用戶定製的例句")
use_openai_input = gr.Checkbox(label="使用 OpenAI Whisper", value=False)
openai_key_input = gr.Textbox(label="OpenAI API Key", type="password", placeholder="請輸入您的 OpenAI API Key")
text_output = gr.Textbox(label="轉錄結果")

description = "上傳音頻文件，選擇 Whisper 模型來轉錄音頻內容。您可以使用本機模型或者 OpenAI Whisper 服務。"

demo = gr.Interface(fn=transcribe_audio, 
                    inputs=[audio_input, model_input, prompt_input, use_openai_input, openai_key_input], 
                    outputs=text_output, 
                    description=description,
                    title="Whisper 語音轉錄應用")

demo.launch()
