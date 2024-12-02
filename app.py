import gradio as gr
import whisper

# 載入模型，預設為 small
MODEL_OPTIONS = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
DEFAULT_MODEL = "small"
LANGUAGE_OPTIONS = ["English", "Chinese (Traditional)"]

# 建立語音轉錄功能
def transcribe_audio(audio, model_size, language):
    model = whisper.load_model(model_size)
    if language == "English":
        result = model.transcribe(audio, language="en")
    else:
        result = model.transcribe(audio, language="zh-tw")
    return result["text"]

# 使用 Gradio 構建介面
audio_input = gr.inputs.Audio(source="upload", type="filepath", label="上傳音頻")
model_input = gr.inputs.Dropdown(choices=MODEL_OPTIONS, default=DEFAULT_MODEL, label="選擇 Whisper 模型")
language_input = gr.inputs.Radio(choices=LANGUAGE_OPTIONS, default="Chinese (Traditional)", label="選擇轉錄語言")
text_output = gr.outputs.Textbox(label="轉錄結果")

description = "上傳音頻文件，選擇 Whisper 模型和語言來轉錄音頻內容。"

demo = gr.Interface(fn=transcribe_audio, 
                    inputs=[audio_input, model_input, language_input], 
                    outputs=text_output, 
                    description=description,
                    title="Whisper 語音轉錄應用")

demo.launch()
