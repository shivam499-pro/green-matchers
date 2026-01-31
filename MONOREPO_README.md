# 🏗️ Green Matchers Monorepo

**Industry-Grade Monorepo Structure for the AI-Powered Green Jobs Platform**

## 🎯 Overview

This monorepo contains the **complete Green Matchers platform** including:
- **Backend** (FastAPI)
- **Web Frontend** (React + Vite)
- **Shared Packages** (API, UI, Hooks, etc.)

## 🚀 Monorepo Benefits

### **1. Code Reusability**
- **Shared API client** for web applications
- **Shared business logic** and utilities
- **Single source of truth** for types and constants

### **2. Development Efficiency**
- **One command** to install all dependencies
- **Single lint/test** configuration
- **Consistent** code style across all apps
- **Easier refactoring** when changes affect multiple apps

### **3. Deployment & CI/CD**
- **Single pipeline** for all apps
- **Atomic deployments** with version synchronization
- **Easier dependency management**
- **Better caching** of shared dependencies

### **4. Scalability**
- **Add new apps** easily (admin panel, etc.)
- **Share more code** as project grows
- **Better team collaboration**
- **Easier onboarding** of new developers

## 📁 Monorepo Structure

```
green-matchers/
├── apps/
│   ├── backend/          # FastAPI backend (formerly Backend/)
│   └── web/              # React web frontend (formerly Frontend/)
├── packages/
│   ├── api/              # Shared API client
│   ├── ui/               # Shared UI components
│   ├── hooks/            # Shared React hooks
│   ├── utils/            # Shared utilities
│   ├── types/            # Shared TypeScript types
│   └── constants/        # Shared constants
├── shared/
│   ├── config/           # Shared configurations
│   └── i18n/             # Internationalization
├── package.json          # Monorepo root
├── turbo.json            # Turborepo configuration
└── MONOREPO_README.md    # This file
```

## 🛠️ Technologies Used

### **Monorepo Tools**
- **Turborepo** - Fast builds and caching
- **npm workspaces** - Dependency management
- **TypeScript** - Type-safe development
- **ESLint + Prettier** - Code quality

### **Backend**
- **FastAPI** - Python web framework
- **MariaDB** - Database with vector support
- **JWT Authentication** - Secure auth
- **SentenceTransformers** - AI embeddings

### **Web Frontend**
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Navigation

## 🚀 Getting Started

### **1. Install Dependencies**
```bash
# Install all dependencies
npm install

# Or install in specific workspace
cd apps/web && npm install
```

### **2. Run Development Servers**
```bash
# Start all apps in parallel
npm run dev

# Or start specific app
cd apps/backend && uvicorn app:app --reload
cd apps/web && npm run dev
```

### **3. Build for Production**
```bash
# Build all apps
npm run build

# Or build specific app
cd apps/web && npm run build
```

## 📦 Shared Packages

### **1. @green-matchers/api**
**Shared API client** for web applications.

**Features:**
- Singleton API client instance
- JWT authentication support
- Request/response interceptors
- Consistent error handling
- TypeScript support
- All API endpoints defined

**Usage:**
```typescript
import { apiClient, API_ENDPOINTS } from '@green-matchers/api';

// Set auth token
apiClient.setToken('your-jwt-token');

// Make API calls
const response = await apiClient.get(API_ENDPOINTS.CAREER_RECOMMENDATIONS);
```

### **2. @green-matchers/ui**
**Shared UI components** for web applications.

**Components:**
- `Button` - Consistent buttons
- `Card` - Reusable cards
- `Input` - Form inputs
- `Modal` - Dialogs
- `LoadingSpinner` - Loading indicators

**Usage:**
```typescript
import { Button } from '@green-matchers/ui';

<Button
  title="Submit"
  onPress={handleSubmit}
  type="primary"
  size="large"
/>
```

## 🔧 Development Workflow

### **1. Adding a New Shared Package**
```bash
# Create new package
mkdir packages/new-package
cd packages/new-package
npm init

# Add to monorepo workspaces
# Edit root package.json and add to workspaces array
```

### **2. Using Shared Packages**
```typescript
// In any app
import { apiClient } from '@green-matchers/api';
import { Button } from '@green-matchers/ui';
```

### **3. Running Tests**
```bash
# Run all tests
npm test

# Run specific app tests
cd apps/web && npm test
```

## 📊 Monorepo Commands

| Command | Description |
|---------|-------------|
| `npm install` | Install all dependencies |
| `npm run dev` | Start all apps in development |
| `npm run build` | Build all apps for production |
| `npm run lint` | Lint all code |
| `npm run test` | Run all tests |
| `npm run format` | Format all code |

## 🎯 Migration Guide

### **From Old Structure to Monorepo**

1. **Move existing code** to appropriate apps folder
2. **Identify shared code** and move to packages
3. **Update imports** to use shared packages
4. **Configure Turborepo** for caching
5. **Set up CI/CD** for monorepo

### **Example: Moving a Component**

**Before:**
```typescript
// Frontend/src/components/Button.jsx
import React from 'react';
export const Button = () => {...};
```

**After:**
```typescript
// packages/ui/Button.tsx
import React from 'react';
export const Button = () => {...};
```

**Usage in Web:**
```typescript
import { Button } from '@green-matchers/ui';
```

## 🏆 Best Practices

### **1. Code Organization**
- **Keep shared code** in packages
- **Avoid circular dependencies**
- **Use TypeScript** for type safety
- **Document shared APIs** thoroughly

### **2. Development**
- **Run specific apps** during development
- **Use Turborepo caching** for faster builds
- **Share as much code** as possible
- **Keep app-specific code** in apps folders

### **3. Deployment**
- **Deploy apps independently**
- **Use semantic versioning** for packages
- **Tag releases** consistently
- **Document breaking changes**

## 🔮 Future Enhancements

### **1. Additional Shared Packages**
- `@green-matchers/auth` - Authentication logic
- `@green-matchers/i18n` - Internationalization
- `@green-matchers/analytics` - Analytics tracking
- `@green-matchers/storage` - Data storage

### **2. Advanced Tooling**
- **Storybook** for component documentation
- **Chromatic** for visual testing
- **Sentry** for error monitoring
- **Feature flags** for gradual rollouts

### **3. Performance**
- **Code splitting** for web
- **Tree shaking** for smaller bundles
- **Lazy loading** for web
- **Optimized builds** with Turborepo

## 📄 License

```markdown
MIT License © 2025 Green Matchers Team
See LICENSE file for details
```

---

🌱 **Built with ❤️ for a Sustainable Future** 🌱

**Monorepo structure designed for scalability, maintainability, and team collaboration.**