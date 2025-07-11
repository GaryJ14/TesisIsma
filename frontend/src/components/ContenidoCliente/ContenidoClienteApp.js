import React from 'react';
import { usePlayer } from '../../context/PlayerContext'; // Asegúrate de que exista
import TblContenidoCliente from './TblContenidoCliente'; // Tu componente personalizado para el cliente

const ContenidoClienteApp = () => {
  const { currentSong, playSong } = usePlayer(); // Hook del reproductor global

  const videoUrl =
    currentSong && currentSong.tipo === 'video' && currentSong.archivo
      ? currentSong.archivo.startsWith('http')
        ? currentSong.archivo
        : `http://localhost:8000${currentSong.archivo}`
      : null;

  return (
    <div style={styles.appContainer}>
      <div
        style={{
          ...styles.listContainer,
          marginRight: videoUrl ? '320px' : '0', // Espacio para el reproductor si es video
        }}
      >
        <TblContenidoCliente onSelectSong={playSong} /> {/* Se pasa la función para reproducir */}
      </div>
    </div>
  );
};

const styles = {
  appContainer: {
    display: 'flex',
    flexDirection: 'row',
    position: 'relative',
    minHeight: '100vh',
    paddingBottom: '80px', // Espacio para el reproductor
    overflow: 'visible',
  },
  listContainer: {
    flex: 1,
    transition: 'margin-right 0.3s ease',
  },
};

export default ContenidoClienteApp;
