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

            <input {...getInputProps()} />
            <div className={`
                border-2 border-dashed border-gray-300 rounded-xl max-w-xl text-center 
                cursor-pointers transition-all duration-300 hover:border--400 break-all p-12 
                ${isDragActive
                    ? "border-white bg-white/10" 
                    : "border-gray-600 hover:border-white/5"}`}>
                <motion.div whileHover={{ scale: 1.1 }}>
                    
                </motion.div>
            </div>
        </motion.div>
    );
}