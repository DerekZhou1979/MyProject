
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../hooks/useCart';
import { CartItem } from '../types';
import { PlusIcon, MinusIcon, TrashIcon } from '../components/Icons';

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
    // In a real app, this would navigate to a checkout process or call an API
    setCheckoutMessage(`Thank you for your mock purchase of ${totalItems} item(s) totaling $${totalPrice.toFixed(2)}! Your cart has been cleared.`);
    clearCart();
    // Hide message after a few seconds
    setTimeout(() => setCheckoutMessage(null), 7000);
  };

  if (checkoutMessage) {
    return (
      <div className="text-center py-16 bg-brand-surface rounded-lg shadow-xl">
        <h1 className="text-3xl font-serif font-bold text-brand-primary mb-4">Checkout Successful!</h1>
        <p className="text-brand-text-secondary text-lg">{checkoutMessage}</p>
        <Link 
          to="/products" 
          className="mt-8 inline-block bg-brand-primary text-brand-bg font-semibold py-3 px-6 rounded-md hover:bg-brand-primary-dark transition-colors"
        >
          Continue Shopping
        </Link>
      </div>
    );
  }

  if (cart.length === 0) {
    return (
      <div className="text-center py-16">
        <h1 className="text-3xl font-serif font-bold text-brand-text mb-4">Your Cart is Empty</h1>
        <p className="text-brand-text-secondary text-lg mb-8">Looks like you haven't added any timeless pieces yet.</p>
        <Link 
          to="/products" 
          className="bg-brand-primary text-brand-bg font-semibold py-3 px-6 rounded-md hover:bg-brand-primary-dark transition-colors"
        >
          Explore Collections
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <h1 className="text-4xl font-serif font-bold text-brand-text text-center">Your Shopping Cart</h1>
      
      <div className="bg-brand-surface shadow-xl rounded-lg overflow-hidden">
        {/* Cart Items */}
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
                <p className="text-md text-brand-primary font-medium mt-1 sm:hidden">${(item.price * item.quantity).toFixed(2)}</p>
              </div>
              
              {/* Quantity Controls */}
              <div className="flex items-center space-x-3 my-2 sm:my-0">
                <button 
                  onClick={() => handleQuantityChange(item, item.quantity - 1)}
                  className="p-2 rounded-full bg-gray-600 hover:bg-gray-500 text-brand-text transition-colors"
                  aria-label="Decrease quantity"
                >
                  <MinusIcon className="w-4 h-4" />
                </button>
                <span className="w-10 text-center font-medium text-brand-text">{item.quantity}</span>
                <button 
                  onClick={() => handleQuantityChange(item, item.quantity + 1)}
                  className="p-2 rounded-full bg-gray-600 hover:bg-gray-500 text-brand-text transition-colors"
                  aria-label="Increase quantity"
                >
                  <PlusIcon className="w-4 h-4" />
                </button>
              </div>

              <p className="hidden sm:block text-lg font-semibold text-brand-primary w-28 text-right">${(item.price * item.quantity).toFixed(2)}</p>
              
              <button 
                onClick={() => removeItem(item.id)}
                className="p-2 rounded-full text-red-400 hover:text-red-300 hover:bg-red-800/50 transition-colors"
                aria-label="Remove item"
              >
                <TrashIcon className="w-5 h-5" />
              </button>
            </div>
          ))}
        </div>

        {/* Cart Summary & Checkout */}
        <div className="bg-gray-800 p-6">
          <div className="flex justify-between items-center mb-4">
            <p className="text-xl text-brand-text-secondary">Subtotal ({totalItems} items):</p>
            <p className="text-2xl font-bold text-brand-primary">${totalPrice.toFixed(2)}</p>
          </div>
          <p className="text-sm text-brand-text-secondary text-right mb-6">Shipping & taxes calculated at mock checkout.</p>
          <button 
            onClick={handleCheckout}
            className="w-full bg-brand-primary text-brand-bg font-bold py-3 px-6 rounded-md text-lg hover:bg-brand-primary-dark transition-colors duration-300"
          >
            Proceed to Mock Checkout
          </button>
          <button 
            onClick={() => {
              if(window.confirm("Are you sure you want to clear your cart?")) {
                clearCart();
              }
            }}
            className="w-full mt-3 text-center text-brand-text-secondary hover:text-red-400 transition-colors text-sm"
          >
            Clear Cart
          </button>
        </div>
      </div>

      <div className="text-center">
        <Link to="/products" className="text-brand-primary hover:underline">
          &larr; Continue Shopping
        </Link>
      </div>
    </div>
  );
};

export default CartPage;
