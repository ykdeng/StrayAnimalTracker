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
  </main>
);

const App = () => (
  <div>
    <Header />
    <MainContent />
    <Footer />
  </div>
);

ReactDOM.render(<App />, document.getElementById('root'));