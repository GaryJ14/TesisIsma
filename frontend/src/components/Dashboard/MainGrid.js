import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Copyright from '../Dashboard/internals/components/Copyright';
import StatCard from '../Dashboard/StatCard';

const MainGrid = () => {
  const [cards, setCards] = useState([]);

  useEffect(() => {
    const fetchStats = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) return;

      try {
        const headers = { Authorization: `Bearer ${token}` };

        const [resUsuarios, resFavoritos] = await Promise.all([
          axios.get("http://localhost:8000/api/estadisticas/dashboard/", { headers }),
          axios.get("http://localhost:8000/api/favoritos/dashboard/", { headers })
        ]);

        const usuarios = resUsuarios.data;  // ← Array de 2 objetos
        const favoritos = resFavoritos.data; // ← Objeto único

        const data = [];

        if (Array.isArray(usuarios)) {
          data.push(...usuarios); // ⬅️ Desempaquetar todos los objetos del array de usuarios
        }

        if (favoritos && favoritos.title) {
          data.push(favoritos);
        }

        setCards(data);
      } catch (err) {
        console.error("❌ Error al obtener estadísticas:", err);
      }
    };

    fetchStats();
  }, []);

  return (
    <Box sx={{ width: '100%', maxWidth: { sm: '100%', md: '1700px' } }}>
      <Typography component="h2" variant="h6" sx={{ mb: 2 }}>
        Estadísticas Generales
      </Typography>

      <Grid container spacing={2} columns={12} sx={{ mb: 2 }}>
        {cards.map((card, index) => (
          <Grid item key={index} xs={12} sm={6} lg={3}>
            <StatCard {...card} />
          </Grid>
        ))}
      </Grid>

      <Copyright sx={{ my: 4 }} />
    </Box>
  );
};

export default MainGrid;
