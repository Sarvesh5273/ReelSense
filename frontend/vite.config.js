import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // This forwards any request starting with /recommendations to your FastAPI server
      '/recommendations': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      // You might add this if you have a root endpoint or others
      '/root': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
});