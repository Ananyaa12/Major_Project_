# Frontend React + Vite Setup & Deployment

## Prerequisites

- Node.js 16+ and npm
- Backend API running on http://localhost:5000

## Installation

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure API URL

Create a `.env` file in the frontend directory:

```
REACT_APP_API_URL=http://localhost:5000/api
```

For production:
```
REACT_APP_API_URL=https://your-backend-domain.com/api
```

### 4. Run Development Server

```bash
npm run dev
```

Application will be available at `http://localhost:3000`

## Build for Production

```bash
npm run build
```

This generates a `dist/` folder with optimized production build.

## Project Structure

```
frontend/
├── index.html                    # HTML entry point
├── package.json                  # Dependencies
├── vite.config.js               # Vite configuration
├── postcss.config.js            # PostCSS/Tailwind config
├── src/
│   ├── App.jsx                  # Main app component
│   ├── main.jsx                 # React entry point
│   ├── index.css                # Global styles
│   ├── components/
│   │   ├── Navigation.jsx       # Header/nav
│   │   └── Hero.jsx             # Landing hero
│   ├── pages/
│   │   ├── HomePage.jsx
│   │   ├── LoginPage.jsx
│   │   ├── DashboardPage.jsx
│   │   ├── PredictionPage.jsx
│   │   ├── FairnessPage.jsx
│   │   ├── AnalyticsPage.jsx
│   │   └── AboutPage.jsx
│   ├── services/
│   │   └── api.js               # API client
│   └── context/
│       └── AuthContext.jsx      # Auth state
```

## Key Features

### 1. Authentication
- JWT token-based authentication
- Token stored in localStorage
- Auto-logout on token expiration
- Protected routes

### 2. API Integration
- Axios client with interceptors
- Automatic token injection
- Error handling
- Service methods for all API endpoints

### 3. State Management
- React Context API for auth
- Local state with useState
- Form state with react-hook-form

### 4. UI Components
- Responsive design (mobile-first)
- Tailwind CSS styling
- Framer Motion animations
- Glass-morphism effects

### 5. Pages

#### Home Page
- Hero section
- Feature highlights
- Research statistics
- How it works section

#### Login Page
- Email/password form
- Form validation
- Error handling
- JWT token management

#### Dashboard Page
- Model performance metrics
- Dataset statistics
- Model comparison data
- Feature importance

#### Prediction Page
- 21-field input form for all BRFSS features
- Real-time prediction
- Risk level visualization
- Probability breakdown

#### Fairness Page
- Fairness evaluation report
- Bias detection across demographics
- Fairness metrics explanation

#### Analytics Page
- Model comparison table
- Feature importance rankings
- Model performance comparison

#### About Page
- Project overview
- Technology stack
- Dataset information
- Contact information

## Styling

### Tailwind CSS
Pre-configured with custom colors and utilities.

Global CSS classes:
- `.glass-effect` - Glassmorphism styling
- `.gradient-bg` - Gradient background
- `.fade-enter`, `.fade-exit` - Fade animations

### Responsive Breakpoints
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

## Form Handling

Using react-hook-form for efficient form management:

```jsx
const { register, handleSubmit, formState: { errors } } = useForm()

<input
  {...register('fieldName', { required: 'Field is required' })}
/>
{errors.fieldName && <p>{errors.fieldName.message}</p>}
```

## API Service Usage

```javascript
import { predictionService } from '../services/api'

// Make prediction
const response = await predictionService.predict({
  HighBP: 1,
  HighChol: 1,
  ...
})

const result = response.data
```

## Authentication Flow

1. User enters credentials on login page
2. Frontend sends POST request to `/api/auth/login`
3. Backend returns JWT token
4. Token stored in localStorage
5. Axios interceptor adds token to all requests
6. Protected routes check authentication
7. Logout clears token and redirects to home

## Development Tools

### Vite Configuration
- React plugin enabled
- Proxy to backend API
- Development server on port 3000
- Hot module replacement (HMR)

### ESLint Configuration
```bash
npm run lint
```

## Deployment

### Option 1: Vercel (Recommended)

1. Push code to GitHub
2. Import project on Vercel
3. Set environment variables:
   - REACT_APP_API_URL=https://your-backend.com/api
4. Deploy

### Option 2: GitHub Pages

```bash
npm run build
npm install -g gh-pages
npx gh-pages -d dist
```

### Option 3: Manual Hosting

1. Build the project: `npm run build`
2. Upload `dist/` folder to web server
3. Configure server to serve `index.html` for all routes

### Option 4: Docker

```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Build:
```bash
docker build -t diabetes-frontend .
docker run -p 80:80 diabetes-frontend
```

## Environment Variables

Development (`.env`):
```
REACT_APP_API_URL=http://localhost:5000/api
```

Production (set on deployment platform):
```
REACT_APP_API_URL=https://diabetes-api.onrender.com/api
```

## Troubleshooting

### Issue: CORS errors
Ensure backend has CORS enabled:
```python
from flask_cors import CORS
CORS(app)
```

### Issue: Token not persisting
Check localStorage:
```javascript
localStorage.getItem('authToken')
```

### Issue: API calls failing
Check:
1. Backend is running
2. API URL is correct
3. Network tab in browser devtools
4. CORS headers

### Issue: Build size too large
Optimize with:
```bash
npm install --save-dev webpack-bundle-analyzer
```

## Performance Optimization

1. Code splitting with React.lazy()
2. Image optimization
3. CSS minification (automatic with Tailwind)
4. Tree shaking in build
5. Lazy load routes

## Security Considerations

1. Store JWT securely (httpOnly cookies preferred in production)
2. Validate all input on frontend
3. Use HTTPS in production
4. Sanitize user input
5. Implement CSRF protection
6. Regular dependency updates: `npm audit fix`

## See Also

- DEPLOYMENT_GUIDE.md - Complete deployment instructions
- ML_PIPELINE_SETUP.md - Backend ML pipeline setup
- BACKEND_API_SETUP.md - Backend API documentation
