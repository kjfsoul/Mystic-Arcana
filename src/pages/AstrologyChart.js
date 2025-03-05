import { useState } from 'react';

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
        <input
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

export default AstrologyChart;
import React, { useState } from 'react';

function AstrologyChart() {
  const [birthDate, setBirthDate] = useState('');
  const [sunSign, setSunSign] = useState(null);
  
  const calculateSunSign = (date) => {
    const input = new Date(date);
    const month = input.getMonth() + 1;
    const day = input.getDate();
    
    if ((month === 1 && day >= 20) || (month === 2 && day <= 18)) {
      return { sign: "Aquarius", element: "Air", traits: "Innovative, progressive, independent" };
    } else if ((month === 2 && day >= 19) || (month === 3 && day <= 20)) {
      return { sign: "Pisces", element: "Water", traits: "Compassionate, artistic, intuitive" };
    } else if ((month === 3 && day >= 21) || (month === 4 && day <= 19)) {
      return { sign: "Aries", element: "Fire", traits: "Bold, ambitious, passionate" };
    } else if ((month === 4 && day >= 20) || (month === 5 && day <= 20)) {
      return { sign: "Taurus", element: "Earth", traits: "Reliable, practical, devoted" };
    } else if ((month === 5 && day >= 21) || (month === 6 && day <= 20)) {
      return { sign: "Gemini", element: "Air", traits: "Curious, adaptable, communicative" };
    } else if ((month === 6 && day >= 21) || (month === 7 && day <= 22)) {
      return { sign: "Cancer", element: "Water", traits: "Nurturing, emotional, protective" };
    } else if ((month === 7 && day >= 23) || (month === 8 && day <= 22)) {
      return { sign: "Leo", element: "Fire", traits: "Creative, passionate, generous" };
    } else if ((month === 8 && day >= 23) || (month === 9 && day <= 22)) {
      return { sign: "Virgo", element: "Earth", traits: "Analytical, practical, diligent" };
    } else if ((month === 9 && day >= 23) || (month === 10 && day <= 22)) {
      return { sign: "Libra", element: "Air", traits: "Balanced, diplomatic, cooperative" };
    } else if ((month === 10 && day >= 23) || (month === 11 && day <= 21)) {
      return { sign: "Scorpio", element: "Water", traits: "Passionate, determined, magnetic" };
    } else if ((month === 11 && day >= 22) || (month === 12 && day <= 21)) {
      return { sign: "Sagittarius", element: "Fire", traits: "Optimistic, adventurous, intellectual" };
    } else {
      return { sign: "Capricorn", element: "Earth", traits: "Disciplined, responsible, practical" };
    }
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (birthDate) {
      setSunSign(calculateSunSign(birthDate));
    }
  };
  
  return (
    <div className="min-h-screen flex flex-col items-center p-6">
      <h1 className="text-3xl mb-8">Astrology Chart</h1>
      
      <form onSubmit={handleSubmit} className="mb-8">
        <div className="flex flex-col mb-4">
          <label htmlFor="birthDate" className="mb-2 text-lg">Enter your birth date:</label>
          <input
            type="date"
            id="birthDate"
            value={birthDate}
            onChange={(e) => setBirthDate(e.target.value)}
            className="px-4 py-2 rounded bg-gray-800 border border-gray-700 text-white"
            required
          />
        </div>
        <button 
          type="submit"
          className="bg-purple-700 hover:bg-purple-800 text-white font-bold py-2 px-6 rounded-full"
        >
          Calculate Sun Sign
        </button>
      </form>
      
      {sunSign && (
        <div className="bg-gray-800 p-8 rounded-lg shadow-lg max-w-md w-full">
          <h2 className="text-2xl font-bold mb-4 text-center text-purple-400">Your Sun Sign: {sunSign.sign}</h2>
          <div className="mb-4">
            <p className="text-md font-bold mb-1">Element:</p>
            <p className="text-lg">{sunSign.element}</p>
          </div>
          <div>
            <p className="text-md font-bold mb-1">Key Traits:</p>
            <p className="text-lg">{sunSign.traits}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default AstrologyChart;
