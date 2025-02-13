from pathlib import Path
import ffmpeg
from typing import List
import uuid
import os

class VideoService:
    def __init__(self, upload_dir: str = "storage/uploads", frames_dir: str = "storage/frames"):
        self.upload_dir = Path(upload_dir)
        self.frames_dir = Path(frames_dir)
        
        # 确保目录存在
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.frames_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_video(self, file_path: Path) -> bool:
        """验证视频文件"""
        try:
            probe = ffmpeg.probe(str(file_path))
            # 检查文件是否包含视频流
            return any(stream["codec_type"] == "video" for stream in probe["streams"])
        except ffmpeg.Error:
            return False
    
    async def extract_frames(self, video_path: Path) -> List[Path]:
        """提取视频关键帧"""
        if not self.validate_video(video_path):
            raise ValueError("Invalid video file")
            
        # 为当前处理创建唯一的会话ID
        session_id = str(uuid.uuid4())
        output_dir = self.frames_dir / session_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # 使用ffmpeg提取关键帧
            stream = ffmpeg.input(str(video_path))
            stream = ffmpeg.filter(stream, 'select', 'eq(pict_type,I)')  # 只选择I帧
            stream = ffmpeg.output(
                stream,
                str(output_dir / 'frame_%d.jpg'),
                vsync='0',
                format='image2'
            )
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            
            # 获取生成的帧列表
            frames = sorted(output_dir.glob('frame_*.jpg'))
            return frames
            
        except ffmpeg.Error as e:
            # 清理输出目录
            if output_dir.exists():
                for file in output_dir.glob('*'):
                    file.unlink()
                output_dir.rmdir()
            raise RuntimeError(f"Error processing video: {e.stderr.decode() if e.stderr else str(e)}") 