import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Loader2 } from 'lucide-react';

interface VerificationProcessProps {
  isVerifying: boolean;
  onVerificationComplete: () => void;
}

const VerificationProcess: React.FC<VerificationProcessProps> = ({ 
  isVerifying, 
  onVerificationComplete 
}) => {
  const [progress, setProgress] = useState(0);
  
  useEffect(() => {
    if (isVerifying) {
      const interval = setInterval(() => {
        setProgress(prev => {
          const newProgress = prev + Math.random() * 5;
          if (newProgress >= 100) {
            clearInterval(interval);
            setTimeout(() => {
              onVerificationComplete();
            }, 500);
            return 100;
          }
          return newProgress;
        });
      }, 200);
      
      return () => clearInterval(interval);
    } else {
      setProgress(0);
    }
  }, [isVerifying, onVerificationComplete]);

  if (!isVerifying) return null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="w-full max-w-xl mx-auto"
    >
      <div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/10">
        <div className="flex items-center justify-center mb-6">
          <Loader2 className="w-10 h-10 text-white animate-spin mr-3" />
          <h2 className="text-2xl font-semibold text-white">Verifying Image</h2>
        </div>
        
        <div className="space-y-6">
          <div className="space-y-2">
            <div className="flex justify-between text-sm text-gray-300">
              <span>Analyzing metadata</span>
              <span>{Math.min(100, Math.round(progress * 1.5))}%</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <motion.div 
                className="bg-white h-2 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${Math.min(100, Math.round(progress * 1.5))}%` }}
                transition={{ duration: 0.3 }}
              />
            </div>
          </div>
          
          <div className="space-y-2">
            <div className="flex justify-between text-sm text-gray-300">
              <span>Detecting AI patterns</span>
              <span>{Math.min(100, Math.round(progress))}%</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <motion.div 
                className="bg-white h-2 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${Math.min(100, Math.round(progress))}%` }}
                transition={{ duration: 0.3 }}
              />
            </div>
          </div>
          
          <div className="space-y-2">
            <div className="flex justify-between text-sm text-gray-300">
              <span>Preparing verification</span>
              <span>{Math.min(100, Math.round(progress * 0.7))}%</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <motion.div 
                className="bg-white h-2 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${Math.min(100, Math.round(progress * 0.7))}%` }}
                transition={{ duration: 0.3 }}
              />
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default VerificationProcess;