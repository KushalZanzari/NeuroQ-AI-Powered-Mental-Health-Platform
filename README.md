# NeuroQ - AI-Powered Mental Health Platform

NeuroQ is an AI-driven platform that helps users monitor and improve their mental well-being. It collects real-time inputs through mood check-ins and conversations, analyzes them using AI models, and provides personalized guidance, coping strategies, and progress reports. With 24/7 AI support, crisis resource integration, and personalized insights, NeuroQ empowers users to manage stress, anxiety, depression, and sleep issues while bridging the gap to professional mental health care
## 🌟 Features

### Frontend
- **User Authentication**: Secure signup, login, and password reset
- **Dark/Light Mode**: Toggle between themes for better user experience
- **Interactive Dashboard**: Mental health check-in forms with real-time analysis
- **AI Chatbot**: Real-time conversational AI for mental health support
- **WebSocket Communication**: Live chat functionality
- **Password Strength Meter**: Enhanced security features
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### Backend
- **FastAPI REST API**: High-performance, modern Python web framework
- **JWT Authentication**: Secure token-based authentication
- **PostgreSQL Database**: Robust relational database with proper indexing
- **WebSocket Support**: Real-time bidirectional communication
- **AI Model Integration**: Machine learning models for mental health prediction
- **Rate Limiting & Security**: Protection against abuse and attacks
- **Comprehensive Logging**: Detailed logging for monitoring and debugging

### AI/ML Capabilities
- **Mental Health Prediction**: Multi-class classification for various disorders
- **Interactive Chatbot**: Context-aware conversational AI
- **Personalized Guidance**: Tailored recommendations based on user input
- **Confidence Scoring**: Transparent AI decision-making process
- **Severity Assessment**: Risk level evaluation and emergency detection

## 🏗️ Project Structure

```
NeuroQ/
├── frontend/              # React.js frontend application
│   ├── public/           # Static assets
│   ├── src/              # Source code
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API integration
│   │   ├── store/        # State management (Zustand)
│   │   └── contexts/     # React contexts
│   ├── package.json      # Dependencies
│   └── Dockerfile        # Frontend container
├── backend/              # FastAPI backend application
│   ├── app/              # Application code
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core configuration
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── websocket/    # WebSocket handlers
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Backend container
├── ai_models/            # AI/ML models and utilities
├── database/             # Database schemas and migrations
├── nginx/                # Nginx configuration
├── scripts/              # Startup and utility scripts
├── docs/                 # Documentation
├── docker-compose.yml    # Development environment
└── docker-compose.prod.yml # Production environment
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- PostgreSQL 13+ (for local development)

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd NeuroQ
   ```

2. **Start the development environment**
   ```bash
   # Windows
   scripts/start-dev.bat
   
   # Linux/macOS
   ./scripts/start-dev.sh
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Local Development

1. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Database Setup**
   ```bash
   # Install PostgreSQL and create database
   createdb neuroq_db
   psql neuroq_db < database/init.sql
   ```

## 🛠️ Tech Stack

### Frontend
- **React.js 18** - Modern UI library
- **Tailwind CSS** - Utility-first CSS framework
- **Zustand** - Lightweight state management
- **React Hook Form** - Form handling
- **Axios** - HTTP client
- **React Router** - Client-side routing
- **Framer Motion** - Animation library

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **JWT** - Authentication tokens
- **WebSockets** - Real-time communication
- **Redis** - Caching and rate limiting

### Database
- **PostgreSQL 15** - Primary database
- **Redis 7** - Caching and session storage

### AI/ML
- **PyTorch** - Deep learning framework
- **Transformers** - Pre-trained language models
- **scikit-learn** - Machine learning utilities
- **OpenAI API** - Advanced AI capabilities

### Deployment
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy and load balancer
- **Prometheus** - Monitoring
- **Grafana** - Visualization

## 📚 Documentation

- [Development Guide](docs/DEVELOPMENT.md) - Detailed development setup and workflow
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment instructions
- [API Documentation](http://localhost:8000/docs) - Interactive API documentation

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/neuroq_db
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
REDIS_URL=redis://localhost:6379
DEBUG=True
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000
```

#### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest
pytest --cov=app tests/
```

### Frontend Testing
```bash
cd frontend
npm test
npm test -- --coverage
```

## 🚀 Deployment

### Production Deployment
```bash
# Using Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Using Kubernetes
kubectl apply -f k8s/
```

### Cloud Providers
- **Heroku**: See deployment guide for Heroku setup
- **AWS**: ECS, EKS, or EC2 deployment options
- **Google Cloud**: Cloud Run or GKE deployment
- **Azure**: Container Instances or AKS deployment

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Input validation and sanitization
- Rate limiting and DDoS protection
- CORS configuration
- Security headers
- SQL injection prevention
- XSS protection

## 📊 Monitoring

- Health check endpoints
- Prometheus metrics
- Grafana dashboards
- Application logging
- Error tracking
- Performance monitoring



## 🙏 Acknowledgments

- FastAPI team for the excellent web framework
- React team for the powerful UI library
- Tailwind CSS team for the utility-first CSS framework
- The open-source community for various libraries and tools

---

**⚠️ Disclaimer**: This platform is for informational and supportive purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with questions about medical conditions.
