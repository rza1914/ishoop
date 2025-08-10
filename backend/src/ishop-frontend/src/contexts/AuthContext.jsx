// src/contexts/AuthContext.jsx - Updated with Real API
import React, { createContext, useContext, useState, useEffect } from 'react';
import * as api from '../api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('ishop_token'));
  const [loading, setLoading] = useState(true);

  // Check if user is logged in on app start
  useEffect(() => {
    const checkAuth = async () => {
      if (token) {
        try {
          const userData = await api.getCurrentUser(token);
          setUser(userData);
        } catch (error) {
          console.error('Auth check failed:', error);
          // Token is invalid, remove it
          localStorage.removeItem('ishop_token');
          setToken(null);
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, [token]);

  const login = async (credentials) => {
    try {
      setLoading(true);
      const response = await api.login(credentials);
      
      // Store token
      const newToken = response.access_token;
      localStorage.setItem('ishop_token', newToken);
      setToken(newToken);
      
      // Get user data
      const userData = await api.getCurrentUser(newToken);
      setUser(userData);
      
      return { success: true };
    } catch (error) {
      console.error('Login failed:', error);
      return { 
        success: false, 
        error: error.message || 'ورود ناموفق بود' 
      };
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData) => {
    try {
      setLoading(true);
      await api.register(userData);
      
      // After successful registration, log the user in
      const loginResult = await login({
        username: userData.email,
        password: userData.password
      });
      
      return loginResult;
    } catch (error) {
      console.error('Registration failed:', error);
      setLoading(false);
      return { 
        success: false, 
        error: error.message || 'ثبت‌نام ناموفق بود' 
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('ishop_token');
    setToken(null);
    setUser(null);
  };

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};