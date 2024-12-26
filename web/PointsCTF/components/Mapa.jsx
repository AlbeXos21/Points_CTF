import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import {FetchApiElementos,ButtonMenu,ListadoElementos} from "./Options.jsx"
import "../css/styles.css"
function Mapa() {
  const coordenadas = "36.76807852,-4.79115457";
  const Initialposition = coordenadas.split(',').map(coord => parseFloat(coord));
  const [elementos,setelementos]=useState([])


  const provinciasAndalucia = {
    "Cádiz": 0,
    "Sevilla": 1,
    "Huelva": 2,
    "Málaga": 3,
    "Córdoba": 4,
    "Granada": 5,
    "Jaén": 6,
    "Almería": 7
};


  const [ProvinciasVisibles,SetProvinciasVisibles] = useState([true,true,true,true,true,true,true,true])

  const CambiarEstadoProvinciasVisibles = (position) => {
    const nuevasProvinciasVisibles = [...ProvinciasVisibles];
    nuevasProvinciasVisibles[position] = !nuevasProvinciasVisibles[position];
    SetProvinciasVisibles(nuevasProvinciasVisibles);
  };
  


useEffect(() => {
    FetchApiElementos().then((data) => {
        if (data) {
            setelementos(data);
        }
    });
}, []);


const [MostrarMenu, SetMostrarMenu] = useState(false); 

const CambiarEstadoMenu = () => {  
  SetMostrarMenu(!MostrarMenu);
};


  return (
    <MapContainer center={Initialposition} zoom={8}style={{ width: '100%', height: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />

      <ButtonMenu nombre="Filtrado por provincia" onButtonClick={CambiarEstadoMenu} MostrarMenu ={MostrarMenu}></ButtonMenu>
      
      {MostrarMenu && <ListadoElementos ProvinciasVisibles={ProvinciasVisibles} onButtonClick={(position) => CambiarEstadoProvinciasVisibles(position)} />}

        {
        elementos.map((element, index) => (
        ProvinciasVisibles[provinciasAndalucia[element.provincia]] && <Marker position={element.coordenadas.split(',').map(coord => parseFloat(coord))}
        key={element.id}
        provincia={element.provincia}
        >
        <Popup><a 
              href={`https://www.wikidata.org/wiki/${element.id}`} 
              target="_blank" 
              rel="noopener noreferrer" 
              style={{ color: 'blue', textDecoration: 'underline' }}
            >  {element.id}
            </a></Popup>
        </Marker>
          
        ))}


  


    </MapContainer>
  );
}

export default Mapa;
