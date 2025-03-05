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
import React, { useState } from 'react';

function TarotReading() {
  const [card, setCard] = useState(null);
  
  const tarotCards = [
    { name: "The Fool", meaning: "New beginnings, adventure, potential" },
    { name: "The Magician", meaning: "Manifestation, power, skill" },
    { name: "The High Priestess", meaning: "Intuition, mystery, inner voice" },
    { name: "The Empress", meaning: "Fertility, nurturing, abundance" },
    { name: "The Emperor", meaning: "Authority, structure, leadership" },
    { name: "The Hierophant", meaning: "Tradition, spiritual wisdom, conformity" },
    { name: "The Lovers", meaning: "Relationships, choices, alignment of values" },
    { name: "The Chariot", meaning: "Control, willpower, victory" },
    { name: "Strength", meaning: "Courage, patience, compassion" },
    { name: "The Hermit", meaning: "Soul-searching, introspection, guidance" }
  ];
  
  const drawCard = () => {
    const randomIndex = Math.floor(Math.random() * tarotCards.length);
    setCard(tarotCards[randomIndex]);
  };
  
  return (
    <div className="min-h-screen flex flex-col items-center p-6">
      <h1 className="text-3xl mb-8">Tarot Reading</h1>
      
      <button 
        onClick={drawCard}
        className="bg-purple-700 hover:bg-purple-800 text-white font-bold py-2 px-6 rounded-full mb-8"
      >
        Draw a Card
      </button>
      
      {card && (
        <div className="bg-gray-800 p-8 rounded-lg shadow-lg max-w-md w-full text-center">
          <h2 className="text-2xl font-bold mb-2 text-purple-400">{card.name}</h2>
          <p className="text-lg text-gray-300">{card.meaning}</p>
        </div>
      )}
    </div>
  );
}

export default TarotReading;
