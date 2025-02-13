import os
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# 存储配置
UPLOAD_DIR = ROOT_DIR / "storage" / "uploads"
FRAMES_DIR = ROOT_DIR / "storage" / "frames"

# 确保存储目录存在
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

# 文件配置
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_VIDEO_TYPES = {
    "video/mp4",
    "video/avi",
    "video/quicktime",  # MOV
}

# 视频处理配置
FRAME_QUALITY = 90  # JPEG质量 