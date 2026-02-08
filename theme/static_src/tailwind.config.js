module.exports = {
  content: [
    '../../../**/*.{html,py,js,jsx}',
  ],
  theme: {
    extend: {
      screens: {
        xs: '375px',
      },
      colors: {
        company: {
          blue: '#100370',
          red: '#63021f',
        }
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInRight: {
          '0%': { transform: 'translateX(100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        }
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out forwards',
        'slide-in-right': 'slideInRight 0.3s cubic-bezier(0, 0, 0.2, 1) forwards',
      }
    },
  },
  plugins: [
    require('daisyui'),
  ],
  daisyui: {
    themes: [
      {
        minimalist: {
          "primary": "#100370",
          "primary-content": "#ffffff",

          "secondary": "#63021f",
          "secondary-content": "#ffffff",

          "accent": "#3a0348",
          "accent-content": "#ffffff",

          "neutral": "#1C1C1E",
          "neutral-content": "#ffffff",

          "base-100": "#000000",
          "base-200": "#1C1C1E",
          "base-300": "#2C2C2E",
          "base-content": "#FFFFFF",

          "info": "#64D2FF",
          "success": "#30D158",
          "warning": "#FFD60A",
          "error": "#FF453A",

          "--rounded-box": "1.5rem",
          "--rounded-btn": "9999px",
          "--rounded-badge": "9999px",
          "--animation-btn": "0.2s",
          "--animation-input": "0.2s",
          "--btn-focus-scale": "0.98",
          "--border-btn": "1px",
          "--tab-border": "0px",
          "--tab-radius": "0.75rem",
        },
      },
    ],
  },
};
