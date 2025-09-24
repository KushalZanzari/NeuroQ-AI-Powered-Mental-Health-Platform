@echo off
REM NeuroQ Development Startup Script for Windows
REM This script starts the development environment

echo 🚀 Starting NeuroQ Development Environment...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker and try again.
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Compose is not installed. Please install Docker Compose and try again.
    exit /b 1
)

REM Create necessary directories
echo [INFO] Creating necessary directories...
if not exist "ai_models" mkdir ai_models
if not exist "nginx\logs" mkdir nginx\logs
if not exist "nginx\ssl" mkdir nginx\ssl

REM Check if environment files exist
if not exist "backend\.env" (
    echo [WARNING] Backend .env file not found. Creating from template...
    copy backend\env.example backend\.env
    echo [WARNING] Please edit backend\.env with your configuration before continuing.
)

if not exist "frontend\.env" (
    echo [WARNING] Frontend .env file not found. Creating...
    echo REACT_APP_API_URL=http://localhost:8000 > frontend\.env
)

REM Start services
echo [INFO] Starting development services...
docker-compose up -d postgres redis

REM Wait for database to be ready
echo [INFO] Waiting for database to be ready...
timeout /t 10 /nobreak >nul

REM Start backend
echo [INFO] Starting backend service...
docker-compose up -d backend

REM Wait for backend to be ready
echo [INFO] Waiting for backend to be ready...
timeout /t 5 /nobreak >nul

REM Start frontend
echo [INFO] Starting frontend service...
docker-compose up -d frontend

REM Wait for frontend to be ready
echo [INFO] Waiting for frontend to be ready...
timeout /t 5 /nobreak >nul

echo.
echo [SUCCESS] 🎉 NeuroQ Development Environment is now running!
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo 🗄️  Database: localhost:5432 (neuroq_db)
echo 🔄 Redis: localhost:6379
echo.
echo To view logs: docker-compose logs -f
echo To stop: docker-compose down
echo.

REM Show running containers
echo [INFO] Running containers:
docker-compose ps

pause
