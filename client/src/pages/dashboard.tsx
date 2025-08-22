import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/hooks/use-toast';
import { User, Package, MapPin, Clock, Eye, Edit, Trash2, X } from 'lucide-react';
import { apiRequest } from '@/lib/queryClient';

interface UserProfile {
  id: string;
  username: string;
  email: string;
  firstName?: string;
  lastName?: string;
  phone?: string;
  profileImageUrl?: string;
  createdAt: string;
}

interface Order {
  id: string;
  customerName: string;
  customerEmail?: string;
  customerPhone?: string;
  total: string;
  status: string;
  items: string;
  createdAt: string;
}

export default function Dashboard() {
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const [editingProfile, setEditingProfile] = useState(false);
  const [profileData, setProfileData] = useState({
    firstName: '',
    lastName: '',
    phone: '',
    username: ''
  });

  // Get current user
  const { data: user, isLoading: userLoading } = useQuery<UserProfile>({
    queryKey: ['/api/auth/user'],
  });

  // Get user orders
  const { data: orders = [], isLoading: ordersLoading } = useQuery<Order[]>({
    queryKey: ['/api/orders', 'user', user?.id],
    enabled: !!user?.id,
  });

  // Update profile mutation
  const updateProfileMutation = useMutation({
    mutationFn: async (data: any) => {
      return apiRequest('PUT', `/api/users/${user?.id}`, data);
    },
    onSuccess: () => {
      toast({
        title: "پروفایل به‌روزرسانی شد",
        description: "اطلاعات شما با موفقیت ذخیره شد",
      });
      setEditingProfile(false);
      queryClient.invalidateQueries({ queryKey: ['/api/auth/user'] });
    },
    onError: () => {
      toast({
        title: "خطا",
        description: "خطا در به‌روزرسانی پروفایل",
        variant: "destructive",
      });
    },
  });

  const handleUpdateProfile = () => {
    updateProfileMutation.mutate(profileData);
  };

  const getStatusBadge = (status: string) => {
    const statusMap: Record<string, { label: string; variant: 'default' | 'secondary' | 'destructive' | 'outline' }> = {
      pending: { label: 'در انتظار', variant: 'outline' },
      processing: { label: 'در حال پردازش', variant: 'secondary' },
      shipped: { label: 'ارسال شده', variant: 'default' },
      delivered: { label: 'تحویل داده شده', variant: 'default' },
      cancelled: { label: 'لغو شده', variant: 'destructive' },
      paid: { label: 'پرداخت شده', variant: 'default' }
    };

    const statusInfo = statusMap[status] || { label: status, variant: 'outline' as const };
    return <Badge variant={statusInfo.variant}>{statusInfo.label}</Badge>;
  };

  const parseOrderItems = (itemsJson: string) => {
    try {
      return JSON.parse(itemsJson);
    } catch {
      return [];
    }
  };

  if (userLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
        <div className="container mx-auto px-4">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-300 rounded w-1/4 mb-6"></div>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="h-64 bg-gray-300 rounded"></div>
              <div className="h-64 bg-gray-300 rounded"></div>
              <div className="h-64 bg-gray-300 rounded"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
        <div className="container mx-auto px-4">
          <Card className="max-w-md mx-auto">
            <CardContent className="text-center py-8">
              <User className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h2 className="text-xl font-semibold mb-2">ورود به حساب کاربری</h2>
              <p className="text-gray-600 mb-4">برای دسترسی به پنل کاربری، وارد شوید</p>
              <Button onClick={() => window.location.href = '/login'}>
                ورود به حساب
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="container mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2" data-testid="dashboard-title">
            سلام {user.firstName || user.username}! 👋
          </h1>
          <p className="text-gray-600">به پنل کاربری آیشاپ خوش آمدید</p>
        </div>

        <Tabs defaultValue="profile" className="w-full">
          <TabsList className="grid w-full grid-cols-3 mb-6">
            <TabsTrigger value="profile" data-testid="profile-tab">
              <User className="h-4 w-4 ml-2" />
              پروفایل
            </TabsTrigger>
            <TabsTrigger value="orders" data-testid="orders-tab">
              <Package className="h-4 w-4 ml-2" />
              سفارشات
            </TabsTrigger>
            <TabsTrigger value="addresses" data-testid="addresses-tab">
              <MapPin className="h-4 w-4 ml-2" />
              آدرس‌ها
            </TabsTrigger>
          </TabsList>

          {/* Profile Tab */}
          <TabsContent value="profile">
            <Card className="dubai-card">
              <CardHeader>
                <div className="flex justify-between items-center">
                  <CardTitle className="flex items-center">
                    <User className="h-5 w-5 ml-2" />
                    اطلاعات پروفایل
                  </CardTitle>
                  <Button
                    variant="outline"
                    onClick={() => {
                      setEditingProfile(!editingProfile);
                      if (!editingProfile) {
                        setProfileData({
                          firstName: user.firstName || '',
                          lastName: user.lastName || '',
                          phone: user.phone || '',
                          username: user.username
                        });
                      }
                    }}
                    data-testid="edit-profile-btn"
                  >
                    {editingProfile ? (
                      <>
                        <X className="h-4 w-4 ml-2" />
                        لغو
                      </>
                    ) : (
                      <>
                        <Edit className="h-4 w-4 ml-2" />
                        ویرایش
                      </>
                    )}
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                {editingProfile ? (
                  <div className="space-y-4">
                    <div className="grid md:grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="firstName">نام</Label>
                        <Input
                          id="firstName"
                          value={profileData.firstName}
                          onChange={(e) => setProfileData(prev => ({ ...prev, firstName: e.target.value }))}
                          data-testid="input-first-name"
                        />
                      </div>
                      <div>
                        <Label htmlFor="lastName">نام خانوادگی</Label>
                        <Input
                          id="lastName"
                          value={profileData.lastName}
                          onChange={(e) => setProfileData(prev => ({ ...prev, lastName: e.target.value }))}
                          data-testid="input-last-name"
                        />
                      </div>
                    </div>
                    <div>
                      <Label htmlFor="phone">شماره تماس</Label>
                      <Input
                        id="phone"
                        value={profileData.phone}
                        onChange={(e) => setProfileData(prev => ({ ...prev, phone: e.target.value }))}
                        placeholder="مثال: 09123456789"
                        data-testid="input-phone"
                      />
                    </div>
                    <div>
                      <Label htmlFor="username">نام کاربری</Label>
                      <Input
                        id="username"
                        value={profileData.username}
                        onChange={(e) => setProfileData(prev => ({ ...prev, username: e.target.value }))}
                        data-testid="input-username"
                      />
                    </div>
                    <div className="flex space-x-2 space-x-reverse">
                      <Button
                        onClick={handleUpdateProfile}
                        disabled={updateProfileMutation.isPending}
                        data-testid="save-profile-btn"
                      >
                        {updateProfileMutation.isPending ? 'در حال ذخیره...' : 'ذخیره تغییرات'}
                      </Button>
                      <Button
                        variant="outline"
                        onClick={() => setEditingProfile(false)}
                        data-testid="cancel-edit-btn"
                      >
                        لغو
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <h3 className="font-semibold text-gray-700 mb-2">اطلاعات شخصی</h3>
                        <div className="space-y-2">
                          <p data-testid="display-name"><strong>نام:</strong> {user.firstName || 'تعین نشده'}</p>
                          <p data-testid="display-lastname"><strong>نام خانوادگی:</strong> {user.lastName || 'تعین نشده'}</p>
                          <p data-testid="display-username"><strong>نام کاربری:</strong> {user.username}</p>
                          <p data-testid="display-phone"><strong>شماره تماس:</strong> {user.phone || 'تعین نشده'}</p>
                        </div>
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-700 mb-2">اطلاعات حساب</h3>
                        <div className="space-y-2">
                          <p data-testid="display-email"><strong>ایمیل:</strong> {user.email}</p>
                          <p data-testid="display-join-date"><strong>تاریخ عضویت:</strong> {new Date(user.createdAt).toLocaleDateString('fa-IR')}</p>
                          <p><strong>وضعیت:</strong> <Badge variant="default">فعال</Badge></p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Orders Tab */}
          <TabsContent value="orders">
            <Card className="dubai-card">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Package className="h-5 w-5 ml-2" />
                  سفارشات من
                </CardTitle>
              </CardHeader>
              <CardContent>
                {ordersLoading ? (
                  <div className="text-center py-8">
                    <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4"></div>
                    <p className="text-gray-600">در حال بارگذاری سفارشات...</p>
                  </div>
                ) : orders.length === 0 ? (
                  <div className="text-center py-8" data-testid="no-orders">
                    <Package className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold mb-2">هنوز سفارشی ندارید</h3>
                    <p className="text-gray-600 mb-4">اولین خرید خود را از آیشاپ تجربه کنید!</p>
                    <Button onClick={() => window.location.href = '/shop'}>
                      شروع خرید
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {orders.map((order) => {
                      const items = parseOrderItems(order.items);
                      return (
                        <div
                          key={order.id}
                          className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                          data-testid={`order-${order.id}`}
                        >
                          <div className="flex justify-between items-start mb-3">
                            <div>
                              <h4 className="font-semibold" data-testid={`order-title-${order.id}`}>
                                سفارش #{order.id.substring(0, 8)}
                              </h4>
                              <p className="text-sm text-gray-600">
                                <Clock className="h-4 w-4 inline ml-1" />
                                {new Date(order.createdAt).toLocaleDateString('fa-IR')}
                              </p>
                            </div>
                            <div className="text-left">
                              {getStatusBadge(order.status)}
                              <p className="text-lg font-bold text-green-600 mt-1">
                                {parseFloat(order.total).toLocaleString('fa-IR')} تومان
                              </p>
                            </div>
                          </div>
                          
                          <div className="border-t pt-3">
                            <h5 className="font-medium mb-2">آیتم‌های سفارش:</h5>
                            <div className="space-y-1">
                              {items.map((item: any, index: number) => (
                                <div key={index} className="flex justify-between text-sm">
                                  <span>{item.name || 'محصول'}</span>
                                  <span>تعداد: {item.quantity || 1}</span>
                                </div>
                              ))}
                            </div>
                          </div>
                          
                          <div className="flex justify-between items-center mt-4 pt-3 border-t">
                            <div className="text-sm text-gray-600">
                              <p><strong>گیرنده:</strong> {order.customerName}</p>
                              {order.customerPhone && <p><strong>تماس:</strong> {order.customerPhone}</p>}
                            </div>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => {
                                // Navigate to order details
                                window.location.href = `/orders/${order.id}`;
                              }}
                              data-testid={`view-order-${order.id}`}
                            >
                              <Eye className="h-4 w-4 ml-1" />
                              جزئیات
                            </Button>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Addresses Tab */}
          <TabsContent value="addresses">
            <Card className="dubai-card">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <MapPin className="h-5 w-5 ml-2" />
                  آدرس‌های من
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center py-8" data-testid="addresses-placeholder">
                  <MapPin className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">مدیریت آدرس‌ها</h3>
                  <p className="text-gray-600 mb-4">این بخش به زودی اضافه خواهد شد</p>
                  <Button variant="outline" disabled>
                    <MapPin className="h-4 w-4 ml-2" />
                    افزودن آدرس جدید
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}