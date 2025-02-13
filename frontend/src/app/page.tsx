'use client'

import { useState } from 'react';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [keyframes, setKeyframes] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // 添加阈值状态
  const [threshold, setThreshold] = useState(5);
  const [edgeThreshold, setEdgeThreshold] = useState(30);
  const [histThreshold, setHistThreshold] = useState(1000);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError('请选择一个视频文件');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('video', file);
    formData.append('threshold', threshold.toString());
    formData.append('edge_threshold', edgeThreshold.toString());
    formData.append('hist_threshold', histThreshold.toString());

    try {
      const response = await fetch('http://localhost:8001/api/process', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setKeyframes(data.keyframes || []);
      setLoading(false);
    } catch (error) {
      console.error('上传失败:', error);
      setError('上传过程中发生错误');
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/download');
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'keyframes.zip';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('下载失败:', error);
      setError('下载过程中发生错误');
    }
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">视频关键帧提取</h1>
        
        <form onSubmit={handleSubmit} className="mb-8 space-y-6">
          {/* 文件上传 */}
          <div className="mb-4">
            <input
              type="file"
              accept="video/*"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-50 file:text-blue-700
                hover:file:bg-blue-100"
            />
          </div>

          {/* 阈值调节 */}
          <div className="space-y-4 p-4 bg-gray-50 rounded-lg">
            <h2 className="text-lg font-semibold mb-4">参数调节</h2>
            
            <div>
              <label className="block text-sm font-medium text-gray-700">
                帧差阈值（越小越敏感，建议：1-10）: {threshold}
              </label>
              <input
                type="range"
                min="1"
                max="20"
                value={threshold}
                onChange={(e) => setThreshold(Number(e.target.value))}
                className="w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                边缘检测阈值（越小越敏感，建议：20-50）: {edgeThreshold}
              </label>
              <input
                type="range"
                min="10"
                max="100"
                value={edgeThreshold}
                onChange={(e) => setEdgeThreshold(Number(e.target.value))}
                className="w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                直方图阈值（越小越敏感，建议：500-2000）: {histThreshold}
              </label>
              <input
                type="range"
                min="100"
                max="5000"
                step="100"
                value={histThreshold}
                onChange={(e) => setHistThreshold(Number(e.target.value))}
                className="w-full"
              />
            </div>
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-500 text-white px-4 py-2 rounded
              hover:bg-blue-600 disabled:bg-gray-400"
          >
            {loading ? '处理中...' : '开始处理'}
          </button>
        </form>

        {error && (
          <div className="text-red-500 mb-4">{error}</div>
        )}

        {keyframes.length > 0 && (
          <div>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">
                提取的关键帧（共 {keyframes.length} 帧）
              </h2>
              <button
                onClick={handleDownload}
                className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
              >
                下载全部
              </button>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {keyframes.map((frame, index) => {
                const fullImageUrl = `http://localhost:8001${frame}`;
                return (
                  <div key={frame} className="aspect-video relative">
                    <img
                      src={fullImageUrl}
                      alt={`关键帧 ${index + 1}`}
                      className="w-full h-full object-cover rounded"
                    />
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
