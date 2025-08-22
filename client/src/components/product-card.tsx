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

  const badgeColors = {
    red: "bg-red-500",
    green: "bg-green-500", 
    blue: "bg-blue-500"
  };

  return (
    <div className="bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow relative">
      {badge && (
        <div className={`absolute top-4 right-4 ${badgeColors[badgeColor]} text-white px-2 py-1 rounded-lg text-xs font-medium z-10`}>
          {badge}
        </div>
      )}
      
      <img 
        src={product.imageUrl || "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&h=300"} 
        alt={product.name} 
        className="w-full h-48 object-cover" 
        data-testid={`product-image-${product.id}`}
      />
      
      <div className="p-6">
        <h4 className="font-semibold text-lg mb-2" data-testid={`product-name-${product.id}`}>
          {product.name}
        </h4>
        <p className="text-gray-600 text-sm mb-4" data-testid={`product-description-${product.id}`}>
          {product.description}
        </p>
        <div className="flex justify-between items-center">
          <div className="flex flex-col">
            <span className="text-2xl font-bold text-primary-600" data-testid={`product-price-${product.id}`}>
              {parseFloat(product.price).toLocaleString('fa-IR')} {product.currency}
            </span>
            {product.originalPrice && parseFloat(product.originalPrice) > parseFloat(product.price) && (
              <span className="text-sm text-gray-500 line-through" data-testid={`product-original-price-${product.id}`}>
                {parseFloat(product.originalPrice).toLocaleString('fa-IR')} {product.currency}
              </span>
            )}
          </div>
          <Button 
            onClick={handleAddToCart}
            className="bg-primary-500 text-white px-4 py-2 rounded-lg hover:bg-primary-600 transition-colors"
            data-testid={`add-to-cart-${product.id}`}
          >
            <Plus className="h-4 w-4 ml-2" />
            افزودن
          </Button>
        </div>
      </div>
    </div>
  );
}
