import { useQuery } from "@tanstack/react-query";
import { BarChart3, ShoppingCart, Users, Package } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export default function AdminDashboard() {
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['/api/stats'],
  });

  const { data: recentOrders, isLoading: ordersLoading } = useQuery({
    queryKey: ['/api/orders/recent'],
  });

  if (statsLoading || ordersLoading) {
    return (
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
            <p className="mt-4 text-gray-600">در حال بارگذاری...</p>
          </div>
        </div>
      </section>
    );
  }

  const statsData = stats || {
    totalSales: "125,000,000 تومان",
    totalOrders: 1234,
    totalUsers: 5678,
    totalProducts: 892
  };

  const ordersData = recentOrders || [];

  return (
    <section className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h3 className="text-3xl font-bold text-gray-800 mb-4">پنل ادمین حرفه‌ای</h3>
          <p className="text-gray-600 max-w-2xl mx-auto">مدیریت کامل فروشگاه با داشبورد پیشرفته و آمار دقیق</p>
        </div>
        
        {/* Dashboard Preview */}
        <div className="glass-dark rounded-3xl p-8 bg-gray-900">
          {/* Dashboard Header */}
          <div className="flex justify-between items-center mb-8 text-white">
            <div>
              <h4 className="text-2xl font-bold mb-2">داشبورد مدیریت</h4>
              <p className="text-gray-400">آمار کلی فروشگاه</p>
            </div>
            <div className="flex space-x-4 space-x-reverse">
              <Select defaultValue="7days">
                <SelectTrigger className="bg-gray-800 text-white border-gray-700" data-testid="time-range-selector">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="7days">7 روز گذشته</SelectItem>
                  <SelectItem value="30days">30 روز گذشته</SelectItem>
                  <SelectItem value="3months">3 ماه گذشته</SelectItem>
                </SelectContent>
              </Select>
              <Button className="bg-primary-500 text-white hover:bg-primary-600" data-testid="export-data">
                📥 خروجی
              </Button>
            </div>
          </div>
          
          {/* Stats Cards */}
          <div className="grid md:grid-cols-4 gap-6 mb-8">
            <div className="bg-gradient-to-r from-blue-500 to-blue-600 p-6 rounded-2xl text-white">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-blue-100 text-sm mb-1">کل فروش</p>
                  <p className="text-2xl font-bold" data-testid="admin-total-sales">{(statsData as any)?.totalSales || "۰ تومان"}</p>
                  <p className="text-blue-100 text-xs mt-2">+12% از ماه قبل</p>
                </div>
                <BarChart3 className="text-3xl text-blue-200" />
              </div>
            </div>
            
            <div className="bg-gradient-to-r from-green-500 to-green-600 p-6 rounded-2xl text-white">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-green-100 text-sm mb-1">سفارشات</p>
                  <p className="text-2xl font-bold" data-testid="admin-total-orders">{((statsData as any)?.totalOrders || 0).toLocaleString('fa-IR')}</p>
                  <p className="text-green-100 text-xs mt-2">+8% از ماه قبل</p>
                </div>
                <ShoppingCart className="text-3xl text-green-200" />
              </div>
            </div>
            
            <div className="bg-gradient-to-r from-purple-500 to-purple-600 p-6 rounded-2xl text-white">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-purple-100 text-sm mb-1">کاربران</p>
                  <p className="text-2xl font-bold" data-testid="admin-total-users">{((statsData as any)?.totalUsers || 0).toLocaleString('fa-IR')}</p>
                  <p className="text-purple-100 text-xs mt-2">+15% از ماه قبل</p>
                </div>
                <Users className="text-3xl text-purple-200" />
              </div>
            </div>
            
            <div className="bg-gradient-to-r from-orange-500 to-orange-600 p-6 rounded-2xl text-white">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-orange-100 text-sm mb-1">محصولات</p>
                  <p className="text-2xl font-bold" data-testid="admin-total-products">{(statsData as any)?.totalProducts || 0}</p>
                  <p className="text-orange-100 text-xs mt-2">+5% از ماه قبل</p>
                </div>
                <Package className="text-3xl text-orange-200" />
              </div>
            </div>
          </div>
          
          {/* Charts Area */}
          <div className="grid md:grid-cols-2 gap-8">
            {/* Sales Chart */}
            <div className="bg-gray-800 p-6 rounded-2xl">
              <h5 className="text-white text-lg font-semibold mb-4">نمودار فروش</h5>
              <div className="h-64 bg-gray-700 rounded-xl flex items-center justify-center">
                <p className="text-gray-400">نمودار فروش در اینجا نمایش داده می‌شود</p>
              </div>
            </div>
            
            {/* Recent Orders */}
            <div className="bg-gray-800 p-6 rounded-2xl">
              <h5 className="text-white text-lg font-semibold mb-4">سفارشات اخیر</h5>
              <div className="space-y-4">
                {(ordersData as any)?.length === 0 ? (
                  <div className="text-gray-400 text-center py-8">
                    سفارش اخیری موجود نیست
                  </div>
                ) : (
                  (ordersData as any)?.map((order: any, index: number) => (
                    <div key={index} className="flex justify-between items-center p-3 bg-gray-700 rounded-lg" data-testid={`recent-order-${index}`}>
                      <div>
                        <p className="text-white font-medium" data-testid={`order-customer-${index}`}>
                          {order.customerName}
                        </p>
                        <p className="text-gray-400 text-sm" data-testid={`order-product-${index}`}>
                          سفارش #{order.id.substring(0, 8)}
                        </p>
                      </div>
                      <div className="text-left">
                        <p className="text-green-400 font-semibold" data-testid={`order-amount-${index}`}>
                          {parseFloat(order.total).toLocaleString('fa-IR')} تومان
                        </p>
                        <p className="text-gray-400 text-xs" data-testid={`order-time-${index}`}>
                          {new Date(order.createdAt).toLocaleDateString('fa-IR')}
                        </p>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
