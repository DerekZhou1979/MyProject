
import React, { useEffect, useState, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Product } from '../types';
import { productService } from '../services/productService';
import { geminiService } from '../services/geminiService';
import LoadingSpinner from '../components/LoadingSpinner';
import { useCart } from '../hooks/useCart';
import { ShoppingCartIcon, SparklesIcon } from '../components/Icons';

const ProductDetailPage: React.FC = () => {
  const { productId } = useParams<{ productId: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedImage, setSelectedImage] = useState<string | undefined>(undefined);
  const [aiDescription, setAiDescription] = useState<string | null>(null);
  const [isGeneratingAiDesc, setIsGeneratingAiDesc] = useState(false);
  const { addItem } = useCart();

  const fetchProductData = useCallback(async () => {
    if (!productId) {
      setError("Product ID is missing.");
      setIsLoading(false);
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      const fetchedProduct = await productService.getProductById(productId);
      if (fetchedProduct) {
        setProduct(fetchedProduct);
        setSelectedImage(fetchedProduct.imageUrl); 
      } else {
        setError("Product not found.");
      }
    } catch (err) {
      console.error("Failed to fetch product:", err);
      setError("Failed to load product details. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  }, [productId]);

  useEffect(() => {
    fetchProductData();
  }, [fetchProductData]);

  const handleAddToCart = () => {
    if (product) {
      addItem(product);
      // Optionally show a toast notification
    }
  };

  const handleGenerateAiDescription = async () => {
    if (!product) return;
    setIsGeneratingAiDesc(true);
    setAiDescription(null);
    try {
      const description = await geminiService.generateCreativeDescription(product);
      setAiDescription(description);
    } catch (e) {
      console.error("AI description generation failed:", e);
      setAiDescription("Failed to generate stylistic insight. Please try again.");
    } finally {
      setIsGeneratingAiDesc(false);
    }
  };

  if (isLoading) {
    return <LoadingSpinner message="Loading product details..." size="lg" />;
  }

  if (error) {
    return <div className="text-center py-10 text-red-400 text-xl">{error}</div>;
  }

  if (!product) {
    return <div className="text-center py-10 text-brand-text-secondary text-xl">Product not found.</div>;
  }

  const gallery = [product.imageUrl, ...(product.galleryImages || [])].filter(Boolean) as string[];

  return (
    <div className="bg-brand-surface p-6 sm:p-8 rounded-lg shadow-2xl">
      <div className="grid md:grid-cols-2 gap-8 lg:gap-12">
        {/* Image Gallery */}
        <div>
          <div className="aspect-w-1 aspect-h-1 w-full rounded-lg overflow-hidden shadow-lg mb-4">
            <img 
              src={selectedImage || product.imageUrl} 
              alt={product.name} 
              className="w-full h-full object-cover object-center"
            />
          </div>
          {gallery.length > 1 && (
            <div className="grid grid-cols-4 gap-2">
              {gallery.map((imgUrl, idx) => (
                <button 
                  key={idx} 
                  onClick={() => setSelectedImage(imgUrl)}
                  className={`aspect-w-1 aspect-h-1 rounded-md overflow-hidden border-2 transition-colors ${selectedImage === imgUrl ? 'border-brand-primary' : 'border-transparent hover:border-gray-500'}`}
                >
                  <img src={imgUrl} alt={`${product.name} thumbnail ${idx+1}`} className="w-full h-full object-cover" />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Product Info */}
        <div className="flex flex-col justify-center">
          <Link to={`/products?category=${encodeURIComponent(product.category)}`} className="text-sm text-brand-primary hover:underline mb-1">{product.category}</Link>
          <h1 className="text-3xl sm:text-4xl font-serif font-bold text-brand-text mb-3">{product.name}</h1>
          <p className="text-3xl font-semibold text-brand-primary mb-4">${product.price.toFixed(2)}</p>
          
          <p className="text-brand-text-secondary leading-relaxed mb-6">{product.description}</p>

          <div className="mb-6">
            <h3 className="text-lg font-semibold text-brand-text mb-2">Key Features:</h3>
            <ul className="list-disc list-inside text-brand-text-secondary space-y-1">
              {product.features.map((feature, index) => (
                <li key={index}>{feature}</li>
              ))}
            </ul>
          </div>

          <div className="mb-6">
            <button 
              onClick={handleGenerateAiDescription}
              disabled={isGeneratingAiDesc}
              className="w-full sm:w-auto flex items-center justify-center space-x-2 bg-transparent border-2 border-purple-400 text-purple-300 font-semibold py-3 px-6 rounded-md hover:bg-purple-400 hover:text-brand-bg transition-colors duration-300 disabled:opacity-50 mb-4"
            >
              <SparklesIcon className="w-5 h-5" />
              <span>{isGeneratingAiDesc ? 'Generating Insight...' : 'Generate Stylistic Insight (AI)'}</span>
            </button>
            {isGeneratingAiDesc && <LoadingSpinner size="sm" />}
            {aiDescription && (
              <div className="mt-3 p-4 bg-gray-700 rounded-md text-brand-text-secondary italic">
                <p className="font-semibold text-purple-300 mb-1">AI Stylistic Insight:</p>
                {aiDescription}
              </div>
            )}
          </div>

          <div className="flex flex-col sm:flex-row gap-4">
            <button 
              onClick={handleAddToCart}
              className="w-full sm:flex-1 bg-brand-primary text-brand-bg font-semibold py-3 px-6 rounded-md hover:bg-brand-primary-dark transition-colors duration-300 flex items-center justify-center space-x-2 text-lg"
            >
              <ShoppingCartIcon className="w-6 h-6" />
              <span>Add to Cart</span>
            </button>
            {/* Could add a "Buy Now" button here */}
          </div>
          <p className="text-sm text-brand-text-secondary mt-4">SKU: {product.sku} | Stock: {product.stock > 0 ? `${product.stock} available` : 'Out of Stock'}</p>
        </div>
      </div>
    </div>
  );
};

export default ProductDetailPage;
