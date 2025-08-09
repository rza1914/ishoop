// src/api.js - Real API Service for iShop Frontend
const BASE_URL = 'http://localhost:8000';

// Helper function to get auth headers
const getAuthHeaders = (token) => ({
  'Content-Type': 'application/json',
  ...(token && { 'Authorization': `Bearer ${token}` })
});

// Helper function to handle API responses
const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }
  return response.json();
};

// Authentication API
export const login = async ({ username, password }) => {
  const response = await fetch(`${BASE_URL}/api/v1/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username,
      password
    })
  });
  return handleResponse(response);
};

export const register = async ({ email, password, full_name }) => {
  const response = await fetch(`${BASE_URL}/api/v1/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email,
      password,
      full_name
    })
  });
  return handleResponse(response);
};

// User API
export const getCurrentUser = async (token) => {
  const response = await fetch(`${BASE_URL}/api/v1/users/me`, {
    method: 'GET',
    headers: getAuthHeaders(token)
  });
  return handleResponse(response);
};

// Products API
export const getProducts = async () => {
  const response = await fetch(`${BASE_URL}/api/v1/products/`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  });
  return handleResponse(response);
};

export const getProductById = async (id) => {
  const response = await fetch(`${BASE_URL}/api/v1/products/${id}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  });
  return handleResponse(response);
};

// Reviews API
export const submitReview = async (productId, reviewData, token) => {
  const response = await fetch(`${BASE_URL}/api/v1/reviews/`, {
    method: 'POST',
    headers: getAuthHeaders(token),
    body: JSON.stringify({
      product_id: productId,
      rating: reviewData.rating,
      comment: reviewData.comment
    })
  });
  return handleResponse(response);
};

export const getProductReviews = async (productId) => {
  const response = await fetch(`${BASE_URL}/api/v1/reviews/?product_id=${productId}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  });
  return handleResponse(response);
};

// Orders API
export const createOrder = async (orderData, token) => {
  const response = await fetch(`${BASE_URL}/api/v1/orders/`, {
    method: 'POST',
    headers: getAuthHeaders(token),
    body: JSON.stringify({
      items: orderData.items.map(item => ({
        product_id: item.id,
        quantity: item.quantity,
        price: item.price
      })),
      total_amount: orderData.totalAmount || orderData.total_amount,
      shipping_address: orderData.shipping_address || orderData.shippingAddress
    })
  });
  return handleResponse(response);
};

export const getOrders = async (token) => {
  const response = await fetch(`${BASE_URL}/api/v1/orders/`, {
    method: 'GET',
    headers: getAuthHeaders(token)
  });
  return handleResponse(response);
};

// Export all functions as default for easy importing
export default {
  login,
  register,
  getCurrentUser,
  getProducts,
  getProductById,
  submitReview,
  getProductReviews,
  createOrder,
  getOrders
};