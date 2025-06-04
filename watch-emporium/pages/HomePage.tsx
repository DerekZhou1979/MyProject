
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import HeroSection from '../components/HeroSection';
import ProductCard from '../components/ProductCard';
import LoadingSpinner from '../components/LoadingSpinner';
import { Product, ProductCategory } from '../types';
import { productService } from '../services/productService';
import { useCart } from '../hooks/useCart';
import { BRAND_INFO } from '../constants.tsx';

const HomePage: React.FC = () => {
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { addItem } = useCart();

  useEffect(() => {
    const fetchProducts = async () => {
      setIsLoading(true);
      try {
        const allProducts = await productService.getProducts();
        // Select a few products as featured, e.g., first 3 or random
        setFeaturedProducts(allProducts.slice(0, 3));
      } catch (error) {
        console.error("Failed to fetch featured products:", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchProducts();
  }, []);

  const handleAddToCart = (product: Product) => {
    addItem(product);
    // Optionally, show a notification
  };

  return (
    <div className="space-y-16">
      <HeroSection />

      <section>
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-serif font-semibold text-brand-text">Featured Timepieces</h2>
          <Link to="/products" className="text-brand-primary hover:text-brand-primary-dark font-medium transition-colors">
            View All Collections &rarr;
          </Link>
        </div>
        {isLoading ? (
          <LoadingSpinner message="Loading featured watches..." />
        ) : featuredProducts.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {featuredProducts.map((product) => (
              <ProductCard key={product.id} product={product} onAddToCart={handleAddToCart} />
            ))}
          </div>
        ) : (
          <p className="text-brand-text-secondary text-center">No featured products available at the moment.</p>
        )}
      </section>

      <section className="bg-brand-surface p-10 rounded-lg shadow-xl">
        <div className="grid md:grid-cols-2 gap-10 items-center">
            <div>
                <h2 className="text-3xl font-serif font-semibold text-brand-text mb-4">The {BRAND_INFO.name} Promise</h2>
                <p className="text-brand-text-secondary mb-4 leading-relaxed">
                    At {BRAND_INFO.name}, we are dedicated to the art of horology. Each timepiece is meticulously assembled by master craftsmen, combining centuries-old techniques with cutting-edge technology. We source only the finest materials, ensuring that every watch is not just an instrument of time, but a legacy to be cherished.
                </p>
                <p className="text-brand-text-secondary mb-6 leading-relaxed">
                    Our commitment to excellence extends beyond the workshop. We strive to provide an unparalleled customer experience, guiding you to find the perfect expression of your individuality.
                </p>
                <Link 
                    to="/about" 
                    className="inline-block bg-brand-primary text-brand-bg font-semibold py-3 px-6 rounded-md hover:bg-brand-primary-dark transition-colors duration-300"
                >
                    Discover Our Story
                </Link>
            </div>
            <div className="aspect-w-16 aspect-h-9 rounded-lg overflow-hidden">
                <img src="https://picsum.photos/seed/craftsmanship/800/450" alt="Craftsmanship" className="object-cover w-full h-full" />
            </div>
        </div>
      </section>
      
      <section>
        <h2 className="text-3xl font-serif font-semibold text-brand-text text-center mb-8">Explore by Category</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {Object.values(ProductCategory).map(category => (
            <Link 
              key={category} 
              to={`/products?category=${encodeURIComponent(category)}`} 
              className="block p-8 bg-brand-surface rounded-lg shadow-lg hover:shadow-xl hover:bg-gray-700 transition-all duration-300 text-center group"
            >
              <h3 className="text-xl font-semibold text-brand-text group-hover:text-brand-primary transition-colors">{category}</h3>
              <p className="text-sm text-brand-text-secondary mt-2">Discover our {category.toLowerCase()} selection.</p>
            </Link>
          ))}
        </div>
      </section>

    </div>
  );
};

export default HomePage;
