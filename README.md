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
   ```

3. 運行應用：

   ```bash
   python app.py
   ```

   在本地訪問：http://127.0.0.1:7860

### 在 Hugging Face Spaces 上運行

你可以將此應用部署到 [Hugging Face Spaces](https://huggingface.co/spaces)，使用 Gradio 構建和運行應用程序。只需將代碼和 `requirements.txt` 上傳到你的 Hugging Face Space 即可。

## 依賴

- Python 3.8 及更高版本
- [Gradio 3.15.0](https://gradio.app/)
- [OpenAI Whisper](https://github.com/openai/whisper)

## 文件結構

- `app.py`：應用的主程序文件。
- `requirements.txt`：列出所有必需的 Python 庫。
- `README.md`：項目描述文件（即您正在閱讀的這個文件）。

## 使用說明

1. 運行應用後，通過界面上傳您需要轉錄的音頻文件。
2. 選擇要使用的 Whisper 模型大小。
3. 點擊提交，等待模型處理並顯示轉錄結果。

## 版本

- v1.0.0：初始版本，支持音頻上傳和模型選擇功能。

## 貢獻

歡迎提交 Issue 和 Pull Request 來改進此項目。如果您有建議或改進意見，請隨時聯繫我。

## 授權

此項目基於 [MIT License](LICENSE)。

