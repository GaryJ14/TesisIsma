import React from 'react';
import Sidebar from '../components/Home/Sidebar';
import Header from '../components/Home/Header';
import SubirApp from '../components/SubirContenido/SubirApp'; 

const SubirContenidoPage = () => {
  return (
    <div style={styles.appContainer}>
      {/* Sidebar a la izquierda */}
      <Sidebar />

      {/* Contenido principal */}
      <div style={styles.mainContent}>
        <Header /> {/* Puedes pasar props si necesitas búsqueda, etc. */}

        {/* Contenido de la subida */}
        <div style={styles.bodyContent}>
          <h1>Sube tu Contenido</h1>
          <SubirApp />
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

export default SubirContenidoPage;
