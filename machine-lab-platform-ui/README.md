# Machine Lab Platform UI

Optional web interface for the SiberBox platform. This Vue.js application provides a dashboard for direct interaction with the Machine Lab Manager API, primarily designed for testing, demonstration, and administrative purposes.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Development](#development)
- [Deployment](#deployment)
- [API Integration](#api-integration)
- [Usage Guide](#usage-guide)
- [Troubleshooting](#troubleshooting)

## Overview

The Machine Lab Platform UI is an **optional** component that provides:

- **Administrative Dashboard**: Web interface for platform management
- **Container Management**: Visual interface for deploying and managing lab environments
- **Host Monitoring**: Real-time view of host status and resource usage
- **User Management**: Interface for authentication and access control
- **Testing Interface**: Convenient way to test API functionality

> **Important Note**: The Machine Lab Manager API is designed to be integrated with larger educational or training platforms. This web UI is primarily for testing, demonstration, or direct interaction scenarios.

## Features

### Core Interface Components
- ✅ **Authentication Dashboard**: Admin login and session management
- ✅ **Host Management Interface**: View and manage container hosts
- ✅ **Container Operations**: Deploy, monitor, and manage lab environments
- ✅ **Real-time Monitoring**: Live status updates and resource usage
- ✅ **Responsive Design**: Mobile-friendly interface using Vuetify
- ✅ **API Documentation Access**: Direct links to Swagger documentation

### User Experience Features
- ✅ **Intuitive Navigation**: Clean, professional interface design
- ✅ **Real-time Updates**: Live data refresh and status monitoring
- ✅ **Error Handling**: User-friendly error messages and notifications
- ✅ **Form Validation**: Client-side validation for all inputs
- ✅ **Loading States**: Visual feedback for all operations

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Vue.js Frontend Application                │
├─────────────────────────────────────────────────────────────┤
│  Vue Router + Vuex Store                                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │    Auth     │ │    Host     │ │ Container   │            │
│  │   Module    │ │  Management │ │ Management  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ Navigation  │ │    API      │ │   Utils     │            │
│  │    Bar      │ │  Services   │ │  & Helpers  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
├─────────────────────────────────────────────────────────────┤
│  API Integration Layer                                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │   Axios     │ │    Auth     │ │   Error     │            │
│  │   Client    │ │ Interceptor │ │  Handling   │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
├─────────────────────────────────────────────────────────────┤
│  Machine Lab Manager API                                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │    Auth     │ │    Hosts    │ │ Containers  │            │
│  │     API     │ │     API     │ │     API     │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Node.js 16+ and npm
- Machine Lab Manager running and accessible
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Quick Setup

1. **Clone and Navigate**
   ```bash
   git clone https://github.com/rafliher/machine-lab-platform.git
   cd machine-lab-platform/machine-lab-platform-ui
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   nano .env
   ```

4. **Start Development Server**
   ```bash
   npm run serve
   ```

5. **Access Application**
   
   Open http://localhost:8080 in your browser

### Production Build

For production deployment:

```bash
# Build optimized production bundle
npm run build

# Serve using a web server (nginx, apache, etc.)
# Built files will be in the 'dist/' directory
```

## Configuration

### Environment Variables

Create a `.env` file with the following configuration:

```bash
# API Configuration
VUE_APP_API_BASE_URL=https://your-manager-domain.com

# Optional: Application Settings
VUE_APP_TITLE=SiberBox Platform
VUE_APP_VERSION=1.0.0

# Optional: Feature Flags
VUE_APP_ENABLE_DEBUG=false
VUE_APP_SHOW_API_DOCS_LINK=true

# Optional: UI Customization
VUE_APP_THEME_COLOR=#1976D2
VUE_APP_LOGO_URL=/logo.png
```

### Development Configuration

For local development with hot-reload:

```bash
# .env.development
VUE_APP_API_BASE_URL=http://localhost:8000
VUE_APP_ENABLE_DEBUG=true
VUE_APP_LOG_LEVEL=debug
```

### Production Configuration

For production deployment:

```bash
# .env.production
VUE_APP_API_BASE_URL=https://api.siberbox.com
VUE_APP_ENABLE_DEBUG=false
VUE_APP_LOG_LEVEL=error
```

## Development

### Development Server

Start the development server with hot-reload:

```bash
npm run serve
```

The application will be available at http://localhost:8080 with:
- Hot module replacement for instant updates
- Vue DevTools integration
- Source maps for debugging
- Development error overlay

### Code Structure

```
src/
├── components/          # Reusable Vue components
│   ├── ContainerDetail.vue
│   ├── ContainerForm.vue
│   ├── HostForm.vue
│   ├── HostItem.vue
│   └── NavigationBar.vue
├── layouts/            # Layout components
│   └── MainLayout.vue
├── pages/              # Page components
│   ├── AuthenticationPage.vue
│   ├── DashboardPage.vue
│   ├── HostManagement.vue
│   └── LoginPage.vue
├── router/             # Vue Router configuration
│   └── index.js
├── services/           # API service modules
│   ├── api.js
│   ├── apiContainerService.js
│   ├── apiHostService.js
│   ├── apiUserService.js
│   └── authService.js
├── store/              # Vuex store modules
│   ├── index.js
│   └── modules/
│       └── auth.js
├── utils/              # Utility functions
│   └── auth.js
├── assets/             # Static assets
└── main.js             # Application entry point
```

### Development Commands

```bash
# Install dependencies
npm install

# Start development server
npm run serve

# Build for production
npm run build

# Run linter
npm run lint

# Fix linting issues
npm run lint --fix

# Run unit tests (if configured)
npm run test:unit

# Run end-to-end tests (if configured)
npm run test:e2e
```

### Code Style

The project uses:
- **ESLint**: For code linting and style enforcement
- **Prettier**: For code formatting
- **Vue Style Guide**: Following Vue.js official style guide

## Deployment

### Static File Hosting

Deploy as static files to any web server:

```bash
# Build production bundle
npm run build

# Deploy 'dist/' directory to your web server
cp -r dist/* /var/www/html/
```

### Nginx Configuration

Example nginx configuration:

```nginx
server {
    listen 80;
    server_name ui.siberbox.com;
    root /var/www/siberbox-ui;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass https://api.siberbox.com/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
```

### Docker Deployment

Deploy using Docker:

```dockerfile
# Dockerfile
FROM node:16-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```bash
# Build and run
docker build -t siberbox-ui .
docker run -d -p 80:80 siberbox-ui
```

### CDN Deployment

Deploy to CDN services:

```bash
# AWS S3 + CloudFront
aws s3 sync dist/ s3://your-bucket-name --delete
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"

# Netlify
netlify deploy --prod --dir=dist

# Vercel
vercel --prod
```

## API Integration

### Authentication Flow

The UI integrates with the Manager API authentication:

```javascript
// Login flow
async login(email, password) {
  const response = await api.post('/auth/login', { email, password });
  const { admin_key } = response.data;
  
  // Store admin key for subsequent requests
  localStorage.setItem('admin_key', admin_key);
  api.defaults.headers.common['X-Admin-Key'] = admin_key;
  
  return response.data;
}
```

### API Service Integration

Example API service usage:

```javascript
// services/apiHostService.js
import api from './api';

export default {
  async getHosts() {
    const response = await api.get('/hosts/');
    return response.data;
  },

  async createHost(hostData) {
    const response = await api.post('/hosts/', hostData);
    return response.data;
  },

  async deleteHost(hostId) {
    await api.delete(`/hosts/${hostId}`);
  }
};
```

### Error Handling

Centralized error handling:

```javascript
// api.js
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Redirect to login
      router.push('/login');
    }
    
    // Show user-friendly error message
    showErrorNotification(error.response?.data?.message || 'An error occurred');
    
    return Promise.reject(error);
  }
);
```

## Usage Guide

### Admin Login

1. **Access Application**: Navigate to the UI URL
2. **Login**: Use admin credentials configured in the Manager
3. **Dashboard**: View system overview and navigation options

### Host Management

1. **View Hosts**: Navigate to Host Management page
2. **Add Host**: Click "Add Host" and fill in host details
3. **Monitor Status**: View real-time host health and resource usage
4. **Remove Host**: Use delete action for unused hosts

### Container Operations

1. **Deploy Environment**: 
   - Navigate to Container Management
   - Upload deployment package (ZIP file)
   - Select target user ID
   - Deploy to available host

2. **Monitor Containers**:
   - View all active containers
   - Check deployment status
   - Monitor resource usage

3. **Manage Containers**:
   - Restart containers as needed
   - Stop and remove completed environments
   - View container details and logs

### System Monitoring

1. **Dashboard Overview**: Real-time system health
2. **Host Status**: Individual host monitoring
3. **Resource Usage**: CPU, memory, container count
4. **Alert Notifications**: System status changes

## Troubleshooting

### Common Issues

#### 1. API Connection Failed

**Symptoms**: Cannot connect to Manager API, authentication errors

**Solutions**:
```bash
# Check API URL configuration
echo $VUE_APP_API_BASE_URL

# Test API connectivity
curl https://your-manager-domain.com/health

# Verify CORS configuration in Manager
# Check browser console for CORS errors

# Test authentication
curl -X POST "https://your-manager-domain.com/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "password"}'
```

#### 2. Build Failures

**Symptoms**: npm run build fails, dependency errors

**Solutions**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node.js version
node --version  # Should be 16+

# Update dependencies
npm update
npm audit fix
```

#### 3. Runtime Errors

**Symptoms**: Application crashes, console errors

**Solutions**:
```bash
# Enable debug mode
echo "VUE_APP_ENABLE_DEBUG=true" >> .env.local

# Check console logs in browser
# Open Developer Tools -> Console

# Check network tab for API errors
# Open Developer Tools -> Network

# Verify environment configuration
npm run serve -- --mode development
```

#### 4. Authentication Issues

**Symptoms**: Login fails, session expires

**Solutions**:
```javascript
// Check localStorage for stored tokens
console.log(localStorage.getItem('admin_key'));

// Clear stored authentication
localStorage.removeItem('admin_key');

// Verify API response format
// Check Network tab in browser DevTools

// Test authentication manually
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "password"}'
```

### Development Debugging

#### Vue DevTools

Install Vue DevTools browser extension for debugging:
- Component inspection
- Vuex state monitoring
- Event tracking
- Performance profiling

#### Console Debugging

Enable debug logging:

```javascript
// In main.js or component
if (process.env.VUE_APP_ENABLE_DEBUG === 'true') {
  console.log('Debug mode enabled');
  window.app = app; // Access app instance in console
}
```

### Performance Optimization

#### Build Optimization

```javascript
// vue.config.js
module.exports = {
  productionSourceMap: false,
  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: 'all',
      },
    },
  },
};
```

#### Network Optimization

```javascript
// Enable API response caching
api.defaults.headers.common['Cache-Control'] = 'max-age=300';

// Implement request debouncing
import { debounce } from 'lodash';
const debouncedSearch = debounce(this.searchHosts, 300);
```

### Security Considerations

#### Content Security Policy

```html
<!-- In public/index.html -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-eval'; 
               style-src 'self' 'unsafe-inline';
               connect-src 'self' https://your-api-domain.com;">
```

#### Environment Variables

```bash
# Never commit sensitive data to .env files
# Use .env.local for local development secrets
echo ".env.local" >> .gitignore

# For production, set environment variables at build time
VUE_APP_API_BASE_URL=https://api.production.com npm run build
```

### Support Resources

- **Vue.js Documentation**: [Vue.js Guide](https://vuejs.org/guide/)
- **Vuetify Documentation**: [Vuetify Components](https://vuetifyjs.com/en/components/)
- **Manager API Documentation**: Available at manager's `/api-docs` endpoint
- **GitHub Issues**: [Report bugs and feature requests](https://github.com/rafliher/machine-lab-platform/issues)

> **Integration Note**: This web UI is designed for testing and demonstration purposes. For production educational platforms, consider integrating the Machine Lab Manager API directly with your existing Learning Management System (LMS) or training platform rather than using this standalone web interface.

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
