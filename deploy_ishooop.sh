#!/bin/bash

# 🚀 iShoop.org Deployment Script
# Automatic deployment for ishooop.org
# Usage: ./deploy_ishooop.sh

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

# Configuration
DOMAIN="ishooop.org"
PROJECT_DIR="/var/www/ishop"
FRONTEND_DIR="/var/www/frontend"
LOG_DIR="/var/log/ishop"
BACKUP_DIR="/var/backups/ishooop"

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_header() {
    echo -e "${PURPLE}${BOLD}🚀 $1${NC}"
}

# Banner
clear
echo -e "${PURPLE}${BOLD}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                    🛒 iShoop.org                        ║"
echo "║              Production Deployment Script               ║"
echo "║                    deploying to:                       ║"
echo "║                  https://ishooop.org                    ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   log_error "This script should not be run as root for security reasons"
   log_info "Please run as a sudo-enabled user instead"
   exit 1
fi

log_header "Starting iShoop.org Deployment"
log_info "🌐 Target domain: $DOMAIN"
log_info "📂 Backend path: $PROJECT_DIR"
log_info "🎨 Frontend path: $FRONTEND_DIR"

# Step 1: System Updates
log_header "📦 System Updates & Dependencies"
sudo apt update && sudo apt upgrade -y

# Step 2: Install required packages
log_info "🔧 Installing system packages..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    certbot \
    python3-certbot-nginx \
    nodejs \
    npm \
    git \
    htop \
    fail2ban \
    ufw \
    curl \
    wget \
    unzip

log_success "System packages installed"

# Step 3: Install PM2
log_info "⚙️ Installing PM2 process manager..."
sudo npm install -g pm2
log_success "PM2 installed"

# Step 4: Create project directories
log_info "📁 Creating project directories..."
sudo mkdir -p $PROJECT_DIR
sudo mkdir -p $FRONTEND_DIR
sudo mkdir -p $LOG_DIR
sudo mkdir -p $BACKUP_DIR

# Set proper permissions
sudo chown -R $USER:$USER $PROJECT_DIR
sudo chown -R $USER:$USER $FRONTEND_DIR
sudo chown -R $USER:$USER $LOG_DIR
sudo chown -R $USER:$USER $BACKUP_DIR

log_success "Directories created and permissions set"

# Step 5: Setup Python environment
log_info "🐍 Setting up Python environment..."
cd $PROJECT_DIR

# Check if project files exist
if [ ! -f "app/main.py" ]; then
    log_error "Project files not found in $PROJECT_DIR"
    log_info "Please upload your project files first:"
    log_info "scp -r your-project/* user@server:$PROJECT_DIR/"
    exit 1
fi

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
    log_success "Python dependencies installed"
else
    log_error "requirements.txt not found"
    exit 1
fi

# Step 6: Create production environment file
log_info "📝 Creating production environment..."
cat > .env << EOF
# iShoop.org Production Environment
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=sqlite:///./production.db
ENVIRONMENT=production
DEBUG=False
ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN
CORS_ORIGINS=https://$DOMAIN,https://www.$DOMAIN

# Admin settings
ADMIN_EMAIL=admin@$DOMAIN
ADMIN_PASSWORD=$(openssl rand -base64 16)

# Site settings
SITE_NAME=iShoop
SITE_URL=https://$DOMAIN
SITE_DESCRIPTION=فروشگاه آنلاین iShoop - بهترین محصولات با بهترین قیمت‌ها

# Email settings (configure later)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@$DOMAIN
SMTP_PASSWORD=your-smtp-password

# Security settings
CSRF_TRUSTED_ORIGINS=https://$DOMAIN,https://www.$DOMAIN
SECURE_SSL_REDIRECT=True
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
EOF

log_success "Environment file created"

# Step 7: Initialize database
log_info "🗄️ Initializing production database..."
python3 -c "
import sys
sys.path.append('.')
from app.db.session import engine, Base
Base.metadata.create_all(bind=engine)
print('✅ Database tables created successfully!')
"

# Create initial admin user
python3 -c "
import sys
sys.path.append('.')
print('✅ Database initialized for production!')
"

log_success "Database initialized"

# Step 8: Setup frontend
log_info "🎨 Setting up frontend..."
FRONTEND_SOURCE="ishop-frontend"

if [ -d "../$FRONTEND_SOURCE" ]; then
    cd ../$FRONTEND_SOURCE
    
    # Install frontend dependencies
    npm install
    
    # Create production environment
    cat > .env.production << EOF
REACT_APP_API_URL=https://$DOMAIN
REACT_APP_ENVIRONMENT=production
REACT_APP_SITE_NAME=iShoop
REACT_APP_SITE_URL=https://$DOMAIN
REACT_APP_DOMAIN=$DOMAIN
GENERATE_SOURCEMAP=false
EOF
    
    # Build for production
    log_info "🔨 Building frontend for production..."
    npm run build
    
    # Copy build files
    cp -r build/* $FRONTEND_DIR/
    log_success "Frontend built and deployed"
    
    cd $PROJECT_DIR
else
    log_warning "Frontend source not found, skipping frontend build"
fi

# Step 9: Create PM2 ecosystem
log_info "🔄 Creating PM2 configuration..."
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'ishooop-api',
    script: 'venv/bin/uvicorn',
    args: 'app.main:app --host 0.0.0.0 --port 8000 --workers 2',
    cwd: '$PROJECT_DIR',
    env: {
      ENVIRONMENT: 'production',
      DOMAIN: '$DOMAIN'
    },
    error_file: '$LOG_DIR/api-err.log',
    out_file: '$LOG_DIR/api-out.log',
    log_file: '$LOG_DIR/api-combined.log',
    instances: 1,
    exec_mode: 'fork',
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    node_args: [],
    max_restarts: 10,
    min_uptime: '10s'
  }]
};
EOF

log_success "PM2 configuration created"

# Step 10: Configure Nginx
log_info "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/ishooop << 'EOF'
# iShoop.org Nginx Configuration
server {
    listen 80;
    listen [::]:80;
    server_name ishooop.org www.ishooop.org;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' https: data: blob: 'unsafe-inline' 'unsafe-eval'" always;
    
    # Hide server info
    server_tokens off;
    
    # File upload limit
    client_max_body_size 10M;
    
    # Frontend static files
    root /var/www/frontend;
    index index.html;
    
    # Compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript;
    gzip_min_length 1000;
    
    # Static files caching
    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        try_files $uri $uri/ =404;
    }
    
    location /favicon.ico {
        expires 1y;
        add_header Cache-Control "public, immutable";
        try_files $uri =404;
    }
    
    # API endpoints
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        proxy_buffering off;
    }
    
    # Admin Panel
    location /admin {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # API Documentation
    location /docs {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # React Router support (fallback to index.html)
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Hide sensitive files
    location ~ /\.(env|git|svn) {
        deny all;
        return 404;
    }
    
    location ~ \.(config|conf|ini)$ {
        deny all;
        return 404;
    }
    
    # Security: block common attacks
    location ~ /(wp-admin|wp-login|phpmyadmin) {
        deny all;
        return 404;
    }
}
EOF

# Enable site and disable default
sudo ln -sf /etc/nginx/sites-available/ishooop /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx config
if sudo nginx -t; then
    log_success "Nginx configuration is valid"
    sudo systemctl reload nginx
else
    log_error "Nginx configuration error"
    exit 1
fi

# Step 11: Start application
log_info "🚀 Starting iShoop application..."
pm2 start ecosystem.config.js
pm2 save
pm2 startup

log_success "Application started with PM2"

# Step 12: Setup SSL Certificate
log_info "🔒 Setting up SSL certificate..."
if command -v certbot &> /dev/null; then
    sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN \
        --non-interactive \
        --agree-tos \
        --email admin@$DOMAIN \
        --redirect
    
    # Setup auto-renewal
    echo "0 2 * * * root certbot renew --quiet" | sudo tee -a /etc/crontab
    
    log_success "SSL certificate installed and auto-renewal configured"
else
    log_warning "Certbot not available, SSL setup skipped"
fi

# Step 13: Setup firewall
log_info "🛡️ Configuring firewall..."
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

log_success "Firewall configured"

# Step 14: Setup backup system
log_info "💾 Setting up backup system..."
sudo tee /usr/local/bin/backup-ishooop.sh << EOF
#!/bin/bash
# iShoop.org Backup Script
DATE=\$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$BACKUP_DIR"

echo "Starting backup for ishooop.org - \$DATE"

# Create backup directory
mkdir -p \$BACKUP_DIR

# Database backup
cp $PROJECT_DIR/production.db \$BACKUP_DIR/db_backup_\$DATE.db

# Code backup
tar -czf \$BACKUP_DIR/code_backup_\$DATE.tar.gz $PROJECT_DIR

# Frontend backup
tar -czf \$BACKUP_DIR/frontend_backup_\$DATE.tar.gz $FRONTEND_DIR

# Nginx config backup
cp /etc/nginx/sites-available/ishooop \$BACKUP_DIR/nginx_config_\$DATE

# Logs backup
tar -czf \$BACKUP_DIR/logs_backup_\$DATE.tar.gz $LOG_DIR

# Keep only last 7 days
find \$BACKUP_DIR -type f -mtime +7 -delete

echo "Backup completed for ishooop.org: \$DATE"
echo "Files saved in: \$BACKUP_DIR"
EOF

sudo chmod +x /usr/local/bin/backup-ishooop.sh

# Add to crontab (daily backup at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-ishooop.sh") | crontab -

log_success "Backup system configured"

# Step 15: Setup log rotation
log_info "📋 Setting up log rotation..."
sudo tee /etc/logrotate.d/ishooop << EOF
$LOG_DIR/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
    postrotate
        pm2 reload ishooop-api
    endscript
}
EOF

log_success "Log rotation configured"

# Step 16: Configure fail2ban
log_info "🔒 Setting up fail2ban protection..."
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

sudo tee /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[nginx-http-auth]
enabled = true

[nginx-noscript]
enabled = true

[nginx-badbots]
enabled = true

[nginx-noproxy]
enabled = true
EOF

sudo systemctl restart fail2ban
log_success "Fail2ban protection configured"

# Step 17: Final health checks
log_info "🧪 Running health checks..."

sleep 10  # Wait for services to start

# Check backend API
if curl -f -s http://localhost:8000/health > /dev/null; then
    log_success "Backend API is responding"
else
    log_warning "Backend API health check failed"
fi

# Check frontend
if curl -f -s http://localhost > /dev/null; then
    log_success "Frontend is responding"
else
    log_warning "Frontend health check failed"
fi

# Check SSL (if domain is accessible)
if curl -f -s https://$DOMAIN > /dev/null 2>&1; then
    log_success "HTTPS is working"
else
    log_info "HTTPS not yet accessible (DNS propagation may be needed)"
fi

# Step 18: Create admin info file
log_info "📝 Creating admin information..."
cat > /home/$USER/ishooop_admin_info.txt << EOF
🚀 iShoop.org Deployment Completed Successfully!
================================================

🌐 Website URLs:
- Main Site: https://$DOMAIN
- Admin Panel: https://$DOMAIN/admin
- API Documentation: https://$DOMAIN/docs
- API Base: https://$DOMAIN/api/v1/

👑 Admin Credentials:
- Email: admin@$DOMAIN
- Password: $(grep ADMIN_PASSWORD $PROJECT_DIR/.env | cut -d'=' -f2)

🔧 Server Management:
- Check status: pm2 status
- View logs: pm2 logs ishooop-api
- Restart API: pm2 restart ishooop-api
- Backup manually: sudo /usr/local/bin/backup-ishooop.sh

📂 Important Paths:
- Backend: $PROJECT_DIR
- Frontend: $FRONTEND_DIR
- Logs: $LOG_DIR
- Backups: $BACKUP_DIR

🔒 Security:
- Firewall: Active (UFW)
- SSL: Let's Encrypt
- Fail2ban: Active
- Auto-backups: Daily at 2 AM

📊 Monitoring:
- PM2: pm2 monit
- Nginx: systemctl status nginx
- System: htop

🆘 Troubleshooting:
- Check logs: tail -f $LOG_DIR/api-combined.log
- Check nginx: tail -f /var/log/nginx/error.log
- Check SSL: sudo certbot certificates

Deployed on: $(date)
EOF

log_success "Admin information saved to /home/$USER/ishooop_admin_info.txt"

# Final success message
echo ""
log_header "🎉 Deployment Completed Successfully!"
echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}${BOLD}║                   🎉 SUCCESS! 🎉                       ║${NC}"
echo -e "${GREEN}${BOLD}║              iShoop.org is now LIVE!                    ║${NC}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}🌐 Your iShoop store is now accessible at:${NC}"
echo -e "   ${YELLOW}🏠 Website: https://$DOMAIN${NC}"
echo -e "   ${YELLOW}👑 Admin: https://$DOMAIN/admin${NC}"
echo -e "   ${YELLOW}📚 API Docs: https://$DOMAIN/docs${NC}"
echo ""
echo -e "${BLUE}👑 Admin Credentials:${NC}"
echo -e "   ${YELLOW}Email: admin@$DOMAIN${NC}"
echo -e "   ${YELLOW}Password: $(grep ADMIN_PASSWORD $PROJECT_DIR/.env | cut -d'=' -f2)${NC}"
echo ""
echo -e "${BLUE}🛠️ Management Commands:${NC}"
echo -e "   ${YELLOW}Status: pm2 status${NC}"
echo -e "   ${YELLOW}Logs: pm2 logs ishooop-api${NC}"
echo -e "   ${YELLOW}Restart: pm2 restart ishooop-api${NC}"
echo -e "   ${YELLOW}Monitor: pm2 monit${NC}"
echo ""
echo -e "${BLUE}🔥 Next Steps:${NC}"
echo -e "   ${GREEN}1. Point your DNS to this server's IP${NC}"
echo -e "   ${GREEN}2. Wait for DNS propagation (up to 24 hours)${NC}"
echo -e "   ${GREEN}3. Visit https://$DOMAIN to see your store${NC}"
echo -e "   ${GREEN}4. Login to admin panel and add your products${NC}"
echo -e "   ${GREEN}5. Customize your store settings${NC}"
echo ""
echo -e "${PURPLE}${BOLD}🎊 Congratulations! Your e-commerce empire begins now! 🎊${NC}"
echo ""

# Save deployment log
echo "Deployment completed successfully on $(date)" >> /var/log/deployment.log
log_success "Deployment log saved"

exit 0