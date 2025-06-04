import path from 'path';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, '.', '');
    return {
      base: '/',
      define: {
        'process.env.API_KEY': JSON.stringify(env.GEMINI_API_KEY),
        'process.env.GEMINI_API_KEY': JSON.stringify(env.GEMINI_API_KEY)
      },
      resolve: {
        alias: {
          '@': path.resolve(__dirname, '.'),
        }
      },
      // 构建配置
      build: {
        outDir: 'dist',
        assetsDir: 'assets',
        // 确保资源文件路径正确
        rollupOptions: {
          output: {
            assetFileNames: 'assets/[name]-[hash][extname]'
          }
        }
      }
    };
});
