import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';

const CalculatorWithDB = () => {
  // State management for calculator functionality
  const [display, setDisplay] = useState('0');
  const [previousValue, setPreviousValue] = useState(null);
  const [operation, setOperation] = useState(null);
  const [waitingForOperand, setWaitingForOperand] = useState(false);
  const [memory, setMemory] = useState(0);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [history, setHistory] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [calculationHistory, setCalculationHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // API base URL
  const API_BASE = 'http://localhost:5000/api';

  // Initialize session on component mount
  useEffect(() => {
    createSession();
    loadHistory();
  }, []);

  // Create a new session
  const createSession = async () => {
    try {
      const response = await fetch(`${API_BASE}/session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      if (data.success) {
        setSessionId(data.session_id);
      }
    } catch (error) {
      console.error('Error creating session:', error);
    }
  };

  // Load calculation history
  const loadHistory = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`${API_BASE}/history?limit=10`);
      const data = await response.json();
      if (data.success) {
        setCalculationHistory(data.history);
      }
    } catch (error) {
      console.error('Error loading history:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Save calculation to database
  const saveCalculation = async (expression, result) => {
    try {
      const response = await fetch(`${API_BASE}/calculate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          expression,
          result,
          session_id: sessionId,
        }),
      });
      const data = await response.json();
      if (data.success) {
        // Reload history to show new calculation
        loadHistory();
      }
    } catch (error) {
      console.error('Error saving calculation:', error);
    }
  };

  // Clear all history
  const clearAllHistory = async () => {
    try {
      const response = await fetch(`${API_BASE}/history/clear`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      if (data.success) {
        setCalculationHistory([]);
        setShowHistory(false);
      }
    } catch (error) {
      console.error('Error clearing history:', error);
    }
  };

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
        
        // Save calculation to database
        const expression = `${currentValue} ${operation} ${inputValue}`;
        saveCalculation(expression, String(newValue));
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

  // History modal component
  const HistoryModal = () => {
    if (!showHistory) return null;

    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        onClick={() => setShowHistory(false)}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          className="bg-white dark:bg-gray-800 rounded-2xl p-6 w-full max-w-2xl max-h-[80vh] overflow-hidden"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-bold text-gray-800 dark:text-white">
              Calculation History
            </h3>
            <button
              onClick={() => setShowHistory(false)}
              className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            >
              ✕
            </button>
          </div>

          <div className="max-h-96 overflow-y-auto mb-4">
            {isLoading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
                <p className="mt-2 text-gray-600 dark:text-gray-400">Loading history...</p>
              </div>
            ) : calculationHistory.length > 0 ? (
              <div className="space-y-2">
                {calculationHistory.map((calc, index) => (
                  <div
                    key={calc.id}
                    className="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg"
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {new Date(calc.timestamp).toLocaleString()}
                        </p>
                        <p className="font-mono text-lg">
                          {calc.expression} = {calc.result}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                No calculations yet
              </div>
            )}
          </div>

          <div className="flex gap-2">
            <button
              onClick={loadHistory}
              className="flex-1 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
            >
              Refresh
            </button>
            <button
              onClick={clearAllHistory}
              className="flex-1 bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors"
            >
              Clear All
            </button>
          </div>
        </motion.div>
      </motion.div>
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="bg-white dark:bg-gray-800 rounded-3xl shadow-2xl p-6 w-full max-w-sm mx-auto"
    >
      {/* Header with theme toggle and history button */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-gray-700 dark:text-gray-300">
          Calculator with DB
        </h2>
        <div className="flex gap-2">
          <motion.button
            whileTap={{ scale: 0.9 }}
            onClick={() => setShowHistory(true)}
            className="p-2 rounded-full bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
            title="View History"
          >
            📊
          </motion.button>
          <motion.button
            whileTap={{ scale: 0.9 }}
            onClick={toggleTheme}
            className="p-2 rounded-full bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
          >
            {isDarkMode ? '☀️' : '🌙'}
          </motion.button>
        </div>
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

      {/* Recent calculations preview */}
      {calculationHistory.length > 0 && (
        <div className="mb-4 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Recent:</p>
          <div className="text-sm font-mono">
            {calculationHistory[0].expression} = {calculationHistory[0].result}
          </div>
        </div>
      )}

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
        <p>Database Connected • Press ESC to clear all</p>
      </div>

      {/* History Modal */}
      <HistoryModal />
    </motion.div>
  );
};

export default CalculatorWithDB;
