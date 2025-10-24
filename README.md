# React Calculator App

A modern, responsive calculator application built with React and Tailwind CSS. Features a clean, macOS-inspired design with dark/light mode toggle, keyboard support, and PWA capabilities.

## Features

### Core Functionality
- ✅ Basic arithmetic operations (+, -, ×, ÷)
- ✅ Decimal number support
- ✅ Clear (C) and All Clear (AC) functions
- ✅ Error handling (divide by zero, overflow)
- ✅ Keyboard input support
- ✅ Memory functions (M+, M-, MR, MC)

### UI/UX Features
- ✅ Modern, responsive design
- ✅ Dark/Light mode toggle
- ✅ Smooth animations with Framer Motion
- ✅ macOS calculator aesthetic
- ✅ Touch-friendly button design
- ✅ Accessibility features (focus states, keyboard navigation)

### Advanced Features
- ✅ Progressive Web App (PWA) support
- ✅ Offline functionality
- ✅ Installable on mobile devices
- ✅ Service worker caching

## Installation & Setup

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn

### Quick Start

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm start
   ```

3. **Open your browser:**
   Navigate to `http://localhost:3000`

### Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build` folder.

## Usage

### Mouse/Touch Input
- Click any number or operation button to input
- Use the display to see current input and results
- Memory buttons (MC, MR, M+, M-) for storing values

### Keyboard Input
- **Numbers:** 0-9 keys
- **Operations:** +, -, *, / keys
- **Decimal:** . (period) key
- **Equals:** = or Enter key
- **Clear:** Escape key
- **All Clear:** Escape key (clears everything)

### Memory Functions
- **MC:** Memory Clear - clears stored memory value
- **MR:** Memory Recall - displays stored memory value
- **M+:** Memory Add - adds current display to memory
- **M-:** Memory Subtract - subtracts current display from memory

### Theme Toggle
Click the sun/moon icon in the top-right corner to switch between light and dark modes.

## Project Structure

```
src/
├── components/
│   └── Calculator.jsx      # Main calculator component
├── App.js                   # Main app component
├── index.js                 # React entry point
├── index.css               # Global styles with Tailwind
└── registerSW.js           # Service worker registration

public/
├── index.html              # HTML template
├── manifest.json           # PWA manifest
└── sw.js                   # Service worker

Configuration files:
├── package.json            # Dependencies and scripts
├── tailwind.config.js      # Tailwind CSS configuration
└── postcss.config.js       # PostCSS configuration
```

## Technical Implementation

### State Management
The calculator uses React hooks for state management:
- `display`: Current display value
- `previousValue`: Previous operand for calculations
- `operation`: Current operation being performed
- `waitingForOperand`: Boolean for input state management
- `memory`: Stored memory value
- `isDarkMode`: Theme state
- `history`: Display history for showing previous calculations

### Key Functions

#### Arithmetic Operations
```javascript
const calculate = (firstValue, secondValue, operation) => {
  // Handles all basic arithmetic with error checking
  // Returns result or throws error for invalid operations
};
```

#### Input Handling
```javascript
const inputNumber = (num) => {
  // Manages number input with proper state transitions
  // Handles waitingForOperand state correctly
};
```

#### Error Handling
- Division by zero detection
- Overflow protection (results > 999999999999)
- Invalid operation handling
- Graceful error display

### Styling & Animation

#### Tailwind CSS Classes
- Custom color palette matching macOS calculator
- Responsive grid layout for buttons
- Dark mode support with `dark:` prefix
- Smooth transitions and hover effects

#### Framer Motion Animations
- Button press animations (`whileTap={{ scale: 0.95 }}`)
- Page load animations
- Smooth theme transitions

### PWA Features

#### Service Worker
- Caches app resources for offline use
- Handles network requests with cache-first strategy
- Automatic cache cleanup for updates

#### Manifest
- App metadata for installation
- Icon definitions
- Display mode configuration

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+

## Performance

- Optimized bundle size with React production build
- Lazy loading of components
- Efficient state management
- Minimal re-renders with useCallback hooks

## Accessibility

- Full keyboard navigation support
- Focus indicators for screen readers
- High contrast mode support
- Touch-friendly button sizes (minimum 44px)
- Semantic HTML structure

## Development

### Code Style
- ESLint configuration for React
- Consistent component structure
- Comprehensive inline comments
- Modular function organization

### Testing
```bash
npm test
```

### Linting
```bash
npm run lint
```

## Deployment

### Static Hosting
The app can be deployed to any static hosting service:
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

### Build Output
The `npm run build` command creates a production-ready build in the `build` directory.

## License

MIT License - feel free to use this project for learning or commercial purposes.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Future Enhancements

Potential improvements for future versions:
- Scientific calculator functions
- History log with export
- Custom themes
- Voice input support
- Multi-language support
- Advanced memory functions
- Calculation history persistence





