import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Tuko Kadi - Find IEBC Registration Centers",
  description: "Locate your nearest IEBC voter registration center in Kenya",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
