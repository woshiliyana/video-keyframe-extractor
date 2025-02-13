# 视频关键帧提取工具

一个基于 Next.js 和 FastAPI 的视频关键帧提取工具，可以智能识别并提取视频中的关键帧。

## 功能特点

- 视频上传和处理
- 可调节的关键帧提取参数
- 实时预览提取的关键帧
- 批量下载关键帧
- 详细的参数调整指南

## 技术栈

### 前端
- Next.js
- TypeScript
- Tailwind CSS

### 后端
- FastAPI
- OpenCV
- NumPy

## 快速开始

### 前端启动
# 安装依赖
npm install

# 启动开发服务器
npm run dev

### 后端启动
# 进入后端目录
cd backend

# 启动服务器
uvicorn main:app --reload --port 8001

## 日常使用说明

每次使用时需要执行以下步骤：

1. 打开两个终端窗口

2. 第一个终端启动后端服务：
   ```bash
   # 进入后端目录
   cd backend
   
   # 激活虚拟环境
   source venv/bin/activate  # macOS/Linux
   # 或
   .\venv\Scripts\activate  # Windows
   
   # 启动后端服务
   uvicorn main:app --reload --port 8001
   ```

3. 第二个终端启动前端服务：
   ```bash
   # 如果不在前端目录，需要先进入：
   # cd 短视频提取关键帧
   
   # 启动前端服务（指定端口 3001）
   npm run dev -- -p 3001
   ```

4. 打开浏览器访问：http://localhost:3001

注意事项：
- ⚠️ 必须先激活虚拟环境再启动后端服务
- ⚠️ 前端服务需要指定 3001 端口
- ⚠️ 两个终端窗口都需要保持开着
- ⚠️ 使用完后可以用 Ctrl+C 停止服务

退出步骤：
1. 在两个终端中分别按 Ctrl+C 停止服务
2. 在后端终端中输入 `deactivate` 退出虚拟环境
3. 关闭终端窗口和浏览器

## 使用方法

1. 启动前端和后端服务器
2. 访问 http://localhost:3001
3. 上传视频文件
4. 调整参数（可参考 [阈值调整指南](docs/threshold-guide.md)）
5. 点击"开始处理"
6. 查看和下载提取的关键帧

## 参数说明

详细的参数调整指南请参考：[阈值调整指南](docs/threshold-guide.md)

- **帧差阈值**：控制判断两帧之间差异的敏感度（1-10）
- **边缘检测阈值**：控制画面边缘检测的灵敏度（20-50）
- **直方图阈值**：控制画面整体颜色变化的判断标准（500-2000）

## 目录结构

.
├── src/                # 前端源代码
│   ├── app/           # Next.js 应用代码
│   └── ...
├── backend/           # 后端代码
│   ├── main.py       # FastAPI 主程序
│   └── ...
├── docs/             # 文档
│   └── threshold-guide.md  # 阈值调整指南
└── README.md         # 项目说明

## 注意事项

- 确保同时运行前端和后端服务器
- 视频文件大小可能影响处理时间
- 不同类型的视频可能需要不同的参数设置

## 许可证

MIT License