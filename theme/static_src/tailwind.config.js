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
          // Dark Theme Configuration
          "primary": "#100370",      // Company Blue (Headers/Branding)
          "primary-content": "#ffffff",
          
          "secondary": "#63021f",    // Company Red
          "secondary-content": "#ffffff",
          
          "accent": "#00b5ff",       // Cyan (High visibility actions)
          "accent-content": "#000000",
          
          "neutral": "#0f0f0f",      // Very dark gray (Footer)
          "neutral-content": "#ffffff",
          
          "base-100": "#1c1917",     // Dark Grey (Main Background)
          "base-200": "#171513",     // Slightly darker (Secondary Background)
          "base-300": "#000000",     // Black (Borders/Inputs)
          "base-content": "#e5e7eb", // Light text
          
          "info": "#00b5ff",
          "success": "#00a96e",
          "warning": "#ffbe00",
          "error": "#ff5861",
          
          "--rounded-box": "0.5rem",
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