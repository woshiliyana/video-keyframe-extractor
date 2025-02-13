from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from video_processor import VideoProcessor
import os
from pathlib import Path
import shutil

app = FastAPI()

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建目录
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("output")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# 挂载静态文件目录
app.mount("/output", StaticFiles(directory="output"), name="output")

@app.post("/api/process")
async def process_video(video: UploadFile):
    try:
        # 清理旧文件
        for file in OUTPUT_DIR.glob("*"):
            file.unlink()
        
        # 保存上传的文件
        file_path = UPLOAD_DIR / video.filename
        with open(file_path, "wb") as buffer:
            content = await video.read()
            buffer.write(content)
        
        # 处理视频
        processor = VideoProcessor()
        result = processor.process_video(
            str(file_path),
            str(OUTPUT_DIR)
        )
        
        # 删除上传的视频文件
        file_path.unlink()
        
        # 修正图片URL，确保只有一个 output 路径
        if "keyframes" in result:
            result["keyframes"] = [f"/output/{os.path.basename(frame)}" for frame in result["keyframes"]]
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "keyframes": []
        }

@app.get("/api/download")
async def download_keyframes():
    # 创建一个临时目录来存放打包文件
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    zip_path = temp_dir / "keyframes.zip"
    
    # 将所有关键帧打包
    shutil.make_archive(str(zip_path.with_suffix("")), 'zip', OUTPUT_DIR)
    
    # 返回zip文件
    return FileResponse(
        zip_path,
        media_type='application/zip',
        filename='keyframes.zip'
    )