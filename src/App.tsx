import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

const Header = () => (
  <header>
    <h1>My React App</h1>
  </header>
);

const Footer = () => (
  <footer>
    <p>&copy; {new Date().getFullYear()} My React App</p>
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