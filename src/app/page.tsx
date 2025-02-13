'use client'

import { useState } from 'react';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [keyframes, setKeyframes] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
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
      if (data.success) {
        setKeyframes(data.keyframes);
      } else {
        setError(data.message || '处理失败');
      }
    } catch (err) {
      setError('上传或处理过程中发生错误');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/download', {
        method: 'GET'
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'keyframes.zip';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        setError('下载失败');
      }
    } catch (err) {
      setError('下载过程中发生错误');
    }
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">视频关键帧提取</h1>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block mb-2">
              选择视频文件：
              <input
                type="file"
                accept="video/*"
                onChange={handleFileChange}
                className="mt-1 block w-full"
              />
            </label>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block mb-2">
                帧差阈值 ({threshold}):
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={threshold}
                  onChange={(e) => setThreshold(Number(e.target.value))}
                  className="w-full"
                />
              </label>
            </div>

            <div>
              <label className="block mb-2">
                边缘检测阈值 ({edgeThreshold}):
                <input
                  type="range"
                  min="20"
                  max="50"
                  value={edgeThreshold}
                  onChange={(e) => setEdgeThreshold(Number(e.target.value))}
                  className="w-full"
                />
              </label>
            </div>

            <div>
              <label className="block mb-2">
                直方图阈值 ({histThreshold}):
                <input
                  type="range"
                  min="500"
                  max="2000"
                  step="100"
                  value={histThreshold}
                  onChange={(e) => setHistThreshold(Number(e.target.value))}
                  className="w-full"
                />
              </label>
            </div>
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
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
                console.log('Full image URL:', fullImageUrl);
                return (
                  <div key={frame} className="aspect-video relative">
                    <img
                      src={fullImageUrl}
                      alt={`关键帧 ${index + 1}`}
                      className="w-full h-full object-cover rounded"
                      onError={(e) => console.error('Image load error:', e)}
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