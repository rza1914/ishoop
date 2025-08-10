#!/usr/bin/env python3
"""
🔍 Pre-Deployment Check for iShop (Fixed Version)
بررسی آمادگی پروژه برای deployment

Usage: python pre_deploy_check_fixed.py [your-domain.com]
"""

import os
import sys
import json
import subprocess
import requests
from pathlib import Path
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class PreDeploymentChecker:
    def __init__(self, domain=None):
        self.domain = domain
        self.issues = []
        self.warnings = []
        self.success_count = 0
        self.total_checks = 0
        
    def log(self, message, color=Colors.BLUE):
        print(f"{color}{message}{Colors.END}")
    
    def success(self, message):
        self.log(f"✅ {message}", Colors.GREEN)
        self.success_count += 1
    
    def error(self, message):
        self.log(f"❌ {message}", Colors.RED)
        self.issues.append(message)
    
    def warning(self, message):
        self.log(f"⚠️ {message}", Colors.YELLOW)
        self.warnings.append(message)
    
    def info(self, message):
        self.log(f"ℹ️ {message}", Colors.BLUE)
    
    def check_file_exists(self, file_path, required=True):
        """Check if a file exists"""
        self.total_checks += 1
        if os.path.exists(file_path):
            self.success(f"File exists: {file_path}")
            return True
        else:
            if required:
                self.error(f"Required file missing: {file_path}")
            else:
                self.warning(f"Optional file missing: {file_path}")
            return False
    
    def check_directory_structure(self):
        """Check project directory structure"""
        self.info("🏗️ Checking project structure...")
        
        required_files = [
            "app/main.py",
            "app/__init__.py",
            "requirements.txt"
        ]
        
        optional_files = [
            ".env",
            "README.md",
            "Dockerfile"
        ]
        
        for file_path in required_files:
            self.check_file_exists(file_path, required=True)
        
        for file_path in optional_files:
            self.check_file_exists(file_path, required=False)
    
    def check_frontend_build(self):
        """Check if frontend is ready"""
        self.info("🎨 Checking frontend...")
        
        frontend_path = "ishop-frontend"
        if os.path.exists(frontend_path):
            self.success("Frontend directory found")
            
            # Check package.json
            package_json = os.path.join(frontend_path, "package.json")
            self.check_file_exists(package_json, required=True)
            
            # Check if build exists
            build_path = os.path.join(frontend_path, "build")
            if os.path.exists(build_path):
                self.success("Frontend build directory exists")
            else:
                self.warning("Frontend not built yet (will be built during deployment)")
            
            # Check src/api.js
            api_file = os.path.join(frontend_path, "src", "api.js")
            self.check_file_exists(api_file, required=True)
            
        else:
            self.error("Frontend directory not found")
    
    def check_backend_dependencies(self):
        """Check backend dependencies"""
        self.info("🐍 Checking backend dependencies...")
        
        try:
            import fastapi
            self.success("FastAPI installed")
        except ImportError:
            self.error("FastAPI not installed")
        
        try:
            import uvicorn
            self.success("Uvicorn installed")
        except ImportError:
            self.error("Uvicorn not installed")
        
        try:
            import sqlalchemy
            self.success("SQLAlchemy installed")
        except ImportError:
            self.error("SQLAlchemy not installed")
        
        # Check requirements.txt
        if os.path.exists("requirements.txt"):
            with open("requirements.txt", "r") as f:
                requirements = f.read()
                required_packages = ["fastapi", "uvicorn", "sqlalchemy"]
                
                for package in required_packages:
                    if package in requirements.lower():
                        self.success(f"{package} in requirements.txt")
                    else:
                        self.warning(f"{package} missing from requirements.txt (will be added)")
    
    def check_backend_functionality(self):
        """Check if backend is working"""
        self.info("🔧 Checking backend functionality...")
        
        try:
            # Try to start server temporarily
            self.info("Testing backend startup...")
            
            # Import main app
            sys.path.insert(0, os.getcwd())
            try:
                from app.main import app
                self.success("Backend app imports successfully")
            except Exception as e:
                self.error(f"Backend import failed: {str(e)}")
                return
            
            # Check if main endpoints exist
            routes = [str(route.path) for route in app.routes]
            
            required_routes = ["/", "/api/v1/products/", "/admin"]
            for route in required_routes:
                if any(route in r for r in routes):
                    self.success(f"Route exists: {route}")
                else:
                    self.error(f"Route missing: {route}")
            
        except Exception as e:
            self.error(f"Backend check failed: {str(e)}")
    
    def check_environment_config(self):
        """Check environment configuration"""
        self.info("⚙️ Checking environment configuration...")
        
        if os.path.exists(".env"):
            self.success(".env file exists")
            
            with open(".env", "r") as f:
                env_content = f.read()
                
                required_vars = ["SECRET_KEY", "DATABASE_URL"]
                for var in required_vars:
                    if var in env_content:
                        self.success(f"Environment variable set: {var}")
                    else:
                        self.warning(f"Environment variable missing: {var}")
        else:
            self.warning(".env file not found (will be created during deployment)")
    
    def check_database(self):
        """Check database setup"""
        self.info("🗄️ Checking database...")
        
        try:
            from app.db.session import engine, Base
            
            # Try to create tables
            Base.metadata.create_all(bind=engine)
            self.success("Database connection successful")
            
            # Check if tables exist
            from sqlalchemy import inspect
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            if tables:
                self.success(f"Database tables exist: {', '.join(tables)}")
            else:
                self.warning("No database tables found (will be created during deployment)")
                
        except Exception as e:
            self.warning(f"Database check failed: {str(e)} (will be setup during deployment)")
    
    def check_domain_configuration(self):
        """Check domain and DNS"""
        if not self.domain:
            self.warning("No domain provided, skipping DNS checks")
            return
        
        self.info(f"🌐 Checking domain: {self.domain}")
        
        try:
            import socket
            ip = socket.gethostbyname(self.domain)
            self.success(f"Domain resolves to: {ip}")
            
            # Check if domain points to current server (basic check)
            try:
                response = requests.get(f"http://{self.domain}", timeout=5)
                self.info(f"Domain is accessible (status: {response.status_code})")
            except:
                self.info("Domain not accessible yet (expected before deployment)")
                
        except socket.gaierror:
            self.warning(f"Domain {self.domain} does not resolve yet")
    
    def check_system_requirements(self):
        """Check system requirements"""
        self.info("💻 Checking system requirements...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version >= (3, 8):
            self.success(f"Python version: {python_version.major}.{python_version.minor}")
        else:
            self.error(f"Python version too old: {python_version.major}.{python_version.minor} (need 3.8+)")
        
        # Check Node.js (if frontend exists)
        if os.path.exists("ishop-frontend"):
            try:
                result = subprocess.run(["node", "--version"], capture_output=True, text=True)
                if result.returncode == 0:
                    self.success(f"Node.js version: {result.stdout.strip()}")
                else:
                    self.error("Node.js not found")
            except FileNotFoundError:
                self.error("Node.js not found")
    
    def fix_requirements_file(self):
        """Fix requirements.txt if needed"""
        if not os.path.exists("requirements.txt"):
            return
        
        with open("requirements.txt", "r") as f:
            requirements = f.read()
        
        # Required packages that might be missing
        required_packages = [
            "sqlalchemy==2.0.23",
            "python-dotenv==1.0.0",
            "email-validator==2.1.0"
        ]
        
        updated = False
        for package in required_packages:
            package_name = package.split("==")[0]
            if package_name not in requirements.lower():
                requirements += f"\n{package}"
                updated = True
                self.info(f"Added {package_name} to requirements.txt")
        
        if updated:
            with open("requirements.txt", "w") as f:
                f.write(requirements)
            self.success("Requirements.txt updated")
    
    def create_deployment_summary(self):
        """Create deployment summary"""
        
        # Create deployment config
        config = {
            "domain": self.domain,
            "timestamp": datetime.now().isoformat(),
            "project_structure": {
                "backend": os.path.exists("app/main.py"),
                "frontend": os.path.exists("ishop-frontend"),
                "requirements": os.path.exists("requirements.txt"),
                "env_file": os.path.exists(".env")
            },
            "readiness_score": f"{(self.success_count / max(self.total_checks, 1)) * 100:.1f}%",
            "issues_count": len(self.issues),
            "warnings_count": len(self.warnings)
        }
        
        with open("deployment_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        self.success("Deployment configuration saved to deployment_config.json")
    
    def create_env_template(self):
        """Create .env template if not exists"""
        if not os.path.exists(".env"):
            env_template = f"""# iShop Environment Configuration
SECRET_KEY=your-super-secret-production-key-here-very-long-and-random
DATABASE_URL=sqlite:///./production.db
ENVIRONMENT=production
DEBUG=False
ALLOWED_HOSTS={self.domain or 'your-domain.com'},www.{self.domain or 'your-domain.com'}
CORS_ORIGINS=https://{self.domain or 'your-domain.com'},https://www.{self.domain or 'your-domain.com'}

# Admin settings
ADMIN_EMAIL=admin@{self.domain or 'your-domain.com'}
ADMIN_PASSWORD=secure-admin-password-here

# Email settings (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
"""
            with open(".env.template", "w") as f:
                f.write(env_template)
            
            self.success("Environment template created: .env.template")
    
    def generate_deployment_script(self):
        """Generate customized deployment script"""
        if not self.domain:
            return
        
        script_content = f"""#!/bin/bash
# Auto-generated deployment script for {self.domain}
# Generated on: {datetime.now().isoformat()}

DOMAIN="{self.domain}"

echo "🚀 Starting deployment for $DOMAIN"
echo "=================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root"
   exit 1
fi

# Update system
echo "📦 Updating system..."
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo "🔧 Installing dependencies..."
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx nodejs npm git

# Install PM2
sudo npm install -g pm2

# Create directories
sudo mkdir -p /var/www/ishop
sudo mkdir -p /var/www/frontend
sudo mkdir -p /var/log/ishop
sudo mkdir -p /var/backups/ishop

# Set permissions
sudo chown -R $USER:$USER /var/www/ishop
sudo chown -R $USER:$USER /var/www/frontend

echo "✅ System setup completed"
echo "📋 Next steps:"
echo "1. Upload your project files to /var/www/ishop"
echo "2. Run the main deployment script"
echo "3. Configure your domain DNS to point to this server"

echo "🎯 Your domain: https://$DOMAIN"
"""
        
        with open("deploy_setup.sh", "w") as f:
            f.write(script_content)
        
        # Make executable on Unix systems
        try:
            os.chmod("deploy_setup.sh", 0o755)
        except:
            pass  # Windows doesn't support chmod
        
        self.success("Deployment setup script generated: deploy_setup.sh")
    
    def run_all_checks(self):
        """Run all pre-deployment checks"""
        self.log("🚀 iShop Pre-Deployment Check", Colors.BOLD)
        self.log("=" * 50, Colors.BOLD)
        
        if self.domain:
            self.info(f"Target domain: {self.domain}")
        
        self.log("-" * 50)
        
        # Run all checks
        self.check_system_requirements()
        self.check_directory_structure()
        self.check_backend_dependencies()
        self.check_backend_functionality()
        self.check_environment_config()
        self.check_database()
        self.check_frontend_build()
        self.check_domain_configuration()
        
        # Fix issues automatically
        self.fix_requirements_file()
        self.create_env_template()
        
        # Generate deployment files
        self.create_deployment_summary()
        self.generate_deployment_script()
        
        # Final report
        self.log("\n" + "=" * 50, Colors.BOLD)
        self.log("📊 Pre-Deployment Report", Colors.BOLD)
        self.log("=" * 50, Colors.BOLD)
        
        total_issues = len(self.issues)
        total_warnings = len(self.warnings)
        
        self.info(f"✅ Successful checks: {self.success_count}")
        self.info(f"❌ Critical issues: {total_issues}")
        self.info(f"⚠️ Warnings: {total_warnings}")
        
        readiness_score = (self.success_count / max(self.total_checks, 1)) * 100
        
        if total_issues == 0:
            self.success(f"🎉 Project is ready for deployment! ({readiness_score:.1f}% ready)")
            
            self.log("\n📋 Quick Deployment Guide:", Colors.BOLD)
            self.log("1. Fix any warnings (optional)")
            self.log("2. Upload files to your server")
            self.log("3. Run deployment script on server")
            
            if self.domain:
                self.log(f"4. Point {self.domain} DNS to your server")
                self.log(f"5. Visit https://{self.domain}")
            
        elif total_issues <= 2:
            self.warning(f"⚠️ Project mostly ready ({readiness_score:.1f}%) but has minor issues")
            self.log("\n🔧 Issues to fix:")
            for issue in self.issues:
                self.log(f"  • {issue}")
        else:
            self.error(f"❌ Project needs work ({readiness_score:.1f}%) - fix critical issues first")
            self.log("\n🔧 Critical issues:")
            for issue in self.issues:
                self.log(f"  • {issue}")
        
        if self.warnings:
            self.log("\n⚠️ Warnings (recommended to fix):")
            for warning in self.warnings[:5]:  # Show only first 5
                self.log(f"  • {warning}")
            if len(self.warnings) > 5:
                self.log(f"  ... and {len(self.warnings) - 5} more")
        
        # Deployment readiness
        if readiness_score >= 90:
            self.success("🚀 Ready for production deployment!")
        elif readiness_score >= 70:
            self.warning("⚠️ Ready for testing deployment")
        else:
            self.error("❌ Not ready for deployment")
        
        return total_issues == 0

def main():
    domain = None
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    
    checker = PreDeploymentChecker(domain)
    ready = checker.run_all_checks()
    
    sys.exit(0 if ready else 1)

if __name__ == "__main__":
    main()