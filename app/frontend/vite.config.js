import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/predict': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/portfolio': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/history': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
})
