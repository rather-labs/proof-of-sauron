export interface ImageMetadata {
    fileName: string;
    fileSize: string;
    dimensions: string;
    dateCreated: string;
    camera?: string;
    location?: string;
    software?: string;
  }
  
  export interface VerificationResult {
    realPercentage: number;
    metadata: ImageMetadata;
    proofGenerated: boolean;
    proofVerified: boolean | null;
    txHash?: string;
  }