import React, { useState, useEffect, useCallback, useMemo } from 'react';

// --- استایل‌های گلوبال ---
const GlobalStyles = () => (
    <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100;200;300;400;500;600;700;800;900&display=swap');
        body, button, input, textarea, div, p, h1, h2, h3, h4, h5, h6, span, a { 
            font-family: 'Vazirmatn', sans-serif;
        }
        .gradient-text {
            background: linear-gradient(135deg, #a2b2ee 0%, #ffffff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
    `}</style>
);

// --- آیکون‌ها ---
const ShoppingCartIcon = () => ( <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg> );
const UserIcon = () => ( <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg> );
const EyeIcon = ({ off = false }) => ( <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">{off ? (<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a9.97 9.97 0 01-1.563 3.029m0 0l-2.145-2.145" />) : (<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />)}</svg> );
const ShippingIcon = () => ( <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10l2 2h8a1 1 0 001-1z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1" /></svg> );
const ShieldIcon = () => ( <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 20.944a11.955 11.955 0 0118-8.944c0 2.592-.868 5.022-2.382 6.984L18 13" /></svg> );
const SupportIcon = () => ( <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" /></svg> );
const CloseIcon = () => (<svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>);
const ArrowUpIcon = () => (<svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" /></svg>);
const SearchIcon = () => (<svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>);
const GoogleIcon = () => (<svg className="w-5 h-5" viewBox="0 0 48 48"><path fill="#FFC107" d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"></path><path fill="#FF3D00" d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z"></path><path fill="#4CAF50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z"></path><path fill="#1976D2" d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.574l6.19,5.238C41.38,36.151,44,30.63,44,24C44,22.659,43.862,21.35,43.611,20.083z"></path></svg>);
const TelegramIcon = () => (<svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor"><path d="M9.78,18.65l.28-4.23c.07-1.03-.2-1.5-.68-1.95c-1.7-1.58-3.26-3-5.22-4.71c-.33-.29-.11-.8.34-.83c3.1-.21,6.22-.43,9.33-.63c3.55-.23,6.38,1.19,6.5,4.81c.06,1.93-.4,3.37-1.12,5.1c-.81,1.93-1.93,3.48-3.4,5.23c-.39.46-.93.42-1.32-.04C12.9,19.94,11.34,19.3,9.78,18.65z"></path></svg>);
const DashboardIcon = () => (<svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>);
const ProductsIcon = () => (<svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>);
const CategoryIcon = () => (<svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>);
const OrdersIcon = () => (<svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>);
const UsersIcon = () => (<svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>);
const BlogIcon = () => (<svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>);
const PlusIcon = () => (<svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>);
const EditIcon = () => (<svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>);
const DeleteIcon = () => (<svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>);

// --- سرویس API واقعی ---
const BASE_URL = 'http://localhost:8000/api/v1'; // آدرس بک‌اند FastAPI

const api = {
    // تابع کمکی برای درخواست‌ها
    _request: async (url, options = {}) => {
        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'خطای ناشناخته در سرور' }));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }
            // Handle cases where response might be empty (e.g., DELETE)
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.indexOf("application/json") !== -1) {
                return await response.json();
            } else {
                return {}; // Return empty object for non-json responses
            }
        } catch (error) {
            console.error("API Request Error:", error);
            throw error;
        }
    },

    // Auth
    login: function(credentials) {
        const formData = new URLSearchParams();
        formData.append('username', credentials.username);
        formData.append('password', credentials.password);
        return this._request(`${BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData,
        });
    },
    register: function(userData) {
        return this._request(`${BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData),
        });
    },
    getCurrentUser: function(token) {
        return this._request(`${BASE_URL}/users/me`, {
            headers: { 'Authorization': `Bearer ${token}` },
        });
    },

    // Products
    getProducts: function() { return this._request(`${BASE_URL}/products`); },
    getProductById: function(id) { return this._request(`${BASE_URL}/products/${id}`); },
    addProduct: function(productData, token) {
        return this._request(`${BASE_URL}/products`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify(productData),
        });
    },
    updateProduct: function(id, productData, token) {
        return this._request(`${BASE_URL}/products/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify(productData),
        });
    },
    deleteProduct: function(id, token) {
        return this._request(`${BASE_URL}/products/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` },
        });
    },

    // Orders
    getOrders: function(token) {
        return this._request(`${BASE_URL}/orders`, {
            headers: { 'Authorization': `Bearer ${token}` },
        });
    },
    createOrder: function(orderData, token) {
        return this._request(`${BASE_URL}/orders`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify(orderData),
        });
    },

    // Reviews
    submitReview: function(reviewData, token) {
        return this._request(`${BASE_URL}/reviews`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify(reviewData),
        });
    },

    // Blog Posts
    getBlogPosts: function() { return this._request(`${BASE_URL}/blog`); },
    getBlogPostById: function(id) { return this._request(`${BASE_URL}/blog/${id}`); },
    addBlogPost: function(postData, token) {
        return this._request(`${BASE_URL}/blog`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify(postData),
        });
    },
    updateBlogPost: function(id, postData, token) {
        return this._request(`${BASE_URL}/blog/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify(postData),
        });
    },
    deleteBlogPost: function(id, token) {
        return this._request(`${BASE_URL}/blog/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` },
        });
    },

    // Users Management
    getUsers: function(token) {
        return this._request(`${BASE_URL}/users`, {
            headers: { 'Authorization': `Bearer ${token}` },
        });
    },
    updateUser: function(id, userData, token) {
        return this._request(`${BASE_URL}/users/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify(userData),
        });
    },
    deleteUser: function(id, token) {
        return this._request(`${BASE_URL}/users/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` },
        });
    },

    // Categories
    getCategories: function() { return this._request(`${BASE_URL}/categories`); },
    addCategory: function(categoryData, token) {
        return this._request(`${BASE_URL}/categories`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify(categoryData),
        });
    },
    updateCategory: function(id, categoryData, token) {
        return this._request(`${BASE_URL}/categories/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify(categoryData),
        });
    },
    deleteCategory: function(id, token) {
        return this._request(`${BASE_URL}/categories/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` },
        });
    },
};

// --- CONTEXT APIs ---
const AuthContext = React.createContext(null);
const useAuth = () => React.useContext(AuthContext);
const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(null);
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // بررسی وجود توکن در localStorage
        const savedToken = localStorage.getItem('ishop_token');
        if (savedToken) {
            setToken(savedToken);
            // دریافت اطلاعات کاربر
            api.getCurrentUser(savedToken)
                .then(setUser)
                .catch(() => {
                    setToken(null);
                    setUser(null);
                    localStorage.removeItem('ishop_token');
                })
                .finally(() => setLoading(false));
        } else {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        if (token) {
            localStorage.setItem('ishop_token', token);
        } else {
            localStorage.removeItem('ishop_token');
        }
    }, [token]);

    const login = async (credentials) => {
        const { access_token } = await api.login(credentials);
        setToken(access_token);
        const userData = await api.getCurrentUser(access_token);
        setUser(userData);
    };

    const register = async (userData) => {
        const { access_token } = await api.register(userData);
        setToken(access_token);
        const currentUser = await api.getCurrentUser(access_token);
        setUser(currentUser);
    };

    const logout = () => {
        setToken(null);
        setUser(null);
        localStorage.removeItem('ishop_token');
    };

    const value = { token, user, loading, login, logout, register };
    return <AuthContext.Provider value={value}>{!loading && children}</AuthContext.Provider>;
};

const CartContext = React.createContext(null);
const useCart = () => React.useContext(CartContext);
const CartProvider = ({ children }) => {
    const [items, setItems] = useState(() => {
        try {
            const localData = localStorage.getItem('ishop_cart');
            return localData ? JSON.parse(localData) : [];
        } catch (error) {
            return [];
        }
    });

    useEffect(() => {
        localStorage.setItem('ishop_cart', JSON.stringify(items));
    }, [items]);

    const addToCart = (product, quantity = 1) => {
        setItems(prevItems => {
            const existingItem = prevItems.find(item => item.id === product.id);
            if (existingItem) {
                return prevItems.map(item =>
                    item.id === product.id
                        ? { ...item, quantity: item.quantity + quantity }
                        : item
                );
            }
            return [...prevItems, { ...product, quantity }];
        });
    };

    const removeFromCart = (productId) => {
        setItems(prevItems => prevItems.filter(item => item.id !== productId));
    };

    const updateQuantity = (productId, quantity) => {
        if (quantity <= 0) {
            removeFromCart(productId);
        } else {
            setItems(prevItems =>
                prevItems.map(item =>
                    item.id === productId ? { ...item, quantity } : item
                )
            );
        }
    };

    const clearCart = () => setItems([]);

    const cartCount = items.reduce((count, item) => count + item.quantity, 0);
    const cartTotal = items.reduce((total, item) => total + item.price * item.quantity, 0);

    const value = { items, addToCart, removeFromCart, updateQuantity, clearCart, cartCount, cartTotal };
    return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
};

// --- Helper Functions ---
const formatPrice = (price) => new Intl.NumberFormat('fa-IR').format(price) + ' تومان';
const formatDate = (dateString) => new Date(dateString).toLocaleDateString('fa-IR', { year: 'numeric', month: 'long', day: 'numeric' });

// --- کامپوننت‌های UI ---
const AuthPage = ({ setPage }) => {
    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const { login, register } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            if (isLogin) {
                await login({ username: email, password });
            } else {
                await register({ email, password, name });
            }
            setPage('home');
        } catch (err) {
            setError(err.message || 'یک خطای غیرمنتظره رخ داد.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-4" style={{background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'}}>
            <div className="w-full max-w-md">
                <div className="bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl p-8 space-y-6 border border-white/20">
                    <h1 className="text-4xl font-bold text-center text-white tracking-wider">iShop</h1>
                    <h2 className="text-2xl font-light text-center text-white">{isLogin ? 'خوش آمدید' : 'ایجاد حساب کاربری'}</h2>
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {!isLogin && (
                            <div>
                                <label className="text-sm font-medium text-gray-200 block mb-2">نام</label>
                                <input
                                    type="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    className="w-full p-3 bg-white/20 rounded-lg border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-[#667eea] transition duration-300"
                                    placeholder="نام شما"
                                    required
                                />
                            </div>
                        )}
                        <div>
                            <label className="text-sm font-medium text-gray-200 block mb-2">ایمیل</label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full p-3 bg-white/20 rounded-lg border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-[#667eea] transition duration-300"
                                placeholder="you@example.com"
                                required
                            />
                        </div>
                        <div>
                            <label className="text-sm font-medium text-gray-200 block mb-2">رمز عبور</label>
                            <div className="relative">
                                <input
                                    type={showPassword ? 'text' : 'password'}
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="w-full p-3 bg-white/20 rounded-lg border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-[#667eea] transition duration-300"
                                    placeholder="••••••••"
                                    required
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute inset-y-0 left-0 px-3 flex items-center text-gray-300 hover:text-white"
                                >
                                    <EyeIcon off={!showPassword} />
                                </button>
                            </div>
                        </div>
                        {error && <p className="text-sm text-red-400 bg-red-500/20 p-3 rounded-lg">{error}</p>}
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full py-3 px-4 bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white font-semibold rounded-lg shadow-lg hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#667eea] focus:ring-offset-gray-900 transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? 'در حال پردازش...' : (isLogin ? 'ورود' : 'ثبت نام')}
                        </button>
                    </form>
                    
                    <div className="flex items-center justify-center space-x-2 space-x-reverse my-4">
                        <span className="h-px w-full bg-white/20"></span>
                        <span className="text-gray-300 text-sm">یا</span>
                        <span className="h-px w-full bg-white/20"></span>
                    </div>

                    <div className="space-y-4">
                        <button
                            type="button"
                            onClick={() => alert('ورود با گوگل هنوز پیاده‌سازی نشده است.')}
                            className="w-full flex items-center justify-center py-2.5 px-4 bg-white/90 text-gray-800 font-semibold rounded-lg shadow-lg hover:bg-white transition-all duration-300"
                        >
                            <GoogleIcon />
                            <span className="mr-2">{isLogin ? 'ورود با گوگل' : 'ثبت نام با گوگل'}</span>
                        </button>
                        <button
                            type="button"
                            onClick={() => alert('ورود با تلگرام هنوز پیاده‌سازی نشده است.')}
                            className="w-full flex items-center justify-center py-2.5 px-4 bg-[#2AABEE] text-white font-semibold rounded-lg shadow-lg hover:bg-[#279cde] transition-all duration-300"
                        >
                            <TelegramIcon />
                            <span className="mr-2">{isLogin ? 'ورود با تلگرام' : 'ثبت نام با تلگرام'}</span>
                        </button>
                    </div>

                    <div className="text-center text-gray-300 pt-4">
                        <button
                            onClick={() => setIsLogin(!isLogin)}
                            className="hover:text-white hover:underline"
                        >
                            {isLogin ? "حساب کاربری ندارید؟ ثبت نام کنید" : 'قبلاً ثبت‌نام کرده‌اید؟ وارد شوید'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

const Navbar = ({ setPage, setIsCartOpen, setSearchTerm }) => {
    const { user, logout } = useAuth();
    const { cartCount } = useCart();
    const [isSearchVisible, setIsSearchVisible] = useState(false);
    const [localSearch, setLocalSearch] = useState('');

    const handleLogout = () => {
        logout();
        setPage('login');
    };
    
    const handleSearchSubmit = (e) => {
        e.preventDefault();
        setSearchTerm(localSearch);
        setPage('products');
        setIsSearchVisible(false);
    };

    return (
        <nav className="bg-white/10 backdrop-blur-lg shadow-lg sticky top-0 z-40 border-b border-white/20">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    <div className="flex items-center space-x-8 space-x-reverse">
                        <button onClick={() => setPage('home')} className="text-white text-2xl font-bold tracking-wider">iShop</button>
                        <div className="hidden md:flex space-x-6 space-x-reverse">
                           <button onClick={() => setPage('home')} className="text-white hover:text-purple-200 transition">خانه</button>
                           <button onClick={() => setPage('products')} className="text-white/80 hover:text-white transition">محصولات</button>
                           <button onClick={() => setPage('blog')} className="text-white/80 hover:text-white transition">وبلاگ</button>
                        </div>
                    </div>
                    <div className="flex items-center space-x-2 space-x-reverse">
                        <div className="relative" onMouseLeave={() => setIsSearchVisible(false)}>
                            <button
                                onMouseEnter={() => setIsSearchVisible(true)}
                                className="relative text-white hover:text-purple-200 p-2 rounded-full transition-colors"
                            >
                                <SearchIcon />
                            </button>
                            <form
                                onSubmit={handleSearchSubmit}
                                className={`absolute top-full mt-2 left-1/2 -translate-x-1/2 w-64 transition-all duration-300 ease-in-out transform ${isSearchVisible ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4 pointer-events-none'}`}
                            >
                                <input
                                    type="text"
                                    value={localSearch}
                                    onChange={(e) => setLocalSearch(e.target.value)}
                                    placeholder="جستجو..."
                                    className="w-full p-2 bg-gray-800/80 backdrop-blur-xl border border-white/20 rounded-lg text-white focus:ring-2 focus:ring-[#667eea] focus:outline-none"
                                />
                            </form>
                        </div>
                        
                        <button
                            onClick={() => setIsCartOpen(true)}
                            className="relative text-white hover:text-purple-200 p-2 rounded-full transition-colors"
                        >
                            <ShoppingCartIcon />
                            {cartCount > 0 && (
                                <span className="absolute -top-1 -right-1 block h-5 w-5 rounded-full bg-red-500 text-white text-xs flex items-center justify-center">
                                    {cartCount}
                                </span>
                            )}
                        </button>
                        {user ? (
                            <div className="flex items-center space-x-3 space-x-reverse">
                                <button onClick={() => setPage('dashboard')} className="text-white/80 hover:text-white transition hidden sm:block">داشبورد</button>
                                <button onClick={() => setPage('admin')} className="text-white/80 hover:text-white transition hidden sm:block">پنل ادمین</button>
                                <UserIcon />
                                <button
                                    onClick={handleLogout}
                                    className="text-gray-300 hover:text-white bg-white/10 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                                >
                                    خروج
                                </button>
                            </div>
                        ) : (
                            <button
                                onClick={() => setPage('login')}
                                className="bg-white/10 px-4 py-2 rounded-xl text-white hover:bg-white/20 transition"
                            >
                                ورود | ثبت‌نام
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
};

const CartSidebar = ({ isOpen, onClose, setPage }) => {
    const { items, removeFromCart, updateQuantity, clearCart, cartTotal, cartCount } = useCart();
    const { token } = useAuth();
    const [checkingOut, setCheckingOut] = useState(false);

    const handleCheckout = async () => {
        if (!token) {
            alert("لطفاً برای تکمیل خرید وارد حساب کاربری خود شوید.");
            onClose();
            setPage('login');
            return;
        }
        setCheckingOut(true);
        try {
            const orderDetails = {
                items: items.map(item => ({
                    product_id: item.id,
                    quantity: item.quantity
                })),
                total: cartTotal,
            };
            await api.createOrder(orderDetails, token);
            clearCart();
            alert("سفارش شما با موفقیت ثبت شد!");
            onClose();
        } catch (err) {
            alert("پرداخت با خطا مواجه شد: " + err.message);
        } finally {
            setCheckingOut(false);
        }
    };

    return (
        <div className={`fixed inset-0 z-50 transition-opacity duration-300 ${isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}>
            <div className="absolute inset-0 bg-black/60" onClick={onClose}></div>
            <div className={`absolute top-0 left-0 h-full w-full max-w-md bg-gray-800/80 backdrop-blur-2xl shadow-2xl border-r border-white/20 flex flex-col transition-transform duration-300 ease-in-out ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}>
                <div className="flex items-center justify-between p-6 border-b border-white/20">
                    <h2 className="text-2xl font-bold text-white">سبد خرید</h2>
                    <button onClick={onClose} className="text-white/80 hover:text-white">
                        <CloseIcon />
                    </button>
                </div>
                {cartCount === 0 ? (
                    <div className="flex-grow flex flex-col items-center justify-center text-center p-6">
                        <p className="text-xl text-gray-300">سبد خرید شما خالی است.</p>
                        <button
                            onClick={() => {
                                onClose();
                                setPage('products');
                            }}
                            className="mt-6 bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white font-semibold py-2 px-6 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300"
                        >
                            مشاهده محصولات
                        </button>
                    </div>
                ) : (
                    <>
                        <div className="flex-grow p-6 overflow-y-auto space-y-4">
                            {items.map(item => (
                                <div key={item.id} className="flex items-center justify-between bg-white/5 p-4 rounded-lg">
                                    <div className="flex items-center space-x-4 space-x-reverse">
                                        <img src={item.imageUrl} alt={item.name} className="w-16 h-16 rounded-lg object-cover" />
                                        <div>
                                            <h3 className="text-md font-bold text-white">{item.name}</h3>
                                            <p className="text-gray-400 text-sm">{formatPrice(item.price)}</p>
                                        </div>
                                    </div>
                                    <div className="flex items-center space-x-3 space-x-reverse">
                                        <input
                                            type="number"
                                            value={item.quantity}
                                            onChange={(e) => updateQuantity(item.id, parseInt(e.target.value))}
                                            className="w-14 p-1 bg-white/10 rounded-md border border-white/20 text-white text-center"
                                            min="1"
                                        />
                                        <button
                                            onClick={() => removeFromCart(item.id)}
                                            className="text-red-500 hover:text-red-400 text-xs"
                                        >
                                            حذف
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                        <div className="p-6 border-t border-white/20">
                            <div className="flex justify-between items-center mb-4">
                                <span className="text-xl text-white font-bold">مجموع:</span>
                                <span className="text-2xl text-white font-black">{formatPrice(cartTotal)}</span>
                            </div>
                            <button
                                onClick={handleCheckout}
                                disabled={checkingOut}
                                className="w-full bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white font-semibold py-3 rounded-lg shadow-lg hover:shadow-xl transition disabled:opacity-50"
                            >
                                {checkingOut ? 'در حال پردازش...' : 'تکمیل خرید'}
                            </button>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

const HomePage = ({ setPage, setSelectedProductId, setSelectedPostId }) => {
    const [products, setProducts] = useState([]);
    const [posts, setPosts] = useState([]);
    const [loadingProducts, setLoadingProducts] = useState(true);
    const [loadingPosts, setLoadingPosts] = useState(true);
    const [errorProducts, setErrorProducts] = useState('');
    const [errorPosts, setErrorPosts] = useState('');

    useEffect(() => {
        // بارگذاری محصولات ویژه
        api.getProducts()
            .then(data => setProducts(data.slice(0, 4)))
            .catch(err => setErrorProducts(err.message))
            .finally(() => setLoadingProducts(false));

        // بارگذاری آخرین مطالب وبلاگ
        api.getBlogPosts()
            .then(data => setPosts(data.slice(0, 3)))
            .catch(err => setErrorPosts(err.message))
            .finally(() => setLoadingPosts(false));
    }, []);
    
    const handleProductClick = (id) => {
        setSelectedProductId(id);
        setPage('productDetail');
    };

    const handlePostClick = (id) => {
        setSelectedPostId(id);
        setPage('blogPost');
    };

    return (
        <div>
            {/* Hero Section */}
            <section className="py-20 md:py-32">
                <div className="container mx-auto px-4 text-center">
                    <h1 className="text-4xl md:text-7xl font-bold text-white mb-6">
                        <span className="gradient-text">فروشگاه iShop</span>
                    </h1>
                    <p className="text-xl md:text-2xl text-white/90 mb-10 max-w-3xl mx-auto">
                        خرید آنلاین محصولات اورجینال با بهترین قیمت‌ها. آینده را امروز تجربه کنید.
                    </p>
                </div>
            </section>

            {/* Featured Products */}
            <section className="py-10 md:py-20">
                <div className="container mx-auto px-4">
                    <h2 className="text-3xl md:text-5xl font-bold text-white mb-12 text-center">محصولات ویژه</h2>
                    {loadingProducts ? (
                        <div className="text-center text-white">در حال بارگذاری محصولات...</div>
                    ) : errorProducts ? (
                        <div className="text-center text-red-400">خطا در بارگذاری محصولات: {errorProducts}</div>
                    ) : products.length > 0 ? (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
                            {products.map(product => (
                                <div
                                    key={product.id}
                                    onClick={() => handleProductClick(product.id)}
                                    className="bg-white/10 backdrop-blur-md rounded-2xl shadow-lg overflow-hidden group transition-all duration-300 hover:shadow-2xl hover:scale-105 border border-white/20 cursor-pointer"
                                >
                                    <div className="h-64 overflow-hidden">
                                        <img
                                            src={product.imageUrl}
                                            alt={product.name}
                                            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                                        />
                                    </div>
                                    <div className="p-6 text-right">
                                        <h3 className="text-xl font-bold text-white mb-2">{product.name}</h3>
                                        <p className="text-2xl font-black text-white">{formatPrice(product.price)}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center text-white">محصولی یافت نشد.</div>
                    )}
                    <div className="text-center mt-12">
                        <button
                            onClick={() => setPage('products')}
                            className="px-8 py-3 bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                        >
                            مشاهده تمام محصولات
                        </button>
                    </div>
                </div>
            </section>

            {/* Features */}
            <section className="py-10 md:py-20">
                <div className="container mx-auto px-4">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
                        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 transition-all duration-300 hover:scale-105 hover:shadow-xl">
                            <div className="w-16 h-16 bg-gradient-to-br from-[#667eea] to-[#764ba2] rounded-2xl flex items-center justify-center text-white mb-6 mx-auto">
                                <ShippingIcon />
                            </div>
                            <h3 className="text-white text-xl font-bold mb-4">ارسال سریع و رایگان</h3>
                            <p className="text-white/80">برای خریدهای بالای ۵۰۰ هزار تومان، ارسال کالا رایگان است.</p>
                        </div>
                        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 transition-all duration-300 hover:scale-105 hover:shadow-xl">
                            <div className="w-16 h-16 bg-gradient-to-br from-[#667eea] to-[#764ba2] rounded-2xl flex items-center justify-center text-white mb-6 mx-auto">
                                <ShieldIcon />
                            </div>
                            <h3 className="text-white text-xl font-bold mb-4">ضمانت اصالت کالا</h3>
                            <p className="text-white/80">تمامی محصولات اورجینال بوده و دارای ضمانت اصالت هستند.</p>
                        </div>
                        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 transition-all duration-300 hover:scale-105 hover:shadow-xl">
                            <div className="w-16 h-16 bg-gradient-to-br from-[#667eea] to-[#764ba2] rounded-2xl flex items-center justify-center text-white mb-6 mx-auto">
                                <SupportIcon />
                            </div>
                            <h3 className="text-white text-xl font-bold mb-4">پشتیبانی ۲۴/۷</h3>
                            <p className="text-white/80">تیم پشتیبانی ما همیشه آماده پاسخگویی به سوالات شماست.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Latest Blog Posts */}
            <section className="py-10 md:py-20">
                <div className="container mx-auto px-4">
                    <h2 className="text-3xl md:text-5xl font-bold text-white mb-12 text-center">آخرین مطالب وبلاگ</h2>
                    {loadingPosts ? (
                        <div className="text-center text-white">در حال بارگذاری مطالب...</div>
                    ) : errorPosts ? (
                        <div className="text-center text-red-400">خطا در بارگذاری مطالب: {errorPosts}</div>
                    ) : posts.length > 0 ? (
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                            {posts.map(post => (
                                <div
                                    key={post.id}
                                    onClick={() => handlePostClick(post.id)}
                                    className="bg-white/10 backdrop-blur-md rounded-2xl shadow-lg overflow-hidden group transition-all duration-300 hover:shadow-2xl hover:scale-105 border border-white/20 cursor-pointer"
                                >
                                    <div className="h-56 overflow-hidden">
                                        <img
                                            src={post.imageUrl}
                                            alt={post.title}
                                            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                                        />
                                    </div>
                                    <div className="p-6">
                                        <h3 className="text-xl font-bold text-white mb-2">{post.title}</h3>
                                        <p className="text-white/80 text-sm mb-4">{post.excerpt}</p>
                                        <span className="text-sm text-indigo-300">ادامه مطلب &larr;</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center text-white">مطلبی یافت نشد.</div>
                    )}
                </div>
            </section>
        </div>
    );
};

const ProductListPage = ({ setPage, setSelectedProductId, searchTerm }) => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [sortOption, setSortOption] = useState('default');

    useEffect(() => {
        api.getProducts()
            .then(setProducts)
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
    }, []);
    
    const filteredAndSortedProducts = useMemo(() => {
        let result = [...products];
        
        // فیلتر بر اساس جستجو
        if (searchTerm) {
            result = result.filter(p => 
                p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                p.description.toLowerCase().includes(searchTerm.toLowerCase())
            );
        }
        
        // مرتب‌سازی
        switch (sortOption) {
            case 'price-asc':
                result.sort((a, b) => a.price - b.price);
                break;
            case 'price-desc':
                result.sort((a, b) => b.price - a.price);
                break;
            case 'name-asc':
                result.sort((a, b) => a.name.localeCompare(b.name, 'fa'));
                break;
            default:
                break;
        }
        return result;
    }, [products, searchTerm, sortOption]);

    const handleProductClick = (id) => {
        setSelectedProductId(id);
        setPage('productDetail');
    };

    if (loading) return <div className="text-center py-10 text-white">در حال بارگذاری محصولات...</div>;
    if (error) return <div className="text-center py-10 text-red-400">خطا: {error}</div>;

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <h1 className="text-4xl font-extrabold text-white mb-4 tracking-tight text-center">تمام محصولات</h1>
            {searchTerm && (
                <p className="text-center text-lg text-white/80 mb-8">
                    نتایج جستجو برای: "{searchTerm}"
                </p>
            )}
            
            <div className="flex justify-end mb-8">
                <select
                    value={sortOption}
                    onChange={(e) => setSortOption(e.target.value)}
                    className="bg-white/10 border border-white/20 text-white rounded-lg p-2 focus:ring-2 focus:ring-[#667eea] focus:outline-none"
                >
                    <option value="default">مرتب‌سازی پیش‌فرض</option>
                    <option value="price-asc">ارزان‌ترین</option>
                    <option value="price-desc">گران‌ترین</option>
                    <option value="name-asc">بر اساس نام</option>
                </select>
            </div>

            {filteredAndSortedProducts.length > 0 ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
                    {filteredAndSortedProducts.map(product => (
                        <div
                            key={product.id}
                            className="bg-white/10 backdrop-blur-md rounded-2xl shadow-lg overflow-hidden group transition-all duration-300 hover:shadow-2xl hover:scale-105 border border-white/20"
                        >
                            <div className="h-64 overflow-hidden">
                                <img
                                    src={product.imageUrl}
                                    alt={product.name}
                                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                                />
                            </div>
                            <div className="p-6 text-right">
                                <h3 className="text-2xl font-bold text-white mb-2">{product.name}</h3>
                                <p className="text-gray-300 mb-4 h-12 overflow-hidden">
                                    {product.description.substring(0, 80)}...
                                </p>
                                <div className="flex justify-between items-center">
                                    <p className="text-2xl font-black text-white">{formatPrice(product.price)}</p>
                                    <button
                                        onClick={() => handleProductClick(product.id)}
                                        className="text-white bg-gradient-to-r from-[#667eea] to-[#764ba2] py-2 px-4 rounded-lg font-semibold hover:shadow-lg transition-all duration-300"
                                    >
                                        مشاهده جزئیات
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="text-center text-white text-2xl py-16">
                    <p>محصولی مطابق با فیلتر شما یافت نشد.</p>
                </div>
            )}
        </div>
    );
};

const ProductDetailPage = ({ productId, setPage }) => {
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [reviewText, setReviewText] = useState('');
    const [reviewRating, setReviewRating] = useState(5);
    const [submitting, setSubmitting] = useState(false);
    const { addToCart } = useCart();
    const { user, token } = useAuth();

    const fetchProduct = useCallback(() => {
        setLoading(true);
        api.getProductById(productId)
            .then(setProduct)
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
    }, [productId]);

    useEffect(() => {
        fetchProduct();
    }, [fetchProduct]);

    const handleReviewSubmit = async (e) => {
        e.preventDefault();
        if (!reviewText) return;
        
        setSubmitting(true);
        try {
            await api.submitReview({
                product_id: productId,
                rating: reviewRating,
                text: reviewText
            }, token);
            setReviewText('');
            setReviewRating(5);
            fetchProduct(); // Refresh product data to show new review
        } catch (err) {
            alert('ثبت نظر با خطا مواجه شد: ' + err.message);
        } finally {
            setSubmitting(false);
        }
    };
    
    if (loading) return <div className="text-center py-10 text-white">در حال بارگذاری جزئیات محصول...</div>;
    if (error) return <div className="text-center py-10 text-red-400">خطا: {error}</div>;
    if (!product) return null;

    return (
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <button
                onClick={() => setPage('products')}
                className="mb-8 text-indigo-300 hover:text-indigo-200"
            >
                &rarr; بازگشت به محصولات
            </button>
            
            <div className="bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl overflow-hidden border border-white/20">
                <div className="md:flex">
                    <div className="md:flex-shrink-0">
                        <img
                            className="h-64 w-full object-cover md:h-full md:w-80"
                            src={product.imageUrl}
                            alt={product.name}
                        />
                    </div>
                    <div className="p-8 flex flex-col justify-between">
                        <div>
                            <h1 className="text-4xl font-extrabold text-white tracking-tight">{product.name}</h1>
                            <p className="mt-4 text-gray-300">{product.description}</p>
                        </div>
                        <div className="mt-8">
                            <span className="text-5xl font-black text-white">{formatPrice(product.price)}</span>
                            <button
                                onClick={() => addToCart(product)}
                                className="mt-4 w-full bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white font-semibold py-3 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                            >
                                افزودن به سبد خرید
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div className="mt-12">
                <h2 className="text-3xl font-bold text-white mb-6">نظرات کاربران</h2>
                <div className="space-y-6">
                    {product.reviews && product.reviews.length > 0 ? (
                        product.reviews.map((review, index) => (
                            <div key={index} className="bg-white/10 p-6 rounded-xl border border-white/20">
                                <div className="flex items-center mb-2">
                                    <p className="font-semibold text-white ml-4">{review.author}</p>
                                    <div className="flex">
                                        {[...Array(5)].map((_, i) => (
                                            <svg
                                                key={i}
                                                className={`w-5 h-5 ${i < review.rating ? 'text-yellow-400' : 'text-gray-500'}`}
                                                fill="currentColor"
                                                viewBox="0 0 20 20"
                                            >
                                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                            </svg>
                                        ))}
                                    </div>
                                </div>
                                <p className="text-gray-300">{review.text}</p>
                            </div>
                        ))
                    ) : (
                        <p className="text-gray-400">هنوز نظری ثبت نشده است. شما اولین نفر باشید!</p>
                    )}
                </div>

                {user && (
                    <form onSubmit={handleReviewSubmit} className="mt-8 bg-white/10 p-6 rounded-xl border border-white/20">
                        <h3 className="text-xl font-semibold text-white mb-4">نظر خود را ثبت کنید</h3>
                        <div className="mb-4">
                            <label className="text-gray-300 block mb-2">امتیاز</label>
                            <div className="flex">
                                {[...Array(5)].map((_, i) => (
                                    <button
                                        type="button"
                                        key={i}
                                        onClick={() => setReviewRating(i + 1)}
                                    >
                                        <svg
                                            className={`w-7 h-7 ${i < reviewRating ? 'text-yellow-400' : 'text-gray-500'} hover:text-yellow-300 transition`}
                                            fill="currentColor"
                                            viewBox="0 0 20 20"
                                        >
                                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                        </svg>
                                    </button>
                                ))}
                            </div>
                        </div>
                        <textarea
                            value={reviewText}
                            onChange={(e) => setReviewText(e.target.value)}
                            className="w-full p-3 bg-white/20 rounded-lg border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-[#667eea] transition duration-300"
                            rows="4"
                            placeholder="نظر خود را بنویسید..."
                            required
                        ></textarea>
                        <button
                            type="submit"
                            disabled={submitting}
                            className="mt-4 bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white font-semibold py-2 px-6 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50"
                        >
                            {submitting ? 'در حال ثبت...' : 'ثبت نظر'}
                        </button>
                    </form>
                )}
            </div>
        </div>
    );
};

// --- صفحات استاتیک فوتر ---
const StaticPage = ({ title, children }) => (
    <div className="max-w-4xl mx-auto px-4 py-12 text-white">
        <div className="bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl p-8 md:p-12 border border-white/20">
            <h1 className="text-4xl font-bold mb-6 text-center">{title}</h1>
            <div className="space-y-4 text-lg text-white/90 leading-relaxed">
                {children}
            </div>
        </div>
    </div>
);

const FaqPage = () => (
    <StaticPage title="سوالات متداول">
        <p>این صفحه در حال ساخت است. به زودی سوالات متداول شما در اینجا قرار خواهد گرفت.</p>
    </StaticPage>
);

const TermsPage = () => (
    <StaticPage title="قوانین و مقررات">
        <p>این صفحه در حال ساخت است. به زودی قوانین و مقررات فروشگاه در اینجا قرار خواهد گرفت.</p>
    </StaticPage>
);

const GuidePage = () => (
    <StaticPage title="راهنمای خرید">
        <p>این صفحه در حال ساخت است. به زودی راهنمای کامل خرید از فروشگاه در اینجا قرار خواهد گرفت.</p>
    </StaticPage>
);

const ContactPage = () => (
    <StaticPage title="تماس با ما">
        <p>شما می‌توانید از طریق راه‌های زیر با ما در تماس باشید:</p>
        <ul className="list-disc list-inside mt-4 space-y-2">
            <li>آدرس: تهران، خیابان ولیعصر، برج آینده</li>
            <li>تلفن تماس: 021-12345678</li>
            <li>ایمیل: info@ishop.com</li>
        </ul>
    </StaticPage>
);

const UserDashboardPage = () => {
    const { user, token } = useAuth();
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        if (token) {
            api.getOrders(token)
                .then(setOrders)
                .catch(err => setError(err.message))
                .finally(() => setLoading(false));
        } else {
            setLoading(false);
        }
    }, [token]);

    const getStatusClass = (status) => {
        switch (status) {
            case 'تحویل داده شده':
                return 'bg-green-500/20 text-green-300';
            case 'در حال پردازش':
                return 'bg-yellow-500/20 text-yellow-300';
            case 'لغو شده':
                return 'bg-red-500/20 text-red-300';
            default:
                return 'bg-gray-500/20 text-gray-300';
        }
    };

    return (
        <div className="max-w-4xl mx-auto px-4 py-12 text-white">
            <h1 className="text-4xl font-bold mb-8 text-center">داشبورد کاربری</h1>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {/* Profile Card */}
                <div className="md:col-span-1 bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl p-6 border border-white/20 text-center">
                    <div className="w-16 h-16 mx-auto mb-4 text-white">
                        <UserIcon />
                    </div>
                    <h2 className="text-2xl font-bold">{user?.name}</h2>
                    <p className="text-white/80">{user?.email}</p>
                </div>

                {/* Order History */}
                <div className="md:col-span-2 bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl p-6 border border-white/20">
                    <h2 className="text-2xl font-bold mb-4">تاریخچه سفارشات</h2>
                    {loading ? (
                        <p>در حال بارگذاری سفارشات...</p>
                    ) : error ? (
                        <p className="text-red-400">خطا: {error}</p>
                    ) : (
                        <div className="space-y-4">
                            {orders.length > 0 ? orders.map(order => (
                                <div key={order.id} className="bg-white/5 p-4 rounded-lg">
                                    <div className="flex justify-between items-center">
                                        <div>
                                            <p className="font-bold">شماره سفارش: {order.id}</p>
                                            <p className="text-sm text-white/70">{formatDate(order.date)}</p>
                                        </div>
                                        <div className="text-left">
                                            <p className="font-bold">{formatPrice(order.total)}</p>
                                            <span className={`text-xs font-semibold px-2 py-1 rounded-full ${getStatusClass(order.status)}`}>
                                                {order.status}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            )) : (
                                <p>شما هنوز سفارشی ثبت نکرده‌اید.</p>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

const BlogPage = ({ setPage, setSelectedPostId }) => {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        api.getBlogPosts()
            .then(setPosts)
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
    }, []);

    const handlePostClick = (id) => {
        setSelectedPostId(id);
        setPage('blogPost');
    };

    return (
        <div className="max-w-4xl mx-auto px-4 py-12 text-white">
            <h1 className="text-4xl font-bold mb-8 text-center">وبلاگ iShop</h1>
            {loading ? (
                <p className="text-center">در حال بارگذاری مطالب...</p>
            ) : error ? (
                <p className="text-center text-red-400">خطا: {error}</p>
            ) : (
                <div className="space-y-8">
                    {posts.length > 0 ? posts.map(post => (
                        <div
                            key={post.id}
                            onClick={() => handlePostClick(post.id)}
                            className="bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl p-6 border border-white/20 flex flex-col md:flex-row gap-6 cursor-pointer hover:bg-white/20 transition-colors"
                        >
                            <img
                                src={post.imageUrl}
                                alt={post.title}
                                className="w-full md:w-1/3 h-48 object-cover rounded-lg"
                            />
                            <div className="flex flex-col">
                                <h2 className="text-2xl font-bold mb-2">{post.title}</h2>
                                <p className="text-sm text-white/70 mb-4">{post.date}</p>
                                <p className="text-white/90 flex-grow">{post.excerpt}</p>
                                <span className="text-indigo-300 mt-4 self-start">ادامه مطلب &larr;</span>
                            </div>
                        </div>
                    )) : (
                        <p className="text-center">مطلبی یافت نشد.</p>
                    )}
                </div>
            )}
        </div>
    );
};

const BlogPostPage = ({ postId, setPage }) => {
    const [post, setPost] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        api.getBlogPostById(postId)
            .then(setPost)
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
    }, [postId]);

    if (loading) return <div className="text-center py-10 text-white">در حال بارگذاری مطلب...</div>;
    if (error) return <div className="text-center py-10 text-red-400">خطا: {error}</div>;
    if (!post) return <div className="text-center py-10 text-white">مطلب مورد نظر یافت نشد.</div>;

    return (
        <div className="max-w-4xl mx-auto px-4 py-12 text-white">
            <button
                onClick={() => setPage('blog')}
                className="mb-8 text-indigo-300 hover:text-indigo-200"
            >
                &rarr; بازگشت به وبلاگ
            </button>
            <div className="bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl p-8 md:p-12 border border-white/20">
                <img
                    src={post.imageUrl}
                    alt={post.title}
                    className="w-full h-64 object-cover rounded-lg mb-8"
                />
                <h1 className="text-4xl font-bold mb-4">{post.title}</h1>
                <p className="text-sm text-white/70 mb-8">{post.date}</p>
                <div
                    className="text-lg text-white/90 leading-relaxed"
                    dangerouslySetInnerHTML={{ __html: post.content }}
                ></div>
            </div>
        </div>
    );
};

// --- Admin Panel Components ---
const AdminDashboardTab = () => {
    const [stats, setStats] = useState({
        products: 0,
        orders: 0,
        users: 0
    });
    const [loading, setLoading] = useState(true);
    const { token } = useAuth();

    useEffect(() => {
        // در صورت وجود API برای آمار، از آن استفاده کنید
        // در غیر این صورت می‌توان از تعداد آیتم‌های هر بخش استفاده کرد
        Promise.all([
            api.getProducts().catch(() => []),
            api.getOrders(token).catch(() => []),
            api.getUsers(token).catch(() => [])
        ]).then(([products, orders, users]) => {
            setStats({
                products: products.length,
                orders: orders.length,
                users: users.length
            });
        }).finally(() => {
            setLoading(false);
        });
    }, [token]);

    return (
        <div>
            <h2 className="text-3xl font-bold mb-6">داشبورد</h2>
            {loading ? (
                <p>در حال بارگذاری آمار...</p>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-white/5 p-6 rounded-lg text-center">
                        <p className="text-4xl font-bold">{stats.products}</p>
                        <p className="text-white/80">محصول</p>
                    </div>
                    <div className="bg-white/5 p-6 rounded-lg text-center">
                        <p className="text-4xl font-bold">{stats.orders}</p>
                        <p className="text-white/80">سفارش</p>
                    </div>
                    <div className="bg-white/5 p-6 rounded-lg text-center">
                        <p className="text-4xl font-bold">{stats.users}</p>
                        <p className="text-white/80">کاربر</p>
                    </div>
                </div>
            )}
        </div>
    );
};

const ProductManagementTab = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [showForm, setShowForm] = useState(false);
    const [editingProduct, setEditingProduct] = useState(null);
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        price: '',
        imageUrl: ''
    });
    const { token } = useAuth();

    const fetchProducts = useCallback(() => {
        api.getProducts()
            .then(setProducts)
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
    }, []);

    useEffect(() => {
        fetchProducts();
    }, [fetchProducts]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (editingProduct) {
                await api.updateProduct(editingProduct.id, {
                    ...formData,
                    price: parseInt(formData.price)
                }, token);
            } else {
                await api.addProduct({
                    ...formData,
                    price: parseInt(formData.price)
                }, token);
            }
            setFormData({ name: '', description: '', price: '', imageUrl: '' });
            setShowForm(false);
            setEditingProduct(null);
            fetchProducts();
        } catch (err) {
            alert('خطا: ' + err.message);
        }
    };

    const handleEdit = (product) => {
        setEditingProduct(product);
        setFormData({
            name: product.name,
            description: product.description,
            price: product.price.toString(),
            imageUrl: product.imageUrl
        });
        setShowForm(true);
    };

    const handleDelete = async (id) => {
        if (window.confirm('آیا از حذف این محصول اطمینان دارید؟')) {
            try {
                await api.deleteProduct(id, token);
                fetchProducts();
            } catch (err) {
                alert('خطا در حذف: ' + err.message);
            }
        }
    };

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold">مدیریت محصولات</h2>
                <button
                    onClick={() => setShowForm(true)}
                    className="bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white px-4 py-2 rounded-lg flex items-center gap-2"
                >
                    <PlusIcon />
                    افزودن محصول
                </button>
            </div>

            {showForm && (
                <div className="mb-8 bg-white/5 p-6 rounded-lg">
                    <h3 className="text-xl font-bold mb-4">
                        {editingProduct ? 'ویرایش محصول' : 'افزودن محصول جدید'}
                    </h3>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-sm font-bold mb-2">نام محصول</label>
                            <input
                                type="text"
                                value={formData.name}
                                onChange={(e) => setFormData({...formData, name: e.target.value})}
                                className="w-full p-2 bg-white/10 border border-white/20 rounded text-white"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-bold mb-2">توضیحات</label>
                            <textarea
                                value={formData.description}
                                onChange={(e) => setFormData({...formData, description: e.target.value})}
                                className="w-full p-2 bg-white/10 border border-white/20 rounded text-white h-24"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-bold mb-2">قیمت (تومان)</label>
                            <input
                                type="number"
                                value={formData.price}
                                onChange={(e) => setFormData({...formData, price: e.target.value})}
                                className="w-full p-2 bg-white/10 border border-white/20 rounded text-white"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-bold mb-2">URL تصویر</label>
                            <input
                                type="url"
                                value={formData.imageUrl}
                                onChange={(e) => setFormData({...formData, imageUrl: e.target.value})}
                                className="w-full p-2 bg-white/10 border border-white/20 rounded text-white"
                                required
                            />
                        </div>
                        <div className="flex gap-4">
                            <button
                                type="submit"
                                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
                            >
                                {editingProduct ? 'بروزرسانی' : 'افزودن'}
                            </button>
                            <button
                                type="button"
                                onClick={() => {
                                    setShowForm(false);
                                    setEditingProduct(null);
                                    setFormData({ name: '', description: '', price: '', imageUrl: '' });
                                }}
                                className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
                            >
                                لغو
                            </button>
                        </div>
                    </form>
                </div>
            )}

            {loading ? (
                <p>در حال بارگذاری محصولات...</p>
            ) : error ? (
                <p className="text-red-400">خطا: {error}</p>
            ) : (
                <div className="space-y-4">
                    {products.map(product => (
                        <div key={product.id} className="bg-white/5 p-4 rounded-lg flex items-center justify-between">
                            <div className="flex items-center gap-4">
                                <img src={product.imageUrl} alt={product.name} className="w-16 h-16 rounded object-cover" />
                                <div>
                                    <h3 className="font-bold">{product.name}</h3>
                                    <p className="text-sm text-white/70">{formatPrice(product.price)}</p>
                                </div>
                            </div>
                            <div className="flex gap-2">
                                <button
                                    onClick={() => handleEdit(product)}
                                    className="text-blue-400 hover:text-blue-300 p-2"
                                >
                                    <EditIcon />
                                </button>
                                <button
                                    onClick={() => handleDelete(product.id)}
                                    className="text-red-400 hover:text-red-300 p-2"
                                >
                                    <DeleteIcon />
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

const CategoryManagementTab = () => {
    const [categories, setCategories] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [showForm, setShowForm] = useState(false);
    const [editingCategory, setEditingCategory] = useState(null);
    const [formData, setFormData] = useState({
        name: '',
        description: ''
    });
    const { token } = useAuth();

    const fetchCategories = useCallback(() => {
        api.getCategories()
            .then(setCategories)
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
    }, []);

    useEffect(() => {
        fetchCategories();
    }, [fetchCategories]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (editingCategory) {
                await api.updateCategory(editingCategory.id, formData, token);
            } else {
                await api.addCategory(formData, token);
            }
            setFormData({ name: '', description: '' });
            setShowForm(false);
            setEditingCategory(null);
            fetchCategories();
        } catch (err) {
            alert('خطا: ' + err.message);
        }
    };

    const handleEdit = (category) => {
        setEditingCategory(category);
        setFormData({
            name: category.name,
            description: category.description
        });
        setShowForm(true);
    };

    const handleDelete = async (id) => {
        if (window.confirm('آیا از حذف این دسته‌بندی اطمینان دارید؟')) {
            try {
                await api.deleteCategory(id, token);
                fetchCategories();
            } catch (err) {
                alert('خطا در حذف: ' + err.message);
            }
        }
    };

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold">مدیریت دسته‌بندی‌ها</h2>
                <button
                    onClick={() => setShowForm(true)}
                    className="bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white px-4 py-2 rounded-lg flex items-center gap-2"
                >
                    <PlusIcon />
                    افزودن دسته‌بندی
                </button>
            </div>

            {showForm && (
                <div className="mb-8 bg-white/5 p-6 rounded-lg">
                    <h3 className="text-xl font-bold mb-4">
                        {editingCategory ? 'ویرایش دسته‌بندی' : 'افزودن دسته‌بندی جدید'}
                    </h3>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-sm font-bold mb-2">نام دسته‌بندی</label>
                            <input
                                type="text"
                                value={formData.name}
                                onChange={(e) => setFormData({...formData, name: e.target.value})}
                                className="w-full p-2 bg-white/10 border border-white/20 rounded text-white"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-bold mb-2">توضیحات</label>
                            <textarea
                                value={formData.description}
                                onChange={(e) => setFormData({...formData, description: e.target.value})}
                                className="w-full p-2 bg-white/10 border border-white/20 rounded text-white h-24"
                            />
                        </div>
                        <div className="flex gap-4">
                            <button
                                type="submit"
                                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
                            >
                                {editingCategory ? 'بروزرسانی' : 'افزودن'}
                            </button>
                            <button
                                type="button"
                                onClick={() => {
                                    setShowForm(false);
                                    setEditingCategory(null);
                                    setFormData({ name: '', description: '' });
                                }}
                                className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
                            >
                                لغو
                            </button>
                        </div>
                    </form>
                </div>
            )}

            {loading ? (
                <p>در حال بارگذاری دسته‌بندی‌ها...</p>
            ) : error ? (
                <p className="text-red-400">خطا: {error}</p>
            ) : (
                <div className="space-y-4">
                    {categories.length > 0 ? categories.map(category => (
                        <div key={category.id} className="bg-white/5 p-4 rounded-lg flex items-center justify-between">
                            <div>
                                <h3 className="font-bold">{category.name}</h3>
                                <p className="text-sm text-white/70">{category.description}</p>
                            </div>
                            <div className="flex gap-2">
                                <button
                                    onClick={() => handleEdit(category)}
                                    className="text-blue-400 hover:text-blue-300 p-2"
                                >
                                    <EditIcon />
                                </button>
                                <button
                                    onClick={() => handleDelete(category.id)}
                                    className="text-red-400 hover:text-red-300 p-2"
                                >
                                    <DeleteIcon />
                                </button>
                            </div>
                        </div>
                    )) : (
                        <p>دسته‌بندی‌ای یافت نشد.</p>
                    )}
                </div>
            )}
        </div>
    );
};

const OrderManagementTab = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const { token } = useAuth();

    const fetchOrders = useCallback(() => {
        api.getOrders(token)
            .then(setOrders)
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
    }, [token]);

    useEffect(() => {
        fetchOrders();
    }, [fetchOrders]);

    const getStatusClass = (status) => {
        switch (status) {
            case 'تحویل داده شده':
                return 'bg-green-500/20 text-green-300';
            case 'در حال پردازش':
                return 'bg-yellow-500/20 text-yellow-300';
            case 'لغو شده':
                return 'bg-red-500/20 text-red-300';
            default:
                return 'bg-gray-500/20 text-gray-300';
        }
    };

    return (
        <div>
            <h2 className="text-3xl font-bold mb-6">مدیریت سفارشات</h2>
            
            {loading ? (
                <p>در حال بارگذاری سفارشات...</p>
            ) : error ? (
                <p className="text-red-400">خطا: {error}</p>
            ) : (
                <div className="space-y-4">
                    {orders.length > 0 ? orders.map(order => (
                        <div key={order.id} className="bg-white/5 p-4 rounded-lg">
                            <div className="flex justify-between items-center mb-4">
                                <div>
                                    <h3 className="font-bold">شماره سفارش: {order.id}</h3>
                                    <p className="text-sm text-white/70">
                                        تاریخ: {formatDate(order.date)}
                                    </p>
                                    <p className="text-sm text-white/70">
                                        مشتری: {order.customer_name}
                                    </p>
                                </div>
                                <div className="text-left">
                                    <p className="font-bold">{formatPrice(order.total)}</p>
                                    <span className={`text-xs font-semibold px-2 py-1 rounded-full ${getStatusClass(order.status)}`}>
                                        {order.status}
                                    </span>
                                </div>
                            </div>
                            {order.items && (
                                <div className="text-sm text-white/70">
                                    <p>محصولات:</p>
                                    <ul className="list-disc list-inside">
                                        {order.items.map((item, index) => (
                                            <li key={index}>
                                                {item.product_name} - تعداد: {item.quantity}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    )) : (
                        <p>سفارشی یافت نشد.</p>
                    )}
                </div>
            )}
        </div>
    );
};

const UserManagementTab = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const { token } = useAuth();

    const fetchUsers = useCallback(() => {
        api.getUsers(token)
            .then(setUsers)
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
    }, [token]);

    useEffect(() => {
        fetchUsers();
    }, [fetchUsers]);

    const handleDelete = async (id) => {
        if (window.confirm('آیا از حذف این کاربر اطمینان دارید؟')) {
            try {
                await api.deleteUser(id, token);
                fetchUsers();
            } catch (err) {
                alert('خطا در حذف: ' + err.message);
            }
        }
    };

    return (
        <div>
            <h2 className="text-3xl font-bold mb-6">مدیریت کاربران</h2>
            
            {loading ? (
                <p>در حال بارگذاری کاربران...</p>
            ) : error ? (
                <p className="text-red-400">خطا: {error}</p>
            ) : (
                <div className="space-y-4">
                    {users.length > 0 ? users.map(user => (
                        <div key={user.id} className="bg-white/5 p-4 rounded-lg flex items-center justify-between">
                            <div>
                                <h3 className="font-bold">{user.name}</h3>
                                <p className="text-sm text-white/70">{user.email}</p>
                                <p className="text-xs text-white/50">
                                    تاریخ عضویت: {formatDate(user.created_at)}
                                </p>
                            </div>
                            <div className="flex gap-2">
                                <button
                                    onClick={() => handleDelete(user.id)}
                                    className="text-red-400 hover:text-red-300 p-2"
                                    disabled={user.is_admin}
                                >
                                    <DeleteIcon />
                                </button>
                            </div>
                        </div>
                    )) : (
                        <p>کاربری یافت نشد.</p>
                    )}
                </div>
            )}
        </div>
    );
};

const BlogManagementTab = () => {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [showForm, setShowForm] = useState(false);
    const [editingPost, setEditingPost] = useState(null);
    const [formData, setFormData] = useState({
        title: '',
        excerpt: '',
        content: '',
        imageUrl: ''
    });
    const { token } = useAuth();

    const fetchPosts = useCallback(() => {
        api.getBlogPosts()
            .then(setPosts)
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
    }, []);

    useEffect(() => {
        fetchPosts();
    }, [fetchPosts]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (editingPost) {
                await api.updateBlogPost(editingPost.id, formData, token);
            } else {
                await api.addBlogPost(formData, token);
            }
            setFormData({ title: '', excerpt: '', content: '', imageUrl: '' });
            setShowForm(false);
            setEditingPost(null);
            fetchPosts();
        } catch (err) {
            alert('خطا: ' + err.message);
        }
    };

    const handleEdit = (post) => {
        setEditingPost(post);
        setFormData({
            title: post.title,
            excerpt: post.excerpt,
            content: post.content,
            imageUrl: post.imageUrl
        });
        setShowForm(true);
    };

    const handleDelete = async (id) => {
        if (window.confirm('آیا از حذف این مطلب اطمینان دارید؟')) {
            try {
                await api.deleteBlogPost(id, token);
                fetchPosts();
            } catch (err) {
                alert('خطا در حذف: ' + err.message);
            }
        }
    };

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold">مدیریت وبلاگ</h2>
                <button
                    onClick={() => setShowForm(true)}
                    className="bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white px-4 py-2 rounded-lg flex items-center gap-2"
                >
                    <PlusIcon />
                    افزودن مطلب
                </button>
            </div>

            {showForm && (
                <div className="mb-8 bg-white/5 p-6 rounded-lg">
                    <h3 className="text-xl font-bold mb-4">
                        {editingPost ? 'ویرایش مطلب' : 'افزودن مطلب جدید'}
                    </h3>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-sm font-bold mb-2">عنوان</label>
                            <input
                                type="text"
                                value={formData.title}
                                onChange={(e) => setFormData({...formData, title: e.target.value})}
                                className="w-full p-2 bg-white/10 border border-white/20 rounded text-white"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-bold mb-2">خلاصه</label>
                            <textarea
                                value={formData.excerpt}
                                onChange={(e) => setFormData({...formData, excerpt: e.target.value})}
                                className="w-full p-2 bg-white/10 border border-white/20 rounded text-white h-24"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-bold mb-2">محتوا</label>
                            <textarea
                                value={formData.content}
                                onChange={(e) => setFormData({...formData, content: e.target.value})}
                                className="w-full p-2 bg-white/10 border border-white/20 rounded text-white h-48"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-bold mb-2">URL تصویر</label>
                            <input
                                type="url"
                                value={formData.imageUrl}
                                onChange={(e) => setFormData({...formData, imageUrl: e.target.value})}
                                className="w-full p-2 bg-white/10 border border-white/20 rounded text-white"
                                required
                            />
                        </div>
                        <div className="flex gap-4">
                            <button
                                type="submit"
                                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
                            >
                                {editingPost ? 'بروزرسانی' : 'افزودن'}
                            </button>
                            <button
                                type="button"
                                onClick={() => {
                                    setShowForm(false);
                                    setEditingPost(null);
                                    setFormData({ title: '', excerpt: '', content: '', imageUrl: '' });
                                }}
                                className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
                            >
                                لغو
                            </button>
                        </div>
                    </form>
                </div>
            )}

            {loading ? (
                <p>در حال بارگذاری مطالب...</p>
            ) : error ? (
                <p className="text-red-400">خطا: {error}</p>
            ) : (
                <div className="space-y-4">
                    {posts.length > 0 ? posts.map(post => (
                        <div key={post.id} className="bg-white/5 p-4 rounded-lg flex items-center justify-between">
                            <div className="flex items-center gap-4">
                                <img src={post.imageUrl} alt={post.title} className="w-16 h-16 rounded object-cover" />
                                <div>
                                    <h3 className="font-bold">{post.title}</h3>
                                    <p className="text-sm text-white/70">{post.excerpt}</p>
                                    <p className="text-xs text-white/50">{post.date}</p>
                                </div>
                            </div>
                            <div className="flex gap-2">
                                <button
                                    onClick={() => handleEdit(post)}
                                    className="text-blue-400 hover:text-blue-300 p-2"
                                >
                                    <EditIcon />
                                </button>
                                <button
                                    onClick={() => handleDelete(post.id)}
                                    className="text-red-400 hover:text-red-300 p-2"
                                >
                                    <DeleteIcon />
                                </button>
                            </div>
                        </div>
                    )) : (
                        <p>مطلبی یافت نشد.</p>
                    )}
                </div>
            )}
        </div>
    );
};

const AdminPanelPage = ({ setPage }) => {
    const [activeTab, setActiveTab] = useState('dashboard');

    const renderTabContent = () => {
        switch (activeTab) {
            case 'dashboard':
                return <AdminDashboardTab />;
            case 'products':
                return <ProductManagementTab />;
            case 'categories':
                return <CategoryManagementTab />;
            case 'orders':
                return <OrderManagementTab />;
            case 'users':
                return <UserManagementTab />;
            case 'blog':
                return <BlogManagementTab />;
            default:
                return <AdminDashboardTab />;
        }
    };

    const TabButton = ({ tabName, icon, label }) => (
        <button
            onClick={() => setActiveTab(tabName)}
            className={`flex items-center px-4 py-3 text-right w-full transition-colors duration-200 ${
                activeTab === tabName
                    ? 'bg-white/20 text-white'
                    : 'text-white/70 hover:bg-white/10 hover:text-white'
            }`}
        >
            {icon}
            {label}
        </button>
    );

    return (
        <div className="max-w-7xl mx-auto px-4 py-12 text-white">
            <h1 className="text-4xl font-bold mb-8 text-center">پنل مدیریت</h1>
            <div className="flex flex-col md:flex-row gap-8">
                <aside className="md:w-1/4">
                    <div className="bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl p-4 border border-white/20">
                        <TabButton tabName="dashboard" icon={<DashboardIcon />} label="داشبورد" />
                        <TabButton tabName="products" icon={<ProductsIcon />} label="مدیریت محصولات" />
                        <TabButton tabName="categories" icon={<CategoryIcon />} label="مدیریت دسته‌بندی" />
                        <TabButton tabName="orders" icon={<OrdersIcon />} label="مدیریت سفارشات" />
                        <TabButton tabName="users" icon={<UsersIcon />} label="مدیریت کاربران" />
                        <TabButton tabName="blog" icon={<BlogIcon />} label="مدیریت وبلاگ" />
                    </div>
                </aside>
                <main className="flex-1 bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl p-8 border border-white/20">
                    {renderTabContent()}
                </main>
            </div>
        </div>
    );
};

const Footer = ({setPage}) => {
    const [isVisible, setIsVisible] = useState(false);

    const toggleVisibility = () => {
        if (window.pageYOffset > 300) {
            setIsVisible(true);
        } else {
            setIsVisible(false);
        }
    };

    const scrollToTop = () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    };

    useEffect(() => {
        window.addEventListener('scroll', toggleVisibility);
        return () => window.removeEventListener('scroll', toggleVisibility);
    }, []);

    return (
        <footer className="bg-black/20 backdrop-blur-lg border-t border-white/20 py-12 mt-20">
            <div className="container mx-auto px-4">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-white/80">
                    <div>
                        <h3 className="text-white text-xl font-bold mb-4">iShop</h3>
                        <p>فروشگاه آنلاین محصولات اورجینال با بهترین قیمت و خدمات پس از فروش.</p>
                    </div>
                    <div>
                        <h4 className="text-white text-lg font-semibold mb-4">لینک‌های مفید</h4>
                        <ul className="space-y-2">
                            <li>
                                <button onClick={() => setPage('home')} className="hover:text-white transition">
                                    خانه
                                </button>
                            </li>
                            <li>
                                <button onClick={() => setPage('products')} className="hover:text-white transition">
                                    محصولات
                                </button>
                            </li>
                            <li>
                                <button onClick={() => setPage('blog')} className="hover:text-white transition">
                                    وبلاگ
                                </button>
                            </li>
                        </ul>
                    </div>
                    <div>
                        <h4 className="text-white text-lg font-semibold mb-4">خدمات مشتریان</h4>
                        <ul className="space-y-2">
                            <li>
                                <button onClick={() => setPage('faq')} className="hover:text-white transition">
                                    سوالات متداول
                                </button>
                            </li>
                            <li>
                                <button onClick={() => setPage('terms')} className="hover:text-white transition">
                                    قوانین و مقررات
                                </button>
                            </li>
                            <li>
                                <button onClick={() => setPage('guide')} className="hover:text-white transition">
                                    راهنمای خرید
                                </button>
                            </li>
                        </ul>
                    </div>
                    <div>
                        <h4 className="text-white text-lg font-semibold mb-4">تماس با ما</h4>
                        <ul className="space-y-2">
                            <li>
                                <button onClick={() => setPage('contact')} className="hover:text-white transition">
                                    ارتباط با ما
                                </button>
                            </li>
                            <li>تهران، خیابان ولیعصر</li>
                            <li>021-12345678</li>
                        </ul>
                    </div>
                </div>
                <div className="border-t border-white/20 mt-8 pt-8 text-center text-white/80">
                    <p>&copy; 2024 فروشگاه iShop. تمامی حقوق محفوظ است.</p>
                </div>
            </div>
            {isVisible && (
                <button
                    onClick={scrollToTop}
                    className="fixed bottom-6 left-6 w-12 h-12 bg-white/20 backdrop-blur-lg rounded-full flex items-center justify-center text-white text-xl z-50 hover:bg-white/30 transition-all"
                >
                    <ArrowUpIcon />
                </button>
            )}
        </footer>
    );
};

// --- کامپوننت اصلی اپلیکیشن ---
function AppContent() {
    const [page, setPage] = useState('home');
    const [selectedProductId, setSelectedProductId] = useState(null);
    const [selectedPostId, setSelectedPostId] = useState(null);
    const [isCartOpen, setIsCartOpen] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');
    const { user, loading } = useAuth();

    const CurrentPage = () => {
        // Protected routes
        if ((page === 'dashboard' || page === 'admin') && !loading && !user) {
            return <AuthPage setPage={setPage} />;
        }

        switch (page) {
            case 'home':
                return <HomePage setPage={setPage} setSelectedProductId={setSelectedProductId} setSelectedPostId={setSelectedPostId} />;
            case 'login':
                return <AuthPage setPage={setPage} />;
            case 'products':
                return <ProductListPage setPage={setPage} setSelectedProductId={setSelectedProductId} searchTerm={searchTerm} />;
            case 'productDetail':
                return <ProductDetailPage productId={selectedProductId} setPage={setPage} />;
            case 'dashboard':
                return <UserDashboardPage />;
            case 'admin':
                return <AdminPanelPage setPage={setPage} />;
            case 'blog':
                return <BlogPage setPage={setPage} setSelectedPostId={setSelectedPostId} />;
            case 'blogPost':
                return <BlogPostPage postId={selectedPostId} setPage={setPage} />;
            case 'faq':
                return <FaqPage />;
            case 'terms':
                return <TermsPage />;
            case 'guide':
                return <GuidePage />;
            case 'contact':
                return <ContactPage />;
            default:
                return <HomePage setPage={setPage} setSelectedProductId={setSelectedProductId} setSelectedPostId={setSelectedPostId} />;
        }
    };
    
    // The login page has its own full-screen layout
    if (page === 'login') {
        return (
            <div dir="rtl" lang="fa">
                <AuthPage setPage={setPage} />
            </div>
        );
    }

    // Main layout for all other pages
    return (
        <div dir="rtl" lang="fa" className="min-h-screen flex flex-col" style={{background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'}}>
            <Navbar setPage={setPage} setIsCartOpen={setIsCartOpen} setSearchTerm={setSearchTerm} />
            <CartSidebar isOpen={isCartOpen} onClose={() => setIsCartOpen(false)} setPage={setPage} />
            <main className="flex-grow">
                <CurrentPage />
            </main>
            <Footer setPage={setPage} />
        </div>
    );
}

export default function App() {
    return (
        <AuthProvider>
            <CartProvider>
                <GlobalStyles />
                <AppContent />
            </CartProvider>
        </AuthProvider>
    );
}