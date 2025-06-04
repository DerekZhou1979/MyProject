
import React, { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { useCart } from '../hooks/use-shopping-cart';
import { BRAND_INFO, NAVIGATION_LINKS } from '../seagull-brand-config';
import { ShoppingCartIcon, MenuIcon, XIcon } from './ui-icons';

const Header: React.FC = () => {
  const { cart } = useCart();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const totalItemsInCart = cart.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <header className="bg-brand-surface shadow-lg sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="flex items-center space-x-2">
          {BRAND_INFO.logoSvg}
          <span className="text-2xl font-serif font-bold text-brand-text tracking-tight">{BRAND_INFO.name}</span>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex space-x-6 items-center">
          {NAVIGATION_LINKS.map((link) => (
            <NavLink
              key={link.name}
              to={link.path}
              className={({ isActive }) =>
                `text-brand-text-secondary hover:text-brand-primary transition-colors duration-200 ${isActive ? 'text-brand-primary font-semibold' : ''}`
              }
            >
              {link.name}
            </NavLink>
          ))}
        </nav>

        <div className="flex items-center space-x-4">
          <Link to="/cart" className="relative text-brand-text-secondary hover:text-brand-primary transition-colors duration-200">
            <ShoppingCartIcon className="w-6 h-6" />
            {totalItemsInCart > 0 && (
              <span className="absolute -top-2 -right-2 bg-brand-primary text-brand-bg text-xs rounded-full h-5 w-5 flex items-center justify-center font-bold">
                {totalItemsInCart}
              </span>
            )}
          </Link>
          <div className="md:hidden">
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="text-brand-text-secondary hover:text-brand-primary focus:outline-none"
            >
              {isMobileMenuOpen ? <XIcon className="w-6 h-6" /> : <MenuIcon className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden bg-brand-surface border-t border-gray-700">
          <nav className="flex flex-col space-y-1 px-4 py-3">
            {NAVIGATION_LINKS.map((link) => (
              <NavLink
                key={link.name}
                to={link.path}
                onClick={() => setIsMobileMenuOpen(false)}
                className={({ isActive }) =>
                  `block px-3 py-2 rounded-md text-base font-medium ${isActive ? 'bg-brand-primary text-brand-bg' : 'text-brand-text-secondary hover:bg-gray-700 hover:text-brand-primary'}`
                }
              >
                {link.name}
              </NavLink>
            ))}
          </nav>
        </div>
      )}
    </header>
  );
};

export default Header;
