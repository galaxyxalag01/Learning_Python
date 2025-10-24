import React, { useEffect } from 'react';
import Calculator from './components/Calculator';
import { register } from './registerSW';

function App() {
  // Register service worker for PWA functionality
  useEffect(() => {
    register({
      onSuccess: (registration) => {
        console.log('Service worker registered successfully');
      },
      onError: (error) => {
        console.log('Service worker registration failed:', error);
      }
    });
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 transition-colors duration-300">
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col items-center justify-center min-h-screen">
          <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-8 text-center">
            React Calculator
          </h1>
          <Calculator />
        </div>
      </div>
    </div>
  );
}

export default App;
