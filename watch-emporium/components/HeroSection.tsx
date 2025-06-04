
import React from 'react';
import { Link } from 'react-router-dom';
import { BRAND_INFO } from '../constants.tsx';

const HeroSection: React.FC = () => {
  return (
    <div className="relative bg-brand-surface text-brand-text py-20 md:py-32 rounded-lg shadow-2xl overflow-hidden">
      <div 
        className="absolute inset-0 bg-cover bg-center opacity-20" 
        style={{ backgroundImage: "url('https://picsum.photos/seed/hero-bg/1600/900')" }}
      ></div>
      <div className="absolute inset-0 bg-gradient-to-br from-brand-bg via-brand-bg/80 to-transparent"></div>
      
      <div className="container mx-auto px-6 relative z-10 text-center">
        <h1 className="text-4xl sm:text-5xl md:text-6xl font-serif font-bold text-brand-text mb-6 leading-tight">
          {BRAND_INFO.name}: <span className="text-brand-primary">{BRAND_INFO.tagline}</span>
        </h1>
        <p className="text-lg md:text-xl text-brand-text-secondary mb-10 max-w-2xl mx-auto">
          Experience the pinnacle of watchmaking. Each ChronoCraft timepiece is a testament to precision, artistry, and enduring style.
        </p>
        <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-6">
          <Link 
            to="/products" 
            className="bg-brand-primary text-brand-bg font-semibold py-3 px-8 rounded-md text-lg hover:bg-brand-primary-dark transition-colors duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            Explore Collections
          </Link>
          <Link 
            to="/about" 
            className="border-2 border-brand-primary text-brand-primary font-semibold py-3 px-8 rounded-md text-lg hover:bg-brand-primary hover:text-brand-bg transition-colors duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            Our Craftsmanship
          </Link>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;
