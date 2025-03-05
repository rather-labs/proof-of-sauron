import ImageUploader from "@/app/components/ImageUploader";
import Image from "next/image";

export default function Home() {

  const handleImageUpload = (file: File) => {
    const url = URL.createObjectURL(file);
    console.log
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="gap-4 row-start-2 items-center sm:items-start text-center">
        <header className="mb-8">
          <h1 className="p-4 text-5xl font-bold tracking-tighter">Proof of Sauron</h1>
          <p className="text-md text-gray-400">Prove image authenticity with zero-knowledge cryptography"</p>
          <p className="text-md text-gray-400"> Don't trust—verify</p> 
        </header>

        <ImageUploader />
        
      </main>
    </div>
  );
}