#!/bin/bash

echo "🔧 اجرای محیط توسعه..."

# Start services
docker-compose up -d db redis

echo "⏳ انتظار برای آماده شدن سرویس‌ها..."
sleep 5

# Start backend in development mode
echo "🚀 شروع Backend..."
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &

# Start frontend in development mode
echo "🎨 شروع Frontend..."
cd ../frontend
npm install
npm start &

echo "✅ محیط توسعه آماده است!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔗 Backend: http://localhost:8000"

wait