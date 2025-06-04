
import React from 'react';
import { Link } from 'react-router-dom';
import { Product } from '../seagull-watch-types';
import { EyeIcon, ShoppingCartIcon } from './ui-icons';

interface ProductCardProps {
  product: Product;
  onAddToCart: (product: Product) => void;
}

const ProductCard: React.FC<ProductCardProps> = ({ product, onAddToCart }) => {
  return (
    <div className="bg-brand-surface rounded-lg shadow-xl overflow-hidden transition-all duration-300 hover:shadow-2xl group flex flex-col">
      <Link to={`/products/${product.id}`} className="block">
        <div className="relative aspect-w-1 aspect-h-1 w-full overflow-hidden">
          <img 
            src={product.imageUrl || `https://picsum.photos/seed/${product.id}/400/400`} 
            alt={product.name} 
            className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-300"
          />
           <div className="absolute inset-0 bg-black bg-opacity-20 group-hover:bg-opacity-10 transition-opacity duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100">
            <EyeIcon className="w-12 h-12 text-white opacity-80" />
          </div>
        </div>
      </Link>
      <div className="p-6 flex flex-col flex-grow">
        <Link to={`/products/${product.id}`} className="block">
          <h3 className="text-xl font-serif font-semibold text-brand-text group-hover:text-brand-primary transition-colors duration-200 truncate" title={product.name}>
            {product.name}
          </h3>
        </Link>
        <p className="text-sm text-brand-text-secondary mt-1">{product.category}</p>
        <p className="text-2xl font-semibold text-brand-primary mt-2 flex-grow">¥{product.price.toLocaleString()}</p>
        <div className="mt-4">
          <button 
            onClick={() => onAddToCart(product)}
            className="w-full bg-brand-primary text-brand-bg font-semibold py-3 px-4 rounded-md hover:bg-brand-primary-dark transition-colors duration-200 flex items-center justify-center space-x-2"
          >
            <ShoppingCartIcon className="w-5 h-5" />
            <span>加入购物车</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
