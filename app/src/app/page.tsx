"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import ImageUploader from "@/app/components/ImageUploader";
import Header from "@/app/components/Header";
import VerificationProcess from "@/app/components/VerificationProcess";
import VerificationResult from "@/app/components/VerificationResult";

// to be replaced
import { verifyImage, generateProof, verifyProof } from "@/app/utils/mockData";


export default function Home() {
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [isVerifying, setIsVerifying] = useState(false);
  const [verificationResult, setVerificationResult] = useState<any | null>(null);
  const [isGeneratingProof, setIsGeneratingProof] = useState(false);
  const [isVerifyingProof, setIsVerifyingProof] = useState(false);

  const handleImageUpload = (file: File) => {
    const imageUrl = URL.createObjectURL(file);
    setUploadedImage(imageUrl);
    setUploadedFile(file);
    setIsVerifying(true);
    setVerificationResult(null);
  };

  const handleVerificationComplete = async () => {
    if (uploadedFile) {
      const result = await verifyImage(uploadedFile);
      setVerificationResult(result);
      setIsVerifying(false);
    }
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="gap-4 row-start-2 items-center sm:items-start text-center">
        <header className="mb-8">
          <h1 className="p-4 text-5xl font-bold tracking-tighter">Proof of Sauron</h1>
          <p className="text-md text-gray-400">Prove image authenticity with zero-knowledge cryptography"</p>
          <p className="text-md text-gray-400"> Don't trust—verify</p> 
        </header>

        <ImageUploader  onImageUpload={handleImageUpload} />
        
        {isVerifying && (
            <motion.div
              key="verifying"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <VerificationProcess 
                isVerifying={isVerifying} 
                onVerificationComplete={handleVerificationComplete} 
              />
            </motion.div>
          )}

      </main>
    </div>
  );
}