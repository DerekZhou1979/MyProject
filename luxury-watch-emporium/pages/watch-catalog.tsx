import React, { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import ProductCard from '../components/watch-product-card';
import LoadingSpinner from '../components/loading-indicator';
import { Product, ProductCategory } from '../seagull-watch-types';
import { productService } from '../services/watch-data-service';
import { useCart } from '../hooks/use-shopping-cart';

const ProductsPage: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchParams, setSearchParams] = useSearchParams();
  const [categories, setCategories] = useState<ProductCategory[]>([]);
  
  const selectedCategory = searchParams.get('category') as ProductCategory | null;
  const { addItem } = useCart();

  useEffect(() => {
    const fetchCategories = async () => {
        try {
            const fetchedCategories = await productService.getProductCategories();
            setCategories(fetchedCategories);
        } catch (error) {
            console.error("Failed to fetch categories:", error);
        }
    };
    fetchCategories();
  }, []);

  useEffect(() => {
    const fetchProducts = async () => {
      setIsLoading(true);
      try {
        const fetchedProducts = await productService.getProducts(selectedCategory || undefined);
        setProducts(fetchedProducts);
      } catch (error) {
        console.error("Failed to fetch products:", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchProducts();
  }, [selectedCategory]);

  const handleCategoryChange = (category: ProductCategory | null) => {
    if (category) {
      setSearchParams({ category: category });
    } else {
      setSearchParams({});
    }
  };

  const handleAddToCart = (product: Product) => {
    addItem(product);
    // 可选择显示"已添加到购物车"提示
  };

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-serif font-bold text-brand-text mb-2">
          {selectedCategory ? selectedCategory : "全部腕表"}
        </h1>
        <p className="text-brand-text-secondary max-w-xl mx-auto">
          探索我们精心策划的高端腕表收藏，每一枚都以精湛工艺和满怀激情制作。
        </p>
      </div>

      {/* 分类筛选 */}
      <div className="flex flex-wrap justify-center gap-3 mb-8 p-4 bg-brand-surface rounded-lg shadow-md">
        <button
          onClick={() => handleCategoryChange(null)}
          className={`px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
            !selectedCategory ? 'bg-brand-primary text-brand-bg' : 'bg-gray-600 text-brand-text-secondary hover:bg-gray-500'
          }`}
        >
          全部腕表
        </button>
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => handleCategoryChange(cat)}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
              selectedCategory === cat ? 'bg-brand-primary text-brand-bg' : 'bg-gray-600 text-brand-text-secondary hover:bg-gray-500'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {isLoading ? (
        <LoadingSpinner message="正在加载腕表..." />
      ) : products.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 md:gap-8">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} onAddToCart={handleAddToCart} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-xl text-brand-text-secondary mb-4">未找到符合条件的腕表。</p>
          <Link to="/products" onClick={() => handleCategoryChange(null)} className="text-brand-primary hover:underline">
            查看全部腕表
          </Link>
        </div>
      )}
    </div>
  );
};

export default ProductsPage;
