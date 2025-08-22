import { type User, type InsertUser, type Product, type InsertProduct, type Category, type InsertCategory, type Order, type InsertOrder } from "@shared/schema";
import { randomUUID } from "crypto";

export interface IStorage {
  // Users
  getUser(id: string): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  getUserByEmail(email: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  
  // Categories
  getCategories(): Promise<Category[]>;
  getCategory(id: string): Promise<Category | undefined>;
  createCategory(category: InsertCategory): Promise<Category>;
  
  // Products
  getProducts(): Promise<Product[]>;
  getProduct(id: string): Promise<Product | undefined>;
  getProductsByCategory(categoryId: string): Promise<Product[]>;
  createProduct(product: InsertProduct): Promise<Product>;
  updateProduct(id: string, product: Partial<InsertProduct>): Promise<Product | undefined>;
  deleteProduct(id: string): Promise<boolean>;
  
  // Orders
  getOrders(): Promise<Order[]>;
  getOrder(id: string): Promise<Order | undefined>;
  getOrdersByUser(userId: string): Promise<Order[]>;
  createOrder(order: InsertOrder): Promise<Order>;
  updateOrderStatus(id: string, status: string): Promise<Order | undefined>;
  
  // Stats
  getStats(): Promise<{
    totalSales: string;
    totalOrders: number;
    totalUsers: number;
    totalProducts: number;
  }>;
}

export class MemStorage implements IStorage {
  private users: Map<string, User>;
  private categories: Map<string, Category>;
  private products: Map<string, Product>;
  private orders: Map<string, Order>;

  constructor() {
    this.users = new Map();
    this.categories = new Map();
    this.products = new Map();
    this.orders = new Map();
    
    // Initialize with sample data
    this.initializeSampleData();
  }

  private initializeSampleData() {
    // Sample categories
    const categories = [
      { id: "cat-1", name: "الکترونیک", nameEn: "electronics", description: "محصولات الکترونیکی" },
      { id: "cat-2", name: "پوشاک", nameEn: "fashion", description: "لباس و پوشاک" },
      { id: "cat-3", name: "لوازم جانبی", nameEn: "accessories", description: "لوازم جانبی و تزئینی" },
      { id: "cat-4", name: "ورزش", nameEn: "sports", description: "لوازم ورزشی" },
    ];
    
    categories.forEach(cat => {
      this.categories.set(cat.id, { ...cat, createdAt: new Date() });
    });
    
    // Sample products
    const products = [
      {
        id: "prod-1",
        name: "گردنبند قلب زیبا",
        description: "گردنبند آویز قلب تاجی مکعبی زیبا",
        price: "220000",
        originalPrice: "250000",
        currency: "تومان",
        categoryId: "cat-3",
        imageUrl: "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&h=300",
        stock: 50,
        isActive: true,
        tags: ["جواهرات", "قلب", "زیبا"],
      },
      {
        id: "prod-2",
        name: "گوشی هوشمند پریمیوم",
        description: "آخرین تکنولوژی با قابلیت‌های پیشرفته",
        price: "15500000",
        originalPrice: "16000000",
        currency: "تومان",
        categoryId: "cat-1",
        imageUrl: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&h=300",
        stock: 25,
        isActive: true,
        tags: ["موبایل", "اندروید", "پریمیوم"],
      },
      {
        id: "prod-3",
        name: "ساعت مچی کلاسیک",
        description: "ساعت مچی با بند چرمی و صفحه کلاسیک",
        price: "1200000",
        currency: "تومان",
        categoryId: "cat-3",
        imageUrl: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&h=300",
        stock: 15,
        isActive: true,
        tags: ["ساعت", "کلاسیک", "چرم"],
      },
      {
        id: "prod-4",
        name: "کوله پشتی اسپرت",
        description: "کوله پشتی مقاوم و شیک برای استفاده روزانه",
        price: "450000",
        originalPrice: "560000",
        currency: "تومان",
        categoryId: "cat-4",
        imageUrl: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&h=300",
        stock: 30,
        isActive: true,
        tags: ["کوله", "اسپرت", "روزانه"],
      },
    ];
    
    products.forEach(prod => {
      this.products.set(prod.id, { 
        ...prod,
        originalPrice: prod.originalPrice || null,
        createdAt: new Date(), 
        updatedAt: new Date() 
      });
    });
    
    // Sample admin user
    this.users.set("admin-1", {
      id: "admin-1",
      username: "admin",
      email: "admin@ishop.ir",
      password: "admin123", // In real app, this would be hashed
      role: "admin",
      createdAt: new Date(),
    });
  }

  async getUser(id: string): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.username === username,
    );
  }

  async getUserByEmail(email: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.email === email,
    );
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = randomUUID();
    const user: User = { 
      ...insertUser, 
      id, 
      role: "user",
      createdAt: new Date() 
    };
    this.users.set(id, user);
    return user;
  }

  async getCategories(): Promise<Category[]> {
    return Array.from(this.categories.values());
  }

  async getCategory(id: string): Promise<Category | undefined> {
    return this.categories.get(id);
  }

  async createCategory(category: InsertCategory): Promise<Category> {
    const id = randomUUID();
    const newCategory: Category = { 
      ...category, 
      id,
      description: category.description || null,
      createdAt: new Date() 
    };
    this.categories.set(id, newCategory);
    return newCategory;
  }

  async getProducts(): Promise<Product[]> {
    return Array.from(this.products.values()).filter(p => p.isActive);
  }

  async getProduct(id: string): Promise<Product | undefined> {
    return this.products.get(id);
  }

  async getProductsByCategory(categoryId: string): Promise<Product[]> {
    return Array.from(this.products.values()).filter(
      p => p.categoryId === categoryId && p.isActive
    );
  }

  async createProduct(product: InsertProduct): Promise<Product> {
    const id = randomUUID();
    const newProduct: Product = { 
      ...product,
      id,
      description: product.description || null,
      originalPrice: product.originalPrice || null,
      currency: product.currency || null,
      categoryId: product.categoryId || null,
      imageUrl: product.imageUrl || null,
      stock: product.stock || 0,
      isActive: true,
      tags: product.tags || null,
      createdAt: new Date(),
      updatedAt: new Date() 
    };
    this.products.set(id, newProduct);
    return newProduct;
  }

  async updateProduct(id: string, product: Partial<InsertProduct>): Promise<Product | undefined> {
    const existing = this.products.get(id);
    if (!existing) return undefined;
    
    const updated = { 
      ...existing, 
      ...product, 
      updatedAt: new Date() 
    };
    this.products.set(id, updated);
    return updated;
  }

  async deleteProduct(id: string): Promise<boolean> {
    const existing = this.products.get(id);
    if (!existing) return false;
    
    const updated = { ...existing, isActive: false, updatedAt: new Date() };
    this.products.set(id, updated);
    return true;
  }

  async getOrders(): Promise<Order[]> {
    return Array.from(this.orders.values());
  }

  async getOrder(id: string): Promise<Order | undefined> {
    return this.orders.get(id);
  }

  async getOrdersByUser(userId: string): Promise<Order[]> {
    return Array.from(this.orders.values()).filter(
      order => order.userId === userId
    );
  }

  async createOrder(order: InsertOrder): Promise<Order> {
    const id = randomUUID();
    const newOrder: Order = { 
      ...order,
      id,
      userId: order.userId || null,
      customerEmail: order.customerEmail || null,
      customerPhone: order.customerPhone || null,
      status: "pending",
      createdAt: new Date(),
      updatedAt: new Date() 
    };
    this.orders.set(id, newOrder);
    return newOrder;
  }

  async updateOrderStatus(id: string, status: string): Promise<Order | undefined> {
    const existing = this.orders.get(id);
    if (!existing) return undefined;
    
    const updated = { 
      ...existing, 
      status, 
      updatedAt: new Date() 
    };
    this.orders.set(id, updated);
    return updated;
  }

  async getStats(): Promise<{
    totalSales: string;
    totalOrders: number;
    totalUsers: number;
    totalProducts: number;
  }> {
    const orders = Array.from(this.orders.values());
    const totalSales = orders.reduce((sum, order) => sum + parseFloat(order.total), 0);
    
    return {
      totalSales: `${totalSales.toLocaleString('fa-IR')} تومان`,
      totalOrders: orders.length,
      totalUsers: this.users.size,
      totalProducts: Array.from(this.products.values()).filter(p => p.isActive).length,
    };
  }
}

export const storage = new MemStorage();
