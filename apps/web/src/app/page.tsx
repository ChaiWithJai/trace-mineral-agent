import { Header, ResearchChat } from "@/components";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1 max-w-4xl w-full mx-auto">
        <ResearchChat />
      </main>
    </div>
  );
}
