import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import Header from "@/components/layout/header";
import Footer from "@/components/layout/footer";
import CartSidebar from "@/components/cart-sidebar";
import ProductCard from "@/components/product-card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Search, Filter } from "lucide-react";

export default function Products() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [sortBy, setSortBy] = useState("newest");
  
  const { data: products, isLoading } = useQuery({
    queryKey: ['/api/products'],
  });

  const { data: categories } = useQuery({
    queryKey: ['/api/categories'],
  });

  const filteredProducts = products ? products.filter((product: any) => {
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.description?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === "all" || product.categoryId === selectedCategory;
    return matchesSearch && matchesCategory;
  }) : [];

  const sortedProducts = [...filteredProducts].sort((a, b) => {
    switch (sortBy) {
      case "price-low":
        return parseFloat(a.price) - parseFloat(b.price);
      case "price-high":
        return parseFloat(b.price) - parseFloat(a.price);
      case "name":
        return a.name.localeCompare(b.name);
      default:
        return new Date(b.createdAt!).getTime() - new Date(a.createdAt!).getTime();
    }
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <Header />
      <CartSidebar />
      
      <main className="pt-24">
        {/* Header Section */}
        <section className="py-16 bg-white">
          <div className="container mx-auto px-4">
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-gray-800 mb-4">محصولات</h1>
              <p className="text-gray-600 max-w-2xl mx-auto">
                مجموعه کاملی از بهترین محصولات با کیفیت عالی و قیمت‌های مناسب
              </p>
            </div>

            {/* Search and Filters */}
            <div className="flex flex-col md:flex-row gap-4 mb-8">
              {/* Search */}
              <div className="relative flex-1">
                <Input
                  type="text"
                  placeholder="جستجو در محصولات..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-3"
                  data-testid="products-search"
                />
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              </div>

              {/* Category Filter */}
              <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                <SelectTrigger className="w-full md:w-48" data-testid="category-filter">
                  <SelectValue placeholder="دسته‌بندی" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">همه دسته‌ها</SelectItem>
                  {categories ? categories.map((category: any) => (
                    <SelectItem key={category.id} value={category.id}>
                      {category.name}
                    </SelectItem>
                  )) : null}
                </SelectContent>
              </Select>

              {/* Sort */}
              <Select value={sortBy} onValueChange={setSortBy}>
                <SelectTrigger className="w-full md:w-48" data-testid="sort-filter">
                  <SelectValue placeholder="مرتب‌سازی" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="newest">جدیدترین</SelectItem>
                  <SelectItem value="price-low">قیمت: کم به زیاد</SelectItem>
                  <SelectItem value="price-high">قیمت: زیاد به کم</SelectItem>
                  <SelectItem value="name">نام محصول</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Results Count */}
            <div className="mb-6">
              <p className="text-gray-600" data-testid="products-count">
                {isLoading ? "در حال بارگذاری..." : `${sortedProducts.length} محصول یافت شد`}
              </p>
            </div>

            {/* Products Grid */}
            {isLoading ? (
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {[1, 2, 3, 4, 5, 6, 7, 8].map(i => (
                  <div key={i} className="bg-white rounded-2xl p-6">
                    <div className="animate-pulse">
                      <div className="bg-gray-300 h-48 rounded mb-4"></div>
                      <div className="bg-gray-300 h-4 rounded mb-2"></div>
                      <div className="bg-gray-300 h-4 rounded w-2/3 mb-4"></div>
                      <div className="bg-gray-300 h-8 rounded"></div>
                    </div>
                  </div>
                ))}
              </div>
            ) : sortedProducts.length === 0 ? (
              <div className="text-center py-16">
                <div className="text-6xl mb-4">🔍</div>
                <h3 className="text-xl font-semibold text-gray-800 mb-2">محصولی یافت نشد</h3>
                <p className="text-gray-600 mb-4">متاسفانه محصولی با این مشخصات پیدا نشد</p>
                <Button
                  onClick={() => {
                    setSearchTerm("");
                    setSelectedCategory("all");
                  }}
                  className="bg-primary-500 text-white"
                  data-testid="clear-filters"
                >
                  پاک کردن فیلترها
                </Button>
              </div>
            ) : (
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {sortedProducts.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
            )}

            {/* Load More Button (if needed) */}
            {!isLoading && sortedProducts.length > 0 && sortedProducts.length >= 20 && (
              <div className="text-center mt-12">
                <Button className="bg-primary-500 text-white px-8 py-3 rounded-xl" data-testid="load-more">
                  نمایش محصولات بیشتر
                </Button>
              </div>
            )}
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
}
