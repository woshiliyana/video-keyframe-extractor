import { Box, Text, VStack, Progress } from '@chakra-ui/react';
import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

export const VideoUpload = () => {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setUploading(true);
    setProgress(0);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('http://localhost:8001/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / (progressEvent.total || 100)
          );
          setProgress(percentCompleted);
        },
      });

      console.log('Upload successful:', response.data);
      // TODO: 显示提取的帧
      
    } catch (error) {
      console.error('Upload failed:', error);
      // TODO: 显示错误信息
    } finally {
      setUploading(false);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'video/*': ['.mp4', '.avi', '.mov']
    },
    multiple: false
  });

  return (
    <VStack spacing={4} w="100%">
      <Box
        {...getRootProps()}
        w="100%"
        h="200px"
        border="2px dashed"
        borderColor={isDragActive ? "blue.400" : "gray.200"}
        borderRadius="lg"
        display="flex"
        alignItems="center"
        justifyContent="center"
        bg={isDragActive ? "blue.50" : "gray.50"}
        cursor="pointer"
        transition="all 0.2s"
        _hover={{ borderColor: "blue.400" }}
      >
        <input {...getInputProps()} />
        <Text color="gray.500">
          {isDragActive
            ? "放开以上传视频"
            : "拖拽视频文件到这里，或点击选择文件"}
        </Text>
      </Box>

      {uploading && (
        <Box w="100%">
          <Progress value={progress} size="sm" colorScheme="blue" />
          <Text mt={2} fontSize="sm" color="gray.500">
            上传中... {progress}%
          </Text>
        </Box>
      )}
    </VStack>
  );
}; 