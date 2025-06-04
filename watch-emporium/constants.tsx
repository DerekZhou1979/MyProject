import React from 'react'; // Required for JSX in logoSvg
import { BrandInfo } from './types';

export const API_KEY_ERROR_MESSAGE = "API Key not configured. Please set the API_KEY environment variable.";

export const BRAND_INFO: BrandInfo = {
  name: "Patek Philippe",
  chineseName: "百达斐丽",
  tagline: "Crafting Heirlooms for Generations.",
  logoSvg: (
    <svg width="40" height="40" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-brand-primary">
      <path d="M50 10C27.9086 10 10 27.9086 10 50C10 72.0914 27.9086 90 50 90C72.0914 90 90 72.0914 90 50C90 27.9086 72.0914 10 50 10ZM50 80C33.4315 80 20 66.5685 20 50C20 33.4315 33.4315 20 50 20C66.5685 20 80 33.4315 80 50C80 66.5685 66.5685 80 50 80Z" fill="currentColor"/>
      <path d="M50 30V50L65 57.5" stroke="currentColor" strokeWidth="5" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M35 50H25" stroke="currentColor" strokeWidth="5" strokeLinecap="round"/>
      <path d="M75 50H65" stroke="currentColor" strokeWidth="5" strokeLinecap="round"/>
      <path d="M50 25V35" stroke="currentColor" strokeWidth="5" strokeLinecap="round"/>
      <path d="M50 75V65" stroke="currentColor" strokeWidth="5" strokeLinecap="round"/>
    </svg>
  )
};

export const GEMINI_MODEL_TEXT = 'gemini-2.5-flash-preview-04-17';
// export const GEMINI_MODEL_IMAGE = 'imagen-3.0-generate-002'; // If image generation was needed

export const NAVIGATION_LINKS = [
  { name: 'Home', path: '/' },
  { name: 'All Watches', path: '/products' },
  { name: 'Our Story', path: '/about' },
  // { name: 'Contact', path: '/contact' }, // Can be added later
];

export const FOOTER_LINKS = {
  company: [
    { name: 'About Us', path: '/about' },
    { name: 'Careers', path: '#' }, // Placeholder
    { name: 'Press', path: '#' },    // Placeholder
  ],
  support: [
    { name: 'FAQ', path: '#' },         // Placeholder
    { name: 'Contact Us', path: '#' }, // Placeholder
    { name: 'Warranty', path: '#' },   // Placeholder
  ],
  legal: [
    { name: 'Privacy Policy', path: '#' }, // Placeholder
    { name: 'Terms of Service', path: '#' },// Placeholder
  ],
};