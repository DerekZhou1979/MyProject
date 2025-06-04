import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../hooks/use-shopping-cart';
import { CartItem } from '../seagull-watch-types';
import { PlusIcon, MinusIcon, TrashIcon } from '../components/ui-icons';

const CartPage: React.FC = () => {
  const { cart, removeItem, updateQuantity, clearCart, totalItems, totalPrice } = useCart();
  const [checkoutMessage, setCheckoutMessage] = useState<string | null>(null);

  const handleQuantityChange = (item: CartItem, newQuantity: number) => {
    if (newQuantity > 0) {
      updateQuantity(item.id, newQuantity);
    } else {
      removeItem(item.id);
    }
  };

  const handleCheckout = () => {
    // 在真实应用中，这里会导航到结账流程或调用API
    setCheckoutMessage(`感谢您的模拟购买！您购买了 ${totalItems} 件商品，总价 ¥${totalPrice.toLocaleString()}。购物车已清空。`);
    clearCart();
    // 几秒后隐藏消息
    setTimeout(() => setCheckoutMessage(null), 7000);
  };

  if (checkoutMessage) {
    return (
      <div className="text-center py-16 bg-brand-surface rounded-lg shadow-xl">
        <h1 className="text-3xl font-serif font-bold text-brand-primary mb-4">结账成功！</h1>
        <p className="text-brand-text-secondary text-lg">{checkoutMessage}</p>
        <Link 
          to="/products" 
          className="mt-8 inline-block bg-brand-primary text-brand-bg font-semibold py-3 px-6 rounded-md hover:bg-brand-primary-dark transition-colors"
        >
          继续购物
        </Link>
      </div>
    );
  }

  if (cart.length === 0) {
    return (
      <div className="text-center py-16">
        <h1 className="text-3xl font-serif font-bold text-brand-text mb-4">您的购物车为空</h1>
        <p className="text-brand-text-secondary text-lg mb-8">看起来您还没有添加任何精美腕表。</p>
        <Link 
          to="/products" 
          className="bg-brand-primary text-brand-bg font-semibold py-3 px-6 rounded-md hover:bg-brand-primary-dark transition-colors"
        >
          探索腕表系列
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <h1 className="text-4xl font-serif font-bold text-brand-text text-center">购物车</h1>
      
      <div className="bg-brand-surface shadow-xl rounded-lg overflow-hidden">
        {/* 购物车商品 */}
        <div className="divide-y divide-gray-700">
          {cart.map((item) => (
            <div key={item.id} className="flex flex-col sm:flex-row items-center p-4 sm:p-6 gap-4">
              <img 
                src={item.imageUrl || `https://picsum.photos/seed/${item.id}/100/100`} 
                alt={item.name} 
                className="w-24 h-24 sm:w-32 sm:h-32 object-cover rounded-md shadow-md"
              />
              <div className="flex-grow text-center sm:text-left">
                <Link to={`/products/${item.id}`} className="text-lg font-semibold text-brand-text hover:text-brand-primary transition-colors">
                  {item.name}
                </Link>
                <p className="text-sm text-brand-text-secondary">{item.category}</p>
                <p className="text-md text-brand-primary font-medium mt-1 sm:hidden">¥{(item.price * item.quantity).toLocaleString()}</p>
              </div>
              
              {/* 数量控制 */}
              <div className="flex items-center space-x-3 my-2 sm:my-0">
                <button 
                  onClick={() => handleQuantityChange(item, item.quantity - 1)}
                  className="p-2 rounded-full bg-gray-600 hover:bg-gray-500 text-brand-text transition-colors"
                  aria-label="减少数量"
                >
                  <MinusIcon className="w-4 h-4" />
                </button>
                <span className="w-10 text-center font-medium text-brand-text">{item.quantity}</span>
                <button 
                  onClick={() => handleQuantityChange(item, item.quantity + 1)}
                  className="p-2 rounded-full bg-gray-600 hover:bg-gray-500 text-brand-text transition-colors"
                  aria-label="增加数量"
                >
                  <PlusIcon className="w-4 h-4" />
                </button>
              </div>

              <p className="hidden sm:block text-lg font-semibold text-brand-primary w-28 text-right">¥{(item.price * item.quantity).toLocaleString()}</p>
              
              <button 
                onClick={() => removeItem(item.id)}
                className="p-2 rounded-full text-red-400 hover:text-red-300 hover:bg-red-800/50 transition-colors"
                aria-label="移除商品"
              >
                <TrashIcon className="w-5 h-5" />
              </button>
            </div>
          ))}
        </div>

        {/* 购物车汇总和结账 */}
        <div className="bg-gray-800 p-6">
          <div className="flex justify-between items-center mb-4">
            <p className="text-xl text-brand-text-secondary">小计 ({totalItems} 件商品):</p>
            <p className="text-2xl font-bold text-brand-primary">¥{totalPrice.toLocaleString()}</p>
          </div>
          <p className="text-sm text-brand-text-secondary text-right mb-6">运费和税费将在模拟结账时计算。</p>
          <button 
            onClick={handleCheckout}
            className="w-full bg-brand-primary text-brand-bg font-bold py-3 px-6 rounded-md text-lg hover:bg-brand-primary-dark transition-colors duration-300"
          >
            进行模拟结账
          </button>
          <button 
            onClick={() => {
              if(window.confirm("确定要清空购物车吗？")) {
                clearCart();
              }
            }}
            className="w-full mt-3 text-center text-brand-text-secondary hover:text-red-400 transition-colors text-sm"
          >
            清空购物车
          </button>
        </div>
      </div>

      <div className="text-center">
        <Link to="/products" className="text-brand-primary hover:underline">
          &larr; 继续购物
        </Link>
      </div>
    </div>
  );
};

export default CartPage;
