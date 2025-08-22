import { useState } from "react";
import { Link, useLocation } from "wouter";
import { ShoppingBag, Search, ShoppingCart, User, Menu, X } from "lucide-react";
import { useCart } from "@/hooks/use-cart";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function Header() {
  const [location] = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { toggleCart, itemCount } = useCart();

  const isActive = (path: string) => location === path;

  return (
    <header className="fixed top-0 w-full z-50 glass">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-4 space-x-reverse">
            <div className="w-10 h-10 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center">
              <ShoppingBag className="text-white text-lg" />
            </div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
              آیشاپ
            </h1>
          </Link>

          {/* Navigation Menu */}
          <nav className="hidden md:flex items-center space-x-8 space-x-reverse">
            <Link 
              href="/" 
              className={`font-medium transition-colors ${
                isActive('/') ? 'text-primary-600' : 'text-gray-700 hover:text-primary-600'
              }`}
              data-testid="nav-home"
            >
              خانه
            </Link>
            <Link 
              href="/products" 
              className={`font-medium transition-colors ${
                isActive('/products') ? 'text-primary-600' : 'text-gray-700 hover:text-primary-600'
              }`}
              data-testid="nav-products"
            >
              محصولات
            </Link>
            <Link 
              href="/contact" 
              className={`font-medium transition-colors ${
                isActive('/contact') ? 'text-primary-600' : 'text-gray-700 hover:text-primary-600'
              }`}
              data-testid="nav-contact"
            >
              تماس با ما
            </Link>
            <Link 
              href="/admin" 
              className={`font-medium transition-colors ${
                isActive('/admin') ? 'text-primary-600' : 'text-gray-700 hover:text-primary-600'
              }`}
              data-testid="nav-admin"
            >
              پنل ادمین
            </Link>
          </nav>

          {/* User Actions */}
          <div className="flex items-center space-x-4 space-x-reverse">
            {/* Search */}
            <div className="relative hidden sm:block">
              <Input 
                type="text" 
                placeholder="جستجو محصولات..." 
                className="pl-10 pr-4 py-2 w-64 glass rounded-xl border-0 focus:ring-2 focus:ring-primary-500 text-sm"
                data-testid="search-input"
              />
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            </div>
            
            {/* Cart */}
            <Button 
              onClick={toggleCart}
              className="relative glass-dark p-3 rounded-xl hover:scale-105 transition-transform"
              data-testid="cart-toggle"
            >
              <ShoppingCart className="text-white h-5 w-5" />
              {itemCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {itemCount}
                </span>
              )}
            </Button>
            
            {/* User Menu */}
            <Button className="glass-dark p-3 rounded-xl hover:scale-105 transition-transform" data-testid="user-menu">
              <User className="text-white h-5 w-5" />
            </Button>
            
            {/* Mobile Menu Toggle */}
            <Button 
              className="md:hidden glass-dark p-3 rounded-xl"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              data-testid="mobile-menu-toggle"
            >
              {isMobileMenuOpen ? 
                <X className="text-white h-5 w-5" /> : 
                <Menu className="text-white h-5 w-5" />
              }
            </Button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden mt-4 glass rounded-2xl p-4">
            <nav className="flex flex-col space-y-4">
              <Link 
                href="/" 
                className={`font-medium transition-colors ${
                  isActive('/') ? 'text-primary-600' : 'text-gray-700 hover:text-primary-600'
                }`}
                onClick={() => setIsMobileMenuOpen(false)}
                data-testid="mobile-nav-home"
              >
                خانه
              </Link>
              <Link 
                href="/products" 
                className={`font-medium transition-colors ${
                  isActive('/products') ? 'text-primary-600' : 'text-gray-700 hover:text-primary-600'
                }`}
                onClick={() => setIsMobileMenuOpen(false)}
                data-testid="mobile-nav-products"
              >
                محصولات
              </Link>
              <Link 
                href="/contact" 
                className={`font-medium transition-colors ${
                  isActive('/contact') ? 'text-primary-600' : 'text-gray-700 hover:text-primary-600'
                }`}
                onClick={() => setIsMobileMenuOpen(false)}
                data-testid="mobile-nav-contact"
              >
                تماس با ما
              </Link>
              <Link 
                href="/admin" 
                className={`font-medium transition-colors ${
                  isActive('/admin') ? 'text-primary-600' : 'text-gray-700 hover:text-primary-600'
                }`}
                onClick={() => setIsMobileMenuOpen(false)}
                data-testid="mobile-nav-admin"
              >
                پنل ادمین
              </Link>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
}
