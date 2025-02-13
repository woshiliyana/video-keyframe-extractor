import cv2
import numpy as np
from pathlib import Path
import os
import sys

class VideoProcessor:
    def __init__(self, threshold=10, edge_threshold=50, hist_threshold=3000):
        """
        初始化视频处理器
        :param threshold: 检测画面变化的阈值，值越小越敏感
        :param edge_threshold: 边缘检测的阈值，值越小越敏感
        :param hist_threshold: 直方图比较的阈值
        """
        self.threshold = threshold
        self.edge_threshold = edge_threshold
        self.hist_threshold = hist_threshold
        
    def detect_scene_change(self, current_frame, prev_frame):
        """
        使用多种方法检测场景变化
        """
        # 1. 帧差法
        diff = cv2.absdiff(current_frame, prev_frame)
        mean_diff = np.mean(diff)
        
        # 2. 边缘检测
        edges_current = cv2.Canny(current_frame, 100, 200)
        edges_prev = cv2.Canny(prev_frame, 100, 200)
        edge_diff = cv2.absdiff(edges_current, edges_prev)
        edge_score = np.mean(edge_diff)
        
        # 3. 直方图比较
        hist_current = cv2.calcHist([current_frame], [0], None, [256], [0, 256])
        hist_prev = cv2.calcHist([prev_frame], [0], None, [256], [0, 256])
        hist_diff = cv2.compareHist(hist_current, hist_prev, cv2.HISTCMP_CHISQR)
        
        # 综合判断
        is_key_frame = (mean_diff > self.threshold or 
                       edge_score > self.edge_threshold or 
                       hist_diff > self.hist_threshold)
        
        return is_key_frame, {
            'mean_diff': mean_diff,
            'edge_score': edge_score,
            'hist_diff': hist_diff
        }
        
    def extract_keyframes(self, video_path, output_dir):
        """
        从视频中提取关键帧
        :param video_path: 视频文件路径
        :param output_dir: 输出目录
        :return: 提取的关键帧路径列表
        """
        # 检查视频文件是否存在
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"视频文件不存在: {video_path}")
            
        # 确保输出目录存在
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 打开视频文件
        print(f"正在打开视频: {video_path}")
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {video_path}")
            
        # 获取视频信息
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"视频信息: 总帧数={total_frames}, FPS={fps}")
        
        prev_gray = None
        frame_count = 0
        keyframes = []
        last_keyframe = -10  # 减少最小间隔
        last_valid_frame = None  # 记录最后一个有效帧
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print(f"已处理完所有帧: {frame_count}")
                    break
                    
                if frame is None:
                    print(f"警告: 第 {frame_count} 帧为空")
                    continue
                
                # 更新最后一个有效帧
                last_valid_frame = frame.copy()
                
                # 转换为灰度图
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # 保存第一帧
                if frame_count == 0:
                    print("正在保存第一帧...")
                    output_path = os.path.join(output_dir, f"keyframe_{frame_count}.jpg")
                    if cv2.imwrite(output_path, frame):
                        keyframes.append(output_path)
                        last_keyframe = frame_count
                        print(f"成功保存第一帧: {output_path}")
                    else:
                        print(f"保存第一帧失败: {output_path}")
                
                if prev_gray is not None and (frame_count - last_keyframe) > 10:
                    is_key_frame, metrics = self.detect_scene_change(gray, prev_gray)
                    
                    if is_key_frame:
                        print(f"检测到关键帧 {frame_count}")
                        print(f"指标: 平均差异={metrics['mean_diff']:.2f}, "
                              f"边缘分数={metrics['edge_score']:.2f}, "
                              f"直方图差异={metrics['hist_diff']:.2f}")
                              
                        output_path = os.path.join(output_dir, f"keyframe_{frame_count}.jpg")
                        if cv2.imwrite(output_path, frame):
                            keyframes.append(output_path)
                            last_keyframe = frame_count
                            print(f"成功保存关键帧: {output_path}")
                        else:
                            print(f"保存关键帧失败: {output_path}")
                
                prev_gray = gray
                frame_count += 1
                
                if frame_count % 100 == 0:
                    print(f"已处理 {frame_count} 帧...")
            
            # 保存最后一帧（使用最后一个有效帧）
            if last_valid_frame is not None and (frame_count - last_keyframe) > 10:
                print("正在保存最后一帧...")
                output_path = os.path.join(output_dir, f"keyframe_{frame_count-1}.jpg")
                if cv2.imwrite(output_path, last_valid_frame):
                    keyframes.append(output_path)
                    print(f"成功保存最后一帧: {output_path}")
                else:
                    print(f"保存最后一帧失败: {output_path}")
                    
        except Exception as e:
            print(f"处理视频时发生错误: {e}")
            raise
        finally:
            cap.release()
        
        return keyframes

    def process_video(self, video_path, output_dir):
        """
        处理视频并返回结果
        :param video_path: 视频文件路径
        :param output_dir: 输出目录
        :return: 字典，包含处理结果和关键帧路径
        """
        try:
            print(f"\n开始处理视频: {video_path}")
            print(f"输出目录: {output_dir}\n")
            
            keyframes = self.extract_keyframes(video_path, output_dir)
            
            result = {
                "success": True,
                "message": f"成功提取 {len(keyframes)} 个关键帧",
                "keyframes": keyframes
            }
            print(f"\n处理完成: {result['message']}")
            return result
            
        except Exception as e:
            print(f"\n处理失败: {str(e)}")
            return {
                "success": False,
                "message": f"处理失败: {str(e)}",
                "keyframes": []
            }

# 测试代码
if __name__ == "__main__":
    try:
        # 创建处理器实例
        processor = VideoProcessor(threshold=10, edge_threshold=50)
        
        # 测试视频处理
        result = processor.process_video(
            video_path="test.mp4",
            output_dir="output"
        )
        
        # 打印结果
        print("\n最终结果:")
        print(result)
        
    except Exception as e:
        print(f"\n程序执行出错: {e}")
        sys.exit(1) 