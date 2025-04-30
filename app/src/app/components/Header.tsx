import React from 'react';
import { motion } from 'framer-motion';
import { Eye } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="py-6 mb-8"
    >
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-center">
          <motion.div 
            className="flex items-center"
            whileHover={{ scale: 1.05 }}
          >
            <Eye className="w-10 h-10 text-white mr-3" />
            <h1 className="text-3xl font-bold text-white">Proof of Sauron</h1>
          </motion.div>
        </div>
        <div className="mt-2 text-center">
          <p className="text-gray-400">Verify the authenticity of images with zero-knowledge proofs</p>
        </div>
      </div>
    </motion.header>
  );
};

export default Header;