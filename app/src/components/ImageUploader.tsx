"use client";

import { useState } from "react";
import Image from "next/image";
import { motion } from "framer-motion";

export default function ImageUploader() {
  return (
    <motion.div
        className="flex flex-col justify-center items-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}   
    >
        <div className="border-2 border-dashed border-gray-300 rounded-xl max-w-xl text-center cursor-pointer transition-all duration-300 hover:border-orange-400 break-all p-12 ">
        </div>
    </motion.div>
       
  );
}
