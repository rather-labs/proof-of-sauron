"use client";

import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, Image as ImageIcon } from 'lucide-react';
import { motion } from 'framer-motion';

interface ImageUploaderProps {
  onImageUpload?: (file: File) => void;
}

const ImageUploader: React.FC<ImageUploaderProps> = ({ onImageUpload }) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      if (onImageUpload) {
        onImageUpload(acceptedFiles[0]);
      }
    }
  }, [onImageUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.webp']
    },
    maxFiles: 1
  });

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-xl mx-auto"
    >
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-300 ${
          isDragActive 
            ? 'border-white bg-white/10' 
            : 'border-gray-600 hover:border-white/70 hover:bg-white/5'
        }`}
      >
        <input {...getInputProps()} />
        <motion.div
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="flex flex-col items-center justify-center gap-4"
        >
          {isDragActive ? (
            <ImageIcon className="w-16 h-16 text-white" />
          ) : (
            <Upload className="w-16 h-16 text-white" />
          )}
          <div className="text-white">
            <p className="text-xl font-medium mb-2">
              {isDragActive ? 'Drop the image here' : 'Upload an image'}
            </p>
            <p className="text-gray-400 text-sm">
              Drag and drop an image, or click to select
            </p>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default ImageUploader;