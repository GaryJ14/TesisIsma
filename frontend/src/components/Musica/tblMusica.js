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
  Button,
  Tabs,
  Tab,
  Alert,
  TextField,
  InputAdornment,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { Delete, Search, Edit } from '@mui/icons-material';
import Swal from 'sweetalert2';
import {
  obtenerContenidos,
  eliminarContenido,
  actualizarContenido,
} from '../../services/ContenidoApi';
import { BACKEND_URL } from '../../config';

export default function TblMusica() {
  const [filtroTipo, setFiltroTipo] = useState('todos');
  const [contenidos, setContenidos] = useState([]);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  const [openEditar, setOpenEditar] = useState(false);
  const [contenidoEditar, setContenidoEditar] = useState(null);
  const [tituloEditar, setTituloEditar] = useState('');
  const [tipoEditar, setTipoEditar] = useState('');
  const [artistaEditar, setArtistaEditar] = useState('');
  const [etiquetasEditar, setEtiquetasEditar] = useState('');
  const [archivoEditar, setArchivoEditar] = useState(null);

  const cargarContenidos = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const data = await obtenerContenidos();
      const ordenados = data.sort((a, b) => new Date(b.fecha_subida) - new Date(a.fecha_subida));
      setContenidos(
        filtroTipo === 'todos'
          ? ordenados
          : ordenados.filter(c => c.tipo === filtroTipo)
      );
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

  const handleEliminar = async (id) => {
    const { value: motivo } = await Swal.fire({
      title: '¿Estás seguro?',
      input: 'textarea',
      inputLabel: 'Motivo de eliminación (opcional)',
      inputPlaceholder: 'Escribe aquí el motivo...',
      showCancelButton: true,
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar',
    });

    if (motivo !== undefined) {
      try {
        await eliminarContenido(id, motivo);
        Swal.fire('Eliminado', 'El contenido fue eliminado.', 'success');
        await cargarContenidos();
      } catch (err) {
        console.error('Error al eliminar:', err);
        Swal.fire('Error', 'No se pudo eliminar el contenido.', 'error');
      }
    }
  };

  const abrirEditar = async (contenido) => {
    const result = await Swal.fire({
      title: '¿Deseas editar este contenido?',
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: 'Sí, editar',
      cancelButtonText: 'Cancelar',
    });

    if (result.isConfirmed) {
      setContenidoEditar(contenido);
      setTituloEditar(contenido.titulo || '');
      setTipoEditar(contenido.tipo || '');
      setArtistaEditar(contenido.artista || '');
      setEtiquetasEditar((contenido.etiquetas_asociadas || []).join(', '));
      setArchivoEditar(null);
      setOpenEditar(true);
    }
  };

  const cerrarEditar = () => {
    setOpenEditar(false);
    setContenidoEditar(null);
    setTituloEditar('');
    setTipoEditar('');
    setArtistaEditar('');
    setEtiquetasEditar('');
    setArchivoEditar(null);
  };

  const guardarCambios = async () => {
    if (!contenidoEditar) return;

    if (!tituloEditar.trim() || !tipoEditar) {
      Swal.fire('Error', 'El título y tipo son obligatorios.', 'error');
      return;
    }

    cerrarEditar();

    const etiquetasArray = etiquetasEditar
      .split(',')
      .map(t => t.trim())
      .filter(t => t.length > 0);

    const confirmEdit = await Swal.fire({
      title: 'Confirmar edición',
      text: '¿Deseas guardar los cambios realizados?',
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: 'Guardar',
      cancelButtonText: 'Cancelar',
    });

    if (!confirmEdit.isConfirmed) return;

    try {
      const formData = new FormData();
      formData.append('titulo', tituloEditar.trim());
      formData.append('tipo', tipoEditar);
      formData.append('artista', artistaEditar.trim());
      etiquetasArray.forEach(etiqueta => formData.append('etiquetas', etiqueta));
      if (archivoEditar) {
        formData.append('archivo', archivoEditar);
      }

      await actualizarContenido(contenidoEditar.id, formData);
      Swal.fire('Guardado', 'Contenido actualizado exitosamente.', 'success');
      await cargarContenidos();
    } catch (err) {
      console.error('Error al actualizar:', err);
      Swal.fire('Error', 'No se pudo actualizar el contenido.', 'error');
    }
  };

  const renderEtiquetas = (etiquetas) => {
    if (!etiquetas || etiquetas.length === 0) return null;

    return etiquetas.map((nombre, idx) => (
      <Chip
        key={idx}
        label={nombre}
        size="small"
        color="info"
        sx={{ mr: 0.5, mb: 0.5 }}
      />
    ));
  };

  const renderArtista = (artista) =>
    artista && (
      <Typography variant="body2" color="textSecondary" sx={{ mb: 1 }}>
        Artista: {artista}
      </Typography>
    );

  const renderContenidoMedia = (contenido) => {
    if (!contenido.archivo) return null;
    const urlCompleta = contenido.archivo.startsWith('http')
      ? contenido.archivo
      : BACKEND_URL + contenido.archivo;

    if (contenido.tipo === 'audio') {
      return <audio controls style={{ width: '100%' }} src={urlCompleta} />;
    }
    if (contenido.tipo === 'video') {
      return <video controls style={{ width: '100%' }} src={urlCompleta} />;
    }
    return null;
  };

  const filteredContenidos = contenidos.filter((contenido) =>
    contenido.titulo.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (contenido.etiquetas_asociadas || []).some(e =>
      e.toLowerCase().includes(searchQuery.toLowerCase())
    )
  );

  return (
    <Box sx={{ mt: 4, px: 3 }}>
      <Typography variant="h4" gutterBottom align="center">
        Biblioteca Multimedia
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

      {error && <Alert severity="error">{error}</Alert>}

      {cargando ? (
        <Box textAlign="center" mt={5}>
          <CircularProgress />
          <Typography variant="body2" mt={2}>Cargando contenido...</Typography>
        </Box>
      ) : filteredContenidos.length === 0 ? (
        <Alert severity="info">No se encontraron contenidos para esta categoría.</Alert>
      ) : (
        <Grid container spacing={3}>
          {filteredContenidos.map((contenido) => (
            <Grid item xs={12} sm={6} md={3} key={contenido.id}>
              <Card variant="outlined" sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
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
                  <Box mb={1}>{renderEtiquetas(contenido.etiquetas_asociadas)}</Box>
                  {renderArtista(contenido.artista)}  
                  {renderContenidoMedia(contenido)}
                </CardContent>
                <CardActions sx={{ justifyContent: 'space-between' }}>
                  <Typography variant="caption">
                    Subido por: {contenido.subido_por_nombre || 'Anónimo'}
                  </Typography>
                  <Box>
                    <Button size="small" color="primary" startIcon={<Edit />} onClick={() => abrirEditar(contenido)} sx={{ mr: 1 }}>
                      Editar
                    </Button>
                    <Button size="small" color="error" startIcon={<Delete />} onClick={() => handleEliminar(contenido.id)}>
                      Eliminar
                    </Button>
                  </Box>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      <Dialog open={openEditar} onClose={cerrarEditar} maxWidth="sm" fullWidth>
        <DialogTitle>Editar Contenido</DialogTitle>
        <DialogContent>
          <TextField label="Título" fullWidth value={tituloEditar} onChange={(e) => setTituloEditar(e.target.value)} sx={{ mb: 2 }} />
          <TextField
            label="Tipo"
            fullWidth
            select
            value={tipoEditar}
            onChange={(e) => setTipoEditar(e.target.value)}
            sx={{ mb: 2 }}
            SelectProps={{ native: true }}
          >
            <option value="audio">Audio</option>
            <option value="video">Video</option>
          </TextField>
          <TextField
            label="Etiquetas (separadas por coma)"
            fullWidth
            value={etiquetasEditar}
            onChange={(e) => setEtiquetasEditar(e.target.value)}
            helperText="Separe las etiquetas con comas"
            sx={{ mb: 2 }}
          />
          <TextField
            label="Artista"
            fullWidth
            value={artistaEditar}
            onChange={(e) => setArtistaEditar(e.target.value)}
            helperText="El nombre del artista"
            sx={{ mb: 2 }}
          />
          <TextField
            type="file"
            fullWidth
            onChange={(e) => setArchivoEditar(e.target.files[0])}
            helperText="Sube un nuevo archivo si deseas reemplazar el actual"
            InputLabelProps={{ shrink: true }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={cerrarEditar}>Cancelar</Button>
          <Button onClick={guardarCambios} variant="contained" color="primary">
            Guardar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
