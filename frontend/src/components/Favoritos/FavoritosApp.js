import React from 'react';
import { usePlayer } from '../../context/PlayerContext'; // Importar el hook usePlayer
import Favoritos from './favoritos';  // El componente que lista los favoritos

const FavoritosApp = () => {
  const { currentSong, playSong } = usePlayer();  // Obtener currentSong y playSong del contexto global

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
          marginRight: videoUrl ? '320px' : '0', // Desplaza la lista a la izquierda cuando haya un video
        }}
      >
        <Favoritos onSelectSong={playSong} />  {/* Al seleccionar una canción, actualizamos el estado global */}
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
    paddingBottom: '80px',
    overflow: 'visible',
  },
  listContainer: {
    flex: 1,
    transition: 'margin-right 0.3s ease',
  },
};

export default FavoritosApp;
