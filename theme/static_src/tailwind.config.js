module.exports = {
  content: [
      '../../../**/*.{html,py,js}',
  ],
  theme: {
    extend: {
      screens: {
        'xs': '375px',
      },
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
          // Apple Dark Mode Premium Configuration
          "primary": "#0A84FF",      // iOS System Blue
          "primary-content": "#ffffff",
          
          "secondary": "#5E5CE6",    // iOS System Indigo
          "secondary-content": "#ffffff",
          
          "accent": "#32D74B",       // iOS System Green (Success/Action)
          "accent-content": "#000000",
          
          "neutral": "#1C1C1E",      // Secondary System Background
          "neutral-content": "#ffffff",
          
          "base-100": "#000000",     // Pure Black (OLED)
          "base-200": "#1C1C1E",     // Secondary Grouped
          "base-300": "#2C2C2E",     // Tertiary Grouped
          "base-content": "#FFFFFF", // Primary Text
          
          "info": "#64D2FF",
          "success": "#30D158",
          "warning": "#FFD60A",
          "error": "#FF453A",        // iOS System Red
          
          "--rounded-box": "1.5rem",   // Slightly softer, more liquid
          "--rounded-btn": "9999px",   // Pill shape default
          "--rounded-badge": "9999px",
          "--animation-btn": "0.2s",
          "--animation-input": "0.2s",
          "--btn-focus-scale": "0.98",
          "--border-btn": "1px",       // Subtle edge for liquid glass
          "--tab-border": "0px",
          "--tab-radius": "0.75rem",
        },
      },
    ],
  },
  theme: {
    extend: {
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
    }
  },
}
