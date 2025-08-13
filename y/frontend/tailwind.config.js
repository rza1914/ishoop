/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'vazir': ['Vazirmatn', 'sans-serif'],
      },
      backdropBlur: {
        'xs': '2px',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'fade-in': 'fadeIn 0.5s ease-out',
        'scale-in': 'scaleIn 0.3s ease-out',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        glow: {
          'from': { boxShadow: '0 0 20px #667eea' },
          'to': { boxShadow: '0 0 30px #764ba2' },
        },
        slideUp: {
          'from': { transform: 'translateY(10px)', opacity: 0 },
          'to': { transform: 'translateY(0)', opacity: 1 },
        },
        slideDown: {
          'from': { transform: 'translateY(-10px)', opacity: 0 },
          'to': { transform: 'translateY(0)', opacity: 1 },
        },
        fadeIn: {
          'from': { opacity: 0 },
          'to': { opacity: 1 },
        },
        scaleIn: {
          'from': { transform: 'scale(0.9)', opacity: 0 },
          'to': { transform: 'scale(1)', opacity: 1 },
        },
      },
    },
  },
  plugins: [],
}