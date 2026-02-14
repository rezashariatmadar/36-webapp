import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'node:path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (!id.includes('node_modules')) return
          if (id.includes('@mui/') || id.includes('@emotion/')) return 'mui'
          if (id.includes('@react-three/fiber') || id.includes('/three/')) return 'three-stack'
          if (id.includes('/motion/') || id.includes('/gsap/')) return 'motion-gsap'
          if (id.includes('react-multi-date-picker') || id.includes('react-date-object')) return 'date-stack'
        },
      },
    },
  },
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
  },
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://127.0.0.1:8000',
      '/admin': 'http://127.0.0.1:8000',
      '/media': 'http://127.0.0.1:8000',
      '/static': 'http://127.0.0.1:8000'
    }
  }
})
