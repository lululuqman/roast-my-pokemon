import { useState, useRef } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [pokemonName, setPokemonName] = useState('')
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState(null) // Stores the backend response
  const [image, setImage] = useState(null) // Stores the official artwork
  
  // Ref to handle audio playback
  const audioRef = useRef(new Audio())

  const handleRoast = async () => {
    if (!pokemonName) return;
    
    setLoading(true);
    setData(null);
    setImage(null);

    // Stop any previous audio
    audioRef.current.pause();

    try {
      const cleanName = pokemonName.toLowerCase().trim();

      // 1. Get the Image (from official PokeAPI)
      // We do this purely for the visual. Your backend handles the text.
      const pokeApiRes = await axios.get(`https://pokeapi.co/api/v2/pokemon/${cleanName}`);
      const imageUrl = pokeApiRes.data.sprites.other['official-artwork'].front_default;
      setImage(imageUrl);

      // 2. Get the ROAST (from YOUR Backend)
      // Make sure this URL matches your backend port (usually 8000)
      const roastRes = await axios.get(`http://localhost:8000/roast/${cleanName}`);
      setData(roastRes.data);

      // 3. Play the Audio
      if (roastRes.data.audio_url) {
        audioRef.current.src = roastRes.data.audio_url;
        audioRef.current.play().catch(e => console.error("Audio play failed:", e));
      }

    } catch (error) {
      console.error(error);
      alert("Pokemon not found or Backend is offline!");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <h1 className="title">🔥 Pokedex Roast</h1>
      
      <div className="input-group">
        <input 
          type="text" 
          placeholder="Enter Pokemon (e.g. Pikachu)" 
          value={pokemonName}
          onChange={(e) => setPokemonName(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleRoast()}
        />
        <button onClick={handleRoast} disabled={loading}>
          {loading ? 'Roasting...' : 'Roast It'}
        </button>
      </div>

      {/* Display Card only when we have data */}
      {image && data && (
        <div className="card">
          <img src={image} alt={data.name} className="poke-img" />
          <h2 style={{textTransform: 'capitalize'}}>{data.name}</h2>
          <div className="roast-text">
            "{data.roast_text}"
          </div>
        </div>
      )}
    </div>
  )
}

export default App