import React from 'react';
import { Link } from 'react-router-dom';
import { BRAND_INFO } from '../seagull-brand-config';

const HeroSection: React.FC = () => {
  return (
    <div className="relative bg-brand-surface text-brand-text py-20 md:py-32 rounded-lg shadow-2xl overflow-hidden">
      <div 
        className="absolute inset-0 bg-cover bg-center opacity-30" 
        style={{ backgroundImage: "url('/images/seagull_hero_banner_1963pilot_main.jpg')" }}
      ></div>
      <div className="absolute inset-0 bg-gradient-to-br from-brand-bg via-brand-bg/80 to-transparent"></div>
      
      <div className="container mx-auto px-6 relative z-10 text-center">
        <h1 className="text-4xl sm:text-5xl md:text-6xl font-serif font-bold text-brand-text mb-6 leading-tight">
          {BRAND_INFO.chineseName}: <span className="text-brand-primary">{BRAND_INFO.tagline}</span>
        </h1>
        <p className="text-lg md:text-xl text-brand-text-secondary mb-10 max-w-2xl mx-auto">
          体验制表技艺的巅峰之作。每一枚海鸥腕表都是精准、艺术与恒久风格的完美见证。始创于1955年，海鸥表70年来一直致力于高品质机芯的研发制造。
        </p>
        <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-6">
          <Link 
            to="/products" 
            className="bg-brand-primary text-brand-bg font-semibold py-3 px-8 rounded-md text-lg hover:bg-brand-primary-dark transition-colors duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            探索系列腕表
          </Link>
          <Link 
            to="/about" 
            className="border-2 border-brand-primary text-brand-primary font-semibold py-3 px-8 rounded-md text-lg hover:bg-brand-primary hover:text-brand-bg transition-colors duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            制表工艺
          </Link>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;
