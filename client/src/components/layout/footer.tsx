import { Link } from "wouter";
import { ShoppingBag, MessageSquare, Instagram, Phone } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useToast } from "@/hooks/use-toast";

export default function Footer() {
  const { toast } = useToast();

  const handleNewsletterSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    toast({
      title: "عضویت موفقیت‌آمیز",
      description: "شما با موفقیت در خبرنامه عضو شدید",
    });
  };

  return (
    <footer className="bg-gray-900 text-white py-16">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div>
            <div className="flex items-center space-x-3 space-x-reverse mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center">
                <ShoppingBag className="text-white text-lg" />
              </div>
              <h3 className="text-2xl font-bold">آیشاپ</h3>
            </div>
            <p className="text-gray-400 leading-relaxed mb-6">
              پلتفرم فروشگاهی کامل با رابط کاربری مدرن و امکانات پیشرفته
            </p>
            <div className="flex space-x-4 space-x-reverse">
              <Button className="w-10 h-10 bg-gray-800 rounded-lg hover:bg-primary-500 transition-colors p-0" data-testid="social-telegram">
                <MessageSquare className="h-4 w-4" />
              </Button>
              <Button className="w-10 h-10 bg-gray-800 rounded-lg hover:bg-primary-500 transition-colors p-0" data-testid="social-instagram">
                <Instagram className="h-4 w-4" />
              </Button>
              <Button className="w-10 h-10 bg-gray-800 rounded-lg hover:bg-primary-500 transition-colors p-0" data-testid="social-whatsapp">
                <Phone className="h-4 w-4" />
              </Button>
            </div>
          </div>
          
          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold mb-6">لینک‌های مفید</h4>
            <ul className="space-y-3">
              <li><Link href="/about" className="text-gray-400 hover:text-white transition-colors" data-testid="footer-about">درباره ما</Link></li>
              <li><Link href="/contact" className="text-gray-400 hover:text-white transition-colors" data-testid="footer-contact">تماس با ما</Link></li>
              <li><Link href="/faq" className="text-gray-400 hover:text-white transition-colors" data-testid="footer-faq">سوالات متداول</Link></li>
              <li><Link href="/terms" className="text-gray-400 hover:text-white transition-colors" data-testid="footer-terms">شرایط استفاده</Link></li>
              <li><Link href="/privacy" className="text-gray-400 hover:text-white transition-colors" data-testid="footer-privacy">حریم خصوصی</Link></li>
            </ul>
          </div>
          
          {/* Categories */}
          <div>
            <h4 className="text-lg font-semibold mb-6">دسته‌بندی‌ها</h4>
            <ul className="space-y-3">
              <li><Link href="/products?category=electronics" className="text-gray-400 hover:text-white transition-colors" data-testid="footer-electronics">الکترونیک</Link></li>
              <li><Link href="/products?category=fashion" className="text-gray-400 hover:text-white transition-colors" data-testid="footer-fashion">پوشاک</Link></li>
              <li><Link href="/products?category=accessories" className="text-gray-400 hover:text-white transition-colors" data-testid="footer-accessories">لوازم جانبی</Link></li>
              <li><Link href="/products?category=sports" className="text-gray-400 hover:text-white transition-colors" data-testid="footer-sports">ورزش</Link></li>
              <li><Link href="/products?category=beauty" className="text-gray-400 hover:text-white transition-colors" data-testid="footer-beauty">زیبایی</Link></li>
            </ul>
          </div>
          
          {/* Newsletter */}
          <div>
            <h4 className="text-lg font-semibold mb-6">خبرنامه</h4>
            <p className="text-gray-400 mb-4">از آخرین اخبار و تخفیف‌ها با خبر شوید</p>
            <form className="space-y-3" onSubmit={handleNewsletterSubmit}>
              <Input 
                type="email" 
                placeholder="ایمیل شما" 
                className="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-primary-500"
                required
                data-testid="newsletter-email"
              />
              <Button 
                type="submit" 
                className="w-full bg-primary-500 text-white py-3 rounded-lg font-semibold hover:bg-primary-600 transition-colors"
                data-testid="newsletter-submit"
              >
                عضویت
              </Button>
            </form>
          </div>
        </div>
        
        {/* Copyright */}
        <div className="border-t border-gray-800 mt-12 pt-8 text-center">
          <p className="text-gray-400">
            © 2025 آیشاپ. تمامی حقوق محفوظ است.
            <span className="text-gray-500 mx-2">|</span>
            Made with ❤️ by iShop Team
          </p>
        </div>
      </div>
    </footer>
  );
}
