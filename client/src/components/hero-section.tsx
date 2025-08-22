import { Button } from "@/components/ui/button";
import { Link } from "wouter";

export default function HeroSection() {
  return (
    <section className="pt-24 pb-16 gradient-bg relative overflow-hidden">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="text-white space-y-6">
            <h2 className="text-5xl md:text-6xl font-bold leading-tight">
              آیشاپ
              <span className="block text-yellow-300">فروشگاه آنلاین</span>
            </h2>
            <p className="text-xl text-gray-200 leading-relaxed">
              پلتفرم فروشگاهی کامل با بهترین محصولات، قیمت‌های مناسب و تحویل سریع
            </p>
            <div className="flex space-x-4 space-x-reverse">
              <Link href="/products">
                <Button className="bg-white text-primary-600 px-8 py-3 rounded-xl font-semibold hover:scale-105 transition-transform" data-testid="browse-products">
                  مشاهده محصولات
                </Button>
              </Link>
              <Link href="/contact">
                <Button className="glass border-2 border-white text-white px-8 py-3 rounded-xl font-semibold hover:scale-105 transition-transform" data-testid="learn-more">
                  درباره ما
                </Button>
              </Link>
            </div>
            
            {/* Stats */}
            <div className="flex space-x-8 space-x-reverse pt-8">
              <div className="text-center">
                <div className="text-2xl font-bold" data-testid="stats-products">1000+</div>
                <div className="text-sm text-gray-200">محصول</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold" data-testid="stats-customers">5000+</div>
                <div className="text-sm text-gray-200">مشتری</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold" data-testid="stats-orders">10000+</div>
                <div className="text-sm text-gray-200">سفارش</div>
              </div>
            </div>
          </div>
          
          <div className="relative">
            <img 
              src="https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&h=600" 
              alt="Modern shopping and ecommerce concept" 
              className="rounded-2xl shadow-2xl floating-animation" 
              data-testid="hero-image"
            />
            
            {/* Floating Cards */}
            <div className="absolute -top-4 -right-4 glass p-4 rounded-xl text-white floating-animation" style={{animationDelay: '0.5s'}}>
              <div className="text-2xl mb-2">🚚</div>
              <div className="text-sm font-semibold">تحویل سریع</div>
            </div>
            
            <div className="absolute -bottom-4 -left-4 glass p-4 rounded-xl text-white floating-animation" style={{animationDelay: '1s'}}>
              <div className="text-2xl mb-2">🛡️</div>
              <div className="text-sm font-semibold">خرید امن</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
