import React from 'react';
import { Link } from 'react-router-dom';

function Navbar({ user }) {
  return (
    <nav className="p-4 bg-gray-800">
      <div className="container mx-auto flex justify-between">
        <Link to="/" className="text-2xl font-bold text-purple-300">Mystic Arcana</Link>
        <div className="space-x-4">
          <Link to="/readings" className="hover:text-purple-300">Tarot</Link>
          <Link to="/astrology" className="hover:text-purple-300">Astrology</Link>
          {user ? <span>{user.username}</span> : <Link to="/login">Login</Link>}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;