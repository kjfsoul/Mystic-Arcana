import { useState } from 'react';

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

export default TarotReading;