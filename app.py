import gradio as gr
import whisper
import os

# 載入模型，預設為 small
MODEL_OPTIONS = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
DEFAULT_MODEL = "small"
LANGUAGE_OPTIONS = ["English", "Chinese (Traditional)"]

# 建立語音轉錄功能
def transcribe_audio(audio, model_size, language):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio)
    return result["text"]

# 使用 Gradio 構建介面
audio_input = gr.Audio(type="filepath", label="上傳音頻")
model_input = gr.Dropdown(choices=MODEL_OPTIONS, value=DEFAULT_MODEL, label="選擇 Whisper 模型")
language_input = gr.Radio(choices=LANGUAGE_OPTIONS, value="Chinese (Traditional)", label="選擇轉錄語言")
text_output = gr.Textbox(label="轉錄結果")

description = "上傳音頻文件，選擇 Whisper 模型來轉錄音頻內容。"

demo = gr.Interface(fn=transcribe_audio, 
                    inputs=[audio_input, model_input, language_input], 
                    outputs=text_output, 
                    description=description,
                    title="Whisper 語音轉錄應用")

demo.launch()
