#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Frontend Files Generator برای iShop
این اسکریپت فایل‌های لازم React رو می‌سازه
"""

import os
from pathlib import Path

def create_frontend_files():
    """ایجاد تمام فایل‌های لازم برای React"""
    
    print("🎨 ایجاد فایل‌های فرانت‌اند...")
    
    # مسیر فرانت‌اند
    frontend_path = Path("frontend")
    
    if not frontend_path.exists():
        print("❌ پوشه frontend یافت نشد!")
        return
    
    # ایجاد فولدرهای ضروری
    (frontend_path / "public").mkdir(exist_ok=True)
    (frontend_path / "src").mkdir(exist_ok=True)
    (frontend_path / "src/components").mkdir(exist_ok=True)
    (frontend_path / "src/hooks").mkdir(exist_ok=True)
    (frontend_path / "src/services").mkdir(exist_ok=True)
    (frontend_path / "src/styles").mkdir(exist_ok=True)
    
    # 1. index.html
    index_html = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#667eea" />
    <meta
      name="description"
      content="فروشگاه آنلاین iShop - بهترین محصولات با بهترین قیمت"
    />
    <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <title>iShop - فروشگاه آنلاین</title>
  </head>
  <body>
    <noscript>برای استفاده از این سایت، لطفاً JavaScript را فعال کنید.</noscript>
    <div id="root"></div>
  </body>
</html>"""
    write_file(frontend_path / "public/index.html", index_html)
    
    # 2. manifest.json
    manifest = """{
  "short_name": "iShop",
  "name": "فروشگاه آنلاین iShop",
  "icons": [
    {
      "src": "favicon.ico",
      "sizes": "64x64 32x32 24x24 16x16",
      "type": "image/x-icon"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#667eea",
  "background_color": "#ffffff"
}"""
    write_file(frontend_path / "public/manifest.json", manifest)
    
    # 3. package.json کامل
    package_json = """{
  "name": "ishop-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.16.4",
    "@testing-library/react": "^13.3.0",
    "@testing-library/user-event": "^13.5.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "web-vitals": "^2.1.4"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}"""
    write_file(frontend_path / "package.json", package_json)
    
    # 4. index.js
    index_js = """import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);"""
    write_file(frontend_path / "src/index.js", index_js)
    
    # 5. App.js مدرن
    app_js = """import React, { useState, useEffect, useCallback, useMemo } from 'react';
import './styles/App.css';

// --- آیکون‌ها ---
const ShoppingCartIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
  </svg>
);

const UserIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
  </svg>
);

const SearchIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
  </svg>
);

// --- API Service ---
const API_BASE = 'http://localhost:8000/api/v1';

const api = {
  getProducts: async () => {
    const response = await fetch(`${API_BASE}/products`);
    return response.json();
  },
  
  getProduct: async (id) => {
    const response = await fetch(`${API_BASE}/products/${id}`);
    return response.json();
  },
  
  login: async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      body: formData
    });
    return response.json();
  }
};

// --- Helper Functions ---
const formatPrice = (price) => new Intl.NumberFormat('fa-IR').format(price) + ' تومان';

// --- کامپوننت‌های اصلی ---
const Navbar = ({ cartCount, onCartClick, onAuthClick, user, onLogout }) => {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <div className="nav-brand">
          <h1>iShop</h1>
        </div>
        
        <div className="nav-menu">
          <a href="#home">خانه</a>
          <a href="#products">محصولات</a>
          <a href="#blog">وبلاگ</a>
        </div>
        
        <div className="nav-actions">
          <button className="search-btn">
            <SearchIcon />
          </button>
          
          <button className="cart-btn" onClick={onCartClick}>
            <ShoppingCartIcon />
            {cartCount > 0 && <span className="cart-badge">{cartCount}</span>}
          </button>
          
          {user ? (
            <div className="user-menu">
              <span>سلام {user.name}</span>
              <button onClick={onLogout}>خروج</button>
            </div>
          ) : (
            <button className="auth-btn" onClick={onAuthClick}>
              <UserIcon />
              ورود
            </button>
          )}
        </div>
      </div>
    </nav>
  );
};

const ProductCard = ({ product, onAddToCart, onClick }) => {
  return (
    <div className="product-card" onClick={() => onClick(product)}>
      <div className="product-image">
        <img src={product.imageUrl} alt={product.name} />
      </div>
      <div className="product-info">
        <h3>{product.name}</h3>
        <p className="product-description">{product.description}</p>
        <div className="product-footer">
          <span className="product-price">{formatPrice(product.price)}</span>
          <button 
            className="add-to-cart-btn"
            onClick={(e) => {
              e.stopPropagation();
              onAddToCart(product);
            }}
          >
            افزودن به سبد
          </button>
        </div>
      </div>
    </div>
  );
};

const AuthModal = ({ isOpen, onClose, onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await onLogin(email, password);
      onClose();
    } catch (error) {
      alert('خطا در ورود: ' + error.message);
    }
    setLoading(false);
  };
  
  if (!isOpen) return null;
  
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="auth-modal" onClick={e => e.stopPropagation()}>
        <h2>ورود به حساب کاربری</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="ایمیل"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="رمز عبور"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <div className="auth-actions">
            <button type="submit" disabled={loading}>
              {loading ? 'در حال ورود...' : 'ورود'}
            </button>
            <button type="button" onClick={onClose}>لغو</button>
          </div>
        </form>
        <div className="auth-hint">
          <p>برای تست: admin@ishop.com / admin123</p>
        </div>
      </div>
    </div>
  );
};

const CartSidebar = ({ isOpen, onClose, items, onUpdateQuantity, onRemove, total }) => {
  if (!isOpen) return null;
  
  return (
    <div className="sidebar-overlay" onClick={onClose}>
      <div className="cart-sidebar" onClick={e => e.stopPropagation()}>
        <div className="cart-header">
          <h2>سبد خرید</h2>
          <button onClick={onClose}>×</button>
        </div>
        
        <div className="cart-items">
          {items.length === 0 ? (
            <p>سبد خرید شما خالی است</p>
          ) : (
            items.map(item => (
              <div key={item.id} className="cart-item">
                <img src={item.imageUrl} alt={item.name} />
                <div className="item-info">
                  <h4>{item.name}</h4>
                  <p>{formatPrice(item.price)}</p>
                  <div className="quantity-controls">
                    <button onClick={() => onUpdateQuantity(item.id, item.quantity - 1)}>-</button>
                    <span>{item.quantity}</span>
                    <button onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}>+</button>
                  </div>
                </div>
                <button className="remove-btn" onClick={() => onRemove(item.id)}>حذف</button>
              </div>
            ))
          )}
        </div>
        
        {items.length > 0 && (
          <div className="cart-footer">
            <div className="cart-total">
              مجموع: {formatPrice(total)}
            </div>
            <button className="checkout-btn">تکمیل خرید</button>
          </div>
        )}
      </div>
    </div>
  );
};

// --- کامپوننت اصلی اپلیکیشن ---
function App() {
  const [products, setProducts] = useState([]);
  const [cartItems, setCartItems] = useState([]);
  const [user, setUser] = useState(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [showCart, setShowCart] = useState(false);
  const [loading, setLoading] = useState(true);
  
  // بارگذاری محصولات
  useEffect(() => {
    const loadProducts = async () => {
      try {
        const data = await api.getProducts();
        setProducts(data);
      } catch (error) {
        console.error('خطا در بارگذاری محصولات:', error);
      }
      setLoading(false);
    };
    
    loadProducts();
  }, []);
  
  // مدیریت سبد خرید
  const addToCart = useCallback((product) => {
    setCartItems(prev => {
      const existing = prev.find(item => item.id === product.id);
      if (existing) {
        return prev.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [...prev, { ...product, quantity: 1 }];
    });
  }, []);
  
  const updateCartQuantity = useCallback((productId, newQuantity) => {
    if (newQuantity <= 0) {
      setCartItems(prev => prev.filter(item => item.id !== productId));
    } else {
      setCartItems(prev =>
        prev.map(item =>
          item.id === productId ? { ...item, quantity: newQuantity } : item
        )
      );
    }
  }, []);
  
  const removeFromCart = useCallback((productId) => {
    setCartItems(prev => prev.filter(item => item.id !== productId));
  }, []);
  
  // محاسبه مجموع
  const cartTotal = useMemo(() => {
    return cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
  }, [cartItems]);
  
  const cartCount = useMemo(() => {
    return cartItems.reduce((count, item) => count + item.quantity, 0);
  }, [cartItems]);
  
  // ورود کاربر
  const handleLogin = async (email, password) => {
    try {
      const response = await api.login(email, password);
      if (response.access_token) {
        setUser({ name: 'کاربر', email });
        localStorage.setItem('token', response.access_token);
      }
    } catch (error) {
      throw new Error('نام کاربری یا رمز عبور اشتباه است');
    }
  };
  
  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('token');
  };
  
  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner"></div>
        <p>در حال بارگذاری...</p>
      </div>
    );
  }
  
  return (
    <div className="App">
      <Navbar
        cartCount={cartCount}
        onCartClick={() => setShowCart(true)}
        onAuthClick={() => setShowAuthModal(true)}
        user={user}
        onLogout={handleLogout}
      />
      
      <main className="main-content">
        {/* Hero Section */}
        <section className="hero">
          <div className="hero-content">
            <h1>فروشگاه آنلاین iShop</h1>
            <p>بهترین محصولات الکترونیکی با بهترین قیمت</p>
          </div>
        </section>
        
        {/* Products Section */}
        <section className="products-section">
          <div className="container">
            <h2>محصولات ویژه</h2>
            <div className="products-grid">
              {products.map(product => (
                <ProductCard
                  key={product.id}
                  product={product}
                  onAddToCart={addToCart}
                  onClick={(product) => console.log('محصول کلیک شد:', product.name)}
                />
              ))}
            </div>
          </div>
        </section>
      </main>
      
      {/* Modals */}
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onLogin={handleLogin}
      />
      
      <CartSidebar
        isOpen={showCart}
        onClose={() => setShowCart(false)}
        items={cartItems}
        onUpdateQuantity={updateCartQuantity}
        onRemove={removeFromCart}
        total={cartTotal}
      />
    </div>
  );
}

export default App;"""
    write_file(frontend_path / "src/App.js", app_js)
    
    # 6. CSS Styles
    create_css_files(frontend_path)
    
    print("✅ تمام فایل‌های فرانت‌اند ایجاد شد!")
    print("🚀 حالا می‌تونی npm install رو اجرا کنی")

def create_css_files(frontend_path):
    """ایجاد فایل‌های CSS"""
    
    # index.css
    index_css = """* {
  font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  margin: 0;
  direction: rtl;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}"""
    write_file(frontend_path / "src/styles/index.css", index_css)
    
    # App.css مدرن
    app_css = """.App {
  min-height: 100vh;
  color: white;
}

/* Navigation */
.navbar {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1rem;
}

.nav-brand h1 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
  background: linear-gradient(135deg, #a2b2ee 0%, #ffffff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-menu {
  display: flex;
  gap: 2rem;
}

.nav-menu a {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-menu a:hover {
  color: white;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.search-btn, .cart-btn, .auth-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.search-btn:hover, .cart-btn:hover, .auth-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

.cart-btn {
  position: relative;
}

.cart-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #ef4444;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: bold;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-menu button {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s;
}

/* Loading Screen */
.loading-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Hero Section */
.hero {
  text-align: center;
  padding: 4rem 1rem;
  background: rgba(0, 0, 0, 0.2);
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #a2b2ee 0%, #ffffff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-content p {
  font-size: 1.2rem;
  opacity: 0.9;
}

/* Products Section */
.products-section {
  padding: 3rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.products-section h2 {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 3rem;
  background: linear-gradient(135deg, #a2b2ee 0%, #ffffff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.product-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  animation: fadeIn 0.5s ease-out;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  background: rgba(255, 255, 255, 0.15);
}

.product-image {
  height: 200px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.product-card:hover .product-image img {
  transform: scale(1.1);
}

.product-info {
  padding: 1.5rem;
}

.product-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.product-description {
  opacity: 0.8;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-price {
  font-size: 1.1rem;
  font-weight: 700;
  color: #a2b2ee;
}

.add-to-cart-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.add-to-cart-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

/* Auth Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.auth-modal {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  margin: 1rem;
  animation: slideUp 0.3s ease-out;
}

.auth-modal h2 {
  margin-top: 0;
  text-align: center;
  margin-bottom: 1.5rem;
}

.auth-modal input {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  color: white;
  font-size: 1rem;
  box-sizing: border-box;
}

.auth-modal input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.auth-modal input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.3);
}

.auth-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.auth-actions button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.auth-actions button[type="submit"] {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.auth-actions button[type="button"] {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.auth-hint {
  margin-top: 1rem;
  text-align: center;
  font-size: 0.8rem;
  opacity: 0.7;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
}

/* Cart Sidebar */
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.cart-sidebar {
  position: fixed;
  top: 0;
  right: 0;
  height: 100%;
  width: 100%;
  max-width: 400px;
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(20px);
  border-left: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
  animation: slideRight 0.3s ease-out;
}

.cart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.cart-header button {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

.cart-items {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.cart-item img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 0.5rem;
}

.item-info {
  flex: 1;
}

.item-info h4 {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
}

.item-info p {
  margin: 0 0 0.5rem 0;
  font-size: 0.8rem;
  opacity: 0.8;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.quantity-controls button {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
}

.remove-btn {
  background: #ef4444;
  border: none;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.75rem;
}

.cart-footer {
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.cart-total {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-align: center;
}

.checkout-btn {
  width: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { 
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideRight {
  from { 
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .nav-menu {
    display: none;
  }
  
  .hero-content h1 {
    font-size: 2rem;
  }
  
  .products-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
  }
  
  .cart-sidebar {
    max-width: 100%;
  }
}"""
    write_file(frontend_path / "src/styles/App.css", app_css)

def write_file(path, content):
    """نوشتن محتوا در فایل"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    create_frontend_files()