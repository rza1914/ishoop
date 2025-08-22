import { Minus, Plus, Trash2, X } from "lucide-react";
import { useCart } from "@/hooks/use-cart";
import { Button } from "@/components/ui/button";

export default function CartSidebar() {
  const { items, isOpen, removeItem, updateQuantity, closeCart, total, clearCart } = useCart();

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black bg-opacity-50 z-40"
        onClick={closeCart}
        data-testid="cart-backdrop"
      />
      
      {/* Sidebar */}
      <div className="fixed inset-y-0 left-0 w-96 bg-white shadow-2xl z-50 transform transition-transform duration-300">
        <div className="h-full flex flex-col">
          {/* Cart Header */}
          <div className="p-6 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-semibold">سبد خرید</h3>
              <Button 
                onClick={closeCart}
                className="text-gray-400 hover:text-gray-600 p-2"
                data-testid="cart-close"
              >
                <X className="h-5 w-5" />
              </Button>
            </div>
          </div>
          
          {/* Cart Items */}
          <div className="flex-1 overflow-y-auto p-6">
            {items.length === 0 ? (
              <div className="text-center text-gray-500 mt-8" data-testid="empty-cart">
                <p>سبد خرید خالی است</p>
              </div>
            ) : (
              <div className="space-y-4">
                {items.map((item) => (
                  <div 
                    key={item.id}
                    className="flex items-center space-x-4 space-x-reverse p-4 border border-gray-200 rounded-lg"
                    data-testid={`cart-item-${item.id}`}
                  >
                    <img 
                      src={item.imageUrl || "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&h=100"} 
                      alt={item.name} 
                      className="w-16 h-16 object-cover rounded-lg" 
                    />
                    <div className="flex-1">
                      <h4 className="font-medium" data-testid={`cart-item-name-${item.id}`}>
                        {item.name}
                      </h4>
                      <p className="text-gray-600 text-sm" data-testid={`cart-item-price-${item.id}`}>
                        {item.price}
                      </p>
                      <div className="flex items-center space-x-2 space-x-reverse mt-2">
                        <Button 
                          onClick={() => updateQuantity(item.id, item.quantity - 1)}
                          className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center p-0"
                          data-testid={`decrease-quantity-${item.id}`}
                        >
                          <Minus className="h-3 w-3" />
                        </Button>
                        <span className="text-sm font-medium" data-testid={`cart-item-quantity-${item.id}`}>
                          {item.quantity}
                        </span>
                        <Button 
                          onClick={() => updateQuantity(item.id, item.quantity + 1)}
                          className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center p-0"
                          data-testid={`increase-quantity-${item.id}`}
                        >
                          <Plus className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                    <Button 
                      onClick={() => removeItem(item.id)}
                      className="text-red-500 hover:text-red-700 p-2"
                      data-testid={`remove-item-${item.id}`}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </div>
          
          {/* Cart Footer */}
          {items.length > 0 && (
            <div className="p-6 border-t border-gray-200">
              <div className="flex justify-between items-center mb-4">
                <span className="font-semibold">مجموع:</span>
                <span className="text-2xl font-bold text-primary-600" data-testid="cart-total">
                  {total}
                </span>
              </div>
              <div className="space-y-2">
                <Button 
                  className="w-full bg-primary-500 text-white py-3 rounded-xl font-semibold hover:bg-primary-600 transition-colors"
                  data-testid="proceed-checkout"
                >
                  ادامه خرید
                </Button>
                <Button 
                  onClick={clearCart}
                  className="w-full bg-gray-500 text-white py-2 rounded-xl font-semibold hover:bg-gray-600 transition-colors"
                  data-testid="clear-cart"
                >
                  خالی کردن سبد
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
