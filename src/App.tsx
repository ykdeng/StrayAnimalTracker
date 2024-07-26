import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

const getCurrentYear = (() => {
  let cachedYear = null;
  return () => {
    if (!cachedYear) {
      cachedYear = new Date().getFullYear();
    }
    return cachedYear;
  };
})();

function cacheFunction(fn) {
  const cache = {};
  return function(...args) {
    const key = JSON.stringify(args);
    if (!cache[key]) {
      cache[key] = fn(...args);
    }
    return cache[key];
  };
}

const calculateExpensiveValue = (value) => {
  console.log("Expensive calculation for:", value);
  return value * 2;
};

const cachedCalculateExpensiveValue = cacheFunction(calculateExpensiveValue);

const Header = () => (
  <header>
    <h1>My React App</h1>
  </header>
);

const Footer = () => (
  <footer>
    <p>&copy; {getCurrentYear()} My React App</p>
  </footer>
);

const MainContent = () => (
  <main>
    <p>Welcome to my React app!</p>
    <p>Expensive Calculation Result: {cachedCalculateExpensiveValue(10)}</p>
  </main>
);

const App = () => (
  <div>
    <Header />
    <Main의Content />
    <Footer />
  </div>
);

ReactDOM.render(<App />, document.getElementById('root'));