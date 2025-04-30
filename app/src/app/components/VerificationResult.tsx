import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, XCircle, AlertCircle, FileText, Copy, Check } from 'lucide-react';
import { VerificationResult as VerificationResultType } from '../types';

interface VerificationResultProps {
  result: VerificationResultType;
  image: string;
  onGenerateProof: () => void;
  onVerifyProof: () => void;
  isGeneratingProof: boolean;
  isVerifyingProof: boolean;
}

const VerificationResultComponent: React.FC<VerificationResultProps> = ({
  result,
  image,
  onGenerateProof,
  onVerifyProof,
  isGeneratingProof,
  isVerifyingProof
}) => {
  const [copied, setCopied] = useState(false);
  const { realPercentage, metadata, proofGenerated, proofVerified, txHash } = result;
  
  const getStatusColor = () => {
    if (realPercentage >= 80) return 'bg-green-500';
    if (realPercentage >= 40) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getStatusIcon = () => {
    if (realPercentage >= 80) return <CheckCircle className="w-6 h-6 text-green-500" />;
    if (realPercentage >= 40) return <AlertCircle className="w-6 h-6 text-yellow-500" />;
    return <XCircle className="w-6 h-6 text-red-500" />;
  };

  const getProofStatusIcon = () => {
    if (proofVerified === true) return <CheckCircle className="w-8 h-8 text-green-500" />;
    if (proofVerified === false) return <XCircle className="w-8 h-8 text-red-500" />;
    return null;
  };

  const handleCopyTxHash = () => {
    if (txHash) {
      navigator.clipboard.writeText(txHash);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // Function to truncate hash for display
  const truncateHash = (hash: string) => {
    if (!hash) return '';
    return `${hash.substring(0, 8)}...${hash.substring(hash.length - 8)}`;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6"
    >
      <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 flex items-center justify-center">
        <div className="relative w-full h-full max-h-[400px] flex items-center justify-center overflow-hidden rounded-lg">
          <img 
            src={image} 
            alt="Uploaded image" 
            className="max-w-full max-h-[400px] object-contain"
          />
        </div>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-semibold text-white">Verification Results</h2>
          {getStatusIcon()}
        </div>

        <div className="mb-6">
          <div className="flex justify-between text-sm text-gray-300 mb-2">
            <span>AI Detection</span>
            <span className="font-medium text-white">{realPercentage}% Real</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-3">
            <motion.div 
              className={`h-3 rounded-full ${getStatusColor()}`}
              initial={{ width: 0 }}
              animate={{ width: `${realPercentage}%` }}
              transition={{ duration: 0.8, ease: "easeOut" }}
            />
          </div>
        </div>

        <div className="mb-6">
          <h3 className="text-lg font-medium text-white mb-3 flex items-center">
            <FileText className="w-5 h-5 mr-2" />
            Image Metadata
          </h3>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div className="text-gray-400">File Name:</div>
            <div className="text-white font-medium">{metadata.fileName}</div>
            
            <div className="text-gray-400">File Size:</div>
            <div className="text-white font-medium">{metadata.fileSize}</div>
            
            <div className="text-gray-400">Dimensions:</div>
            <div className="text-white font-medium">{metadata.dimensions}</div>
            
            <div className="text-gray-400">Date Created:</div>
            <div className="text-white font-medium">{metadata.dateCreated}</div>
            
            {metadata.camera && (
              <>
                <div className="text-gray-400">Camera:</div>
                <div className="text-white font-medium">{metadata.camera}</div>
              </>
            )}
            
            {metadata.software && (
              <>
                <div className="text-gray-400">Software:</div>
                <div className="text-white font-medium">{metadata.software}</div>
              </>
            )}
          </div>
        </div>

        {txHash && proofVerified !== null && (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6 p-4 bg-white/5 rounded-lg"
          >
            <h3 className="text-lg font-medium text-white mb-2">Transaction Hash</h3>
            <div className="flex items-center">
              <div className="bg-white/10 rounded-l-md py-2 px-3 flex-grow overflow-hidden text-ellipsis font-mono text-sm text-gray-300">
                {truncateHash(txHash)}
              </div>
              <button 
                onClick={handleCopyTxHash}
                className="bg-white/20 hover:bg-white/30 rounded-r-md p-2 transition-colors"
                title="Copy to clipboard"
              >
                {copied ? (
                  <Check className="w-5 h-5 text-green-400" />
                ) : (
                  <Copy className="w-5 h-5 text-white" />
                )}
              </button>
            </div>
            <p className="text-xs text-gray-400 mt-2">
              This transaction hash verifies the proof on the blockchain
            </p>
          </motion.div>
        )}

        <div className="space-y-3">
          {!proofGenerated ? (
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={onGenerateProof}
              disabled={isGeneratingProof}
              className={`w-full py-3 px-4 rounded-lg font-medium flex items-center justify-center ${
                isGeneratingProof 
                  ? 'bg-white/20 text-gray-300 cursor-not-allowed' 
                  : 'bg-white text-black hover:bg-white/90'
              }`}
            >
              {isGeneratingProof ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Generating Proof...
                </>
              ) : (
                'Generate Proof'
              )}
            </motion.button>
          ) : (
            <div className="space-y-3">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={onVerifyProof}
                disabled={isVerifyingProof || proofVerified !== null}
                className={`w-full py-3 px-4 rounded-lg font-medium flex items-center justify-center ${
                  isVerifyingProof || proofVerified !== null
                    ? 'bg-white/20 text-gray-300 cursor-not-allowed' 
                    : 'bg-white text-black hover:bg-white/90'
                }`}
              >
                {isVerifyingProof ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Verifying Proof...
                  </>
                ) : proofVerified !== null ? (
                  <div className="flex items-center justify-center">
                    {getProofStatusIcon()}
                    <span className="ml-2">
                      {proofVerified ? 'Proof Verified' : 'Proof Invalid'}
                    </span>
                  </div>
                ) : (
                  'Verify Proof'
                )}
              </motion.button>
              
              {proofVerified !== null && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`p-4 rounded-lg flex items-center ${
                    proofVerified ? 'bg-green-500/20 text-green-200' : 'bg-red-500/20 text-red-200'
                  }`}
                >
                  {proofVerified ? (
                    <CheckCircle className="w-5 h-5 mr-2 flex-shrink-0" />
                  ) : (
                    <XCircle className="w-5 h-5 mr-2 flex-shrink-0" />
                  )}
                  <span>
                    {proofVerified 
                      ? 'The proof has been successfully verified. This image is authentic.' 
                      : 'The proof verification failed. This image may have been manipulated.'}
                  </span>
                </motion.div>
              )}
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default VerificationResultComponent;