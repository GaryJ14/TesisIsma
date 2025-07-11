import React, { useState } from 'react';
import Sidebar from '../components/Home/Sidebar';
import Header from '../components/Home/Header';
import ContenidoClienteApp from '../components/ContenidoCliente/ContenidoClienteApp'; // Asegúrate de que la ruta sea correcta

const ContenidoClientePage = () => {
  const [searchResults, setSearchResults] = useState([]);

  const setSearchResultsHandler = (results) => {
    setSearchResults(results);
  };

  return (
    <div style={styles.appContainer}>
      {/* Sidebar a la izquierda */}
      <Sidebar />

      {/* Contenido principal */}
      <div style={styles.mainContent}>
        <Header setSearchResults={setSearchResultsHandler} />

        {/* Contenido del cliente */}
        <div style={styles.bodyContent}>
          <h1>Mis Contenidos Subidos</h1>
          <ContenidoClienteApp />
        </div>
      </div>
    </div>
  );
};

const styles = {
  appContainer: {
    display: 'flex',
    height: '100vh',
    backgroundColor: '#121212',
    color: '#fff',
    backgroundImage: 'radial-gradient(at 50% 50%, hsla(210, 100%, 16%, 0.5), hsl(220, 30%, 5%))',
  },
  mainContent: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    backgroundImage: 'radial-gradient(at 50% 50%, hsla(210, 100%, 16%, 0.5), hsl(220, 30%, 5%))',
    color: '#fff',
  },
  bodyContent: {
    flex: 1,
    overflowY: 'auto',
    padding: '20px',
  },
};

export default ContenidoClientePage;
