
import React, { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import ProductCard from '../components/ProductCard';
import LoadingSpinner from '../components/LoadingSpinner';
import { Product, ProductCategory } from '../types';
import { productService } from '../services/productService';
import { useCart } from '../hooks/useCart';

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
    // Optionally, show a "Added to cart" toast/message
  };

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-serif font-bold text-brand-text mb-2">
          {selectedCategory ? selectedCategory : "All Timepieces"}
        </h1>
        <p className="text-brand-text-secondary max-w-xl mx-auto">
          Explore our curated collection of fine watches, each crafted with precision and passion.
        </p>
      </div>

      {/* Category Filters */}
      <div className="flex flex-wrap justify-center gap-3 mb-8 p-4 bg-brand-surface rounded-lg shadow-md">
        <button
          onClick={() => handleCategoryChange(null)}
          className={`px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
            !selectedCategory ? 'bg-brand-primary text-brand-bg' : 'bg-gray-600 text-brand-text-secondary hover:bg-gray-500'
          }`}
        >
          All Watches
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
        <LoadingSpinner message="Loading watches..." />
      ) : products.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 md:gap-8">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} onAddToCart={handleAddToCart} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-xl text-brand-text-secondary mb-4">No watches found matching your criteria.</p>
          <Link to="/products" onClick={() => handleCategoryChange(null)} className="text-brand-primary hover:underline">
            View all watches
          </Link>
        </div>
      )}
    </div>
  );
};

export default ProductsPage;
