export default function FeaturesSection() {
  const features = [
    {
      icon: "🤖",
      title: "بات تلگرام هوشمند",
      description: "بات AI که محصولات را از پیام‌های forward شده تشخیص داده و به صورت خودکار به فروشگاه اضافه می‌کند",
      gradient: "from-primary-500 to-secondary-500"
    },
    {
      icon: "📊",
      title: "پنل ادمین حرفه‌ای",
      description: "داشبورد کامل با آمار فروش، مدیریت محصولات، سفارشات و کاربران با نمودارهای تحلیلی",
      gradient: "from-green-500 to-emerald-500"
    },
    {
      icon: "📱",
      title: "طراحی ریسپانسیو",
      description: "تجربه کاربری عالی در تمام دستگاه‌ها با طراحی مدرن و گلاسمورفیزم",
      gradient: "from-orange-500 to-red-500"
    }
  ];

  return (
    <section className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h3 className="text-3xl font-bold text-gray-800 mb-4">چرا آیشاپ؟</h3>
          <p className="text-gray-600 max-w-2xl mx-auto">
            ما بهترین تجربه خرید آنلاین را با امکانات پیشرفته و خدمات باکیفیت ارائه می‌دهیم
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div 
              key={index}
              className="glass p-8 rounded-2xl hover:scale-105 transition-transform"
              data-testid={`feature-${index}`}
            >
              <div className={`w-16 h-16 bg-gradient-to-r ${feature.gradient} rounded-2xl flex items-center justify-center mb-6 text-2xl`}>
                {feature.icon}
              </div>
              <h4 className="text-xl font-semibold mb-4" data-testid={`feature-title-${index}`}>
                {feature.title}
              </h4>
              <p className="text-gray-600 leading-relaxed" data-testid={`feature-description-${index}`}>
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
