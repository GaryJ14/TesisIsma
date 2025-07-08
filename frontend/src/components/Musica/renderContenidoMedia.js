// renderContenidoMedia.js
export const BACKEND_URL = 'http://localhost:8000';

export const renderContenidoMedia = (contenido) => {
  if (!contenido.archivo) return null;

  const urlCompleta = contenido.archivo.startsWith('http')
    ? contenido.archivo
    : BACKEND_URL + contenido.archivo;

  if (contenido.tipo === 'audio') {
    return (
      <audio controls style={{ width: '100%' }}>
        <source src={urlCompleta} type="audio/mpeg" />
        Tu navegador no soporta el elemento de audio.
      </audio>
    );
  }

  if (contenido.tipo === 'video') {
    return (
      <video controls style={{ width: '100%' }}>
        <source src={urlCompleta} type="video/mp4" />
        Tu navegador no soporta el elemento de video.
      </video>
    );
  }

  return null;
};
