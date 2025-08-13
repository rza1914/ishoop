import React, { useState, useEffect, useCallback, useMemo } from 'react';
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

const ArrowRightIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
  </svg>
);

const StarIcon = ({ filled = true }) => (
  <svg xmlns="http://www.w3.org/2000/svg" className={`h-4 w-4 ${filled ? 'text-yellow-400' : 'text-gray-400'}`} fill={filled ? 'currentColor' : 'none'} viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
  </svg>
);

const CloseIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
  </svg>
);

const DashboardIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
  </svg>
);

const OrdersIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
  </svg>
);

const HeartIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
  </svg>
);

// --- API Service ---
const API_BASE = 'http://localhost:8000/api/v1';

const api = {
  getProducts: async (search = '') => {
    const url = search ? `${API_BASE}/products?search=${encodeURIComponent(search)}` : `${API_BASE}/products`;
    const response = await fetch(url);
    if (!response.ok) throw new Error('Failed to fetch products');
    return response.json();
  },
  
  getProduct: async (id) => {
    const response = await fetch(`${API_BASE}/products/${id}`);
    if (!response.ok) throw new Error('Product not found');
    return response.json();
  },
  
  getBlogPosts: async () => {
    const response = await fetch(`${API_BASE}/blog`);
    if (!response.ok) throw new Error('Failed to fetch blog posts');
    return response.json();
  },
  
  getBlogPost: async (id) => {
    const response = await fetch(`${API_BASE}/blog/${id}`);
    if (!response.ok) throw new Error('Blog post not found');
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
    
    if (!response.ok) throw new Error('Login failed');
    return response.json();
  },
  
  submitReview: async (reviewData) => {
    const response = await fetch(`${API_BASE}/reviews`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(reviewData)
    });
    return response.json();
  },

  createOrder: async (orderData) => {
    const response = await fetch(`${API_BASE}/orders`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(orderData)
    });
    if (!response.ok) throw new Error('Order creation failed');
    return response.json();
  },

  getOrders: async () => {
    const response = await fetch(`${API_BASE}/orders`);
    if (!response.ok) throw new Error('Failed to fetch orders');
    return response.json();
  }
};

// --- Helper Functions ---
const formatPrice = (price) => new Intl.NumberFormat('fa-IR').format(price) + ' تومان';
const formatDate = (dateStr) => new Date(dateStr).toLocaleDateString('fa-IR');

// --- کامپوننت Navigation ---
const Navbar = ({ 
  cartCount, 
  onCartClick, 
  onAuthClick, 
  user, 
  onLogout, 
  currentPage, 
  onPageChange,
  onSearch,
  searchTerm,
  setSearchTerm 
}) => {
  const [showSearchBox, setShowSearchBox] = useState(false);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      onSearch(searchTerm);
      onPageChange('products');
      setShowSearchBox(false);
    }
  };

  return (
    <nav className="navbar">
      <div className="nav-container">
        <div className="nav-brand">
          <h1 onClick={() => onPageChange('home')}>iShop</h1>
        </div>
        
        <div className="nav-menu">
          <button 
            className={currentPage === 'home' ? 'active' : ''}
            onClick={() => onPageChange('home')}
          >
            خانه
          </button>
          <button 
            className={currentPage === 'products' ? 'active' : ''}
            onClick={() => onPageChange('products')}
          >
            محصولات
          </button>
          <button 
            className={currentPage === 'blog' ? 'active' : ''}
            onClick={() => onPageChange('blog')}
          >
            وبلاگ
          </button>
        </div>
        
        <div className="nav-actions">
          <div className="search-container">
            <button 
              className="search-btn"
              onClick={() => setShowSearchBox(!showSearchBox)}
            >
              <SearchIcon />
              <span>جستجو</span>
            </button>
            
            {showSearchBox && (
              <form 
                className="search-form"
                onSubmit={handleSearchSubmit}
              >
                <input
                  type="text"
                  placeholder="جستجو در محصولات..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="search-input-nav"
                  autoFocus
                />
                <button type="submit">جستجو</button>
              </form>
            )}
          </div>
          
          <button className="cart-btn" onClick={onCartClick}>
            <ShoppingCartIcon />
            <span>سبد خرید</span>
            {cartCount > 0 && <span className="cart-badge">{cartCount}</span>}
          </button>
          
          {user ? (
            <div className="user-dropdown">
              <button className="user-btn">
                <UserIcon />
                <span>{user.name}</span>
              </button>
              <div className="user-menu">
                <button onClick={() => onPageChange('dashboard')}>
                  <DashboardIcon />
                  داشبورد
                </button>
                <button onClick={onLogout}>
                  خروج
                </button>
              </div>
            </div>
          ) : (
            <button className="auth-btn" onClick={onAuthClick}>
              <UserIcon />
              <span>ورود</span>
            </button>
          )}
        </div>
      </div>
    </nav>
  );
};

// --- صفحه اصلی ---
const HomePage = ({ products, onProductClick, onAddToCart }) => {
  return (
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
            {products.slice(0, 4).map(product => (
              <div
                key={product.id}
                className="product-card"
                onClick={() => onProductClick(product)}
              >
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
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🚚</div>
              <h3>ارسال سریع</h3>
              <p>ارسال رایگان برای خریدهای بالای ۵۰۰ هزار تومان</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🛡️</div>
              <h3>ضمانت اصالت</h3>
              <p>تمامی محصولات اورجینال و دارای ضمانت معتبر</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">💬</div>
              <h3>پشتیبانی ۲۴/۷</h3>
              <p>تیم پشتیبانی ما همیشه در خدمت شماست</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
};

// --- صفحه محصولات ---
const ProductsPage = ({ products, onProductClick, onAddToCart, searchTerm }) => {
  const [localSearchTerm, setLocalSearchTerm] = useState(searchTerm || '');
  const [selectedCategory, setSelectedCategory] = useState('');
  
  const categories = useMemo(() => {
    const cats = [...new Set(products.map(p => p.category))];
    return cats.filter(Boolean);
  }, [products]);
  
  const filteredProducts = useMemo(() => {
    return products.filter(product => {
      const matchesSearch = product.name.toLowerCase().includes(localSearchTerm.toLowerCase()) ||
                           product.description.toLowerCase().includes(localSearchTerm.toLowerCase());
      const matchesCategory = !selectedCategory || product.category === selectedCategory;
      return matchesSearch && matchesCategory;
    });
  }, [products, localSearchTerm, selectedCategory]);
  
  return (
    <div className="products-page">
      <div className="container">
        <h1>تمام محصولات</h1>
        
        {/* فیلترها */}
        <div className="filters">
          <input
            type="text"
            placeholder="جستجو در محصولات..."
            value={localSearchTerm}
            onChange={(e) => setLocalSearchTerm(e.target.value)}
            className="search-input"
          />
          
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="category-select"
          >
            <option value="">همه دسته‌ها</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
        
        {/* محصولات */}
        <div className="products-grid">
          {filteredProducts.map(product => (
            <div
              key={product.id}
              className="product-card"
              onClick={() => onProductClick(product)}
            >
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
          ))}
        </div>
        
        {filteredProducts.length === 0 && (
          <div className="no-results">
            <p>محصولی با این مشخصات یافت نشد.</p>
          </div>
        )}
      </div>
    </div>
  );
};

// --- جزئیات محصول ---
const ProductDetailPage = ({ product, onBack, onAddToCart }) => {
  const [reviewText, setReviewText] = useState('');
  const [reviewRating, setReviewRating] = useState(5);
  const [submitting, setSubmitting] = useState(false);
  
  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    
    try {
      await api.submitReview({
        product_id: product.id,
        rating: reviewRating,
        text: reviewText
      });
      
      setReviewText('');
      setReviewRating(5);
      alert('نظر شما با موفقیت ثبت شد!');
    } catch (error) {
      alert('خطا در ثبت نظر');
    }
    
    setSubmitting(false);
  };
  
  return (
    <div className="product-detail-page">
      <div className="container">
        <button className="back-btn" onClick={onBack}>
          <ArrowRightIcon />
          بازگشت
        </button>
        
        <div className="product-detail">
          <div className="product-image">
            <img src={product.imageUrl} alt={product.name} />
          </div>
          
          <div className="product-info">
            <h1>{product.name}</h1>
            <p className="product-description">{product.description}</p>
            <p className="product-price">{formatPrice(product.price)}</p>
            
            <div className="product-actions">
              <button 
                className="add-to-cart-btn large"
                onClick={() => onAddToCart(product)}
              >
                افزودن به سبد خرید
              </button>
              <button className="wishlist-btn">
                <HeartIcon />
                علاقه‌مندی‌ها
              </button>
            </div>
          </div>
        </div>
        
        {/* نظرات */}
        <div className="reviews-section">
          <h2>نظرات کاربران</h2>
          
          {product.reviews && product.reviews.length > 0 ? (
            <div className="reviews-list">
              {product.reviews.map((review, index) => (
                <div key={index} className="review">
                  <div className="review-header">
                    <span className="author">{review.author}</span>
                    <div className="rating">
                      {[...Array(5)].map((_, i) => (
                        <StarIcon key={i} filled={i < review.rating} />
                      ))}
                    </div>
                  </div>
                  <p className="review-text">{review.text}</p>
                </div>
              ))}
            </div>
          ) : (
            <p>هنوز نظری ثبت نشده است.</p>
          )}
          
          {/* فرم ثبت نظر */}
          <div className="review-form">
            <h3>نظر خود را ثبت کنید</h3>
            <form onSubmit={handleReviewSubmit}>
              <div className="rating-input">
                <span>امتیاز:</span>
                <div className="stars">
                  {[...Array(5)].map((_, i) => (
                    <button
                      key={i}
                      type="button"
                      onClick={() => setReviewRating(i + 1)}
                    >
                      <StarIcon filled={i < reviewRating} />
                    </button>
                  ))}
                </div>
              </div>
              
              <textarea
                value={reviewText}
                onChange={(e) => setReviewText(e.target.value)}
                placeholder="نظر خود را بنویسید..."
                required
              ></textarea>
              
              <button type="submit" disabled={submitting}>
                {submitting ? 'در حال ثبت...' : 'ثبت نظر'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

// --- صفحه وبلاگ ---
const BlogPage = ({ posts, onPostClick }) => {
  return (
    <div className="blog-page">
      <div className="container">
        <h1>وبلاگ iShop</h1>
        
        <div className="blog-grid">
          {posts.map(post => (
            <div
              key={post.id}
              className="blog-card"
              onClick={() => onPostClick(post)}
            >
              <div className="blog-image">
                <img src={post.imageUrl} alt={post.title} />
              </div>
              <div className="blog-info">
                <h2>{post.title}</h2>
                <p className="blog-excerpt">{post.excerpt}</p>
                <span className="blog-date">{formatDate(post.date)}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// --- جزئیات مطلب وبلاگ ---
const BlogPostPage = ({ post, onBack }) => {
  return (
    <div className="blog-post-page">
      <div className="container">
        <button className="back-btn" onClick={onBack}>
          <ArrowRightIcon />
          بازگشت به وبلاگ
        </button>
        
        <article className="blog-post">
          <img src={post.imageUrl} alt={post.title} className="blog-hero-image" />
          <h1>{post.title}</h1>
          <p className="blog-date">{formatDate(post.date)}</p>
          <div 
            className="blog-content"
            dangerouslySetInnerHTML={{ __html: post.content }}
          ></div>
        </article>
      </div>
    </div>
  );
};

// --- داشبورد کاربری ---
const DashboardPage = ({ user }) => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getOrders()
      .then(setOrders)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const renderContent = () => {
    switch (activeTab) {
      case 'orders':
        return (
          <div className="orders-content">
            <h2>سفارشات من</h2>
            {loading ? (
              <p>در حال بارگذاری...</p>
            ) : orders.length > 0 ? (
              <div className="orders-list">
                {orders.map(order => (
                  <div key={order.id} className="order-card">
                    <div className="order-header">
                      <span>سفارش #{order.id}</span>
                      <span className={`order-status ${order.status.replace(' ', '-')}`}>
                        {order.status}
                      </span>
                    </div>
                    <div className="order-details">
                      <p>تاریخ: {formatDate(order.date)}</p>
                      <p>مبلغ: {formatPrice(order.total)}</p>
                      {order.tracking_code && (
                        <p>کد رهگیری: {order.tracking_code}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p>هنوز سفارشی ثبت نکرده‌اید.</p>
            )}
          </div>
        );
      
      case 'wishlist':
        return (
          <div className="wishlist-content">
            <h2>علاقه‌مندی‌ها</h2>
            <p>این بخش در حال توسعه است.</p>
          </div>
        );
      
      case 'profile':
        return (
          <div className="profile-content">
            <h2>اطلاعات کاربری</h2>
            <div className="profile-form">
              <div className="form-group">
                <label>نام:</label>
                <input type="text" value={user?.name || ''} readOnly />
              </div>
              <div className="form-group">
                <label>ایمیل:</label>
                <input type="email" value={user?.email || ''} readOnly />
              </div>
              <p className="note">برای ویرایش اطلاعات با پشتیبانی تماس بگیرید.</p>
            </div>
          </div>
        );
      
      default:
        return (
          <div className="dashboard-overview">
            <h2>خوش آمدید {user?.name}</h2>
            <div className="dashboard-stats">
              <div className="stat-card">
                <h3>تعداد سفارشات</h3>
                <p className="stat-number">{orders.length}</p>
              </div>
              <div className="stat-card">
                <h3>علاقه‌مندی‌ها</h3>
                <p className="stat-number">0</p>
              </div>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="dashboard-page">
      <div className="container">
        <h1>داشبورد کاربری</h1>
        
        <div className="dashboard-layout">
          <div className="dashboard-sidebar">
            <button 
              className={activeTab === 'dashboard' ? 'active' : ''}
              onClick={() => setActiveTab('dashboard')}
            >
              <DashboardIcon />
              داشبورد
            </button>
            <button 
              className={activeTab === 'orders' ? 'active' : ''}
              onClick={() => setActiveTab('orders')}
            >
              <OrdersIcon />
              سفارشات من
            </button>
            <button 
              className={activeTab === 'wishlist' ? 'active' : ''}
              onClick={() => setActiveTab('wishlist')}
            >
              <HeartIcon />
              علاقه‌مندی‌ها
            </button>
            <button 
              className={activeTab === 'profile' ? 'active' : ''}
              onClick={() => setActiveTab('profile')}
            >
              <UserIcon />
              پروفایل
            </button>
          </div>
          
          <div className="dashboard-content">
            {renderContent()}
          </div>
        </div>
      </div>
    </div>
  );
};

// --- مودال احراز هویت ---
const AuthModal = ({ isOpen, onClose, onLogin }) => {
  const [email, setEmail] = useState('admin@ishop.com');
  const [password, setPassword] = useState('admin123');
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
        <button className="modal-close" onClick={onClose}>
          <CloseIcon />
        </button>
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
          <p>اطلاعات تست: admin@ishop.com / admin123</p>
        </div>
      </div>
    </div>
  );
};

// --- سایدبار سبد خرید ---
const CartSidebar = ({ isOpen, onClose, items, onUpdateQuantity, onRemove, total, onCheckout }) => {
  if (!isOpen) return null;
  
  return (
    <div className="sidebar-overlay" onClick={onClose}>
      <div className="cart-sidebar" onClick={e => e.stopPropagation()}>
        <div className="cart-header">
          <h2>سبد خرید</h2>
          <button onClick={onClose}>
            <CloseIcon />
          </button>
        </div>
        
        <div className="cart-items">
          {items.length === 0 ? (
            <div className="empty-cart">
              <p>سبد خرید شما خالی است</p>
              <button onClick={onClose}>ادامه خرید</button>
            </div>
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
                <button className="remove-btn" onClick={() => onRemove(item.id)}>
                  <CloseIcon />
                </button>
              </div>
            ))
          )}
        </div>
        
        {items.length > 0 && (
          <div className="cart-footer">
            <div className="cart-total">
              مجموع: {formatPrice(total)}
            </div>
            <button className="checkout-btn" onClick={onCheckout}>
              تکمیل خرید
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

// --- فوتر ---
const Footer = ({ onPageChange }) => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>iShop</h3>
            <p>فروشگاه آنلاین محصولات اورجینال با بهترین قیمت و خدمات پس از فروش.</p>
          </div>
          
          <div className="footer-section">
            <h4>لینک‌های مفید</h4>
            <ul>
              <li><button onClick={() => onPageChange('home')}>خانه</button></li>
              <li><button onClick={() => onPageChange('products')}>محصولات</button></li>
              <li><button onClick={() => onPageChange('blog')}>وبلاگ</button></li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h4>خدمات مشتریان</h4>
            <ul>
              <li><a href="#faq">سوالات متداول</a></li>
              <li><a href="#terms">قوانین و مقررات</a></li>
              <li><a href="#guide">راهنمای خرید</a></li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h4>تماس با ما</h4>
            <ul>
              <li>تهران، خیابان ولیعصر</li>
              <li>021-12345678</li>
              <li>info@ishop.com</li>
            </ul>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>&copy; 2024 فروشگاه iShop. تمامی حقوق محفوظ است.</p>
        </div>
      </div>
    </footer>
  );
};

// --- کامپوننت اصلی اپلیکیشن ---
function App() {
  // State ها
  const [currentPage, setCurrentPage] = useState('home');
  const [products, setProducts] = useState([]);
  const [blogPosts, setBlogPosts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [selectedBlogPost, setSelectedBlogPost] = useState(null);
  const [cartItems, setCartItems] = useState([]);
  const [user, setUser] = useState(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [showCart, setShowCart] = useState(false);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  
  // بارگذاری اولیه
  useEffect(() => {
    const loadData = async () => {
      try {
        const [productsData, blogData] = await Promise.all([
          api.getProducts(),
          api.getBlogPosts()
        ]);
        
        setProducts(productsData);
        setBlogPosts(blogData);
      } catch (error) {
        console.error('خطا در بارگذاری داده‌ها:', error);
        alert('خطا در اتصال به سرور. لطفاً بررسی کنید که backend در حال اجرا باشد.');
      }
      setLoading(false);
    };
    
    loadData();
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
    
    // نمایش پیام موفقیت
    alert(`${product.name} به سبد خرید اضافه شد!`);
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
  
  // محاسبات سبد خرید
  const cartTotal = useMemo(() => {
    return cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
  }, [cartItems]);
  
  const cartCount = useMemo(() => {
    return cartItems.reduce((count, item) => count + item.quantity, 0);
  }, [cartItems]);
  
  // مدیریت صفحات
  const handlePageChange = (page) => {
    setCurrentPage(page);
    setSelectedProduct(null);
    setSelectedBlogPost(null);
  };
  
  const handleProductClick = async (product) => {
    try {
      const fullProduct = await api.getProduct(product.id);
      setSelectedProduct(fullProduct);
      setCurrentPage('productDetail');
    } catch (error) {
      console.error('خطا در بارگذاری جزئیات محصول:', error);
    }
  };
  
  const handleBlogPostClick = async (post) => {
    try {
      const fullPost = await api.getBlogPost(post.id);
      setSelectedBlogPost(fullPost);
      setCurrentPage('blogPost');
    } catch (error) {
      console.error('خطا در بارگذاری مطلب:', error);
    }
  };
  
  // جستجو
  const handleSearch = async (term) => {
    try {
      setLoading(true);
      const searchResults = await api.getProducts(term);
      setProducts(searchResults);
      setSearchTerm(term);
    } catch (error) {
      console.error('خطا در جستجو:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // احراز هویت
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
    if (currentPage === 'dashboard') {
      setCurrentPage('home');
    }
  };
  
  // تکمیل خرید
  const handleCheckout = async () => {
    try {
      const orderData = {
        total: cartTotal,
        items: cartItems.map(item => ({
          product_id: item.id,
          quantity: item.quantity,
          price: item.price
        }))
      };
      
      const order = await api.createOrder(orderData);
      
      // پاک کردن سبد خرید
      setCartItems([]);
      setShowCart(false);
      
      alert(`سفارش با موفقیت ثبت شد!\nکد رهگیری: ${order.tracking_code}`);
      
    } catch (error) {
      console.error('خطا در ثبت سفارش:', error);
      alert('خطا در ثبت سفارش. لطفاً دوباره تلاش کنید.');
    }
  };
  
  // نمایش صفحه بارگذاری
  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner"></div>
        <p>در حال بارگذاری...</p>
      </div>
    );
  }
  
  // رندر محتوا
  const renderContent = () => {
    switch (currentPage) {
      case 'products':
        return (
          <ProductsPage
            products={products}
            onProductClick={handleProductClick}
            onAddToCart={addToCart}
            searchTerm={searchTerm}
          />
        );
      
      case 'blog':
        return (
          <BlogPage
            posts={blogPosts}
            onPostClick={handleBlogPostClick}
          />
        );
      
      case 'productDetail':
        return selectedProduct ? (
          <ProductDetailPage
            product={selectedProduct}
            onBack={() => handlePageChange('products')}
            onAddToCart={addToCart}
          />
        ) : null;
      
      case 'blogPost':
        return selectedBlogPost ? (
          <BlogPostPage
            post={selectedBlogPost}
            onBack={() => handlePageChange('blog')}
          />
        ) : null;
      
      case 'dashboard':
        return user ? (
          <DashboardPage user={user} />
        ) : (
          <>
            {setShowAuthModal(true)}
            {handlePageChange('home')}
          </>
        );
      
      default:
        return (
          <HomePage
            products={products}
            onProductClick={handleProductClick}
            onAddToCart={addToCart}
          />
        );
    }
  };
  
  return (
    <div className="App">
      <Navbar
        cartCount={cartCount}
        onCartClick={() => setShowCart(true)}
        onAuthClick={() => setShowAuthModal(true)}
        user={user}
        onLogout={handleLogout}
        currentPage={currentPage}
        onPageChange={handlePageChange}
        onSearch={handleSearch}
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
      />
      
      {renderContent()}
      
      <Footer onPageChange={handlePageChange} />
      
      {/* مودال‌ها */}
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
        onCheckout={handleCheckout}
      />
    </div>
  );
}

export default App;