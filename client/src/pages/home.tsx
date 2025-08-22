import Header from "@/components/layout/header";
import Footer from "@/components/layout/footer";
import CartSidebar from "@/components/cart-sidebar";
import HeroSection from "@/components/hero-section";
import FeaturesSection from "@/components/features-section";
import AdminDashboard from "@/components/admin-dashboard";
import TelegramBotDemo from "@/components/telegram-bot-demo";
import ProductCard from "@/components/product-card";
import { useQuery } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Link } from "wouter";
import { useForm } from "react-hook-form";
import { useToast } from "@/hooks/use-toast";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { CONTACT_INFO } from "@/lib/constants";

export default function Home() {
  const { toast } = useToast();
  const { register, handleSubmit, reset } = useForm();
  
  const { data: products, isLoading } = useQuery({
    queryKey: ['/api/products'],
  });

  const onContactSubmit = (data: any) => {
    console.log('Contact form data:', data);
    toast({
      title: "پیام ارسال شد",
      description: "پیام شما با موفقیت ارسال شد. به زودی با شما تماس خواهیم گرفت.",
    });
    reset();
  };

  const featuredProducts = products ? products.slice(0, 4) : [];

  return (
    <div className="min-h-screen dubai-gradient">
      <Header />
      <CartSidebar />
      
      <main>
        <HeroSection />
        <FeaturesSection />
        
        {/* Products Showcase */}
        <section className="py-16 relative overflow-hidden">
          <div className="container mx-auto px-4">
            <div className="flex justify-between items-center mb-12">
              <div>
                <h3 className="text-4xl font-bold bg-gradient-to-r from-amber-400 via-yellow-500 to-amber-600 bg-clip-text text-transparent mb-2 floating-animation">محصولات پیشنهادی</h3>
                <p className="text-gray-700 font-medium">✨ بهترین محصولات با کیفیت الماسی ✨</p>
              </div>
              
              {/* Filters */}
              <div className="hidden md:flex space-x-4 space-x-reverse">
                <Button className="gold-gradient text-white px-8 py-3 rounded-2xl font-semibold shadow-lg hover:shadow-2xl pulse-glow" data-testid="filter-all">همه 💎</Button>
                <Button className="dubai-card text-gray-800 px-6 py-3 rounded-2xl font-medium" data-testid="filter-electronics">🔌 الکترونیک</Button>
                <Button className="dubai-card text-gray-800 px-6 py-3 rounded-2xl font-medium" data-testid="filter-fashion">👕 پوشاک</Button>
                <Button className="dubai-card text-gray-800 px-6 py-3 rounded-2xl font-medium" data-testid="filter-accessories">💍 لوازم جانبی</Button>
              </div>
            </div>
            
            {isLoading ? (
              <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
                {[1, 2, 3, 4].map(i => (
                  <div key={i} className="dubai-card rounded-3xl p-8 floating-animation">
                    <div className="animate-pulse">
                      <div className="bg-gradient-to-r from-gray-200 to-gray-300 h-56 rounded-2xl mb-6"></div>
                      <div className="bg-gradient-to-r from-gray-200 to-gray-300 h-5 rounded-xl mb-3"></div>
                      <div className="bg-gradient-to-r from-gray-200 to-gray-300 h-5 rounded-xl w-2/3"></div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
                {featuredProducts.map((product: any, index: number) => {
                  let badge = "";
                  let badgeColor: "red" | "green" | "blue" = "red";
                  
                  if (index === 0) {
                    badge = "جدید";
                    badgeColor = "red";
                  } else if (index === 1) {
                    badge = "پرفروش";
                    badgeColor = "green";
                  } else if (index === 3 && product.originalPrice) {
                    badge = "تخفیف ۲۰%";
                    badgeColor = "blue";
                  }

                  return (
                    <ProductCard 
                      key={product.id} 
                      product={product} 
                      badge={badge}
                      badgeColor={badgeColor}
                    />
                  );
                })}
              </div>
            )}
            
            <div className="text-center mt-16">
              <Link href="/products">
                <Button className="gold-gradient text-white px-12 py-4 rounded-2xl font-bold text-lg shadow-2xl hover:shadow-3xl pulse-glow transform hover:scale-105 transition-all duration-300" data-testid="view-all-products">
                  🛍️ مشاهده همه محصولات
                  <span className="mr-3 rtl-flip text-xl">←</span>
                </Button>
              </Link>
            </div>
          </div>
        </section>

        <AdminDashboard />
        <TelegramBotDemo />

        {/* Contact & Support */}
        <section className="py-20 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600/10 via-purple-600/10 to-pink-600/10"></div>
          <div className="container mx-auto px-4 relative z-10">
            <div className="text-center mb-16">
              <h3 className="text-5xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-6 floating-animation">✨ تماس با ما ✨</h3>
              <p className="text-gray-700 text-lg max-w-3xl mx-auto font-medium">🌟 سوالی دارید؟ تیم پشتیبانی حرفه‌ای ما ۲۴ ساعته در خدمت شما هستیم 🌟</p>
            </div>
            
            <div className="grid md:grid-cols-2 gap-12">
              {/* Contact Form */}
              <div className="glass p-8 rounded-2xl">
                <h4 className="text-xl font-semibold mb-6">پیام بگذارید</h4>
                <form className="space-y-4" onSubmit={handleSubmit(onContactSubmit)}>
                  <div>
                    <label className="block text-gray-700 font-medium mb-2">نام و نام خانوادگی</label>
                    <Input 
                      {...register("name", { required: true })}
                      className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent" 
                      data-testid="contact-name"
                    />
                  </div>
                  <div>
                    <label className="block text-gray-700 font-medium mb-2">ایمیل</label>
                    <Input 
                      type="email" 
                      {...register("email", { required: true })}
                      className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent" 
                      data-testid="contact-email"
                    />
                  </div>
                  <div>
                    <label className="block text-gray-700 font-medium mb-2">موضوع</label>
                    <Select>
                      <SelectTrigger className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent" data-testid="contact-subject">
                        <SelectValue placeholder="انتخاب موضوع" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="technical">سوال فنی</SelectItem>
                        <SelectItem value="order">مشکل در سفارش</SelectItem>
                        <SelectItem value="partnership">پیشنهاد همکاری</SelectItem>
                        <SelectItem value="other">سایر</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="block text-gray-700 font-medium mb-2">پیام</label>
                    <Textarea 
                      rows={4} 
                      {...register("message", { required: true })}
                      className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent" 
                      data-testid="contact-message"
                    />
                  </div>
                  <Button 
                    type="submit" 
                    className="w-full bg-primary-500 text-white py-3 rounded-xl font-semibold hover:bg-primary-600 transition-colors"
                    data-testid="contact-submit"
                  >
                    ارسال پیام
                  </Button>
                </form>
              </div>
              
              {/* Contact Info */}
              <div className="space-y-8">
                <div className="flex items-start space-x-4 space-x-reverse">
                  <div className="w-12 h-12 bg-primary-500 rounded-xl flex items-center justify-center flex-shrink-0">
                    📍
                  </div>
                  <div>
                    <h5 className="font-semibold text-lg mb-2">آدرس</h5>
                    <p className="text-gray-600" data-testid="contact-address">{CONTACT_INFO.address}</p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-4 space-x-reverse">
                  <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center flex-shrink-0">
                    📞
                  </div>
                  <div>
                    <h5 className="font-semibold text-lg mb-2">تلفن</h5>
                    <p className="text-gray-600" dir="ltr" data-testid="contact-phone">{CONTACT_INFO.phone}</p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-4 space-x-reverse">
                  <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center flex-shrink-0">
                    📱
                  </div>
                  <div>
                    <h5 className="font-semibold text-lg mb-2">تلگرام</h5>
                    <p className="text-gray-600" data-testid="contact-telegram">{CONTACT_INFO.telegram}</p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-4 space-x-reverse">
                  <div className="w-12 h-12 bg-red-500 rounded-xl flex items-center justify-center flex-shrink-0">
                    📧
                  </div>
                  <div>
                    <h5 className="font-semibold text-lg mb-2">ایمیل</h5>
                    <p className="text-gray-600" data-testid="contact-email-display">{CONTACT_INFO.email}</p>
                  </div>
                </div>
                
                {/* Social Media */}
                <div className="pt-6">
                  <h5 className="font-semibold text-lg mb-4">ما را دنبال کنید</h5>
                  <div className="flex space-x-4 space-x-reverse">
                    <Button className="w-10 h-10 bg-blue-600 rounded-lg hover:scale-105 transition-transform p-0" data-testid="social-telegram-follow">
                      📱
                    </Button>
                    <Button className="w-10 h-10 bg-pink-600 rounded-lg hover:scale-105 transition-transform p-0" data-testid="social-instagram-follow">
                      📷
                    </Button>
                    <Button className="w-10 h-10 bg-green-600 rounded-lg hover:scale-105 transition-transform p-0" data-testid="social-whatsapp-follow">
                      📞
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
}
