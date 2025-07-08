import React, { useState, useEffect } from 'react';
import { FaHeart, FaRegHeart } from 'react-icons/fa';
import axios from 'axios';
import Swal from 'sweetalert2';
import { toggleFavorito, obtenerFavoritos } from '../../services/ContenidoApi';

const SongListTable = ({ onSelectSong }) => {
  const [contenidos, setContenidos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [favoritoIds, setFavoritoIds] = useState([]);  // Solo IDs, no objetos

  const toggleFavoritoHandler = async (contenidoId) => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) throw new Error('No estás autenticado.');

      const response = await toggleFavorito(contenidoId);

      if (response.status === 'agregado') {
        Swal.fire('Agregado!', 'El contenido ha sido agregado a tus favoritos.', 'success');
        setFavoritoIds((prev) => [...prev, contenidoId]);
      } else if (response.status === 'eliminado') {
        Swal.fire('Eliminado!', 'El contenido ha sido eliminado de tus favoritos.', 'success');
        setFavoritoIds((prev) => prev.filter(id => id !== contenidoId));
      } else {
        Swal.fire('Error', 'Hubo un problema al modificar el favorito.', 'error');
      }
    } catch (error) {
      console.error('Error al modificar el favorito', error);
      Swal.fire('Error', `Ocurrió un error al modificar el favorito: ${error.message}`, 'error');
    }
  };

  useEffect(() => {
  const fetchData = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setError('No autenticado. Por favor inicia sesión.');
        setLoading(false);
        return;
      }

      const favoritosResponse = await obtenerFavoritos();
      console.log('✅ Favoritos obtenidos del backend: ', favoritosResponse);

      const favoritosIds = favoritosResponse.map(f => f.id);

      console.log('✅ IDs de favoritos: ', favoritosIds);

      setFavoritoIds(favoritosIds);

      const contenidosResponse = await axios.get('http://localhost:8000/api/contenidos/por-etiquetas-favoritas/', {
        headers: { Authorization: `Bearer ${token}` },
      });

      setContenidos(Array.isArray(contenidosResponse.data) ? contenidosResponse.data : []);
      setLoading(false);
    } catch (err) {
      setError('Error al cargar contenidos: ' + (err.response?.data?.detail || err.message));
      setLoading(false);
    }
  };

  fetchData();
  }, []); // ← ✅ Esto garantiza que se ejecute solo una vez


  if (loading) return <p style={{ color: 'white' }}>Cargando contenidos...</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>;
  if (contenidos.length === 0) return <p style={{ color: 'white' }}>No hay contenidos recomendados.</p>;

  return (
    <div style={{ paddingBottom: '100px', color: 'white' }}>
      <div style={{ display: 'flex', fontWeight: 'bold', padding: '10px' }}>
        <span style={{ width: 40 }}>#</span>
        <span style={{ flex: 3 }}>TÍTULO</span>
        <span style={{ flex: 2 }}>TIPO</span>
        <span style={{ flex: 2 }}>ARTISTA</span>
        <span style={{ flex: 3 }}>ETIQUETAS</span>
        <span style={{ width: 40, textAlign: 'center' }}>❤️</span>
      </div>

      {contenidos.map((contenido, index) => (
        <div
          key={contenido.id}
          style={{
            display: 'flex',
            padding: '10px',
            cursor: 'pointer',
            backgroundColor: index % 2 === 0 ? '#222' : 'transparent',
            alignItems: 'center',
          }}
          onClick={() => onSelectSong(contenido)}
        >
          <span style={{ width: 40 }}>{index + 1}</span>
          <div style={{ flex: 3 }}>
            <div>{contenido.titulo}</div>
            <div style={{ fontSize: 12, color: '#aaa' }}>
              Subido por: {contenido.subido_por_nombre || 'Desconocido'}
            </div>
          </div>
          <span style={{ flex: 2 }}>{contenido.tipo}</span>
          <span style={{ flex: 2 }}>{contenido.artista || 'Desconocido'}</span>

          <div style={{ flex: 3 }}>
            {(contenido.etiquetas || contenido.etiquetas_asociadas || []).map((etiqueta, idx) => {
              const nombre = typeof etiqueta === 'string' ? etiqueta : etiqueta.nombre;
              return (
                <span
                  key={idx}
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
              );
            })}
          </div>

          <span
            style={{ width: 40, textAlign: 'center' }}
            onClick={(e) => {
              e.stopPropagation();
              toggleFavoritoHandler(contenido.id);
            }}
          >
            {favoritoIds.includes(contenido.id) ? (
              <FaHeart style={{ cursor: 'pointer', color: '#1DB954' }} />
            ) : (
              <FaRegHeart style={{ cursor: 'pointer' }} />
            )}
          </span>
        </div>
      ))}
    </div>
  );
};

export default SongListTable;
