# InvaSee Frontend

A sophisticated, nature-inspired landing page for InvaSee - an invasive species tracking and reporting platform.

## 🌿 Features

- **Nature-Inspired Design**: White canvas with green color palette, organic blob shapes, and subtle gradients
- **Responsive & Accessible**: Mobile-first design with semantic HTML and ARIA labels
- **Smooth Animations**: Entrance animations and hover effects using Tailwind transitions
- **Reusable Components**: Modular React components for maintainability
- **Performance Optimized**: Lazy loading for map components and optimized production builds

## 🚀 Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm

### Installation

```bash
npm install
```

### Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Build

Create a production build:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

## 📁 Project Structure

```
src/
├── components/
│   ├── Button.jsx          # Reusable button component (primary & outline variants)
│   ├── Header.jsx          # Fixed header with navigation
│   ├── Hero.jsx            # Hero section with headline and phone mock
│   ├── HowItWorks.jsx      # Three-step process cards
│   ├── MapPreview.jsx      # Lazy-loaded map placeholder
│   ├── TreePet.jsx         # Tree growth visualization
│   └── Footer.jsx          # Footer with links
├── App.jsx                 # Main app component
├── index.css               # Tailwind imports and base styles
└── main.jsx                # App entry point
```

## 🎨 Design System

### Color Palette
- Primary Green: `#22c55e` (green-500)
- Secondary Green: `#16a34a` (green-600)
- Text: `#111827` (gray-900)
- Background: `#ffffff` (white)

### Typography
System font stack for optimal performance and native feel

### Accessibility
- Semantic HTML5 elements
- ARIA labels on all interactive elements
- 4.5:1 contrast ratio compliance
- Visible focus rings for keyboard navigation
- Proper heading hierarchy

## 🛠️ Tech Stack

- **React 18**: UI library
- **Vite**: Build tool and dev server
- **Tailwind CSS v4**: Utility-first CSS framework
- **PostCSS**: CSS processing

## 📝 License

See the main repository for license information.
