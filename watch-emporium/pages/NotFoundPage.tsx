
import React from 'react';
import { Link } from 'react-router-dom';

const NotFoundPage: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
      <h1 className="text-8xl font-serif font-bold text-brand-primary mb-4">404</h1>
      <h2 className="text-3xl font-semibold text-brand-text mb-6">Page Not Found</h2>
      <p className="text-brand-text-secondary mb-8 max-w-md">
        Oops! The page you're looking for doesn't seem to exist. It might have been moved, deleted, or perhaps it never existed at all.
      </p>
      <div className="flex space-x-4">
        <Link 
          to="/" 
          className="bg-brand-primary text-brand-bg font-semibold py-3 px-6 rounded-md hover:bg-brand-primary-dark transition-colors"
        >
          Go to Homepage
        </Link>
        <Link 
          to="/products" 
          className="border-2 border-brand-primary text-brand-primary font-semibold py-3 px-6 rounded-md hover:bg-brand-primary hover:text-brand-bg transition-colors"
        >
          Explore Watches
        </Link>
      </div>
    </div>
  );
};

export default NotFoundPage;
