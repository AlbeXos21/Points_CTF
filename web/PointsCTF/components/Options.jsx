import React, { useEffect, useState } from "react";

export function ButtonMenu({nombre,onButtonClick,MostrarMenu}) {


  return (
    <>
    <button style={{
      position: 'absolute', 
      top: '10px', 
      right: '30px', 
      backgroundColor: !MostrarMenu ? 'white' : 'gray' , 
      color: !MostrarMenu ? 'black' : 'white', 
      padding: '10px 20px', 
      borderRadius: '5px', 
      border: 'none', 
      cursor: 'pointer',
      fontSize: "1.2em",
      zIndex: 1000 // Asegura que esté por encima del mapa
    }} onClick={onButtonClick} className="Boton">
      {nombre}
      
    </button>

    </>
   
  );
}




export function ListadoElementos({onButtonClick,ProvinciasVisibles}){
  return (
    <>
<ul className="lista_opciones">
  {["Cádiz", "Sevilla", "Huelva", "Málaga", "Cordoba", "Granada", "Jaén", "Almeria"].map((provincia, index) => (
    <li key={index}>
      <button
        style={{
          backgroundColor: ProvinciasVisibles[index] ? "white" : "gray",
          color: ProvinciasVisibles[index] ? "black" : "white",
          padding: "10px",
          border: "none",
          cursor: "pointer",
          transition: "background-color 0.3s ease, color 0.3s ease" // Transiciones suaves
        }}
        className={`boton-opcion ${ProvinciasVisibles[index] ? "activo" : "inactivo"}`}
        onClick={() => onButtonClick(index)}
      >
        {provincia}
      </button>
    </li>
  ))}
</ul>

    </>
   
  );
}




export function FetchApiElementos() {
  return fetch("http://127.0.0.1:5000/id")
      .then((response) => {
          if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
      })
      .then((data) => {
          return data; // Devuelve los datos para usarlos en la función que llame a FetchApiElementos
      })
      .catch((error) => {
          console.error('Error en FetchApiElementos:', error);
      });
}