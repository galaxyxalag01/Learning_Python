import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';

const Calculator = () => {
  // State management for calculator functionality
  const [display, setDisplay] = useState('0');
  const [previousValue, setPreviousValue] = useState(null);
  const [operation, setOperation] = useState(null);
  const [waitingForOperand, setWaitingForOperand] = useState(false);
  const [memory, setMemory] = useState(0);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [history, setHistory] = useState('');

  // Toggle dark/light mode
  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  // Apply theme to document
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  // Input number function
  const inputNumber = useCallback((num) => {
    if (waitingForOperand) {
      setDisplay(String(num));
      setWaitingForOperand(false);
    } else {
      setDisplay(display === '0' ? String(num) : display + num);
    }
  }, [display, waitingForOperand]);

  // Input decimal function
  const inputDecimal = useCallback(() => {
    if (waitingForOperand) {
      setDisplay('0.');
      setWaitingForOperand(false);
    } else if (display.indexOf('.') === -1) {
      setDisplay(display + '.');
    }
  }, [display, waitingForOperand]);

  // Clear function (C)
  const clear = useCallback(() => {
    setDisplay('0');
  }, []);

  // All Clear function (AC)
  const allClear = useCallback(() => {
    setDisplay('0');
    setPreviousValue(null);
    setOperation(null);
    setWaitingForOperand(false);
    setHistory('');
  }, []);

  // Perform calculation
  const calculate = useCallback((firstValue, secondValue, operation) => {
    const first = parseFloat(firstValue);
    const second = parseFloat(secondValue);

    switch (operation) {
      case '+':
        return first + second;
      case '-':
        return first - second;
      case '×':
        return first * second;
      case '÷':
        if (second === 0) {
          throw new Error('Cannot divide by zero');
        }
        return first / second;
      default:
        return second;
    }
  }, []);

  // Perform operation
  const performOperation = useCallback((nextOperation) => {
    const inputValue = parseFloat(display);

    if (previousValue === null) {
      setPreviousValue(inputValue);
    } else if (operation) {
      try {
        const currentValue = previousValue || 0;
        const newValue = calculate(currentValue, inputValue, operation);
        
        // Check for overflow
        if (Math.abs(newValue) > 999999999999) {
          throw new Error('Result too large');
        }

        setDisplay(String(newValue));
        setPreviousValue(newValue);
        setHistory(`${currentValue} ${operation} ${inputValue} =`);
      } catch (error) {
        setDisplay('Error');
        setPreviousValue(null);
        setOperation(null);
        setWaitingForOperand(true);
        return;
      }
    }

    setWaitingForOperand(true);
    setOperation(nextOperation);
  }, [display, previousValue, operation, calculate]);

  // Memory functions
  const memoryAdd = useCallback(() => {
    setMemory(memory + parseFloat(display));
  }, [memory, display]);

  const memorySubtract = useCallback(() => {
    setMemory(memory - parseFloat(display));
  }, [memory, display]);

  const memoryRecall = useCallback(() => {
    setDisplay(String(memory));
    setWaitingForOperand(true);
  }, [memory]);

  const memoryClear = useCallback(() => {
    setMemory(0);
  }, []);

  // Keyboard input handler
  const handleKeyPress = useCallback((event) => {
    const { key } = event;

    // Prevent default for calculator keys
    if (/[0-9+\-*/.=]/.test(key) || key === 'Enter' || key === 'Escape') {
      event.preventDefault();
    }

    // Number keys
    if (/[0-9]/.test(key)) {
      inputNumber(parseInt(key));
    }
    // Decimal point
    else if (key === '.') {
      inputDecimal();
    }
    // Operations
    else if (key === '+') {
      performOperation('+');
    }
    else if (key === '-') {
      performOperation('-');
    }
    else if (key === '*') {
      performOperation('×');
    }
    else if (key === '/') {
      performOperation('÷');
    }
    // Equals
    else if (key === '=' || key === 'Enter') {
      performOperation(null);
    }
    // Clear
    else if (key === 'Escape') {
      allClear();
    }
  }, [inputNumber, inputDecimal, performOperation, allClear]);

  // Add keyboard event listener
  useEffect(() => {
    document.addEventListener('keydown', handleKeyPress);
    return () => {
      document.removeEventListener('keydown', handleKeyPress);
    };
  }, [handleKeyPress]);

  // Button component with animation
  const Button = ({ onClick, children, className = '', type = 'number' }) => {
    const baseClasses = 'calc-button w-full h-16 text-2xl font-medium rounded-lg transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2';
    
    const typeClasses = {
      number: 'bg-calc-button-light dark:bg-gray-600 text-black dark:text-white hover:bg-gray-300 dark:hover:bg-gray-500',
      operation: 'bg-calc-button-orange text-white hover:bg-orange-600',
      function: 'bg-calc-button dark:bg-gray-700 text-white hover:bg-gray-600 dark:hover:bg-gray-600',
      memory: 'bg-purple-600 text-white hover:bg-purple-700'
    };

    return (
      <motion.button
        whileTap={{ scale: 0.95 }}
        className={`${baseClasses} ${typeClasses[type]} ${className}`}
        onClick={onClick}
      >
        {children}
      </motion.button>
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="bg-white dark:bg-gray-800 rounded-3xl shadow-2xl p-6 w-full max-w-sm mx-auto"
    >
      {/* Header with theme toggle */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Calculator</h2>
        <motion.button
          whileTap={{ scale: 0.9 }}
          onClick={toggleTheme}
          className="p-2 rounded-full bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
        >
          {isDarkMode ? '☀️' : '🌙'}
        </motion.button>
      </div>

      {/* Display */}
      <div className="bg-black dark:bg-gray-900 rounded-2xl p-4 mb-4 text-right">
        <div className="text-gray-400 dark:text-gray-500 text-sm mb-1 min-h-[20px]">
          {history}
        </div>
        <div className="text-white text-4xl font-light overflow-hidden">
          {display}
        </div>
      </div>

      {/* Memory buttons row */}
      <div className="grid grid-cols-4 gap-3 mb-3">
        <Button onClick={memoryClear} type="memory" className="text-sm">MC</Button>
        <Button onClick={memoryRecall} type="memory" className="text-sm">MR</Button>
        <Button onClick={memoryAdd} type="memory" className="text-sm">M+</Button>
        <Button onClick={memorySubtract} type="memory" className="text-sm">M-</Button>
      </div>

      {/* Calculator buttons */}
      <div className="grid grid-cols-4 gap-3">
        {/* Row 1 */}
        <Button onClick={allClear} type="function">AC</Button>
        <Button onClick={clear} type="function">C</Button>
        <Button onClick={() => performOperation('÷')} type="operation">÷</Button>
        <Button onClick={() => performOperation('×')} type="operation">×</Button>

        {/* Row 2 */}
        <Button onClick={() => inputNumber(7)} type="number">7</Button>
        <Button onClick={() => inputNumber(8)} type="number">8</Button>
        <Button onClick={() => inputNumber(9)} type="number">9</Button>
        <Button onClick={() => performOperation('-')} type="operation">-</Button>

        {/* Row 3 */}
        <Button onClick={() => inputNumber(4)} type="number">4</Button>
        <Button onClick={() => inputNumber(5)} type="number">5</Button>
        <Button onClick={() => inputNumber(6)} type="number">6</Button>
        <Button onClick={() => performOperation('+')} type="operation">+</Button>

        {/* Row 4 */}
        <Button onClick={() => inputNumber(1)} type="number">1</Button>
        <Button onClick={() => inputNumber(2)} type="number">2</Button>
        <Button onClick={() => inputNumber(3)} type="number">3</Button>
        <Button 
          onClick={() => performOperation(null)} 
          type="operation" 
          className="row-span-2 h-full"
        >
          =
        </Button>

        {/* Row 5 */}
        <Button onClick={() => inputNumber(0)} type="number" className="col-span-2">0</Button>
        <Button onClick={inputDecimal} type="number">.</Button>
      </div>

      {/* Footer */}
      <div className="mt-6 text-center text-sm text-gray-500 dark:text-gray-400">
        <p>Use keyboard for input • Press ESC to clear all</p>
      </div>
    </motion.div>
  );
};

export default Calculator;





