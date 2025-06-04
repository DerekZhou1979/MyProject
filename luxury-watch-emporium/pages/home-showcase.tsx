import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import HeroSection from '../components/hero-banner';
import ProductCard from '../components/watch-product-card';
import LoadingSpinner from '../components/loading-indicator';
import { Product, ProductCategory } from '../seagull-watch-types';
import { productService } from '../services/watch-data-service';
import { useCart } from '../hooks/use-shopping-cart';
import { BRAND_INFO } from '../seagull-brand-config';

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
          <h2 className="text-3xl font-serif font-semibold text-brand-text">精选时计</h2>
          <Link to="/products" className="text-brand-primary hover:text-brand-primary-dark font-medium transition-colors">
            查看所有系列 &rarr;
          </Link>
        </div>
        {isLoading ? (
          <LoadingSpinner message="正在加载精选腕表..." />
        ) : featuredProducts.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {featuredProducts.map((product) => (
              <ProductCard key={product.id} product={product} onAddToCart={handleAddToCart} />
            ))}
          </div>
        ) : (
          <p className="text-brand-text-secondary text-center">暂无精选产品。</p>
        )}
      </section>

      <section className="bg-brand-surface p-10 rounded-lg shadow-xl">
        <div className="grid md:grid-cols-2 gap-10 items-center">
            <div>
                <h2 className="text-3xl font-serif font-semibold text-brand-text mb-4">{BRAND_INFO.chineseName}的承诺</h2>
                <p className="text-brand-text-secondary mb-4 leading-relaxed">
                    在{BRAND_INFO.chineseName}，我们专注于钟表艺术。每一枚时计都由制表大师精心组装，将数百年的传统工艺与尖端技术完美融合。我们只选用最优质的材料，确保每一块手表不仅仅是计时工具，更是值得珍藏的传世之作。
                </p>
                <p className="text-brand-text-secondary mb-6 leading-relaxed">
                    我们对卓越的承诺不止于制表工坊。我们致力于提供无与伦比的客户体验，引导您找到最能表达个人品味的时计杰作。70年来，海鸥表始终是中国制表行业的开创者和领先者。
                </p>
                <Link 
                    to="/about" 
                    className="inline-block bg-brand-primary text-brand-bg font-semibold py-3 px-6 rounded-md hover:bg-brand-primary-dark transition-colors duration-300"
                >
                    了解我们的故事
                </Link>
            </div>
            <div className="aspect-w-16 aspect-h-9 rounded-lg overflow-hidden">
                <img src="/images/seagull_team_main.jpg" alt="海鸥表制表工艺" className="object-cover w-full h-full" />
            </div>
        </div>
      </section>
      
      <section>
        <h2 className="text-3xl font-serif font-semibold text-brand-text text-center mb-8">按系列探索</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {Object.values(ProductCategory).map(category => (
            <Link 
              key={category} 
              to={`/products?category=${encodeURIComponent(category)}`} 
              className="block p-8 bg-brand-surface rounded-lg shadow-lg hover:shadow-xl hover:bg-gray-700 transition-all duration-300 text-center group"
            >
              <h3 className="text-xl font-semibold text-brand-text group-hover:text-brand-primary transition-colors">{category}</h3>
              <p className="text-sm text-brand-text-secondary mt-2">探索我们的{category}系列。</p>
            </Link>
          ))}
        </div>
      </section>

    </div>
  );
};

export default HomePage;
