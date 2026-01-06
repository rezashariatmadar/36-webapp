module.exports = {
  content: [
      '../../../**/*.{html,py,js}',
  ],
  theme: {
    extend: {
      colors: {
        company: {
          blue: '#100370',
          red: '#63021f',
        }
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
          "accent": "#00b5ff",
          "neutral": "#1c1917",
          "base-100": "#ffffff",
          "base-200": "#f9fafb",
          "base-300": "#f3f4f6",
          "info": "#00b5ff",
          "success": "#00a96e",
          "warning": "#ffbe00",
          "error": "#ff5861",
          "--rounded-box": "0.5rem", // More squared for minimalist
          "--rounded-btn": "0.25rem",
          "--rounded-badge": "1.9rem",
          "--animation-btn": "0.25s",
          "--animation-input": "0.2s",
          "--btn-focus-scale": "0.98",
          "--border-btn": "1px",
          "--tab-border": "1px",
          "--tab-radius": "0.5rem",
        },
      },
    ],
  },
}
