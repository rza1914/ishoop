import { Plus } from "lucide-react";
import { useCart } from "@/hooks/use-cart";
import { Button } from "@/components/ui/button";
import type { Product } from "@shared/schema";

interface ProductCardProps {
  product: Product;
  badge?: string;
  badgeColor?: "red" | "green" | "blue";
}

export default function ProductCard({ product, badge, badgeColor = "red" }: ProductCardProps) {
  const { addItem } = useCart();

  const handleAddToCart = () => {
    addItem({
      id: product.id,
      name: product.name,
      price: `${parseFloat(product.price).toLocaleString('fa-IR')} ${product.currency}`,
      imageUrl: product.imageUrl || ""
    });
  };

  return (
    <div className="dubai-card rounded-3xl overflow-hidden shadow-2xl group relative floating-animation">
      {badge && (
        <div className={`absolute top-6 right-6 z-10 px-4 py-2 rounded-2xl text-sm font-bold text-white backdrop-blur-md ${
          badgeColor === "red" ? "bg-gradient-to-r from-red-500 to-pink-500" :
          badgeColor === "green" ? "bg-gradient-to-r from-green-500 to-emerald-500" :
          "bg-gradient-to-r from-blue-500 to-indigo-500"
        } shadow-lg`} data-testid={`product-badge-${product.id}`}>
          {badge} ✨
        </div>
      )}
      
      <div className="relative aspect-square overflow-hidden rounded-t-3xl">
        <img 
          src={product.imageUrl || "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&h=400"} 
          alt={product.name}
          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
          data-testid={`product-image-${product.id}`}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/30 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-all duration-300"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-all duration-300"></div>
      </div>
      
      <div className="p-8 relative">
        <div className="absolute inset-0 bg-gradient-to-t from-white/20 to-transparent"></div>
        <div className="relative z-10">
          <h4 className="font-bold text-xl mb-3 bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent group-hover:from-blue-600 group-hover:to-purple-600 transition-all duration-300" data-testid={`product-name-${product.id}`}>
            {product.name}
          </h4>
          <p className="text-gray-600 text-sm mb-6 line-clamp-2 leading-relaxed" data-testid={`product-description-${product.id}`}>
            {product.description}
          </p>
          
          <div className="flex justify-between items-center">
            <div className="flex flex-col">
              <span className="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent" data-testid={`product-price-${product.id}`}>
                💎 {parseFloat(product.price).toLocaleString('fa-IR')} {product.currency}
              </span>
              {product.originalPrice && parseFloat(product.originalPrice) > parseFloat(product.price) && (
                <span className="text-sm text-gray-500 line-through mt-1" data-testid={`product-original-price-${product.id}`}>
                  {parseFloat(product.originalPrice).toLocaleString('fa-IR')} {product.currency}
                </span>
              )}
            </div>
            
            <Button 
              onClick={handleAddToCart}
              className="gold-gradient text-white px-6 py-3 rounded-2xl hover:shadow-lg transform hover:scale-105 transition-all duration-300 font-semibold"
              data-testid={`add-to-cart-${product.id}`}
            >
              <Plus className="h-5 w-5 ml-2" />
              🛒 افزودن
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}