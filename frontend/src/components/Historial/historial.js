import React, { useState, useEffect } from 'react';
import { usePlayer } from '../../context/PlayerContext';
import { FaTrash, FaHeart, FaRegHeart } from 'react-icons/fa';
import axios from 'axios';
import Swal from 'sweetalert2';

const Historial = () => {
  const { playSong } = usePlayer();
  const [contenidos, setContenidos] = useState([]);
  const [favoritoIds, setFavoritoIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const token = localStorage.getItem('access_token');

  const fetchHistorial = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/historial/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setContenidos(res.data);
    } catch (err) {
      console.error(err);
      setError('Error al cargar el historial');
    }
  };

  const fetchFavoritos = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/favoritos/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      const ids = res.data.map(f => f.id || f.contenido_id);
      setFavoritoIds(ids);
    } catch (err) {
      console.error('Error al obtener favoritos', err);
    }
  };

  const toggleFavorito = async (contenidoId) => {
    try {
      const res = await axios.post(`http://localhost:8000/api/favoritos/toggle/${contenidoId}/`, null, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.data.status === 'agregado') {
        setFavoritoIds(prev => [...prev, contenidoId]);
      } else if (res.data.status === 'eliminado') {
        setFavoritoIds(prev => prev.filter(id => id !== contenidoId));
      }
    } catch (err) {
      console.error('Error al modificar favorito:', err);
    }
  };

  const eliminarContenido = async (contenidoId) => {
    const confirmar = await Swal.fire({
      title: '¿Eliminar del historial?',
      text: 'Esta acción no se puede deshacer.',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Sí, eliminarlo',
    });

    if (confirmar.isConfirmed) {
      try {
        await axios.delete(`http://localhost:8000/api/eliminarhistorial/${contenidoId}/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setContenidos(prev => prev.filter(c => c.id !== contenidoId));
      } catch (err) {
        console.error('Error al eliminar contenido', err);
      }
    }
  };

  const eliminarTodoHistorial = async () => {
    const confirmar = await Swal.fire({
      title: '¿Eliminar TODO el historial?',
      text: 'Esta acción no se puede deshacer.',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Sí, eliminar todo',
    });

    if (confirmar.isConfirmed) {
      try {
        await axios.delete(`http://localhost:8000/api/eliminarTodohistorial/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setContenidos([]);
      } catch (err) {
        console.error('Error al eliminar historial', err);
      }
    }
  };

  useEffect(() => {
    if (!token) {
      setError('No autenticado');
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      await fetchHistorial();
      await fetchFavoritos();
      setLoading(false);
    };

    fetchData();
  }, []);

  if (loading) return <p style={{ color: 'white' }}>Cargando historial...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div style={{ paddingBottom: '100px', color: 'white' }}>
      <div style={styles.deleteAllButtonContainer}>
        <button style={styles.deleteAllButton} onClick={eliminarTodoHistorial}>Eliminar Todo el Historial</button>
      </div>

      <div style={{ display: 'flex', fontWeight: 'bold', padding: '10px', borderBottom: '2px solid #333' }}>
        <span style={{ width: 50 }}>#</span>
        <span style={{ flex: 3 }}>TÍTULO</span>
        <span style={{ flex: 2 }}>TIPO</span>
        <span style={{ flex: 3 }}>ETIQUETAS</span>
        <span style={{ width: 40, textAlign: 'center' }}>🗑</span>
        <span style={{ width: 40, textAlign: 'center' }}>❤️</span>
      </div>

      {contenidos.map((contenido, index) => (
        <div
          key={contenido.id}
          style={{
            display: 'flex',
            padding: '10px',
            backgroundColor: index % 2 === 0 ? '#222' : 'transparent',
            alignItems: 'center',
            borderBottom: '1px solid #333',
            cursor: 'pointer',
          }}
          onClick={() => playSong(contenido)}
        >
          <span style={{ width: 50 }}>{index + 1}</span>
          <div style={{ flex: 3 }}>
            <div>{contenido.titulo}</div>
            <div style={{ fontSize: 12, color: '#aaa' }}>
              Subido por: {contenido.subido_por_nombre || 'Desconocido'}
            </div>
          </div>
          <span style={{ flex: 2 }}>{contenido.tipo}</span>
          <div style={{ flex: 3 }}>
            {(contenido.etiquetas_asociadas || []).map((etiqueta, idx) => (
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
                {typeof etiqueta === 'string' ? etiqueta : etiqueta.nombre}
              </span>
            ))}
          </div>
          <span
            style={{ width: 40, textAlign: 'center' }}
            onClick={(e) => {
              e.stopPropagation();
              eliminarContenido(contenido.id);
            }}
          >
            <FaTrash style={{ color: '#f44336', cursor: 'pointer' }} />
          </span>
          <span
            style={{ width: 40, textAlign: 'center' }}
            onClick={(e) => {
              e.stopPropagation();
              toggleFavorito(contenido.id);
            }}
          >
            {favoritoIds.includes(contenido.id) ? (
              <FaHeart style={{ color: '#1DB954', cursor: 'pointer' }} />
            ) : (
              <FaRegHeart style={{ color: '#aaa', cursor: 'pointer' }} />
            )}
          </span>
        </div>
      ))}
    </div>
  );
};

const styles = {
  deleteAllButtonContainer: {
    display: 'flex',
    justifyContent: 'flex-end',
    marginBottom: '10px',
  },
  deleteAllButton: {
    backgroundColor: '#b9283d',
    color: 'white',
    padding: '8px 16px',
    border: 'none',
    borderRadius: '5px',
    fontSize: '14px',
    cursor: 'pointer',
  },
};

export default Historial;
