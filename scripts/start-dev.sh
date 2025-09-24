#!/bin/bash

# NeuroQ Development Startup Script
# This script starts the development environment

set -e

echo "🚀 Starting NeuroQ Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p ai_models
mkdir -p nginx/logs
mkdir -p nginx/ssl

# Check if environment files exist
if [ ! -f "backend/.env" ]; then
    print_warning "Backend .env file not found. Creating from template..."
    cp backend/env.example backend/.env
    print_warning "Please edit backend/.env with your configuration before continuing."
fi

if [ ! -f "frontend/.env" ]; then
    print_warning "Frontend .env file not found. Creating..."
    echo "REACT_APP_API_URL=http://localhost:8000" > frontend/.env
fi

# Start services
print_status "Starting development services..."
docker-compose up -d postgres redis

# Wait for database to be ready
print_status "Waiting for database to be ready..."
sleep 10

# Check if database is ready
while ! docker-compose exec postgres pg_isready -U neuroq_user -d neuroq_db > /dev/null 2>&1; do
    print_status "Waiting for database..."
    sleep 2
done

print_success "Database is ready!"

# Start backend
print_status "Starting backend service..."
docker-compose up -d backend

# Wait for backend to be ready
print_status "Waiting for backend to be ready..."
sleep 5

# Check if backend is ready
while ! curl -f http://localhost:8000/health > /dev/null 2>&1; do
    print_status "Waiting for backend..."
    sleep 2
done

print_success "Backend is ready!"

# Start frontend
print_status "Starting frontend service..."
docker-compose up -d frontend

# Wait for frontend to be ready
print_status "Waiting for frontend to be ready..."
sleep 5

# Check if frontend is ready
while ! curl -f http://localhost:3000 > /dev/null 2>&1; do
    print_status "Waiting for frontend..."
    sleep 2
done

print_success "Frontend is ready!"

echo ""
print_success "🎉 NeuroQ Development Environment is now running!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🗄️  Database: localhost:5432 (neuroq_db)"
echo "🔄 Redis: localhost:6379"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
echo ""

# Show running containers
print_status "Running containers:"
docker-compose ps
