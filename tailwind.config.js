/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'calc-bg': '#1c1c1c',
        'calc-display': '#000000',
        'calc-button': '#505050',
        'calc-button-orange': '#ff9500',
        'calc-button-light': '#d4d4d2',
      },
      animation: {
        'button-press': 'buttonPress 0.1s ease-in-out',
      },
      keyframes: {
        buttonPress: {
          '0%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(0.95)' },
          '100%': { transform: 'scale(1)' },
        }
      }
    },
  },
  plugins: [],
}

