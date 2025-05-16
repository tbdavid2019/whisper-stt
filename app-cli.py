import os
import sys
import whisper
import requests
import subprocess
import math
from pydub import AudioSegment
import time

# 常量定義
MODEL_OPTIONS = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
DEFAULT_MODEL = "small"
DEFAULT_PROMPT = "請轉錄以下內容為繁體中文"
MAX_FILE_SIZE_MB = 25  # OpenAI API 文件大小限制為 25MB

# 檢查 ffmpeg 是否已安裝
def is_ffmpeg_installed():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        return True
    except FileNotFoundError:
        return False

# 檢查文件大小
def check_file_size(file_path, max_size_mb=MAX_FILE_SIZE_MB):
    try:
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        return file_size_mb <= max_size_mb, file_size_mb
    except Exception as e:
        print(f"檢查文件大小時出錯: {str(e)}")
        return True, 0

# 分割音頻文件為較小的片段
def split_audio_file(file_path, segment_duration_ms=30000):  # 默認 30 秒一段
    try:
        # 載入音頻
        print(f"正在載入音頻文件: {file_path}")
        audio = AudioSegment.from_file(file_path)
        duration_ms = len(audio)
        
        # 計算需要分割的段數
        segments_count = math.ceil(duration_ms / segment_duration_ms)
        print(f"音頻總長度: {duration_ms/1000:.1f} 秒，將分割為 {segments_count} 個片段")
        
        # 分割音頻
        file_name = os.path.splitext(file_path)[0]
        file_ext = os.path.splitext(file_path)[1]
        segment_files = []
        
        for i in range(segments_count):
            start_time = i * segment_duration_ms
            end_time = min((i + 1) * segment_duration_ms, duration_ms)
            segment = audio[start_time:end_time]
            
            segment_path = f"{file_name}_part{i+1}{file_ext}"
            print(f"正在導出片段 {i+1}/{segments_count}...")
            segment.export(segment_path, format=file_ext.replace(".", ""))
            segment_files.append(segment_path)
        
        return segment_files
    except Exception as e:
        print(f"分割音頻文件時出錯: {str(e)}")
        return [file_path]  # 發生錯誤時返回原始文件

# 使用本地 Whisper 模型進行轉錄，實時顯示結果
def transcribe_with_local_model(audio_path, model_size, prompt):
    if not is_ffmpeg_installed():
        print("錯誤: 找不到 ffmpeg。請安裝 ffmpeg 後再使用本地模型。")
        print("在 Mac 上，您可以使用 'brew install ffmpeg' 命令安裝。")
        return
    
    try:
        print(f"正在載入 {model_size} 模型...")
        model = whisper.load_model(model_size)
        
        # 分割音頻為較小的片段以實時顯示結果
        segments = split_audio_file(audio_path)
        
        full_text = ""
        for i, segment_path in enumerate(segments):
            print(f"\n處理片段 {i+1}/{len(segments)}...")
            
            # 使用 Whisper 模型轉錄當前片段
            result = model.transcribe(
                segment_path, 
                language="zh", 
                task="transcribe", 
                initial_prompt=prompt
            )
            
            # 顯示當前片段的轉錄結果
            segment_text = result["text"]
            print(f"片段 {i+1} 轉錄結果: {segment_text}")
            
            # 累積完整文本
            full_text += segment_text + " "
            
            # 如果是臨時創建的分割文件，則刪除
            if segment_path != audio_path:
                os.remove(segment_path)
        
        return full_text.strip()
    
    except Exception as e:
        print(f"使用本地模型轉錄時出錯: {str(e)}")
        return None

# 使用 OpenAI API 進行轉錄，實時顯示結果
def transcribe_with_openai_api(audio_path, api_key, prompt):
    # 檢查文件大小
    is_size_ok, file_size_mb = check_file_size(audio_path)
    if not is_size_ok:
        print(f"警告: 音頻文件大小 ({file_size_mb:.1f}MB) 超過 OpenAI API 限制 (25MB)。")
        print("將嘗試分割文件...")
    
    try:
        # 分割音頻為較小的片段
        segments = split_audio_file(audio_path)
        
        full_text = ""
        for i, segment_path in enumerate(segments):
            print(f"\n處理片段 {i+1}/{len(segments)}...")
            
            # 檢查當前片段的大小
            is_segment_size_ok, segment_size_mb = check_file_size(segment_path)
            if not is_segment_size_ok:
                print(f"警告: 片段 {i+1} 大小 ({segment_size_mb:.1f}MB) 超過限制，將跳過此片段。")
                continue
            
            # 使用 OpenAI API 轉錄當前片段
            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            
            with open(segment_path, "rb") as f:
                files = {
                    "file": (os.path.basename(segment_path), f)
                }
                
                data = {
                    "model": "whisper-1",
                    "prompt": prompt
                }
                
                print(f"正在發送片段 {i+1} 到 OpenAI API...")
                response = requests.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    headers=headers,
                    files=files,
                    data=data
                )
            
            if response.status_code == 200:
                segment_text = response.json().get("text", "")
                print(f"片段 {i+1} 轉錄結果: {segment_text}")
                full_text += segment_text + " "
            else:
                print(f"片段 {i+1} 轉錄失敗: {response.status_code} - {response.text}")
            
            # 如果是臨時創建的分割文件，則刪除
            if segment_path != audio_path:
                os.remove(segment_path)
        
        return full_text.strip()
    
    except Exception as e:
        print(f"使用 OpenAI API 轉錄時出錯: {str(e)}")
        return None

# 主函數
def main():
    print("===== Whisper 語音轉錄 CLI 工具 =====")
    print("這個工具可以將音頻文件轉錄為文字，並在處理過程中實時顯示結果。")
    
    # 獲取音頻文件路徑
    audio_path = input("\n請輸入音頻文件路徑: ").strip()
    if not os.path.exists(audio_path):
        print(f"錯誤: 找不到文件 '{audio_path}'")
        return
    
    # 選擇使用本地模型還是 OpenAI API
    use_openai = input("\n是否使用 OpenAI API? (y/n，默認: n): ").strip().lower() == 'y'
    
    if use_openai:
        # 使用 OpenAI API
        api_key = input("\n請輸入您的 OpenAI API Key: ").strip()
        if not api_key:
            print("錯誤: API Key 不能為空")
            return
        
        prompt = input("\n請輸入轉錄提示 (默認: '請轉錄以下內容為繁體中文'): ").strip()
        if not prompt:
            prompt = DEFAULT_PROMPT
        
        print("\n開始使用 OpenAI API 進行轉錄...")
        full_text = transcribe_with_openai_api(audio_path, api_key, prompt)
        
    else:
        # 使用本地模型
        print("\n可用的模型: " + ", ".join(MODEL_OPTIONS))
        model_size = input(f"請選擇模型 (默認: {DEFAULT_MODEL}): ").strip()
        if not model_size or model_size not in MODEL_OPTIONS:
            model_size = DEFAULT_MODEL
        
        prompt = input("\n請輸入轉錄提示 (默認: '請轉錄以下內容為繁體中文'): ").strip()
        if not prompt:
            prompt = DEFAULT_PROMPT
        
        print("\n開始使用本地模型進行轉錄...")
        full_text = transcribe_with_local_model(audio_path, model_size, prompt)
    
    if full_text:
        print("\n===== 完整轉錄結果 =====")
        print(full_text)
        
        # 保存結果到文件
        output_path = os.path.splitext(audio_path)[0] + "_transcript.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"\n轉錄結果已保存到: {output_path}")

if __name__ == "__main__":
    main()