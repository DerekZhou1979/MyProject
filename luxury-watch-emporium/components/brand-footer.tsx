
import React from 'react';
import { Link } from 'react-router-dom';
import { BRAND_INFO, FOOTER_LINKS } from '../seagull-brand-config';

const Footer: React.FC = () => {
  return (
    <footer className="bg-brand-surface border-t border-gray-700 text-brand-text-secondary">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-8">
          {/* Brand Info */}
          <div className="col-span-1 md:col-span-2 lg:col-span-1">
            <Link to="/" className="flex items-center space-x-2 mb-4">
              {BRAND_INFO.logoSvg}
              <span className="text-xl font-serif font-bold text-brand-text">{BRAND_INFO.name}</span>
            </Link>
            <p className="text-sm">{BRAND_INFO.tagline}</p>
            <p className="text-sm mt-1">{BRAND_INFO.chineseName}</p>
          </div>

          {/* Links Sections */}
          <div>
            <h5 className="font-semibold text-brand-text mb-3">Company</h5>
            <ul className="space-y-2">
              {FOOTER_LINKS.company.map(link => (
                <li key={link.name}><Link to={link.path} className="hover:text-brand-primary transition-colors text-sm">{link.name}</Link></li>
              ))}
            </ul>
          </div>
          <div>
            <h5 className="font-semibold text-brand-text mb-3">Support</h5>
            <ul className="space-y-2">
              {FOOTER_LINKS.support.map(link => (
                <li key={link.name}><Link to={link.path} className="hover:text-brand-primary transition-colors text-sm">{link.name}</Link></li>
              ))}
            </ul>
          </div>
          <div>
            <h5 className="font-semibold text-brand-text mb-3">Legal</h5>
            <ul className="space-y-2">
              {FOOTER_LINKS.legal.map(link => (
                <li key={link.name}><Link to={link.path} className="hover:text-brand-primary transition-colors text-sm">{link.name}</Link></li>
              ))}
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-700 pt-8 text-center">
          <p className="text-sm">&copy; {new Date().getFullYear()} {BRAND_INFO.chineseName}. 版权所有.</p>
          <p className="text-xs mt-1">中国制表行业的开创者和领先者 | 始创于1955年</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
