# NeuroQ Development Guide

This guide covers how to set up and develop the NeuroQ platform locally.

## Project Structure

```
NeuroQ/
├── frontend/              # React.js frontend application
│   ├── public/           # Static assets
│   ├── src/              # Source code
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── store/        # State management
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
├── docker/               # Docker configuration
├── docs/                 # Documentation
└── docker-compose.yml    # Multi-container setup
```

## Prerequisites

### Required Software

- **Node.js** (v18 or higher)
- **Python** (v3.11 or higher)
- **PostgreSQL** (v13 or higher)
- **Redis** (v6 or higher)
- **Docker** (optional, for containerized development)

### Development Tools

- **Git** for version control
- **VS Code** or your preferred IDE
- **Postman** or **Insomnia** for API testing
- **pgAdmin** or **DBeaver** for database management

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd NeuroQ
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Database Setup

1. **Install PostgreSQL**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   
   # macOS (with Homebrew)
   brew install postgresql
   
   # Windows
   # Download from https://www.postgresql.org/download/windows/
   ```

2. **Create Database**
   ```bash
   # Connect to PostgreSQL
   sudo -u postgres psql
   
   # Create database and user
   CREATE DATABASE neuroq_db;
   CREATE USER neuroq_user WITH PASSWORD 'neuroq_password';
   GRANT ALL PRIVILEGES ON DATABASE neuroq_db TO neuroq_user;
   \q
   ```

3. **Run Database Migrations**
   ```bash
   cd backend
   alembic upgrade head
   ```

#### Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env with your configuration
DATABASE_URL=postgresql://neuroq_user:neuroq_password@localhost:5432/neuroq_db
SECRET_KEY=your-secret-key-here
DEBUG=True
```

#### Start Backend Server

```bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
python -m uvicorn app.main:app --reload
```

### 3. Frontend Setup

#### Install Node.js Dependencies

```bash
cd frontend

# Install dependencies
npm install

# Or using yarn
yarn install
```

#### Environment Configuration

```bash
# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000" > .env
```

#### Start Frontend Development Server

```bash
# Start development server
npm start

# Or using yarn
yarn start
```

### 4. Redis Setup (Optional)

```bash
# Install Redis
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS (with Homebrew)
brew install redis

# Start Redis
redis-server
```

## Development Workflow

### 1. Code Structure

#### Backend Development

- **Models**: Define database models in `app/models/`
- **Schemas**: Create Pydantic schemas in `app/schemas/`
- **API Endpoints**: Add routes in `app/api/v1/endpoints/`
- **Services**: Implement business logic in `app/services/`

#### Frontend Development

- **Components**: Create reusable components in `src/components/`
- **Pages**: Add new pages in `src/pages/`
- **Services**: API integration in `src/services/`
- **Store**: State management in `src/store/`

### 2. Database Development

#### Creating Migrations

```bash
cd backend

# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

#### Model Development

```python
# Example model in app/models/example.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Example(Base):
    __tablename__ = "examples"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

### 3. API Development

#### Creating New Endpoints

```python
# Example endpoint in app/api/v1/endpoints/example.py
from fastapi import APIRouter, Depends
from app.schemas.example import ExampleCreate, Example
from app.services.example_service import ExampleService

router = APIRouter()

@router.post("/", response_model=Example)
def create_example(example: ExampleCreate, db: Session = Depends(get_db)):
    return ExampleService.create_example(db, example)
```

#### Testing APIs

```bash
# Using curl
curl -X POST "http://localhost:8000/api/v1/examples" \
     -H "Content-Type: application/json" \
     -d '{"name": "Test Example"}'

# Using Python requests
import requests

response = requests.post(
    "http://localhost:8000/api/v1/examples",
    json={"name": "Test Example"}
)
print(response.json())
```

### 4. Frontend Development

#### Creating New Components

```jsx
// Example component in src/components/Example/Example.js
import React from 'react';

const Example = ({ title, description }) => {
  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">{title}</h3>
      </div>
      <div className="card-content">
        <p>{description}</p>
      </div>
    </div>
  );
};

export default Example;
```

#### State Management

```javascript
// Example store in src/store/exampleStore.js
import { create } from 'zustand';

const useExampleStore = create((set) => ({
  examples: [],
  loading: false,
  
  fetchExamples: async () => {
    set({ loading: true });
    try {
      const response = await api.get('/examples');
      set({ examples: response.data, loading: false });
    } catch (error) {
      set({ loading: false });
    }
  },
}));

export default useExampleStore;
```

## Testing

### Backend Testing

```bash
cd backend

# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

### Frontend Testing

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## Code Quality

### Backend Code Quality

```bash
# Install development dependencies
pip install black isort flake8 mypy

# Format code
black app/
isort app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

### Frontend Code Quality

```bash
# Install development dependencies
npm install --save-dev eslint prettier

# Format code
npm run format

# Lint code
npm run lint

# Fix linting issues
npm run lint:fix
```

## Debugging

### Backend Debugging

1. **Use Debugger**
   ```python
   import pdb; pdb.set_trace()
   ```

2. **Logging**
   ```python
   import logging
   logger = logging.getLogger(__name__)
   logger.info("Debug message")
   ```

3. **API Documentation**
   - Visit http://localhost:8000/docs for interactive API docs
   - Visit http://localhost:8000/redoc for alternative documentation

### Frontend Debugging

1. **React Developer Tools**
   - Install browser extension
   - Inspect components and state

2. **Console Logging**
   ```javascript
   console.log('Debug message', data);
   ```

3. **Network Tab**
   - Monitor API calls
   - Check request/response data

## Performance Optimization

### Backend Optimization

1. **Database Queries**
   - Use eager loading
   - Add database indexes
   - Optimize query patterns

2. **Caching**
   - Implement Redis caching
   - Use response caching
   - Cache expensive operations

3. **Async Operations**
   - Use async/await
   - Implement background tasks
   - Use connection pooling

### Frontend Optimization

1. **Bundle Optimization**
   - Code splitting
   - Lazy loading
   - Tree shaking

2. **Performance Monitoring**
   - Use React DevTools Profiler
   - Monitor bundle size
   - Optimize images

3. **State Management**
   - Minimize re-renders
   - Use memoization
   - Optimize selectors

## Common Issues and Solutions

### Database Connection Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -h localhost -U neuroq_user -d neuroq_db
```

### Port Conflicts

```bash
# Check port usage
netstat -tulpn | grep :8000
netstat -tulpn | grep :3000

# Kill process using port
sudo kill -9 $(lsof -t -i:8000)
```

### Dependency Issues

```bash
# Backend
pip install --upgrade pip
pip install -r requirements.txt

# Frontend
rm -rf node_modules package-lock.json
npm install
```

## Contributing

### Git Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Make Changes**
   - Write code
   - Add tests
   - Update documentation

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

4. **Push and Create PR**
   ```bash
   git push origin feature/new-feature
   ```

### Code Standards

1. **Commit Messages**
   - Use conventional commits
   - Be descriptive and concise

2. **Code Style**
   - Follow existing patterns
   - Use consistent naming
   - Add comments for complex logic

3. **Testing**
   - Write tests for new features
   - Maintain test coverage
   - Test edge cases

## Resources

### Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Tools

- [Postman](https://www.postman.com/) - API testing
- [pgAdmin](https://www.pgadmin.org/) - Database management
- [Redis Commander](https://github.com/joeferner/redis-commander) - Redis management
- [Docker Desktop](https://www.docker.com/products/docker-desktop) - Container management

### Learning Resources

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [React Tutorial](https://reactjs.org/tutorial/tutorial.html)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Zustand Documentation](https://github.com/pmndrs/zustand)
