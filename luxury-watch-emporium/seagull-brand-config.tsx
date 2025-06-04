import React from 'react'; // JSX支持所需
import { BrandInfo } from './seagull-watch-types';

// API密钥错误提示信息
export const API_KEY_ERROR_MESSAGE = "API Key not configured. Please set the API_KEY environment variable.";

// 品牌信息配置
export const BRAND_INFO: BrandInfo = {
  name: "SEAGULL",
  chineseName: "海鸥表",
  tagline: "中国制表行业的开创者和领先者",
  logoSvg: (
    <img 
      src="/images/seagull-logo.png" 
      alt="海鸥表 SEAGULL Logo" 
      width="70" 
      height="50" 
      className="object-contain filter invert brightness-200"
    />
  )
};

// Gemini AI模型配置
export const GEMINI_MODEL_TEXT = 'gemini-2.5-flash-preview-04-17';
export const GEMINI_MODEL_IMAGE = 'imagen-3.0-generate-002'; // 图像生成模型（如需要）

// 网站导航链接配置
export const NAVIGATION_LINKS = [
  { name: '首页', path: '/' },
  { name: '全部腕表', path: '/products' },
  { name: '品牌故事', path: '/about' },
  // { name: '联系我们', path: '/contact' }, // 可后续添加
];

// 网站页脚链接配置
export const FOOTER_LINKS = {
  company: [
    { name: '品牌故事', path: '/about' },
    { name: '制表工艺', path: '#' }, 
    { name: '品牌资讯', path: '#' },    
  ],
  support: [
    { name: '售后服务', path: '#' },         
    { name: '联系我们', path: '#' }, 
    { name: '产品保修', path: '#' },   
  ],
  legal: [
    { name: '隐私政策', path: '#' }, 
    { name: '使用条款', path: '#' },
  ],
};
