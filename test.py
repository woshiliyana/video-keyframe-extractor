import argparse
from video_processor import VideoProcessor
import cv2
import os
from pathlib import Path

def process_video(video_path, output_dir="output", threshold=12, edge_threshold=45, hist_threshold=3000):
    """
    处理视频并提取关键帧
    """
    # 确保输出目录存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 清理输出目录
    for file in Path(output_dir).glob("*.jpg"):
        file.unlink()
    
    # 创建处理器实例
    processor = VideoProcessor(
        threshold=threshold,
        edge_threshold=edge_threshold,
        hist_threshold=hist_threshold
    )
    
    # 获取视频信息
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps
    cap.release()
    
    print("\n视频信息:")
    print(f"- 总帧数: {total_frames}")
    print(f"- FPS: {fps}")
    print(f"- 时长: {duration:.2f} 秒")
    print(f"\n使用参数:")
    print(f"- 帧差阈值: {threshold}")
    print(f"- 边缘阈值: {edge_threshold}")
    print(f"- 直方图阈值: {hist_threshold}")
    print("\n开始处理...")
    
    # 处理视频
    result = processor.process_video(video_path, output_dir)
    
    # 显示结果
    if result["success"]:
        keyframes = result["keyframes"]
        print("\n处理完成!")
        print(f"- 提取关键帧数: {len(keyframes)}")
        print(f"- 平均提取间隔: {duration/len(keyframes):.2f} 秒")
        print(f"- 输出目录: {output_dir}/")
        print("\n关键帧列表:")
        for frame in keyframes:
            print(f"- {os.path.basename(frame)}")
    else:
        print("\n处理失败:")
        print(f"- 错误: {result['message']}")

def main():
    parser = argparse.ArgumentParser(description="视频关键帧提取工具")
    
    parser.add_argument(
        "video_path",
        help="视频文件路径"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="output",
        help="输出目录 (默认: output)"
    )
    
    parser.add_argument(
        "-t", "--threshold",
        type=float,
        default=12,
        help="帧差阈值 (默认: 12)"
    )
    
    parser.add_argument(
        "-e", "--edge-threshold",
        type=float,
        default=45,
        help="边缘阈值 (默认: 45)"
    )
    
    parser.add_argument(
        "-hist", "--hist-threshold",
        type=float,
        default=3000,
        help="直方图阈值 (默认: 3000)"
    )
    
    args = parser.parse_args()
    
    try:
        process_video(
            args.video_path,
            args.output,
            args.threshold,
            args.edge_threshold,
            args.hist_threshold
        )
    except Exception as e:
        print(f"\n错误: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 