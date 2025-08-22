import { useForm } from "react-hook-form";
import Header from "@/components/layout/header";
import Footer from "@/components/layout/footer";
import CartSidebar from "@/components/cart-sidebar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
import { CONTACT_INFO } from "@/lib/constants";
import { MapPin, Phone, MessageSquare, Mail, Clock, Users, CheckCircle } from "lucide-react";

interface ContactFormData {
  name: string;
  email: string;
  subject: string;
  message: string;
}

export default function Contact() {
  const { toast } = useToast();
  const { register, handleSubmit, reset, setValue } = useForm<ContactFormData>();

  const onSubmit = (data: ContactFormData) => {
    console.log('Contact form data:', data);
    toast({
      title: "پیام ارسال شد",
      description: "پیام شما با موفقیت ارسال شد. به زودی با شما تماس خواهیم گرفت.",
    });
    reset();
  };

  const contactMethods = [
    {
      icon: MapPin,
      title: "آدرس",
      value: CONTACT_INFO.address,
      color: "bg-primary-500",
      testId: "contact-address"
    },
    {
      icon: Phone,
      title: "تلفن",
      value: CONTACT_INFO.phone,
      color: "bg-green-500",
      testId: "contact-phone",
      direction: "ltr" as const
    },
    {
      icon: MessageSquare,
      title: "تلگرام",
      value: CONTACT_INFO.telegram,
      color: "bg-blue-500",
      testId: "contact-telegram"
    },
    {
      icon: Mail,
      title: "ایمیل",
      value: CONTACT_INFO.email,
      color: "bg-red-500",
      testId: "contact-email"
    }
  ];

  const features = [
    {
      icon: Clock,
      title: "پاسخگویی سریع",
      description: "پاسخ به پیام‌های شما در کمتر از 24 ساعت"
    },
    {
      icon: Users,
      title: "تیم متخصص",
      description: "تیم پشتیبانی حرفه‌ای و با تجربه"
    },
    {
      icon: CheckCircle,
      title: "حل مشکل تضمینی",
      description: "حل قطعی مشکلات و سوالات شما"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <Header />
      <CartSidebar />
      
      <main className="pt-24">
        {/* Hero Section */}
        <section className="py-16 bg-white">
          <div className="container mx-auto px-4">
            <div className="text-center mb-12">
              <h1 className="text-4xl font-bold text-gray-800 mb-4" data-testid="contact-page-title">
                تماس با ما
              </h1>
              <p className="text-gray-600 max-w-2xl mx-auto text-lg">
                سوالی دارید؟ نظر یا پیشنهادی؟ ما همیشه آماده‌ی شنیدن صدای شما هستیم
              </p>
            </div>

            {/* Contact Methods */}
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
              {contactMethods.map((method, index) => (
                <Card key={index} className="hover:shadow-lg transition-shadow">
                  <CardContent className="p-6 text-center">
                    <div className={`w-16 h-16 ${method.color} rounded-2xl flex items-center justify-center mx-auto mb-4`}>
                      <method.icon className="text-white text-2xl" />
                    </div>
                    <h3 className="font-semibold text-lg mb-2">{method.title}</h3>
                    <p 
                      className="text-gray-600" 
                      dir={method.direction || "rtl"}
                      data-testid={method.testId}
                    >
                      {method.value}
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>

        {/* Contact Form & Info */}
        <section className="py-16 bg-gray-50">
          <div className="container mx-auto px-4">
            <div className="grid lg:grid-cols-2 gap-12">
              {/* Contact Form */}
              <Card className="glass">
                <CardContent className="p-8">
                  <h2 className="text-2xl font-semibold mb-6">پیام بگذارید</h2>
                  <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                    <div>
                      <label className="block text-gray-700 font-medium mb-2">
                        نام و نام خانوادگی *
                      </label>
                      <Input 
                        {...register("name", { required: true })}
                        className="w-full"
                        placeholder="نام کامل خود را وارد کنید"
                        data-testid="contact-form-name"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-gray-700 font-medium mb-2">
                        ایمیل *
                      </label>
                      <Input 
                        type="email" 
                        {...register("email", { required: true })}
                        className="w-full"
                        placeholder="example@domain.com"
                        data-testid="contact-form-email"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-gray-700 font-medium mb-2">
                        موضوع *
                      </label>
                      <Select onValueChange={(value) => setValue("subject", value)}>
                        <SelectTrigger className="w-full" data-testid="contact-form-subject">
                          <SelectValue placeholder="موضوع پیام خود را انتخاب کنید" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="technical">سوال فنی</SelectItem>
                          <SelectItem value="order">مشکل در سفارش</SelectItem>
                          <SelectItem value="partnership">پیشنهاد همکاری</SelectItem>
                          <SelectItem value="suggestion">پیشنهاد و انتقاد</SelectItem>
                          <SelectItem value="billing">مسائل مالی</SelectItem>
                          <SelectItem value="other">سایر موارد</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div>
                      <label className="block text-gray-700 font-medium mb-2">
                        پیام *
                      </label>
                      <Textarea 
                        rows={6} 
                        {...register("message", { required: true })}
                        className="w-full resize-none"
                        placeholder="پیام خود را با جزئیات بنویسید..."
                        data-testid="contact-form-message"
                      />
                    </div>
                    
                    <Button 
                      type="submit" 
                      className="w-full bg-primary-500 text-white py-3 text-lg font-semibold hover:bg-primary-600 transition-colors"
                      data-testid="contact-form-submit"
                    >
                      ارسال پیام
                    </Button>
                  </form>
                </CardContent>
              </Card>

              {/* Contact Info & Features */}
              <div className="space-y-8">
                {/* Working Hours */}
                <Card>
                  <CardContent className="p-6">
                    <h3 className="text-xl font-semibold mb-4 flex items-center">
                      <Clock className="text-primary-500 ml-3" />
                      ساعات کاری
                    </h3>
                    <div className="space-y-2 text-gray-600">
                      <div className="flex justify-between">
                        <span>شنبه تا چهارشنبه:</span>
                        <span>9:00 - 18:00</span>
                      </div>
                      <div className="flex justify-between">
                        <span>پنج‌شنبه:</span>
                        <span>9:00 - 13:00</span>
                      </div>
                      <div className="flex justify-between">
                        <span>جمعه:</span>
                        <span>تعطیل</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Features */}
                <div className="space-y-6">
                  {features.map((feature, index) => (
                    <div key={index} className="flex items-start space-x-4 space-x-reverse" data-testid={`contact-feature-${index}`}>
                      <div className="w-12 h-12 bg-primary-500 rounded-xl flex items-center justify-center flex-shrink-0">
                        <feature.icon className="text-white text-lg" />
                      </div>
                      <div>
                        <h4 className="text-lg font-semibold mb-2">{feature.title}</h4>
                        <p className="text-gray-600">{feature.description}</p>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Social Media */}
                <Card>
                  <CardContent className="p-6">
                    <h3 className="text-xl font-semibold mb-4">ما را دنبال کنید</h3>
                    <div className="flex space-x-4 space-x-reverse">
                      <Button 
                        className="w-12 h-12 bg-blue-600 rounded-xl hover:scale-105 transition-transform p-0"
                        data-testid="contact-social-telegram"
                      >
                        <MessageSquare className="h-5 w-5" />
                      </Button>
                      <Button 
                        className="w-12 h-12 bg-pink-600 rounded-xl hover:scale-105 transition-transform p-0"
                        data-testid="contact-social-instagram"
                      >
                        📷
                      </Button>
                      <Button 
                        className="w-12 h-12 bg-green-600 rounded-xl hover:scale-105 transition-transform p-0"
                        data-testid="contact-social-whatsapp"
                      >
                        <Phone className="h-5 w-5" />
                      </Button>
                    </div>
                    <p className="text-gray-600 text-sm mt-4">
                      از آخرین اخبار، تخفیف‌ها و محصولات جدید مطلع شوید
                    </p>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </section>

        {/* FAQ Section */}
        <section className="py-16 bg-white">
          <div className="container mx-auto px-4">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-800 mb-4">سوالات متداول</h2>
              <p className="text-gray-600">پاسخ سوالات رایج در اینجا</p>
            </div>

            <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
              <Card>
                <CardContent className="p-6">
                  <h3 className="font-semibold text-lg mb-3">چگونه سفارش ثبت کنم؟</h3>
                  <p className="text-gray-600">
                    محصولات مورد نظر را به سبد خرید اضافه کرده و مراحل خرید را تکمیل کنید.
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <h3 className="font-semibold text-lg mb-3">مدت زمان ارسال چقدر است؟</h3>
                  <p className="text-gray-600">
                    معمولاً بین 2 تا 5 روز کاری، بسته به موقعیت جغرافیایی شما.
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <h3 className="font-semibold text-lg mb-3">آیا امکان مرجوعی کالا وجود دارد؟</h3>
                  <p className="text-gray-600">
                    بله، تا 7 روز پس از تحویل امکان مرجوعی کالا وجود دارد.
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <h3 className="font-semibold text-lg mb-3">روش‌های پرداخت کدامند؟</h3>
                  <p className="text-gray-600">
                    پرداخت آنلاین، کارت به کارت و پرداخت در محل تحویل.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
}
