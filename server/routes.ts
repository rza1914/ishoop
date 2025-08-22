import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { insertUserSchema, insertProductSchema, insertCategorySchema, insertOrderSchema, googleAuthSchema, telegramAuthSchema } from "@shared/schema";
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import session from 'express-session';
import passport from 'passport';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';
import rateLimit from 'express-rate-limit';
import Stripe from 'stripe';

export async function registerRoutes(app: Express): Promise<Server> {
  
  // Payment configuration
  let stripe: Stripe | null = null;
  if (process.env.STRIPE_SECRET_KEY) {
    stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
      apiVersion: '2024-06-20',
    });
  }

  // Session configuration
  app.use(session({
    secret: process.env.SESSION_SECRET || 'ishop-secret-key-2024',
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: process.env.NODE_ENV === 'production',
      maxAge: 24 * 60 * 60 * 1000 // 24 hours
    }
  }));

  // Admin middleware
  const requireAdmin = async (req: any, res: any, next: any) => {
    const user = req.user;
    if (!user || user.role !== 'admin') {
      return res.status(403).json({ 
        error: 'دسترسی مجاز نیست',
        message: 'تنها ادمین‌ها می‌توانند به این بخش دسترسی داشته باشند'
      });
    }
    next();
  };

  // Passport configuration
  app.use(passport.initialize());
  app.use(passport.session());

  // Rate limiting for auth endpoints
  const authLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5, // 5 attempts per window
    message: { error: 'تعداد تلاش‌های شما زیاد است. لطفاً 15 دقیقه بعد تلاش کنید.' }
  });

  // Passport serialization
  passport.serializeUser((user: any, done) => {
    done(null, user.id);
  });

  passport.deserializeUser(async (id: string, done) => {
    try {
      const user = await storage.getUser(id);
      done(null, user);
    } catch (error) {
      done(error, null);
    }
  });

  // Google OAuth Strategy
  if (process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET) {
    passport.use(new GoogleStrategy({
      clientID: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
      callbackURL: "/api/auth/google/callback"
    },
    async (accessToken, refreshToken, profile, done) => {
      try {
        // Check if user exists with Google ID
        let user = await storage.getUserByGoogleId(profile.id);
        
        if (!user) {
          // Check if user exists with email
          user = await storage.getUserByEmail(profile.emails?.[0]?.value || '');
          
          if (user) {
            // Link Google account to existing user
            user = await storage.updateUser(user.id, { googleId: profile.id });
          } else {
            // Create new user
            const userData = {
              email: profile.emails?.[0]?.value || '',
              firstName: profile.name?.givenName || '',
              lastName: profile.name?.familyName || '',
              profileImageUrl: profile.photos?.[0]?.value || '',
              googleId: profile.id,
              username: profile.emails?.[0]?.value?.split('@')[0] || `user_${Date.now()}`,
              isVerified: true
            };
            
            user = await storage.createUser(userData);
          }
        }
        
        return done(null, user);
      } catch (error) {
        return done(error, null);
      }
    }));
  }

  // Authentication middleware
  const requireAuth = (req: any, res: any, next: any) => {
    if (req.isAuthenticated()) {
      return next();
    }
    res.status(401).json({ error: 'Authentication required' });
  };


  // Auth Routes
  
  // Google OAuth
  app.get('/api/auth/google',
    passport.authenticate('google', { scope: ['profile', 'email'] })
  );

  app.get('/api/auth/google/callback',
    passport.authenticate('google', { failureRedirect: '/login' }),
    (req, res) => {
      res.redirect('/');
    }
  );

  // Traditional login
  app.post('/api/auth/login', authLimiter, async (req, res) => {
    try {
      const { email, password } = req.body;
      
      if (!email || !password) {
        return res.status(400).json({ error: 'Email and password required' });
      }
      
      const user = await storage.getUserByEmail(email);
      if (!user || !user.password) {
        return res.status(401).json({ error: 'Invalid credentials' });
      }
      
      const isValid = await bcrypt.compare(password, user.password);
      if (!isValid) {
        return res.status(401).json({ error: 'Invalid credentials' });
      }
      
      req.login(user, (err) => {
        if (err) {
          return res.status(500).json({ error: 'Login failed' });
        }
        
        const { password: _, ...userWithoutPassword } = user;
        res.json({ user: userWithoutPassword, message: 'Login successful' });
      });
      
    } catch (error) {
      res.status(500).json({ error: 'Server error' });
    }
  });

  // Register
  app.post('/api/auth/register', authLimiter, async (req, res) => {
    try {
      const { username, email, password, firstName, lastName, phone } = req.body;
      
      if (!username || !email || !password) {
        return res.status(400).json({ error: 'Required fields missing' });
      }
      
      // Check if user exists
      const existingUser = await storage.getUserByEmail(email);
      if (existingUser) {
        return res.status(400).json({ error: 'User already exists' });
      }
      
      // Hash password
      const hashedPassword = await bcrypt.hash(password, 12);
      
      const userData = {
        username,
        email,
        password: hashedPassword,
        firstName,
        lastName,
        phone,
        isVerified: false
      };
      
      const user = await storage.createUser(userData);
      const { password: _, ...userWithoutPassword } = user;
      
      res.status(201).json({ 
        user: userWithoutPassword, 
        message: 'User created successfully' 
      });
      
    } catch (error) {
      res.status(500).json({ error: 'Server error' });
    }
  });

  // Logout
  app.post('/api/auth/logout', (req, res) => {
    req.logout((err) => {
      if (err) {
        return res.status(500).json({ error: 'Logout failed' });
      }
      res.json({ message: 'Logged out successfully' });
    });
  });

  // Get current user
  app.get('/api/auth/user', (req, res) => {
    if (req.isAuthenticated()) {
      const user = req.user as any;
      const { password: _, ...userWithoutPassword } = user;
      res.json(userWithoutPassword);
    } else {
      res.status(401).json({ error: 'Not authenticated' });
    }
  });

  // Telegram Bot Authentication Middleware
  const botAuth = (req: any, res: any, next: any) => {
    const botToken = req.headers['x-bot-token'];
    const expectedToken = process.env.BOT_SECRET_TOKEN || 'default-bot-secret';
    
    if (botToken !== expectedToken) {
      return res.status(401).json({ error: 'Unauthorized bot request' });
    }
    next();
  };

  // Telegram Bot API - Import Product
  app.post("/api/bot/import-product", botAuth, async (req, res) => {
    try {
      const { name, description, price, category, imageUrl, tags } = req.body;
      
      // تبدیل قیمت از درهم به تومان (نرخ تقریبی: 1 درهم = 10,000 تومان)
      const priceInToman = parseFloat(price) * 10000;
      
      // پیدا کردن دسته‌بندی بر اساس نام
      const categories = await storage.getCategories();
      let categoryId = null;
      
      if (category) {
        const foundCategory = categories.find(cat => 
          cat.name.includes(category) || cat.nameEn.toLowerCase().includes(category.toLowerCase())
        );
        categoryId = foundCategory?.id || null;
      }
      
      // ساختن محصول جدید
      const productData = {
        name: name || 'محصول وارداتی',
        description: description || 'محصول وارد شده از طریق بات تلگرام',
        price: priceInToman.toString(),
        currency: 'تومان',
        categoryId,
        imageUrl: imageUrl || null,
        stock: 10, // موجودی پیش‌فرض
        tags: tags || []
      };
      
      const validatedData = insertProductSchema.parse(productData);
      const product = await storage.createProduct(validatedData);
      
      res.status(201).json({ 
        success: true, 
        product,
        message: 'محصول با موفقیت اضافه شد'
      });
    } catch (error) {
      console.error('Bot import error:', error);
      res.status(400).json({ 
        success: false,
        error: 'خطا در اضافه کردن محصول',
        details: error
      });
    }
  });

  // Payment Routes
  
  // Create payment intent (for one-time payments)
  app.post("/api/payment/create-intent", requireAuth, async (req, res) => {
    try {
      if (!stripe) {
        return res.status(500).json({ error: 'Payment system not configured' });
      }

      const { amount, currency = 'usd', orderId } = req.body;

      if (!amount || amount < 50) {
        return res.status(400).json({ error: 'Invalid amount' });
      }

      const paymentIntent = await stripe.paymentIntents.create({
        amount: Math.round(amount * 100), // Convert to cents
        currency,
        metadata: {
          orderId: orderId || '',
          userId: (req.user as any)?.id || ''
        }
      });

      res.json({
        clientSecret: paymentIntent.client_secret,
        paymentIntentId: paymentIntent.id
      });

    } catch (error) {
      console.error('Payment error:', error);
      res.status(500).json({ error: 'Payment creation failed' });
    }
  });

  // Confirm payment
  app.post("/api/payment/confirm", requireAuth, async (req, res) => {
    try {
      if (!stripe) {
        return res.status(500).json({ error: 'Payment system not configured' });
      }

      const { paymentIntentId, orderId } = req.body;

      if (!paymentIntentId) {
        return res.status(400).json({ error: 'Payment intent ID required' });
      }

      const paymentIntent = await stripe.paymentIntents.retrieve(paymentIntentId);

      if (paymentIntent.status === 'succeeded') {
        // Update order status if orderId provided
        if (orderId) {
          await storage.updateOrderStatus(orderId, 'paid');
        }

        res.json({
          success: true,
          status: paymentIntent.status,
          message: 'Payment confirmed successfully'
        });
      } else {
        res.json({
          success: false,
          status: paymentIntent.status,
          message: 'Payment not completed'
        });
      }

    } catch (error) {
      console.error('Payment confirmation error:', error);
      res.status(500).json({ error: 'Payment confirmation failed' });
    }
  });

  // ZarinPal simulation (Iranian gateway)
  app.post("/api/payment/zarinpal/request", requireAuth, async (req, res) => {
    try {
      const { amount, orderId, description } = req.body;

      if (!amount || amount < 1000) {
        return res.status(400).json({ error: 'مبلغ باید حداقل 1000 تومان باشد' });
      }

      // Simulate ZarinPal request
      const authority = `ZARIN_${Date.now()}_${Math.random().toString(36).substring(7)}`;
      
      // In real implementation, you would call ZarinPal API here
      res.json({
        success: true,
        authority,
        paymentUrl: `https://sandbox.zarinpal.com/pg/StartPay/${authority}`,
        message: 'Payment request created successfully'
      });

    } catch (error) {
      console.error('ZarinPal error:', error);
      res.status(500).json({ error: 'خطا در ایجاد درخواست پرداخت' });
    }
  });

  // ZarinPal verify
  app.post("/api/payment/zarinpal/verify", requireAuth, async (req, res) => {
    try {
      const { authority, status, orderId } = req.body;

      if (status === 'OK' && authority) {
        // In real implementation, verify with ZarinPal
        const refId = Math.floor(Math.random() * 1000000);
        
        // Update order status
        if (orderId) {
          await storage.updateOrderStatus(orderId, 'paid');
        }

        res.json({
          success: true,
          refId,
          message: 'پرداخت با موفقیت انجام شد'
        });
      } else {
        res.json({
          success: false,
          message: 'پرداخت لغو شد یا با خطا مواجه شد'
        });
      }

    } catch (error) {
      console.error('ZarinPal verify error:', error);
      res.status(500).json({ error: 'خطا در تأیید پرداخت' });
    }
  });

  // Categories
  app.get("/api/categories", async (req, res) => {
    try {
      const categories = await storage.getCategories();
      res.json(categories);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch categories" });
    }
  });

  app.post("/api/categories", async (req, res) => {
    try {
      const validatedData = insertCategorySchema.parse(req.body);
      const category = await storage.createCategory(validatedData);
      res.status(201).json(category);
    } catch (error) {
      res.status(400).json({ error: "Invalid category data" });
    }
  });

  // Products
  app.get("/api/products", async (req, res) => {
    try {
      const { category } = req.query;
      let products;
      
      if (category && typeof category === 'string') {
        products = await storage.getProductsByCategory(category);
      } else {
        products = await storage.getProducts();
      }
      
      res.json(products);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch products" });
    }
  });

  app.get("/api/products/:id", async (req, res) => {
    try {
      const product = await storage.getProduct(req.params.id);
      if (!product) {
        return res.status(404).json({ error: "Product not found" });
      }
      res.json(product);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch product" });
    }
  });

  app.post("/api/products", async (req, res) => {
    try {
      const validatedData = insertProductSchema.parse(req.body);
      const product = await storage.createProduct(validatedData);
      res.status(201).json(product);
    } catch (error) {
      res.status(400).json({ error: "Invalid product data" });
    }
  });

  app.put("/api/products/:id", async (req, res) => {
    try {
      const validatedData = insertProductSchema.partial().parse(req.body);
      const product = await storage.updateProduct(req.params.id, validatedData);
      if (!product) {
        return res.status(404).json({ error: "Product not found" });
      }
      res.json(product);
    } catch (error) {
      res.status(400).json({ error: "Invalid product data" });
    }
  });

  app.delete("/api/products/:id", async (req, res) => {
    try {
      const deleted = await storage.deleteProduct(req.params.id);
      if (!deleted) {
        return res.status(404).json({ error: "Product not found" });
      }
      res.json({ success: true });
    } catch (error) {
      res.status(500).json({ error: "Failed to delete product" });
    }
  });

  // Orders
  app.get("/api/orders", async (req, res) => {
    try {
      const { userId } = req.query;
      let orders;
      
      if (userId && typeof userId === 'string') {
        orders = await storage.getOrdersByUser(userId);
      } else {
        orders = await storage.getOrders();
      }
      
      res.json(orders);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch orders" });
    }
  });

  app.post("/api/orders", async (req, res) => {
    try {
      const validatedData = insertOrderSchema.parse(req.body);
      const order = await storage.createOrder(validatedData);
      res.status(201).json(order);
    } catch (error) {
      res.status(400).json({ error: "Invalid order data" });
    }
  });

  app.put("/api/orders/:id/status", async (req, res) => {
    try {
      const { status } = req.body;
      if (!status) {
        return res.status(400).json({ error: "Status is required" });
      }
      
      const order = await storage.updateOrderStatus(req.params.id, status);
      if (!order) {
        return res.status(404).json({ error: "Order not found" });
      }
      res.json(order);
    } catch (error) {
      res.status(500).json({ error: "Failed to update order status" });
    }
  });

  // Users
  app.post("/api/users", async (req, res) => {
    try {
      const validatedData = insertUserSchema.parse(req.body);
      
      // Check if user already exists
      const existingUser = await storage.getUserByEmail(validatedData.email);
      if (existingUser) {
        return res.status(409).json({ error: "User with this email already exists" });
      }
      
      const user = await storage.createUser(validatedData);
      
      // Don't send password back
      const { password, ...userWithoutPassword } = user;
      res.status(201).json(userWithoutPassword);
    } catch (error) {
      res.status(400).json({ error: "Invalid user data" });
    }
  });

  // Login
  app.post("/api/auth/login", async (req, res) => {
    try {
      const { email, password } = req.body;
      
      if (!email || !password) {
        return res.status(400).json({ error: "Email and password are required" });
      }
      
      const user = await storage.getUserByEmail(email);
      if (!user || user.password !== password) {
        return res.status(401).json({ error: "Invalid credentials" });
      }
      
      // Don't send password back
      const { password: _, ...userWithoutPassword } = user;
      res.json({ user: userWithoutPassword, token: "mock-jwt-token" });
    } catch (error) {
      res.status(500).json({ error: "Login failed" });
    }
  });

  // Stats for admin dashboard
  app.get("/api/stats", requireAuth, requireAdmin, async (req, res) => {
    try {
      const stats = await storage.getStats();
      res.json(stats);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch stats" });
    }
  });

  // Recent orders for admin dashboard (admin only)
  app.get("/api/orders/recent", requireAuth, requireAdmin, async (req, res) => {
    try {
      const orders = await storage.getOrders();
      const recentOrders = orders
        .sort((a, b) => new Date(b.createdAt!).getTime() - new Date(a.createdAt!).getTime())
        .slice(0, 5);
      res.json(recentOrders);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch recent orders" });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
