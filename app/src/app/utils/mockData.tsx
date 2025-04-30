import { ImageMetadata, VerificationResult } from '../types';

// This will be populated with correct data in the future
export const verifyImage = (file: File): Promise<VerificationResult> => {
  return new Promise((resolve) => {
    // Simulate processing time
    setTimeout(() => {
      // Generate random result for demo purposes
      const realPercentage = Math.floor(Math.random() * 101);
      
      const metadata: ImageMetadata = {
        fileName: file.name,
        fileSize: formatFileSize(file.size),
        dimensions: '1920 x 1080',
        dateCreated: new Date().toLocaleDateString(),
        camera: Math.random() > 0.5 ? 'Canon EOS R5' : undefined,
        software: realPercentage < 50 ? 'Adobe Photoshop' : undefined
      };
      
      resolve({
        realPercentage,
        metadata,
        proofGenerated: false,
        proofVerified: null
      });
    }, 3000);
  });
};

export const generateProof = (): Promise<boolean> => {
  return new Promise((resolve) => {
    // Simulate processing time
    setTimeout(() => {
      resolve(true);
    }, 2500);
  });
};

const generateRandomHash = (): string => {
  const characters = '0123456789abcdef';
  let hash = '0x';
  for (let i = 0; i < 64; i++) {
    hash += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return hash;
};

export const verifyProof = (): Promise<{verified: boolean, txHash: string}> => {
  return new Promise((resolve) => {
    // Simulate processing time
    setTimeout(() => {
      // Random result for demo purposes
      const verified = Math.random() > 0.3;
      const txHash = generateRandomHash();
      resolve({
        verified,
        txHash
      });
    }, 2000);
  });
};

// Helper function to format file size
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};