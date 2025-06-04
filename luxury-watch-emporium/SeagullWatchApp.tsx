import React from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom';
import Header from './components/navigation-header';
import Footer from './components/brand-footer';
import HomePage from './pages/home-showcase';
import ProductsPage from './pages/watch-catalog';
import ProductDetailPage from './pages/watch-detail-view';
import CartPage from './pages/shopping-cart';
import AboutPage from './pages/brand-story';
import NotFoundPage from './pages/page-not-found';

const App: React.FC = () => {
  return (
    <HashRouter>
      <div className="flex flex-col min-h-screen bg-brand-bg">
        <Header />
        <main className="flex-grow container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/products" element={<ProductsPage />} />
            <Route path="/products/:productId" element={<ProductDetailPage />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </HashRouter>
  );
};

export default App;
