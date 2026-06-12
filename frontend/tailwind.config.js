/** @type {import('tailwindcss').Config} */

import tailwindcssAnimate from "tailwindcss-animate";

export default {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        dg: {
          base: "var(--dg-bg-base)",
          surface: "var(--dg-bg-surface)",
          elevated: "var(--dg-bg-elevated)",
          overlay: "var(--dg-bg-overlay)",
          border: "var(--dg-border-subtle)",
          accent: "var(--dg-accent-primary)",
          warm: "var(--dg-accent-warm)",
          muted: "var(--dg-accent-muted)",
          olive: "var(--dg-olive)",
          textPrimary: "var(--dg-text-primary)",
          textSecondary: "var(--dg-text-secondary)",
          textMuted: "var(--dg-text-muted)",
          code: "var(--dg-text-code)",
          error: "var(--dg-error)",
          warning: "var(--dg-warning)",
          success: "var(--dg-success)",
        },
        border: "var(--border)",
        input: "var(--input)",
        ring: "var(--ring)",
        background: "var(--dg-bg-base)",
        foreground: "var(--dg-text-primary)",
        primary: {
          DEFAULT: "var(--primary)",
          foreground: "var(--primary-foreground)",
        },
        secondary: {
          DEFAULT: "var(--secondary)",
          foreground: "var(--secondary-foreground)",
        },
        destructive: {
          DEFAULT: "var(--destructive)",
          foreground: "var(--destructive-foreground)",
        },
        muted: {
          DEFAULT: "var(--muted)",
          foreground: "var(--muted-foreground)",
        },
        accent: {
          DEFAULT: "var(--accent)",
          foreground: "var(--accent-foreground)",
        },
        popover: {
          DEFAULT: "var(--popover)",
          foreground: "var(--popover-foreground)",
        },
        card: {
          DEFAULT: "var(--card)",
          foreground: "var(--card-foreground)",
        },
      },
      fontFamily: {
        syne: ["Inter", "system-ui", "sans-serif"],
        inter: ["Inter", "system-ui", "sans-serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
        squircle: "22px",
        pill: "999px",
      },
      backdropBlur: {
        console: "16px",
      },
    },
  },
  plugins: [tailwindcssAnimate],
};
