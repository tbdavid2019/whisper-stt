---
title: Whisper Stt
emoji: 🚀
colorFrom: green
colorTo: green
sdk: gradio
sdk_version: 5.7.1
app_file: app.py
pinned: false
short_description: 上傳mp3或聲音檔案, 轉成文字逐字稿給你
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference


---

# Whisper 語音轉錄應用

這是一個使用 [OpenAI Whisper](https://github.com/openai/whisper) 模型進行語音轉錄的開源項目。此應用使用 [Gradio](https://gradio.app/) 來構建簡單友好的用戶界面，讓您可以輕鬆上傳音頻文件並進行語音轉錄。這個應用能幫助您將音頻中的語音內容轉換為文字，支持多種語言和模型選擇。

## 功能

- 上傳音頻文件，並使用 Whisper 模型進行語音轉錄。
- 支持選擇不同大小的 Whisper 模型（tiny, base, small, medium, large, large-v2, large-v3）。
- 簡單易用的界面，通過 Gradio 提供。
- 支持從 YouTube 下載視頻並轉錄其音頻內容。
- 支持使用 OpenAI API 進行轉錄（需要 API Key）。
- 提供命令行界面 (CLI) 版本，可在處理過程中實時顯示轉錄結果。

## 如何運行

### 本地運行

1. 克隆此倉庫：

   ```bash
   git clone https://github.com/tbdavid2019/whisper-stt.git
   cd whisper-stt
   ```

2. 安裝所需的 Python 包：

   建議使用 Python 3.8 或更高版本。

   ```bash
   pip install -r requirements.txt
   brew install ffmpeg

   ```

3. 運行應用：

   **Web 界面版本：**
   ```bash
   python app.py
   ```
   在本地訪問：http://127.0.0.1:7860

   **命令行界面版本：**
   ```bash
   python app-cli.py
   ```
   按照提示輸入音頻文件路徑和其他選項。

### 在 Hugging Face Spaces 上運行

你可以將此應用部署到 [Hugging Face Spaces](https://huggingface.co/spaces)，使用 Gradio 構建和運行應用程序。只需將代碼和 `requirements.txt` 上傳到你的 Hugging Face Space 即可。

## 依賴

- Python 3.8 及更高版本
- [Gradio](https://gradio.app/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [FFmpeg](https://ffmpeg.org/)（處理音頻所必需）
- [PyDub](https://github.com/jiaaro/pydub)（音頻處理）
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)（YouTube 下載）

## 文件結構

- `app.py`：Web 界面應用的主程序文件。
- `app-cli.py`：命令行界面版本的應用程序，支持實時顯示轉錄結果。
- `requirements.txt`：列出所有必需的 Python 庫。
- `README.md`：項目描述文件（即您正在閱讀的這個文件）。

## 使用說明

### Web 界面版本

1. 運行應用後，通過界面上傳您需要轉錄的音頻文件或提供 YouTube 視頻 URL。
2. 選擇要使用的 Whisper 模型大小。
3. 可選：勾選"使用 OpenAI Whisper"並輸入您的 API Key 以使用 OpenAI API 進行轉錄。
4. 點擊提交，等待模型處理並顯示轉錄結果。

### 命令行界面版本

1. 在終端中運行 `python app-cli.py`。
2. 按照提示輸入音頻文件路徑。
3. 選擇是否使用 OpenAI API 進行轉錄。
4. 如果使用本地模型，選擇模型大小。
5. 程序會將音頻分割成較小的片段，並在處理每個片段時實時顯示轉錄結果。
6. 處理完成後，完整的轉錄結果會顯示在終端中，並保存到文本文件。

## 版本

- v1.0.0：初始版本，支持音頻上傳和模型選擇功能。
- v1.1.0：添加 YouTube 下載和轉錄功能。
- v1.2.0：添加 OpenAI API 支持，允許使用 OpenAI Whisper 服務。
- v1.3.0：添加命令行界面版本，支持實時顯示轉錄結果。

## 貢獻

歡迎提交 Issue 和 Pull Request 來改進此項目。如果您有建議或改進意見，請隨時聯繫我。

## 授權

此項目基於 [MIT License](LICENSE)。

