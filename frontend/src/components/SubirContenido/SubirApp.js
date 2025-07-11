import React from 'react';
import TblSubirContenido from './TblSubirContenido'; // Asegúrate de que la ruta sea correcta
import { usePlayer } from '../../context/PlayerContext';

const SubirApp = () => {
  const { currentSong } = usePlayer();

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
          ...styles.uploadContainer,
          marginRight: videoUrl ? '320px' : '0', // Deja espacio para el video
        }}
      >
        <TblSubirContenido />
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
    paddingBottom: '80px', // espacio para el reproductor
    overflow: 'visible',
  },
  uploadContainer: {
    flex: 1,
    transition: 'margin-right 0.3s ease',
  },
};

export default SubirApp;
