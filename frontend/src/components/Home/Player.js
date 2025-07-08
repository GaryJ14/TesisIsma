import React, { useEffect, useRef, useState } from 'react';
import { FaPlay, FaPause, FaBackward, FaForward, FaRandom, FaRedoAlt, FaVolumeUp, FaHeart } from 'react-icons/fa';
import { usePlayer } from '../../context/PlayerContext';
import axios from 'axios';

const BACKEND_URL = 'http://localhost:8000';

const Player = () => {
  const { currentSong, isPlaying, playSong, pauseSong } = usePlayer();
  const audioRef = useRef(null);
  const [volume, setVolume] = useState(0.6);

  useEffect(() => {
    if (currentSong && audioRef.current) {
      audioRef.current.load();
      audioRef.current.play();
      registrarEnHistorial(currentSong.id);
    }
  }, [currentSong]);

  const togglePlay = () => {
    if (!currentSong || !audioRef.current) return;
    if (audioRef.current.paused) {
      audioRef.current.play();
      playSong(currentSong);
      registrarEnHistorial(currentSong.id);
    } else {
      audioRef.current.pause();
      pauseSong();
    }
  };

  const handleVolumeChange = (e) => {
    const vol = parseFloat(e.target.value);
    setVolume(vol);
    if (audioRef.current) {
      audioRef.current.volume = vol;
    }
  };

  const construirUrl = (archivo) => {
    if (!archivo) return '';
    return archivo.startsWith('http') ? archivo : `${BACKEND_URL}${archivo}`;
  };

  const renderMedia = () => {
    const url = construirUrl(currentSong?.archivo);
    if (!url) return null;

    if (currentSong.tipo === 'audio') {
      return (
        <audio ref={audioRef} style={{ width: '100%' }} controls>
          <source src={url} type="audio/mpeg" />
          Tu navegador no soporta el audio.
        </audio>
      );
    } else if (currentSong.tipo === 'video') {
      return (
        <video ref={audioRef} style={styles.videoPlayer} controls>
          <source src={url} type="video/mp4" />
          Tu navegador no soporta el video.
        </video>
      );
    }
    return null;
  };

  if (!currentSong) {
    return (
      <div style={styles.container}>
        <div style={{ flex: 1, color: '#aaa' }}>Selecciona una canción para reproducir</div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.songInfo}>
        <div style={{ marginLeft: 10 }}>
          <div style={styles.songTitle}>{currentSong.titulo}</div>
          <div style={styles.artist}>Subido por: {currentSong.subido_por_nombre || 'Desconocido'}</div>
        </div>
        <FaHeart style={{ color: '#1DB954', marginLeft: 10, cursor: 'pointer' }} />
      </div>

      <div style={styles.centerControls}>
        <div style={styles.buttons}>
          <FaRandom style={styles.icon} />
          <FaBackward style={styles.icon} />
          <div style={styles.playButton} onClick={togglePlay}>
            {isPlaying ? <FaPause color="#000" /> : <FaPlay color="#000" />}
          </div>
          <FaForward style={styles.icon} />
          <FaRedoAlt style={styles.icon} />
        </div>

        {renderMedia()}
      </div>

      <div style={styles.volume}>
        <FaVolumeUp />
        <input
          type="range"
          min="0"
          max="1"
          step="0.01"
          value={volume}
          onChange={handleVolumeChange}
          style={styles.volumeBar}
        />
      </div>
    </div>
  );
};

const registrarEnHistorial = async (contenidoId) => {
  const token = localStorage.getItem('access_token');
  if (!token) return;

  try {
    const historialResponse = await axios.get('http://localhost:8000/api/historial/', {
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: 'application/json',
      },
    });

    const yaRegistrado = historialResponse.data.some(
      (item) => item.contenido_id === contenidoId
    );

    if (!yaRegistrado) {
      await axios.post(
        'http://localhost:8000/api/historial/',
        { contenido_id: contenidoId },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            Accept: 'application/json',
          },
        }
      );
      console.log('✅ Contenido registrado en historial');
    } else {
      console.log('ℹ️ Ya estaba en el historial');
    }
  } catch (err) {
    console.error('❌ Error al registrar en historial:', err);
  }
};

const styles = {
  container: {
    position: 'fixed',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: '#000',
    color: '#fff',
    padding: '10px 20px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    height: '80px',
    zIndex: 1,
  },
  songInfo: {
    display: 'flex',
    alignItems: 'center',
    flex: 1,
  },
  songTitle: {
    fontWeight: 'bold',
    fontSize: 14,
  },
  artist: {
    fontSize: 12,
    color: '#aaa',
  },
  centerControls: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    flex: 2,
  },
  buttons: {
    display: 'flex',
    alignItems: 'center',
    gap: 20,
    marginBottom: 5,
  },
  playButton: {
    backgroundColor: '#fff',
    borderRadius: '50%',
    width: 32,
    height: 32,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    cursor: 'pointer',
  },
  icon: {
    fontSize: 14,
    cursor: 'pointer',
  },
  volume: {
    display: 'flex',
    alignItems: 'center',
    gap: 10,
    flex: 1,
    justifyContent: 'flex-end',
  },
  volumeBar: {
    width: 100,
  },
  videoPlayer: {
    width: '300px',
    height: 'auto',
    borderRadius: 8,
    backgroundColor: 'black',
    position: 'fixed',
    right: 30,
    top: '80px',
    zIndex: 1000,
  },
};

export default Player;
