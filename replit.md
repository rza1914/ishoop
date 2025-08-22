# iShop - Persian E-commerce Platform

## Overview

iShop is a modern Persian e-commerce platform built with React, Express, and PostgreSQL. It features a comprehensive admin dashboard, product management system, shopping cart functionality, and is designed with RTL (Right-to-Left) support for Persian language users. The application includes both customer-facing features and administrative tools for managing products, orders, and categories.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: React with TypeScript using Vite for build tooling
- **Routing**: Wouter for client-side routing
- **State Management**: TanStack React Query for server state, React Context for cart management
- **UI Framework**: Radix UI components with custom styling
- **Styling**: Tailwind CSS with Persian/Farsi font support (Vazirmatn)
- **Language Support**: RTL layout with Persian text throughout the interface

### Backend Architecture
- **Server**: Express.js with TypeScript
- **API Design**: RESTful API with route handlers for products, categories, orders, and admin functions
- **Data Validation**: Zod schemas for runtime type checking and validation
- **Storage Layer**: Abstract storage interface with in-memory implementation (designed to be swapped for database later)

### Data Storage Solutions
- **Database**: PostgreSQL configured with Drizzle ORM
- **Schema Management**: Drizzle Kit for migrations and schema management
- **Connection**: Neon serverless PostgreSQL adapter
- **Development**: In-memory storage implementation for development/testing

### Core Data Models
- **Users**: Authentication and user management with role-based access
- **Products**: Full product catalog with pricing, descriptions, categories, and inventory
- **Categories**: Hierarchical product categorization with Persian/English names
- **Orders**: Order management with customer details and item tracking

### Authentication and Authorization
- **Session Management**: PostgreSQL session store with connect-pg-simple
- **User Roles**: Role-based access control (admin vs regular users)
- **Security**: Session-based authentication with secure cookie handling

### Key Features
- **Shopping Cart**: Persistent cart with localStorage backup and quantity management
- **Admin Dashboard**: Complete administrative interface with statistics and management tools
- **Product Management**: CRUD operations for products with image upload support
- **Order Processing**: Order creation, status tracking, and management
- **Responsive Design**: Mobile-first design with glassmorphism UI effects
- **Toast Notifications**: User feedback system for actions and errors

## External Dependencies

### Database and ORM
- **PostgreSQL**: Primary database with Neon serverless hosting
- **Drizzle ORM**: Type-safe database operations and schema management
- **Drizzle Zod**: Schema validation integration

### UI and Styling
- **Radix UI**: Accessible component primitives for complex UI elements
- **Tailwind CSS**: Utility-first styling framework
- **shadcn/ui**: Pre-built component library with Radix UI integration
- **Lucide React**: Icon library for consistent iconography

### Development Tools
- **TanStack React Query**: Data fetching and caching layer
- **React Hook Form**: Form handling with validation
- **Hookform Resolvers**: Zod integration for form validation
- **Wouter**: Lightweight React router

### Build and Development
- **Vite**: Fast build tool and development server
- **TypeScript**: Static type checking
- **ESBuild**: Fast JavaScript bundler for production builds
- **PostCSS**: CSS processing with Tailwind integration

### Fonts and Internationalization
- **Google Fonts**: Vazirmatn for Persian text, Inter for English fallback
- **RTL Support**: Right-to-left layout support for Persian language