// src/pages/ProductDetailPage.jsx - Updated with Real API
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
import { useAuth } from '../contexts/AuthContext';
import * as api from '../api';

const ProductDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const { isAuthenticated, token } = useAuth();
  
  const [product, setProduct] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [reviewsLoading, setReviewsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [quantity, setQuantity] = useState(1);
  
  // Review form state
  const [reviewForm, setReviewForm] = useState({
    rating: 5,
    comment: ''
  });
  const [reviewSubmitting, setReviewSubmitting] = useState(false);
  const [showReviewForm, setShowReviewForm] = useState(false);

  // Fetch product details
  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        setError(null);
        const productData = await api.getProductById(id);
        setProduct(productData);
      } catch (err) {
        console.error('Failed to fetch product:', err);
        setError('خطا در بارگذاری محصول. لطفاً دوباره تلاش کنید.');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchProduct();
    }
  }, [id]);

  // Fetch product reviews
  useEffect(() => {
    const fetchReviews = async () => {
      try {
        setReviewsLoading(true);
        const reviewsData = await api.getProductReviews(id);
        setReviews(reviewsData);
      } catch (err) {
        console.error('Failed to fetch reviews:', err);
        // Don't show error for reviews, just log it
      } finally {
        setReviewsLoading(false);
      }
    };

    if (id) {
      fetchReviews();
    }
  }, [id]);

  const handleAddToCart = () => {
    if (product) {
      addToCart({
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.image_url || '/api/placeholder/300/300',
        quantity: quantity
      });
    }
  };

  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    
    if (!isAuthenticated) {
      navigate('/login', { 
        state: { 
          from: `/products/${id}`, 
          message: 'برای ثبت نظر لطفاً وارد شوید' 
        }
      });
      return;
    }

    setReviewSubmitting(true);
    
    try {
      await api.submitReview(id, reviewForm, token);
      
      // Reset form
      setReviewForm({ rating: 5, comment: '' });
      setShowReviewForm(false);
      
      // Refresh reviews
      const updatedReviews = await api.getProductReviews(id);
      setReviews(updatedReviews);
      
    } catch (err) {
      console.error('Failed to submit review:', err);
      alert('خطا در ثبت نظر. لطفاً دوباره تلاش کنید.');
    } finally {
      setReviewSubmitting(false);
    }
  };

  const renderStars = (rating, interactive = false, onChange = null) => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      stars.push(
        <button
          key={i}
          type={interactive ? "button" : undefined}
          onClick={interactive ? () => onChange(i) : undefined}
          className={`text-2xl ${interactive ? 'cursor-pointer hover:scale-110' : ''} transition-transform ${
            i <= rating ? 'text-yellow-400' : 'text-gray-300'
          }`}
          disabled={!interactive}
        >
          ★
        </button>
      );
    }
    return <div className="flex">{stars}</div>;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">در حال بارگذاری محصول...</p>
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-xl mb-4">⚠️</div>
          <p className="text-red-600 mb-4">{error || 'محصول یافت نشد'}</p>
          <button 
            onClick={() => navigate('/products')}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            بازگشت به فروشگاه
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          {/* Product Details */}
          <div className="bg-white/70 backdrop-blur-md rounded-2xl p-8 shadow-lg border border-white/20 mb-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Product Image */}
              <div>
                <img
                  src={product.image_url || '/api/placeholder/500/500'}
                  alt={product.name}
                  className="w-full rounded-2xl shadow-lg"
                />
              </div>
              
              {/* Product Info */}
              <div>
                <h1 className="text-3xl font-bold text-gray-800 mb-4">{product.name}</h1>
                
                <div className="flex items-center gap-4 mb-6">
                  <span className="text-3xl font-bold text-blue-600">
                    {product.price.toLocaleString()} تومان
                  </span>
                  {product.stock_quantity !== undefined && (
                    <span className={`px-3 py-1 rounded-full text-sm ${
                      product.stock_quantity > 0 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {product.stock_quantity > 0 ? `${product.stock_quantity} موجود` : 'ناموجود'}
                    </span>
                  )}
                </div>
                
                <p className="text-gray-600 mb-6 leading-relaxed">
                  {product.description}
                </p>
                
                {product.stock_quantity > 0 && (
                  <div className="flex items-center gap-4 mb-6">
                    <label className="text-gray-700 font-medium">تعداد:</label>
                    <select
                      value={quantity}
                      onChange={(e) => setQuantity(parseInt(e.target.value))}
                      className="px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      {[...Array(Math.min(product.stock_quantity, 10))].map((_, i) => (
                        <option key={i + 1} value={i + 1}>{i + 1}</option>
                      ))}
                    </select>
                  </div>
                )}
                
                <div className="flex gap-4">
                  <button
                    onClick={handleAddToCart}
                    disabled={product.stock_quantity === 0}
                    className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white py-3 px-6 rounded-xl text-lg font-medium transition-colors"
                  >
                    {product.stock_quantity === 0 ? 'ناموجود' : 'افزودن به سبد خرید'}
                  </button>
                  
                  <button
                    onClick={() => navigate('/products')}
                    className="bg-gray-100 hover:bg-gray-200 text-gray-800 py-3 px-6 rounded-xl transition-colors"
                  >
                    بازگشت
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Reviews Section */}
          <div className="bg-white/70 backdrop-blur-md rounded-2xl p-8 shadow-lg border border-white/20">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-800">نظرات کاربران</h2>
              <button
                onClick={() => setShowReviewForm(!showReviewForm)}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl transition-colors"
              >
                {showReviewForm ? 'لغو' : 'ثبت نظر'}
              </button>
            </div>

            {/* Review Form */}
            {showReviewForm && (
              <form onSubmit={handleReviewSubmit} className="bg-gray-50 rounded-xl p-6 mb-6">
                <div className="mb-4">
                  <label className="block text-gray-700 font-medium mb-2">امتیاز:</label>
                  {renderStars(reviewForm.rating, true, (rating) => 
                    setReviewForm(prev => ({ ...prev, rating }))
                  )}
                </div>
                
                <div className="mb-4">
                  <label className="block text-gray-700 font-medium mb-2">نظر شما:</label>
                  <textarea
                    value={reviewForm.comment}
                    onChange={(e) => setReviewForm(prev => ({ ...prev, comment: e.target.value }))}
                    rows="4"
                    className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="نظر خود را بنویسید..."
                    required
                  />
                </div>
                
                <button
                  type="submit"
                  disabled={reviewSubmitting}
                  className="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white px-6 py-2 rounded-xl transition-colors"
                >
                  {reviewSubmitting ? 'در حال ثبت...' : 'ثبت نظر'}
                </button>
              </form>
            )}

            {/* Reviews List */}
            {reviewsLoading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
                <p className="text-gray-600">در حال بارگذاری نظرات...</p>
              </div>
            ) : reviews.length > 0 ? (
              <div className="space-y-4">
                {reviews.map((review) => (
                  <div key={review.id} className="bg-gray-50 rounded-xl p-6">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                          <span className="text-blue-600 font-medium">
                            {review.user?.full_name?.charAt(0) || '؟'}
                          </span>
                        </div>
                        <div>
                          <h4 className="font-medium text-gray-800">
                            {review.user?.full_name || 'کاربر ناشناس'}
                          </h4>
                          {renderStars(review.rating)}
                        </div>
                      </div>
                      <span className="text-sm text-gray-500">
                        {new Date(review.created_at).toLocaleDateString('fa-IR')}
                      </span>
                    </div>
                    <p className="text-gray-700 leading-relaxed">{review.comment}</p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <div className="text-4xl mb-4">💭</div>
                <p className="text-gray-600">هنوز نظری ثبت نشده است. اولین نفر باشید!</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetailPage;