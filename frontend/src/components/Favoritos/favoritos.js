import React, { useEffect, useState } from 'react';
import { FaHeart } from 'react-icons/fa';
import { usePlayer } from '../../context/PlayerContext';
import { obtenerFavoritos, toggleFavorito } from '../../services/ContenidoApi';

const Favoritos = () => {
  const { playSong } = usePlayer();
  const [favoritos, setFavoritos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFavoritos = async () => {
      try {
        const response = await obtenerFavoritos();
        setFavoritos(response);
        setLoading(false);
      } catch (error) {
        console.error('Error al obtener los favoritos', error);
        setLoading(false);
      }
    };

    fetchFavoritos();
  }, []);

  const handleSongSelect = (song) => {
    playSong(song);
  };

  const toggleFavoritoHandler = async (contenidoId) => {
    try {
      const response = await toggleFavorito(contenidoId);
      if (response.status === 'agregado' || response.status === 'eliminado') {
        const actualizados = await obtenerFavoritos();
        setFavoritos(actualizados);
      }
    } catch (error) {
      console.error('Error al modificar el favorito', error);
    }
  };

  if (loading) return <p style={{ color: 'white' }}>Cargando...</p>;

  return (
    <div style={styles.tableContainer}>
      <div style={styles.tableHeader}>
        <span style={{ width: 50 }}>#</span>
        <span style={{ flex: 3 }}>TÍTULO</span>
        <span style={{ flex: 2 }}>TIPO</span>
        <span style={{ flex: 2 }}>ARTISTA</span>
        <span style={{ flex: 3 }}>ETIQUETAS</span>
        <span style={{ width: 60, textAlign: 'center' }}>❤️</span>
      </div>

      {favoritos.map((contenido, index) => (
        <div
          key={contenido.id || index}
          style={{
            display: 'flex',
            padding: '15px',
            cursor: 'pointer',
            backgroundColor: index % 2 === 0 ? '#222' : 'transparent',
            alignItems: 'center',
            borderBottom: '1px solid #444',
          }}
          onClick={() => handleSongSelect(contenido)}
        >
          <span style={{ width: 50 }}>{index + 1}</span>
          <div style={{ flex: 3 }}>
            <div>{contenido.titulo}</div>
            <div style={{ fontSize: 12, color: '#aaa' }}>
              Subido por: {contenido.subido_por_nombre || 'Desconocido'}
            </div>
          </div>
          <span style={{ flex: 2 }}>{contenido.tipo}</span>
          <span style={{ flex: 2 }}>{contenido.artista || 'Desconocido'}</span>

          <div style={{ flex: 3 }}>
            {(contenido.etiquetas_asociadas || []).map((nombre, idx) => (
              <span
                key={`${contenido.id}-etq-${idx}`}
                style={{
                  fontSize: '12px',
                  backgroundColor: '#1DB954',
                  color: 'white',
                  padding: '2px 6px',
                  borderRadius: '12px',
                  marginRight: '5px',
                }}
              >
                {nombre}
              </span>
            ))}
          </div>

          <span
            style={{ width: 60, textAlign: 'center' }}
            onClick={(e) => {
              e.stopPropagation();
              toggleFavoritoHandler(contenido.id);
            }}
          >
            <FaHeart color="#1DB954" style={{ cursor: 'pointer' }} />
          </span>
        </div>
      ))}
    </div>
  );
};

const styles = {
  tableContainer: {
    marginTop: '20px',
    color: 'white',
  },
  tableHeader: {
    display: 'flex',
    fontWeight: 'bold',
    padding: '10px',
    backgroundColor: '#333',
    borderRadius: '5px',
  },
};

export default Favoritos;
