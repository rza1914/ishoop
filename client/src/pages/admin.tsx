import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { queryClient } from "@/lib/queryClient";
import Header from "@/components/layout/header";
import Footer from "@/components/layout/footer";
import CartSidebar from "@/components/cart-sidebar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { insertProductSchema, insertCategorySchema } from "@shared/schema";
import { Plus, Edit, Trash2, BarChart3, ShoppingCart, Users, Package } from "lucide-react";
import { apiRequest } from "@/lib/queryClient";
import { z } from "zod";

type ProductFormData = z.infer<typeof insertProductSchema>;
type CategoryFormData = z.infer<typeof insertCategorySchema>;

export default function Admin() {
  const { toast } = useToast();
  const [selectedProduct, setSelectedProduct] = useState<any>(null);
  const [isProductModalOpen, setIsProductModalOpen] = useState(false);
  const [isCategoryModalOpen, setIsCategoryModalOpen] = useState(false);

  // Queries
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['/api/stats'],
  });

  const { data: products, isLoading: productsLoading } = useQuery({
    queryKey: ['/api/products'],
  });

  const { data: categories, isLoading: categoriesLoading } = useQuery({
    queryKey: ['/api/categories'],
  });

  const { data: orders, isLoading: ordersLoading } = useQuery({
    queryKey: ['/api/orders'],
  });

  const { data: recentOrders } = useQuery({
    queryKey: ['/api/orders/recent'],
  });

  // Product form
  const productForm = useForm<ProductFormData>({
    resolver: zodResolver(insertProductSchema),
    defaultValues: {
      name: "",
      description: "",
      price: "",
      categoryId: "",
      imageUrl: "",
      stock: 0,
      tags: [],
    },
  });

  // Category form
  const categoryForm = useForm<CategoryFormData>({
    resolver: zodResolver(insertCategorySchema),
    defaultValues: {
      name: "",
      nameEn: "",
      description: "",
    },
  });

  // Mutations
  const createProductMutation = useMutation({
    mutationFn: (data: ProductFormData) => apiRequest('POST', '/api/products', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/products'] });
      queryClient.invalidateQueries({ queryKey: ['/api/stats'] });
      toast({
        title: "محصول اضافه شد",
        description: "محصول جدید با موفقیت اضافه شد",
      });
      setIsProductModalOpen(false);
      productForm.reset();
    },
    onError: () => {
      toast({
        title: "خطا",
        description: "در اضافه کردن محصول خطایی رخ داد",
        variant: "destructive",
      });
    },
  });

  const updateProductMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<ProductFormData> }) =>
      apiRequest('PUT', `/api/products/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/products'] });
      toast({
        title: "محصول بروزرسانی شد",
        description: "تغییرات محصول با موفقیت ذخیره شد",
      });
      setIsProductModalOpen(false);
      setSelectedProduct(null);
      productForm.reset();
    },
    onError: () => {
      toast({
        title: "خطا",
        description: "در بروزرسانی محصول خطایی رخ داد",
        variant: "destructive",
      });
    },
  });

  const deleteProductMutation = useMutation({
    mutationFn: (id: string) => apiRequest('DELETE', `/api/products/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/products'] });
      queryClient.invalidateQueries({ queryKey: ['/api/stats'] });
      toast({
        title: "محصول حذف شد",
        description: "محصول با موفقیت حذف شد",
      });
    },
    onError: () => {
      toast({
        title: "خطا",
        description: "در حذف محصول خطایی رخ داد",
        variant: "destructive",
      });
    },
  });

  const createCategoryMutation = useMutation({
    mutationFn: (data: CategoryFormData) => apiRequest('POST', '/api/categories', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/categories'] });
      toast({
        title: "دسته‌بندی اضافه شد",
        description: "دسته‌بندی جدید با موفقیت اضافه شد",
      });
      setIsCategoryModalOpen(false);
      categoryForm.reset();
    },
    onError: () => {
      toast({
        title: "خطا",
        description: "در اضافه کردن دسته‌بندی خطایی رخ داد",
        variant: "destructive",
      });
    },
  });

  const updateOrderStatusMutation = useMutation({
    mutationFn: ({ id, status }: { id: string; status: string }) =>
      apiRequest('PUT', `/api/orders/${id}/status`, { status }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/orders'] });
      queryClient.invalidateQueries({ queryKey: ['/api/orders/recent'] });
      toast({
        title: "وضعیت سفارش بروزرسانی شد",
        description: "وضعیت سفارش با موفقیت تغییر کرد",
      });
    },
    onError: () => {
      toast({
        title: "خطا",
        description: "در بروزرسانی وضعیت سفارش خطایی رخ داد",
        variant: "destructive",
      });
    },
  });

  const handleProductSubmit = (data: ProductFormData) => {
    if (selectedProduct) {
      updateProductMutation.mutate({ id: selectedProduct.id, data });
    } else {
      createProductMutation.mutate(data);
    }
  };

  const handleCategorySubmit = (data: CategoryFormData) => {
    createCategoryMutation.mutate(data);
  };

  const openProductModal = (product?: any) => {
    if (product) {
      setSelectedProduct(product);
      productForm.reset({
        name: product.name,
        description: product.description,
        price: product.price,
        originalPrice: product.originalPrice,
        categoryId: product.categoryId,
        imageUrl: product.imageUrl,
        stock: product.stock,
        tags: product.tags || [],
      });
    } else {
      setSelectedProduct(null);
      productForm.reset();
    }
    setIsProductModalOpen(true);
  };

  if (statsLoading || productsLoading || categoriesLoading || ordersLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
        <Header />
        <CartSidebar />
        <main className="pt-24">
          <div className="container mx-auto px-4 py-16">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
              <p className="mt-4 text-gray-600">در حال بارگذاری پنل ادمین...</p>
            </div>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  const statsData = stats || {
    totalSales: "0 تومان",
    totalOrders: 0,
    totalUsers: 0,
    totalProducts: 0
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <Header />
      <CartSidebar />
      
      <main className="pt-24">
        {/* Header */}
        <section className="py-8 bg-white border-b">
          <div className="container mx-auto px-4">
            <h1 className="text-3xl font-bold text-gray-800" data-testid="admin-title">پنل مدیریت آیشاپ</h1>
            <p className="text-gray-600 mt-2">مدیریت کامل فروشگاه و محصولات</p>
          </div>
        </section>

        {/* Stats Cards */}
        <section className="py-8 bg-white">
          <div className="container mx-auto px-4">
            <div className="grid md:grid-cols-4 gap-6">
              <Card className="bg-gradient-to-r from-blue-500 to-blue-600 text-white">
                <CardContent className="p-6">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="text-blue-100 text-sm mb-1">کل فروش</p>
                      <p className="text-2xl font-bold" data-testid="admin-sales-stat">{(statsData as any)?.totalSales || "۰ تومان"}</p>
                      <p className="text-blue-100 text-xs mt-2">+12% از ماه قبل</p>
                    </div>
                    <BarChart3 className="text-3xl text-blue-200" />
                  </div>
                </CardContent>
              </Card>
              
              <Card className="bg-gradient-to-r from-green-500 to-green-600 text-white">
                <CardContent className="p-6">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="text-green-100 text-sm mb-1">سفارشات</p>
                      <p className="text-2xl font-bold" data-testid="admin-orders-stat">{((statsData as any)?.totalOrders || 0).toLocaleString('fa-IR')}</p>
                      <p className="text-green-100 text-xs mt-2">+8% از ماه قبل</p>
                    </div>
                    <ShoppingCart className="text-3xl text-green-200" />
                  </div>
                </CardContent>
              </Card>
              
              <Card className="bg-gradient-to-r from-purple-500 to-purple-600 text-white">
                <CardContent className="p-6">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="text-purple-100 text-sm mb-1">کاربران</p>
                      <p className="text-2xl font-bold" data-testid="admin-users-stat">{((statsData as any)?.totalUsers || 0).toLocaleString('fa-IR')}</p>
                      <p className="text-purple-100 text-xs mt-2">+15% از ماه قبل</p>
                    </div>
                    <Users className="text-3xl text-purple-200" />
                  </div>
                </CardContent>
              </Card>
              
              <Card className="bg-gradient-to-r from-orange-500 to-orange-600 text-white">
                <CardContent className="p-6">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="text-orange-100 text-sm mb-1">محصولات</p>
                      <p className="text-2xl font-bold" data-testid="admin-products-stat">{(statsData as any)?.totalProducts || 0}</p>
                      <p className="text-orange-100 text-xs mt-2">+5% از ماه قبل</p>
                    </div>
                    <Package className="text-3xl text-orange-200" />
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        {/* Management Tabs */}
        <section className="py-8">
          <div className="container mx-auto px-4">
            <Tabs defaultValue="products" className="space-y-6">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="products" data-testid="tab-products">محصولات</TabsTrigger>
                <TabsTrigger value="categories" data-testid="tab-categories">دسته‌بندی‌ها</TabsTrigger>
                <TabsTrigger value="orders" data-testid="tab-orders">سفارشات</TabsTrigger>
                <TabsTrigger value="analytics" data-testid="tab-analytics">آمار</TabsTrigger>
              </TabsList>

              {/* Products Tab */}
              <TabsContent value="products">
                <Card>
                  <CardHeader>
                    <div className="flex justify-between items-center">
                      <CardTitle>مدیریت محصولات</CardTitle>
                      <Button onClick={() => openProductModal()} data-testid="add-product-btn">
                        <Plus className="h-4 w-4 ml-2" />
                        افزودن محصول
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {products ? products.map((product: any) => (
                        <div key={product.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg" data-testid={`product-item-${product.id}`}>
                          <div className="flex items-center space-x-4 space-x-reverse">
                            <img 
                              src={product.imageUrl || "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&h=100"} 
                              alt={product.name}
                              className="w-16 h-16 object-cover rounded-lg"
                            />
                            <div>
                              <h4 className="font-semibold" data-testid={`product-name-${product.id}`}>{product.name}</h4>
                              <p className="text-gray-600 text-sm">{product.description}</p>
                              <p className="text-primary-600 font-semibold">{parseFloat(product.price).toLocaleString('fa-IR')} {product.currency}</p>
                            </div>
                          </div>
                          <div className="flex space-x-2 space-x-reverse">
                            <Button 
                              onClick={() => openProductModal(product)}
                              variant="outline"
                              size="sm"
                              data-testid={`edit-product-${product.id}`}
                            >
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button 
                              onClick={() => deleteProductMutation.mutate(product.id)}
                              variant="destructive"
                              size="sm"
                              data-testid={`delete-product-${product.id}`}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      )) : null}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Categories Tab */}
              <TabsContent value="categories">
                <Card>
                  <CardHeader>
                    <div className="flex justify-between items-center">
                      <CardTitle>مدیریت دسته‌بندی‌ها</CardTitle>
                      <Button onClick={() => setIsCategoryModalOpen(true)} data-testid="add-category-btn">
                        <Plus className="h-4 w-4 ml-2" />
                        افزودن دسته‌بندی
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {categories?.map((category) => (
                        <div key={category.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg" data-testid={`category-item-${category.id}`}>
                          <div>
                            <h4 className="font-semibold" data-testid={`category-name-${category.id}`}>{category.name}</h4>
                            <p className="text-gray-600 text-sm">{category.description}</p>
                            <p className="text-xs text-gray-500">{category.nameEn}</p>
                          </div>
                          <div className="text-sm text-gray-600">
                            {products?.filter(p => p.categoryId === category.id).length || 0} محصول
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Orders Tab */}
              <TabsContent value="orders">
                <Card>
                  <CardHeader>
                    <CardTitle>مدیریت سفارشات</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {orders?.map((order) => (
                        <div key={order.id} className="p-4 border border-gray-200 rounded-lg" data-testid={`order-item-${order.id}`}>
                          <div className="flex justify-between items-start mb-4">
                            <div>
                              <h4 className="font-semibold" data-testid={`order-customer-${order.id}`}>{order.customerName}</h4>
                              <p className="text-sm text-gray-600">{order.customerEmail}</p>
                              <p className="text-sm text-gray-600">{order.customerPhone}</p>
                            </div>
                            <div className="text-left">
                              <p className="font-semibold text-lg" data-testid={`order-total-${order.id}`}>
                                {parseFloat(order.total).toLocaleString('fa-IR')} تومان
                              </p>
                              <p className="text-sm text-gray-600">
                                {new Date(order.createdAt!).toLocaleDateString('fa-IR')}
                              </p>
                            </div>
                          </div>
                          <div className="flex justify-between items-center">
                            <Select
                              value={order.status}
                              onValueChange={(status) => updateOrderStatusMutation.mutate({ id: order.id, status })}
                            >
                              <SelectTrigger className="w-48" data-testid={`order-status-${order.id}`}>
                                <SelectValue />
                              </SelectTrigger>
                              <SelectContent>
                                <SelectItem value="pending">در انتظار</SelectItem>
                                <SelectItem value="processing">در حال پردازش</SelectItem>
                                <SelectItem value="shipped">ارسال شده</SelectItem>
                                <SelectItem value="delivered">تحویل داده شده</SelectItem>
                                <SelectItem value="cancelled">لغو شده</SelectItem>
                              </SelectContent>
                            </Select>
                            <span className="text-xs text-gray-500">#{order.id.substring(0, 8)}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Analytics Tab */}
              <TabsContent value="analytics">
                <div className="grid md:grid-cols-2 gap-6">
                  <Card>
                    <CardHeader>
                      <CardTitle>نمودار فروش</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="h-64 bg-gray-100 rounded-xl flex items-center justify-center">
                        <p className="text-gray-500">نمودار فروش در اینجا نمایش داده می‌شود</p>
                      </div>
                    </CardContent>
                  </Card>
                  
                  <Card>
                    <CardHeader>
                      <CardTitle>سفارشات اخیر</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        {recentOrders?.slice(0, 5).map((order: any, index: number) => (
                          <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg" data-testid={`recent-order-${index}`}>
                            <div>
                              <p className="font-medium">{order.customerName}</p>
                              <p className="text-sm text-gray-600">#{order.id.substring(0, 8)}</p>
                            </div>
                            <div className="text-left">
                              <p className="font-semibold text-green-600">
                                {parseFloat(order.total).toLocaleString('fa-IR')} تومان
                              </p>
                              <p className="text-xs text-gray-500">
                                {new Date(order.createdAt).toLocaleDateString('fa-IR')}
                              </p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>
            </Tabs>
          </div>
        </section>
      </main>

      <Footer />

      {/* Product Modal */}
      {isProductModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
            <h3 className="text-xl font-semibold mb-4">
              {selectedProduct ? 'ویرایش محصول' : 'افزودن محصول جدید'}
            </h3>
            <form onSubmit={productForm.handleSubmit(handleProductSubmit)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">نام محصول</label>
                <Input {...productForm.register('name')} data-testid="product-name-input" />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">توضیحات</label>
                <Textarea {...productForm.register('description')} data-testid="product-description-input" />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">قیمت</label>
                <Input {...productForm.register('price')} data-testid="product-price-input" />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">قیمت اصلی (اختیاری)</label>
                <Input {...productForm.register('originalPrice')} data-testid="product-original-price-input" />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">دسته‌بندی</label>
                <Select onValueChange={(value) => productForm.setValue('categoryId', value)}>
                  <SelectTrigger data-testid="product-category-select">
                    <SelectValue placeholder="انتخاب دسته‌بندی" />
                  </SelectTrigger>
                  <SelectContent>
                    {categories?.map((category) => (
                      <SelectItem key={category.id} value={category.id}>
                        {category.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">URL تصویر</label>
                <Input {...productForm.register('imageUrl')} data-testid="product-image-input" />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">موجودی</label>
                <Input 
                  type="number" 
                  {...productForm.register('stock', { valueAsNumber: true })} 
                  data-testid="product-stock-input"
                />
              </div>
              
              <div className="flex space-x-4 space-x-reverse pt-4">
                <Button 
                  type="submit" 
                  className="flex-1"
                  disabled={createProductMutation.isPending || updateProductMutation.isPending}
                  data-testid="product-submit-btn"
                >
                  {selectedProduct ? 'بروزرسانی' : 'افزودن'}
                </Button>
                <Button 
                  type="button" 
                  variant="outline" 
                  onClick={() => setIsProductModalOpen(false)}
                  className="flex-1"
                  data-testid="product-cancel-btn"
                >
                  لغو
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Category Modal */}
      {isCategoryModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md">
            <h3 className="text-xl font-semibold mb-4">افزودن دسته‌بندی جدید</h3>
            <form onSubmit={categoryForm.handleSubmit(handleCategorySubmit)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">نام فارسی</label>
                <Input {...categoryForm.register('name')} data-testid="category-name-input" />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">نام انگلیسی</label>
                <Input {...categoryForm.register('nameEn')} data-testid="category-name-en-input" />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">توضیحات</label>
                <Textarea {...categoryForm.register('description')} data-testid="category-description-input" />
              </div>
              
              <div className="flex space-x-4 space-x-reverse pt-4">
                <Button 
                  type="submit" 
                  className="flex-1"
                  disabled={createCategoryMutation.isPending}
                  data-testid="category-submit-btn"
                >
                  افزودن
                </Button>
                <Button 
                  type="button" 
                  variant="outline" 
                  onClick={() => setIsCategoryModalOpen(false)}
                  className="flex-1"
                  data-testid="category-cancel-btn"
                >
                  لغو
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
