export default function TelegramBotDemo() {
  const botFeatures = [
    {
      icon: "🧠",
      title: "پردازش هوشمند",
      description: "تشخیص خودکار نام، قیمت و دسته‌بندی محصول از متن پیام",
      color: "bg-blue-500"
    },
    {
      icon: "💱",
      title: "تبدیل ارز خودکار",
      description: "تبدیل هوشمند قیمت از درهم به تومان با نرخ روز",
      color: "bg-green-500"
    },
    {
      icon: "🏷️",
      title: "تشخیص دسته‌بندی",
      description: "شناسایی دسته‌بندی محصول از روی هشتگ‌ها و کلمات کلیدی",
      color: "bg-purple-500"
    },
    {
      icon: "🛡️",
      title: "امنیت بالا",
      description: "دسترسی محدود به ادمین‌های مجاز و تأیید قبل از اضافه کردن",
      color: "bg-red-500"
    }
  ];

  return (
    <section className="py-16 bg-gradient-to-r from-blue-50 to-indigo-50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h3 className="text-3xl font-bold text-gray-800 mb-4">بات تلگرام هوشمند</h3>
          <p className="text-gray-600 max-w-2xl mx-auto">
            پارس خودکار محصولات از پیام‌های forward شده با قابلیت تبدیل ارز و تشخیص دسته‌بندی
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 gap-12 items-center">
          {/* Bot Demo Interface */}
          <div className="bg-white rounded-3xl shadow-2xl overflow-hidden">
            {/* Telegram Header */}
            <div className="bg-blue-500 p-4 text-white">
              <div className="flex items-center space-x-3 space-x-reverse">
                <div className="w-10 h-10 bg-blue-400 rounded-full flex items-center justify-center">
                  🤖
                </div>
                <div>
                  <h4 className="font-semibold">iShop Bot</h4>
                  <p className="text-xs text-blue-100">آنلاین</p>
                </div>
              </div>
            </div>
            
            {/* Chat Messages */}
            <div className="h-96 p-4 space-y-4 overflow-y-auto bg-gray-50" data-testid="bot-chat-area">
              {/* User Message (Forward) */}
              <div className="flex justify-end">
                <div className="bg-blue-500 text-white p-3 rounded-2xl rounded-br-sm max-w-xs">
                  <p className="text-xs text-blue-100 mb-1">Forwarded from: فروشگاه دبی</p>
                  <p>گردنبند قلب زیبا ۱ تکه</p>
                  <p>گردنبند آویز قلب تاجی مکعبی زیبا</p>
                  <p>💳 قیمت: 22درهم</p>
                  <p>#بدلیجات</p>
                </div>
              </div>
              
              {/* Bot Response */}
              <div className="flex justify-start">
                <div className="bg-white p-4 rounded-2xl rounded-bl-sm shadow-md max-w-sm">
                  <div className="flex items-center mb-2">
                    <span className="text-blue-500 ml-2">🤖</span>
                    <span className="font-semibold text-gray-800">محصول شناسایی شد!</span>
                  </div>
                  <div className="space-y-2 text-sm">
                    <p><span className="text-gray-600">📝 نام:</span> گردنبند قلب زیبا ۱ تکه</p>
                    <p><span className="text-gray-600">💰 قیمت:</span> <span className="text-green-600 font-bold">220,000 تومان</span></p>
                    <p><span className="text-gray-600">📂 دسته‌بندی:</span> لوازم جانبی</p>
                  </div>
                  <div className="flex space-x-2 space-x-reverse mt-4">
                    <button className="bg-green-500 text-white px-3 py-1 rounded-lg text-xs font-medium" data-testid="confirm-product">
                      ✅ اضافه کن
                    </button>
                    <button className="bg-gray-500 text-white px-3 py-1 rounded-lg text-xs font-medium" data-testid="edit-product">
                      ✏️ ویرایش
                    </button>
                  </div>
                </div>
              </div>
              
              {/* Bot Success Message */}
              <div className="flex justify-start">
                <div className="bg-green-100 p-3 rounded-2xl rounded-bl-sm max-w-xs">
                  <div className="flex items-center text-green-800">
                    <span className="ml-2">✅</span>
                    <span className="font-semibold">محصول با موفقیت اضافه شد!</span>
                  </div>
                  <p className="text-green-700 text-sm mt-1">محصول در دسته‌بندی "لوازم جانبی" قرار گرفت</p>
                </div>
              </div>
            </div>
            
            {/* Input Area */}
            <div className="p-4 border-t bg-white">
              <div className="flex space-x-2 space-x-reverse">
                <input 
                  type="text" 
                  placeholder="پیام forward کنید..." 
                  className="flex-1 p-3 border border-gray-300 rounded-full" 
                  disabled
                  data-testid="bot-input"
                />
                <button className="bg-blue-500 text-white p-3 rounded-full" disabled>
                  ✈️
                </button>
              </div>
            </div>
          </div>
          
          {/* Bot Features */}
          <div className="space-y-6">
            {botFeatures.map((feature, index) => (
              <div key={index} className="flex items-start space-x-4 space-x-reverse" data-testid={`bot-feature-${index}`}>
                <div className={`w-12 h-12 ${feature.color} rounded-xl flex items-center justify-center flex-shrink-0 text-white text-lg`}>
                  {feature.icon}
                </div>
                <div>
                  <h4 className="text-xl font-semibold mb-2" data-testid={`bot-feature-title-${index}`}>
                    {feature.title}
                  </h4>
                  <p className="text-gray-600" data-testid={`bot-feature-description-${index}`}>
                    {feature.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
