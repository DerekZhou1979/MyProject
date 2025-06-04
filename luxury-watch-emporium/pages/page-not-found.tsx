import React from 'react';
import { Link } from 'react-router-dom';

const NotFoundPage: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
      <h1 className="text-8xl font-serif font-bold text-brand-primary mb-4">404</h1>
      <h2 className="text-3xl font-semibold text-brand-text mb-6">页面未找到</h2>
      <p className="text-brand-text-secondary mb-8 max-w-md">
        抱歉！您访问的页面似乎不存在。它可能已被移动、删除，或者从未存在过。
      </p>
      <div className="flex space-x-4">
        <Link 
          to="/" 
          className="bg-brand-primary text-brand-bg font-semibold py-3 px-6 rounded-md hover:bg-brand-primary-dark transition-colors"
        >
          返回首页
        </Link>
        <Link 
          to="/products" 
          className="border-2 border-brand-primary text-brand-primary font-semibold py-3 px-6 rounded-md hover:bg-brand-primary hover:text-brand-bg transition-colors"
        >
          探索腕表
        </Link>
      </div>
    </div>
  );
};

export default NotFoundPage;
