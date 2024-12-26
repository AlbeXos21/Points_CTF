import React, { useEffect, useState } from 'react';
import Mapa from '../components/Mapa.jsx';
import "./index.css"
function App() {



  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <h1>Mapa Interactivo con React Leaflet</h1>
      <Mapa />
    </div>
  );
}

export default App;