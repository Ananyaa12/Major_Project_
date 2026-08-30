# Complete Deployment Guide

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Backend Deployment (Render)](#backend-deployment-render)
3. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
4. [Database Setup (MongoDB Atlas)](#database-setup-mongodb-atlas)
5. [Production Checklist](#production-checklist)
6. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Local Development Setup

### Step 1: Clone & Install

```bash
# Clone repository
git clone https://github.com/yourusername/diabetes-prediction.git
cd diabetes-prediction

# Create Python virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Or macOS/Linux
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
```

### Step 2: Train ML Models

```bash
# From project root
cd ..
python train_pipeline.py
```

Expected output:
- Models saved in `ml_pipeline/trained_models/`
- Results in `ml_pipeline/results/`
- Training takes 15-30 minutes

### Step 3: Run Locally

**Terminal 1 - Backend**:
```bash
cd backend
python app.py
# API at http://localhost:5000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
# App at http://localhost:3000
```

### Step 4: Test

1. Open http://localhost:3000
2. Click "Get Started"
3. Login with demo credentials
4. Make a prediction

---

## Backend Deployment (Render)

### Prerequisites
- GitHub account with code pushed
- Render account (https://render.com)
- Trained ML models

### Step 1: Prepare Backend for Deployment

Create `backend/requirements.txt` if not exists:
```bash
# Add to backend/requirements.txt
flask==3.0.0
flask-cors==4.0.0
pyjwt==2.8.1
joblib==1.3.2
numpy==1.24.3
pandas==2.1.3
scikit-learn==1.3.2
xgboost==2.0.1
lightgbm==4.1.1
catboost==1.2.2
```

Create `backend/gunicorn.conf.py`:
```python
workers = 4
worker_class = "sync"
bind = "0.0.0.0:5000"
timeout = 120
```

### Step 2: Push to GitHub

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 3: Create Render Web Service

1. Log in to [Render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect GitHub repository
4. Configure:
   - **Name**: `diabetes-api`
   - **Runtime**: `Python 3.10`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app`

### Step 4: Set Environment Variables

In Render dashboard, add Environment Variables:
```
SECRET_KEY=your-random-secret-key-here
FLASK_ENV=production
```

### Step 5: Deploy

1. Click "Deploy"
2. Wait for build and deployment (5-10 minutes)
3. Render will provide your API URL: `https://diabetes-api-xxxxx.onrender.com`
4. Add health check endpoint
5. Enable auto-deploy on push

### Troubleshooting

**Issue**: `ModuleNotFoundError`
- Ensure all dependencies are in requirements.txt
- Check `pip list` locally

**Issue**: Models not found
- Upload trained models to GitHub
- Or rebuild models in Render

**Issue**: Slow response
- Check logs: Render Dashboard → Logs
- Increase worker count (paid tier only)

---

## Frontend Deployment (Vercel)

### Prerequisites
- GitHub account with code pushed
- Vercel account (https://vercel.com)
- Backend API URL (from Render)

### Step 1: Configure Frontend

Update `frontend/.env.production`:
```
REACT_APP_API_URL=https://diabetes-api-xxxxx.onrender.com/api
```

### Step 2: Build Locally to Test

```bash
cd frontend
npm run build
npm run preview
```

### Step 3: Push to GitHub

```bash
git add .
git commit -m "Configure production environment"
git push origin main
```

### Step 4: Deploy to Vercel

1. Go to [Vercel.com](https://vercel.com)
2. Click "New Project"
3. Import GitHub repository
4. Configure:
   - **Framework Preset**: React
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

### Step 5: Add Environment Variables

In Vercel project settings:
```
REACT_APP_API_URL=https://diabetes-api-xxxxx.onrender.com/api
```

### Step 6: Deploy

1. Click "Deploy"
2. Wait for build (2-5 minutes)
3. Vercel provides your URL: `https://diabetes-prediction.vercel.app`
4. Enable auto-deploy on push

### Custom Domain (Optional)

In Vercel project settings → Domains:
```
Add your custom domain
DNS configuration will be provided
```

---

## Database Setup (MongoDB Atlas)

### Step 1: Create MongoDB Atlas Account

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up (free tier available)
3. Create new organization

### Step 2: Create Cluster

1. Click "Create a Deployment"
2. Choose **Shared** (free tier)
3. Select region closest to your users
4. Cluster name: `diabetes-db`
5. Create cluster (5-10 minutes)

### Step 3: Create Database User

1. In MongoDB Atlas, go to Database Access
2. Add new database user:
   - Username: `diabetes_user`
   - Password: Generate strong password
   - Permissions: Read/write to any database
3. Add user

### Step 4: Configure Network Access

1. Go to Network Access
2. Click "Add IP Address"
3. Options:
   - **Development**: 0.0.0.0/0 (allow all)
   - **Production**: Add specific Render IP

### Step 5: Get Connection String

1. Click "Connect" on cluster
2. Choose "Drivers"
3. Language: Python
4. Copy connection string:
```
mongodb+srv://diabetes_user:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### Step 6: Update Backend Configuration

In `backend/app.py`, add MongoDB connection:
```python
from pymongo import MongoClient

MONGODB_URI = os.environ.get(
    'MONGODB_URI',
    'mongodb+srv://user:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority'
)

client = MongoClient(MONGODB_URI)
db = client['diabetes_db']

# Collections
users_collection = db['users']
predictions_collection = db['predictions']
recommendations_collection = db['recommendations']
```

### Step 7: Add to Render Environment

In Render project settings, add:
```
MONGODB_URI=mongodb+srv://diabetes_user:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

---

## Production Checklist

### Security
- [ ] Change SECRET_KEY to random value
- [ ] Use HTTPS everywhere
- [ ] Set FLASK_ENV=production
- [ ] Enable CORS only for frontend domain
- [ ] Add rate limiting
- [ ] Validate all inputs
- [ ] Use strong passwords
- [ ] Enable MongoDB IP whitelist

### Performance
- [ ] Enable caching headers
- [ ] Compress responses
- [ ] Optimize images
- [ ] Enable CDN for frontend
- [ ] Add monitoring/alerts
- [ ] Set up auto-scaling

### Monitoring
- [ ] Set up error logging (Sentry)
- [ ] Monitor API response times
- [ ] Track uptime
- [ ] Alert on failures
- [ ] Regular backups

### Documentation
- [ ] Document API endpoints
- [ ] Create admin guide
- [ ] Update README with production URLs
- [ ] Document deployment process

---

## Production URLs

After deployment, update frontend `.env.production`:

```
REACT_APP_API_URL=https://your-api-domain.com/api
```

Update any documentation:
- README.md
- API docs
- Frontend code

---

## Monitoring & Maintenance

### Set Up Error Tracking (Sentry)

```bash
# Install Sentry SDK
pip install sentry-sdk[flask]
npm install @sentry/react
```

Backend configuration:
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    environment="production"
)
```

### Monitor Performance

Use tools:
- **Vercel Analytics** - Frontend performance
- **Render Logs** - Backend errors
- **MongoDB Charts** - Database metrics

### Regular Maintenance

1. **Weekly**:
   - Check error logs
   - Monitor API response times
   - Review database disk usage

2. **Monthly**:
   - Update dependencies: `pip list --outdated`
   - Review security updates
   - Backup database
   - Check costs

3. **Quarterly**:
   - Load testing
   - Security audit
   - Performance optimization
   - Update documentation

### Updating Deployment

**For Backend**:
```bash
# Make changes
git add .
git commit -m "Update backend"
git push origin main
# Render auto-deploys
```

**For Frontend**:
```bash
# Make changes
git add .
git commit -m "Update frontend"
git push origin main
# Vercel auto-deploys
```

**For ML Models**:
```bash
# Retrain models
python train_pipeline.py
# Upload to GitHub
git add ml_pipeline/trained_models/
git commit -m "Update ML models"
git push origin main
# Render redeploys with new models
```

### Scaling

**If frontend is slow**:
- Upgrade Vercel to Pro (auto-scaling)
- Enable edge caching

**If API is slow**:
- Upgrade Render to Standard (more resources)
- Add database indexing
- Implement caching

**If database is slow**:
- Upgrade MongoDB to dedicated cluster
- Add indexes
- Optimize queries

---

## Rollback Procedure

If deployment has issues:

**Frontend (Vercel)**:
1. Vercel Dashboard → Deployments
2. Find previous working deployment
3. Click "Redeploy"

**Backend (Render)**:
1. Render Dashboard → Deploys
2. Click previous successful deploy
3. Click "Redeploy"

---

## FAQ

**Q: How long does deployment take?**
A: Frontend (2-5 min), Backend (5-10 min), Database (instant)

**Q: Can I use free tier for production?**
A: Not recommended. Free tiers have limitations:
- Render: Spins down after 15 min inactivity
- Vercel: 100GB/month bandwidth
- MongoDB: 5GB storage limit

**Q: How do I update the dataset?**
A: Models are built from CSV. To update:
1. Replace CSV file
2. Run `python train_pipeline.py`
3. Push new models to GitHub
4. Backend automatically redeploys

**Q: Can I run this on my own server?**
A: Yes. Use Docker or direct installation on any server.

---

## Support

- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- MongoDB Docs: https://docs.mongodb.com
- Flask Docs: https://flask.palletsprojects.com

## Next Steps

1. ✅ Complete all deployment steps
2. ✅ Test all features in production
3. ✅ Set up monitoring
4. ✅ Create backup strategy
5. ✅ Document for team

Your system is now live! 🚀
