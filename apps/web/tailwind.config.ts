import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Princeton Idea Exchange inspired palette
        cream: {
          50: "#fdfcfa",
          100: "#f8f6f3",
          200: "#ebeae6",
          300: "#dddbd6",
          400: "#c5c3be",
        },
        charcoal: {
          DEFAULT: "#2a3132",
          light: "#5f6566",
          dark: "#1a2021",
        },
        accent: {
          DEFAULT: "#ff5900",
          light: "#ff7a33",
          dark: "#cc4700",
        },
        navy: {
          DEFAULT: "#001666",
          light: "#cadcfc",
        },
        // Keep mineral for compatibility
        mineral: {
          50: "#fff7ed",
          100: "#ffedd5",
          200: "#fed7aa",
          300: "#fdba74",
          400: "#fb923c",
          500: "#ff5900",
          600: "#cc4700",
          700: "#9a3412",
          800: "#7c2d12",
          900: "#431407",
        },
      },
      fontFamily: {
        serif: ["Libre Baskerville", "Georgia", "serif"],
        sans: ["DM Sans", "Inter", "system-ui", "sans-serif"],
      },
      borderRadius: {
        "4xl": "2rem",
        "5xl": "2.5rem",
      },
      animation: {
        "fade-in": "fadeIn 0.5s ease-out",
        "slide-up": "slideUp 0.4s ease-out",
        "pulse-soft": "pulseSoft 2s ease-in-out infinite",
        "typing": "typing 1.2s ease-in-out infinite",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        pulseSoft: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.7" },
        },
        typing: {
          "0%": { opacity: "0.3" },
          "50%": { opacity: "1" },
          "100%": { opacity: "0.3" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
