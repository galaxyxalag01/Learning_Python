import React, { useEffect, useState } from 'react';
import Calculator from './components/Calculator';
import CalculatorWithDB from './components/CalculatorWithDB';
import { register } from './registerSW';

function App() {
  const [activeCalculator, setActiveCalculator] = useState('basic');

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
            React Calculator Suite
          </h1>
          
          {/* Calculator Selection */}
          <div className="mb-8 flex gap-4">
            <button
              onClick={() => setActiveCalculator('basic')}
              className={`px-6 py-3 rounded-lg font-medium transition-colors ${
                activeCalculator === 'basic'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
              }`}
            >
              Basic Calculator
            </button>
            <button
              onClick={() => setActiveCalculator('database')}
              className={`px-6 py-3 rounded-lg font-medium transition-colors ${
                activeCalculator === 'database'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
              }`}
            >
              Calculator with Database
            </button>
          </div>

          {/* Calculator Display */}
          {activeCalculator === 'basic' && <Calculator />}
          {activeCalculator === 'database' && <CalculatorWithDB />}

          {/* Info Section */}
          <div className="mt-8 max-w-2xl text-center">
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg">
              <h2 className="text-xl font-bold text-gray-800 dark:text-white mb-4">
                Calculator Features
              </h2>
              <div className="grid md:grid-cols-2 gap-4 text-sm text-gray-600 dark:text-gray-400">
                <div>
                  <h3 className="font-semibold text-gray-800 dark:text-white mb-2">Basic Calculator</h3>
                  <ul className="space-y-1">
                    <li>• Standard arithmetic operations</li>
                    <li>• Memory functions (M+, M-, MR, MC)</li>
                    <li>• Keyboard support</li>
                    <li>• Dark/Light theme</li>
                  </ul>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-800 dark:text-white mb-2">Database Calculator</h3>
                  <ul className="space-y-1">
                    <li>• All basic features</li>
                    <li>• PostgreSQL database storage</li>
                    <li>• Calculation history</li>
                    <li>• Session tracking</li>
                    <li>• Statistics and analytics</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
