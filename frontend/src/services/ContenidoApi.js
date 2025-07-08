import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';
const API_CONTENIDOS = `${API_BASE}/contenidos/`;

const obtenerToken = () => localStorage.getItem('access_token');
const getAuthHeaders = () => ({
  Authorization: `Bearer ${obtenerToken()}`,
  Accept: 'application/json',
});

// ======================= CONTENIDOS =======================
export const obtenerContenidos = async () => {
  const response = await axios.get(API_CONTENIDOS, { headers: getAuthHeaders() });
  return response.data;
};

export const actualizarContenido = async (id, formData) => {
  const response = await fetch(`${API_CONTENIDOS}actualizar/${id}/`, {
    method: 'PUT',
    headers: {
      Authorization: `Bearer ${obtenerToken()}`,
    },
    body: formData,
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error('Error al actualizar:', errorText);
    throw new Error('Error al actualizar contenido');
  }

  return response.json();
};

export const eliminarContenido = async (id, motivo) => {
  const response = await fetch(`${API_CONTENIDOS}eliminar/${id}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify({ motivo }),
  });

  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Error al eliminar contenido');
  return data;
};

export const obtenerContenidoPorId = async (contenidoId) => {
  const response = await axios.get(`${API_CONTENIDOS}${contenidoId}/`, {
    headers: getAuthHeaders(),
  });
  return response.data;
};

export const obtenerContenidosEliminados = async () => {
  const response = await axios.get(`${API_CONTENIDOS}eliminados/`, {
    headers: getAuthHeaders(),
  });
  return response.data;
};

export const obtenerContenidosPorEtiquetasFavoritas = async () => {
  const response = await axios.get(`${API_CONTENIDOS}por-etiquetas-favoritas/`, {
    headers: getAuthHeaders(),
  });
  return response.data;
};

export const buscarContenido = async (query) => {
  const response = await axios.get(`${API_CONTENIDOS}buscar/${query}/`, {
    headers: getAuthHeaders(),
  });
  return response.data;
};

// ======================= FAVORITOS =======================
export const obtenerFavoritos = async () => {
  const response = await axios.get(`${API_BASE}/favoritos/`, {
    headers: getAuthHeaders(),
  });
  return response.data;
};

export const toggleFavorito = async (contenidoId) => {
  const response = await axios.post(
    `${API_BASE}/favoritos/toggle/${contenidoId}/`,
    null,
    { headers: getAuthHeaders() }
  );
  return response.data;
};

// ======================= HISTORIAL =======================
export const obtenerHistorial = async () => {
  const response = await axios.get(`${API_BASE}/historial/`, {
    headers: getAuthHeaders(),
  });
  return response.data;
};

export const eliminarHistorial = async (contenidoId) => {
  const response = await axios.delete(`${API_BASE}/eliminarhistorial/${contenidoId}/`, {
    headers: getAuthHeaders(),
  });
  return response.data;
};

export const eliminarTodoHistorial = async () => {
  const response = await axios.delete(`${API_BASE}/eliminartodohistorial/`, {
    headers: getAuthHeaders(),
  });
  return response.data;
};

// ======================= RECOMENDACIONES =======================
export const obtenerRecomendaciones = async () => {
  const response = await axios.get(`${API_BASE}/recomendaciones/`, {
    headers: getAuthHeaders(),
  });
  return response.data;
};

// ======================= DASHBOARD ESTADÍSTICAS =======================
export const obtenerEstadisticasUsuarios = async () => {
  const response = await axios.get(`${API_BASE}/estadisticas/dashboard/`, {
    headers: getAuthHeaders(),
  });
  return response.data;
};

export const obtenerEstadisticasFavoritos = async () => {
  const response = await axios.get(`${API_BASE}/favoritos/dashboard/`, {
    headers: getAuthHeaders(),
  });
  return response.data;
};
