"use client";

import Image from "next/image";
import { useState, useCallback } from "react";
import { Upload, Image as ImageIcon } from "lucide-react";
import { useDropzone } from "react-dropzone";
import { motion } from "framer-motion";



interface ImageUploaderProps {
    onImageUpload: (file: File) => void;
}
export default function ImageUploader({ onImageUpload }: ImageUploaderProps) {
    const onDrop = useCallback((acceptedFiles: File[]) => {
        const file = acceptedFiles[0];
        if (file) {
            const url = URL.createObjectURL(file);
            onImageUpload(file);
        }
      }, [onImageUpload]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: { 
            "image/*": [".png", ".jpg", ".jpeg", ".gif", ".webp"] 
        },
        maxFiles: 1,
        multiple: false,
    });

    return (
        <motion.div
            className="flex flex-col justify-center items-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            whileHover={{ scale: 1.05 }}>

            <div className={`
                border-2 border-dashed border-gray-300 rounded-xl max-w-xl text-center 
                cursor-pointers transition-all duration-300 hover:border--400 break-all p-12 
                ${isDragActive
                    ? "border-white bg-white/10" 
                    : "border-gray-600 hover:border-white/5"}`}>

                <input {...getInputProps()} />
                <motion.div 
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    className="flex flex-col items-center justify-center gap-4" {...getRootProps()}
                    >

                    {isDragActive ? (
                        <ImageIcon className="w-16 h-16 text-white" />
                    ) : (
                        <Upload className="w-16 h-16 text-white" />
                    )}

                    <div className="text-white">
                        <p className="text-xl font-medium mt-4">
                            {isDragActive
                                ? "Drop the image here"
                                : "Upload an image"}
                        </p>
                        <p className="text-gray-400 text-sm mt-2">
                            Drag and drop an image 
                        </p>
                    </div>
                </motion.div>
            </div>
        </motion.div>
    );
}