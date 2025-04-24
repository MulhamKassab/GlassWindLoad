import './App.css';
import CalculatorPage from './pages/CalculatorPage';

<div className="logo-container">
  <img src={`${process.env.PUBLIC_URL}/logo.png`} alt="Gutmann Logo" className="company-logo" />
</div>

function App() {
  return <CalculatorPage />;
}

export default App;
