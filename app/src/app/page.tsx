import ImageUploader from "@/components/ImageUploader";
import Image from "next/image";

export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-4 row-start-2 items-center sm:items-start text-center">
        <header className="mb-8">
          <h1 className="p-4 text-5xl font-bold tracking-tighter">Proof of Sauron</h1>
          <p className="text-lg text-gray-500">"Don't trust—verify. Prove image authenticity with zero-knowledge cryptography."</p>
        </header>

        <ImageUploader />
        
      </main>
    </div>
  );
}