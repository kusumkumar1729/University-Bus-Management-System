#!/bin/bash
# Exit on error
set -e

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🧱 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Build complete."
