
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import axios from 'axios';

// Components
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import TarotReading from './pages/TarotReading';
import AstrologyChart from './pages/AstrologyChart';
import UserProfile from './pages/UserProfile';
import Blog from './pages/Blog';
import BlogPost from './pages/BlogPost';
import Login from './pages/Login';
import Register from './pages/Register';
import ReadingHistory from './pages/ReadingHistory';
import ReadingResult from './pages/ReadingResult';
import Horoscope from './pages/Horoscope';
import PlanetAlignment from './pages/PlanetAlignment';

function App() {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    // Check if user is logged in
    const checkAuthStatus = async () => {
      try {
        const response = await axios.get('/api/profile', { withCredentials: true });
        if (response.data && response.data.user) {
          setUser(response.data.user);
        }
      } catch (error) {
        console.log('Not logged in');
      }
    };
    
    checkAuthStatus();
  }, []);
  
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <div className="stars"></div>
        <div className="twinkling"></div>
        
        <Navbar user={user} setUser={setUser} />
        
        <div className="relative z-10 flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/readings" element={<TarotReading />} />
            <Route path="/readings/history" element={<ReadingHistory />} />
            <Route path="/readings/result/:id" element={<ReadingResult />} />
            <Route path="/astrology" element={<AstrologyChart />} />
            <Route path="/astrology/horoscope/:sign" element={<Horoscope />} />
            <Route path="/astrology/planet-alignment" element={<PlanetAlignment />} />
            <Route path="/profile" element={<UserProfile user={user} setUser={setUser} />} />
            <Route path="/blog" element={<Blog />} />
            <Route path="/blog/post/:id" element={<BlogPost />} />
            <Route path="/login" element={<Login setUser={setUser} />} />
            <Route path="/register" element={<Register setUser={setUser} />} />
          </Routes>
        </div>
        
        <Footer />
      </div>
    </Router>
  );
}

export default App;
