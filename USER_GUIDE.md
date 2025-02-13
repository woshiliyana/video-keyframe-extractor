# 视频关键帧提取工具 - 用户使用指南

## 1. 准备工作

确保你的目录结构如下：

video_keyframes/
├── video_processor.py   # 核心处理程序
├── test.py             # 测试脚本
├── output/             # 输出目录
└── requirements.txt    # 依赖文件

## 2. 处理新视频

### 步骤 1: 准备视频文件
- 将你的视频文件复制到 video_keyframes 目录
- 视频可以使用任何名称，如 my_video.mp4

### 步骤 2: 运行程序
使用默认参数：
python test.py my_video.mp4

或者自定义参数（更敏感的检测）：
python test.py my_video.mp4 -t 10 -e 40 -hist 2500

### 步骤 3: 查看结果
- 所有关键帧图片都保存在 output 目录中
- 图片按照帧号命名，如 keyframe_0.jpg, keyframe_100.jpg 等
- 程序会显示提取了多少个关键帧
- 可以直接打开 output 目录查看所有图片

## 3. 处理多个视频

### 方法 1: 清理后处理
1. 删除旧的关键帧：
   在 video_keyframes 目录下运行：
   rm -rf output/*

2. 处理新视频：
   python test.py new_video.mp4

### 方法 2: 使用不同输出目录
为每个视频使用独立的输出目录：
python test.py video1.mp4 -o output_video1
python test.py video2.mp4 -o output_video2

## 4. 参数调整

如果提取的关键帧太多或太少，可以调整参数：

提取的帧太多？增加阈值：
python test.py video.mp4 -t 15 -e 50 -hist 3500

提取的帧太少？降低阈值：
python test.py video.mp4 -t 8 -e 35 -hist 2000

## 5. 常见问题

### Q: 如何知道使用什么参数？
A: 
1. 先用默认参数测试
2. 查看结果数量
3. 根据需要调整参数：
   - 帧数太多：提高阈值
   - 帧数太少：降低阈值

### Q: 处理新视频前需要删除旧的输出吗？
A: 
- 程序会自动清理输出目录
- 但建议为不同视频使用不同的输出目录

### Q: 支持哪些视频格式？
A: 支持常见格式：
- MP4
- AVI
- MOV
- 等

## 6. 使用建议

1. 先用短视频测试参数
2. 记录效果好的参数组合
3. 重要视频建议使用独立输出目录
4. 定期备份重要的关键帧

## 7. 命令参数说明

查看帮助：
python test.py --help

参数说明：
- -t 或 --threshold: 帧差阈值（默认：12）
- -e 或 --edge-threshold: 边缘阈值（默认：45）
- -hist 或 --hist-threshold: 直方图阈值（默认：3000）
- -o 或 --output: 输出目录（默认：output）