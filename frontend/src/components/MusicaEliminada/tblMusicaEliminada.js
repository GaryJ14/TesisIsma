import React, { useEffect, useState, useCallback } from 'react';
import {
  Box,
  Typography,
  Chip,
  CircularProgress,
  Grid,
  Card,
  CardContent,
  CardActions,
  CardHeader,
  Tabs,
  Tab,
  Alert,
  TextField,
  InputAdornment,
} from '@mui/material';
import { Search } from '@mui/icons-material';
import { obtenerContenidosEliminados  } from '../../services/ContenidoApi';
import { BACKEND_URL } from '../../config';

export default function TblMusicaEliminada() {
  const [filtroTipo, setFiltroTipo] = useState('todos');
  const [contenidos, setContenidos] = useState([]);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  const cargarContenidos = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const data = await obtenerContenidosEliminados ();
      if (filtroTipo === 'todos') {
        setContenidos(data);
      } else {
        setContenidos(data.filter(c => c.tipo === filtroTipo));
      }
    } catch (err) {
      console.error('Error al cargar:', err);
      setError('No se pudo cargar el contenido');
    } finally {
      setCargando(false);
    }
  }, [filtroTipo]);

  useEffect(() => {
    cargarContenidos();
  }, [cargarContenidos]);

  const renderEtiquetas = (etiquetas) => {
    if (!etiquetas || etiquetas.length === 0) return null;
    return etiquetas.map((etiqueta, idx) => (
      <Chip
        key={idx}
        label={etiqueta.nombre}
        size="small"
        color="info"
        sx={{ mr: 0.5, mb: 0.5 }}
      />
    ));
  };

  const renderArtista = (artista) => {
    if (!artista) return null;
    return (
      <Typography variant="body2" color="textSecondary" sx={{ mb: 1 }}>
        Artista: {artista}
      </Typography>
    );
  };

  const renderContenidoMedia = (contenido) => {
    if (!contenido.archivo) return null;

    const urlCompleta = contenido.archivo.startsWith('http')
      ? contenido.archivo
      : `${BACKEND_URL}${contenido.archivo.startsWith('/') ? '' : '/'}${contenido.archivo}`;

    const extension = urlCompleta.split('.').pop().toLowerCase();

    if (extension === 'mp3') {
      return (
        <audio controls style={{ width: '100%' }}>
          <source src={urlCompleta} type="audio/mpeg" />
          Tu navegador no soporta el elemento de audio.
        </audio>
      );
    }

    if (extension === 'mp4' || extension === 'webm') {
      return (
        <video controls style={{ width: '100%' }}>
          <source src={urlCompleta} type="video/mp4" />
          Tu navegador no soporta el elemento de video.
        </video>
      );
    }

    return (
      <Typography variant="caption" color="error">
        Formato no compatible
      </Typography>
    );
  };

  const filteredContenidos = contenidos.filter((contenido) =>
    (contenido?.titulo?.toLowerCase() || '').includes(searchQuery.toLowerCase()) ||
    contenido?.etiquetas?.some(e => (e?.nombre?.toLowerCase() || '').includes(searchQuery.toLowerCase()))
  );

  return (
    <Box sx={{ mt: 4, px: 3 }}>
      <Typography variant="h4" gutterBottom align="center">
        Multimedia Eliminada
      </Typography>

      <TextField
        fullWidth
        label="Buscar contenido"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        sx={{ mb: 2 }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Search />
            </InputAdornment>
          ),
        }}
      />

      <Tabs
        value={filtroTipo}
        onChange={(_, newVal) => setFiltroTipo(newVal)}
        sx={{ mb: 2 }}
        centered
      >
        <Tab label="Todos" value="todos" />
        <Tab label="Audio" value="audio" />
        <Tab label="Video" value="video" />
      </Tabs>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {cargando ? (
        <Box textAlign="center" mt={5}>
          <CircularProgress />
          <Typography variant="body2" mt={2}>
            Cargando contenido...
          </Typography>
        </Box>
      ) : filteredContenidos.length === 0 ? (
        <Alert severity="info">No se encontraron contenidos para esta categoría.</Alert>
      ) : (
        <Grid container spacing={3}>
          {filteredContenidos.map((contenido) => (
            <Grid item xs={12} sm={6} md={3} key={contenido.id}>
              <Card
                variant="outlined"
                sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
              >
                <CardHeader
                  title={contenido.titulo}
                  subheader={
                    contenido.fecha_subida
                      ? `Subido el ${new Date(contenido.fecha_subida).toLocaleDateString()}`
                      : 'Fecha no disponible'
                  }
                  titleTypographyProps={{ variant: 'h6' }}
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box mb={1}>{renderEtiquetas(contenido.etiquetas)}</Box>
                  {renderArtista(contenido.artista)}
                  {renderContenidoMedia(contenido)}
                </CardContent>
                <CardActions sx={{ justifyContent: 'space-between' }}>
                  <Typography variant="caption">
                    Subido por: {contenido.subido_por_nombre || 'Anónimo'}
                  </Typography>
                  <Typography variant="caption">
                    Motivo de Eliminacion: {contenido.motivo_eliminacion || 'Eliminado sin motivo'}
                  </Typography>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
}
