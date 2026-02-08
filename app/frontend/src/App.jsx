import { useState } from 'react'
import Dashboard from './pages/Dashboard'
import Portfolio from './pages/Portfolio'
import './App.css'

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')

  return (
    <div className="App">
      <nav style={{ padding: '1rem', background: '#f0f0f0', marginBottom: '2rem' }}>
        <button onClick={() => setCurrentPage('dashboard')} style={{ marginRight: '1rem' }}>
          Dashboard
        </button>
        <button onClick={() => setCurrentPage('portfolio')}>
          Portfolio
        </button>
      </nav>
      
      {currentPage === 'dashboard' && <Dashboard />}
      {currentPage === 'portfolio' && <Portfolio />}
    </div>
  )
}

export default App
