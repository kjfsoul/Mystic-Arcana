
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import TarotReading from './pages/TarotReading';
import AstrologyChart from './pages/AstrologyChart';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Simulate a logged in user
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
            <Route path="/" element={<Home />} />
            <Route path="/readings" element={<TarotReading />} />
            <Route path="/astrology" element={<AstrologyChart />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

// Simple Home component
function Home() {
  return (
    <div className="flex flex-col items-center justify-center pt-10">
      <h1 className="text-4xl font-bold mb-6 text-center">Welcome to Mystic Arcana</h1>
      <p className="text-xl max-w-2xl text-center mb-8">
        Explore the hidden mysteries of tarot and astrology. Discover insights about your destiny and cosmic influences.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl">
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg text-center">
          <h2 className="text-2xl font-bold mb-3 text-purple-400">Tarot Readings</h2>
          <p className="mb-4">Draw a card and receive mystical insights into your questions.</p>
          <a href="/readings" className="inline-block bg-purple-700 hover:bg-purple-800 text-white font-bold py-2 px-4 rounded-full">
            Get a Reading
          </a>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg text-center">
          <h2 className="text-2xl font-bold mb-3 text-purple-400">Astrology Charts</h2>
          <p className="mb-4">Calculate your sun sign and discover what the stars reveal about you.</p>
          <a href="/astrology" className="inline-block bg-purple-700 hover:bg-purple-800 text-white font-bold py-2 px-4 rounded-full">
            Check Your Chart
          </a>
        </div>
      </div>
    </div>
  );
}

export default App;
