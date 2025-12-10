import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: "Trace Mineral Discovery",
  description: "Multi-paradigm research for trace mineral therapeutics",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-cream-100 text-charcoal antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
