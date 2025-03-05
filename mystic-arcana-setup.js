// Mystic Arcana Repl Setup (Run in Replit Shell or Assistant)

// 1. Update .replit for Node.js and port 3000
const replitContent = `
run = "PORT=3000 npm start"
language = "nodejs"
modules = ["nodejs-20"]

[env]
NODE_ENV = "development"

[[ports]]
localPort = 3000
externalPort = 3000
`;

// Write .replit
require('fs').writeFileSync('.replit', replitContent);

// 2. Create public/index.html
const indexHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mystic Arcana | Astrology, Tarot & Spiritual Wellness</title>
  <meta name="description" content="Explore the mystical arts with Mystic Arcana - Your daily source for astrology insights, tarot readings, spiritual wellness, and occult wisdom.">
  <link rel="icon" href="/favicon.ico" />
</head>
<body>
  <div id="root"></div>
</body>
</html>`;

// Write public/index.html
require('fs').mkdirSync('public', { recursive: true });
require('fs').writeFileSync('public/index.html', indexHtml);

// 3. Create src/App.js
const appJs = `import React, { useState, useEffect } from 'react';
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

export default App;`;

// Write src/App.js
require('fs').mkdirSync('src', { recursive: true });
require('fs').writeFileSync('src/App.js', appJs);

// 4. Create src/components/Navbar.js
const navbarJs = `import React from 'react';
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

export default Navbar;`;

// Write src/components/Navbar.js
require('fs').mkdirSync('src/components', { recursive: true });
require('fs').writeFileSync('src/components/Navbar.js', navbarJs);

// 5. Create src/index.js
const indexJs = `import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);`;

// Write src/index.js
require('fs').writeFileSync('src/index.js', indexJs);

// 6. Create src/index.css
const indexCss = `@tailwind base;
@tailwind components;
@tailwind utilities;

/* Commented out until stars.png and twinkling.png are added to static/ */
/* .stars {
  background-image: url('../static/stars.png');
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
} */
/* .twinkling {
  background-image: url('../static/twinkling.png');
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
} */`;

// Write src/index.css
require('fs').writeFileSync('src/index.css', indexCss);

// 7. Create src/pages/TarotReading.js
const tarotReadingJs = `import { useState } from 'react';

const cards = [
  { name: "The Fool", meaning: "New beginnings, adventure." },
  { name: "The Magician", meaning: "Skill, manifestation." },
  { name: "The Tower", meaning: "Sudden change, upheaval." },
];

function TarotReading() {
  const [card, setCard] = useState(null);

  const drawCard = () => {
    const randomCard = cards[Math.floor(Math.random() * cards.length)];
    setCard(randomCard);
  };

  return (
    <div className="text-center">
      <h1 className="text-3xl mb-4">Tarot Reading</h1>
      <button
        onClick={drawCard}
        className="bg-purple-600 hover:bg-purple-700 text-white py-2 px-4 rounded"
      >
        Draw a Card
      </button>
      {card && (
        <div className="mt-4 p-4 bg-gray-800 rounded max-w-md mx-auto">
          <h2 className="text-2xl">{card.name}</h2>
          <p>{card.meaning}</p>
        </div>
      )}
    </div>
  );
}

export default TarotReading;`;

// Write src/pages/TarotReading.js
require('fs').mkdirSync('src/pages', { recursive: true });
require('fs').writeFileSync('src/pages/TarotReading.js', tarotReadingJs);

// 8. Create src/pages/AstrologyChart.js
const astrologyChartJs = `import { useState } from 'react';

const getSunSign = (date) => {
  const month = date.getMonth() + 1;
  const day = date.getDate();
  if ((month === 3 && day >= 21) || (month === 4 && day <= 19)) return "Aries";
  if ((month === 4 && day >= 20) || (month === 5 && day <= 20)) return "Taurus";
  if ((month === 5 && day >= 21) || (month === 6 && day <= 20)) return "Gemini";
  if ((month === 6 && day >= 21) || (month === 7 && day <= 22)) return "Cancer";
  if ((month === 7 && day >= 23) || (month === 8 && day <= 22)) return "Leo";
  if ((month === 8 && day >= 23) || (month === 9 && day <= 22)) return "Virgo";
  if ((month === 9 && day >= 23) || (month === 10 && day <= 22)) return "Libra";
  if ((month === 10 && day >= 23) || (month === 11 && day <= 21)) return "Scorpio";
  if ((month === 11 && day >= 22) || (month === 12 && day <= 21)) return "Sagittarius";
  if ((month === 12 && day >= 22) || (month === 1 && day <= 19)) return "Capricorn";
  if ((month === 1 && day >= 20) || (month === 2 && day <= 18)) return "Aquarius";
  if ((month === 2 && day >= 19) || (month === 3 && day <= 20)) return "Pisces";
  return "Unknown";
};

function AstrologyChart() {
  const [birthDate, setBirthDate] = useState('');
  const [sign, setSign] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    const date = new Date(birthDate);
    const sunSign = getSunSign(date);
    setSign(sunSign);
  };

  return (
    <div className="text-center">
      <h1 className="text-3xl mb-4">Astrology Chart</h1>
      <form onSubmit={handleSubmit} className="mb-4">
        <label htmlFor="birthDate" className="sr-only">Birth Date</label>
        <input
          id="birthDate"
          type="date"
          value={birthDate}
          onChange={(e) => setBirthDate(e.target.value)}
          className="p-2 bg-gray-800 border border-gray-700 rounded text-white"
        />
        <button
          type="submit"
          className="ml-2 bg-purple-600 hover:bg-purple-700 text-white py-2 px-4 rounded"
        >
          Get Sign
        </button>
      </form>
      {sign && (
        <div className="p-4 bg-gray-800 rounded max-w-md mx-auto">
          <h2 className="text-2xl">Your Sun Sign: {sign}</h2>
        </div>
      )}
    </div>
  );
}

export default AstrologyChart;`;

// Write src/pages/AstrologyChart.js
require('fs').writeFileSync('src/pages/AstrologyChart.js', astrologyChartJs);

// 9. Create package.json
const packageJson = `{
  "name": "mystic-arcana",
  "version": "1.0.0",
  "private": true,
  "main": "src/index.js",
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "dependencies": {
    "@heroicons/react": "^2.2.0",
    "@replit/object-storage": "^1.0.0",
    "axios": "^1.8.1",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^6.30.0",
    "react-scripts": "5.0.1"
  },
  "devDependencies": {
    "tailwindcss": "^3.3.3",
    "postcss": "^8.4.31",
    "autoprefixer": "^10.4.16"
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "description": "Mystic Arcana - Astrology, Tarot & Spiritual Wellness",
  "author": "kjfsoul",
  "license": "MIT"
}`;

// Write package.json
require('fs').writeFileSync('package.json', packageJson);

// 10. Install dependencies and start
console.log("Killing any existing Node processes...");
require('child_process').execSync('killall node');
console.log("Installing dependencies...");
require('child_process').execSync('npm install');
console.log("Starting the app on port 3000...");
require('child_process').execSync('PORT=3000 npm start');

// Instructions for user
console.log(`
Mystic Arcana is now set up! Check the app at https://your-repl.repl.co.
If you see a 404 or port conflict, run these commands in the shell:
1. killall node
2. lsof -i :3000 (note PID, kill with kill -9 <PID>)
3. npm start
If issues persist, share your Repl URL (e.g., https://replit.com/@kjfsoul/Mystic-Arcana) and errors.
Target live by 8:00 PM CST (March 5, 2025).
`);