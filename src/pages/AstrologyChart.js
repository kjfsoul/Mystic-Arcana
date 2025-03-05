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

export default AstrologyChart;