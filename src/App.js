import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import TarotReading from './pages/TarotReading';
import AstrologyChart from './pages/AstrologyChart';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    setUser({ id: 1, username: "testuser" });
  }, []);

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-indigo-900 text-white">
        {/* <div className="stars"></div> */}
        {/* <div className="twinkling"></div> */}
        <Navbar user={user} setUser={setUser} />
        <div className="container mx-auto p-4 relative z-10 flex-grow">
          <Routes>
            <Route path="/" element={<h1 className="text-3xl text-center">Welcome to Mystic Arcana</h1>} />
            <Route path="/readings" element={<TarotReading />} />
            <Route path="/astrology" element={<AstrologyChart />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;