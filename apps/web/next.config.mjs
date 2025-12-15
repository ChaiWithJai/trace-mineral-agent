/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    LANGGRAPH_API_URL: process.env.LANGGRAPH_API_URL || "http://127.0.0.1:2024",
    NEXT_PUBLIC_LANGGRAPH_API_URL: process.env.LANGGRAPH_API_URL || "http://127.0.0.1:2024",
  },
};

export default nextConfig;
