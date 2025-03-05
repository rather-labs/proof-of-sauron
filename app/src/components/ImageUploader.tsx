"use client";

import Image from "next/image";
import { useState } from "react";
import { useDropzone } from 'react-dropzone';
import { Upload, Image as ImageIcon } from "lucide-react";
import { motion } from "framer-motion";



interface ImageUploaderProps {
    onFileUpload: (file: File) => void;
}
export default function ImageUploader({ onFileUpload }: ImageUploaderProps) {
    const [isDragging, setIsDragging] = useState(false);

    const handleDragOver = (e: React.DragEvent) => {
        setIsDragging(true);
    };

    const handleDragLeave = (e: React.DragEvent) => {
        setIsDragging(false)
    };


    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);

        const file = e.dataTransfer.files[0];
        let isValidFile = e.dataTransfer.files.length != 0;
        isValidFile &&= file && file.type.startsWith("image/");

        if(isValidFile) {   
            const fileReader = new FileReader();
            // Handle file reading here if needed
            onFileUpload(file);
            console.log(file);

        }
        console.log(file );
    };

    return (
        <motion.div
            className="flex flex-col justify-center items-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            whileHover={{ scale: 1.05 }} 
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            
            >

            <div className={`
                border-2 border-dashed border-gray-300 rounded-xl max-w-xl text-center 
                cursor-pointers transition-all duration-300 hover:border--400 break-all p-12 
                ${isDragging
                    ? "border-white bg-white/10" 
                    : "border-gray-600 hover:border-white/5"}`}>
                <motion.div whileHover={{ scale: 1.1 }}>
                    
                </motion.div>
            </div>
        </motion.div>
    );
}