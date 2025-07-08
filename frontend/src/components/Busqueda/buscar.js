import React, { useState, useEffect, useCallback } from 'react';
import { FaHeart, FaRegHeart } from 'react-icons/fa';
import { useSearch } from '../../context/SearchContext';
import axios from 'axios';
import Swal from 'sweetalert2';
import { obtenerFavoritos } from '../../services/ContenidoApi';

const API_BASE = 'http://localhost:8000';

const Buscar = ({ onSelectSong }) => {
  const { searchResults } = useSearch();
  const [favoritoIds, setFavoritoIds] = useState([]);
  const [contenidosRecomendados, setContenidosRecomendados] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const token = localStorage.getItem('access_token');
  const headers = token ? { Authorization: `Bearer ${token}` } : {};

  const isFavorito = useCallback(
    (id) => favoritoIds.includes(id),
    [favoritoIds]
  );

  const fetchFavoritos = async () => {
    try {
      const response = await obtenerFavoritos();
      const ids = response.map((f) => f.id);
      setFavoritoIds(ids);
    } catch (error) {
      console.error('Error al obtener favoritos', error);
    }
  };

  const fetchRecomendaciones = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE}/api/recomendaciones/`, { headers });
      const aleatorios = res.data.sort(() => Math.random() - 0.5);
      setContenidosRecomendados(aleatorios);
    } catch (err) {
      setError('Error al cargar recomendaciones: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const toggleFavoritoHandler = async (contenidoId) => {
    try {
      const res = await axios.post(`${API_BASE}/api/favoritos/toggle/${contenidoId}/`, null, {
        headers: { ...headers, Accept: 'application/json' },
      });

      if (res.data.status === 'agregado') {
        Swal.fire('Agregado', 'Contenido marcado como favorito.', 'success');
        setFavoritoIds((prev) => [...prev, contenidoId]);
      } else if (res.data.status === 'eliminado') {
        Swal.fire('Eliminado', 'Contenido eliminado de tus favoritos.', 'success');
        setFavoritoIds((prev) => prev.filter((id) => id !== contenidoId));
      } else {
        Swal.fire('Error', 'No se pudo modificar el favorito.', 'error');
      }
    } catch (err) {
      Swal.fire('Error', `No se pudo modificar el favorito: ${err.message}`, 'error');
    }
  };

  useEffect(() => {
    fetchFavoritos();
    fetchRecomendaciones();
  }, []);

  if (loading) return <p style={{ color: 'white' }}>Cargando contenidos...</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>;

  const renderFilaContenido = (contenido, index) => (
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

      {/* ✅ Etiquetas en su propia columna */}
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
                display: 'inline-block',
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
        {isFavorito(contenido.id) ? (
          <FaHeart style={{ cursor: 'pointer', color: '#1DB954' }} />
        ) : (
          <FaRegHeart style={{ cursor: 'pointer' }} />
        )}
      </span>
    </div>
  );

  return (
    <div style={styles.container}>
      {/* Resultados de búsqueda */}
      {searchResults.length > 0 ? (
        <div style={styles.tableContainer}>
          <div style={styles.tableHeader}>
            <span style={{ width: 40 }}>#</span>
            <span style={{ flex: 3 }}>TÍTULO</span>
            <span style={{ flex: 2 }}>TIPO</span>
            <span style={{ flex: 2 }}>ARTISTA</span>
            <span style={{ flex: 3 }}>ETIQUETAS</span>
            <span style={{ width: 40, textAlign: 'center' }}>❤️</span>
          </div>
          {searchResults.map((r, i) => renderFilaContenido(r, i))}
        </div>
      ) : (
        <p style={{ color: 'white' }}>No hay resultados para la búsqueda.</p>
      )}

      {/* Recomendaciones */}
      <div style={{ marginTop: '20px' }}>
        <h2>También te podría interesar</h2>
        <div style={{ display: 'flex', fontWeight: 'bold', padding: '10px' }}>
          <span style={{ width: 40 }}>#</span>
          <span style={{ flex: 3 }}>TÍTULO</span>
          <span style={{ flex: 2 }}>TIPO</span>
          <span style={{ flex: 2 }}>ARTISTA</span>
          <span style={{ flex: 3 }}>ETIQUETAS</span>
          <span style={{ width: 40, textAlign: 'center' }}>❤️</span>
        </div>
        {contenidosRecomendados.map((c, i) => renderFilaContenido(c, i))}
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '20px',
    color: '#fff',
  },
  tableContainer: {
    marginTop: '20px',
  },
  tableHeader: {
    display: 'flex',
    fontWeight: 'bold',
    padding: '10px',
    backgroundColor: '#333',
    borderRadius: '5px',
  },
};

export default Buscar;
