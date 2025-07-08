import React, { useState } from 'react';
import { FaHome, FaChevronDown, FaSearch } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { useSearch } from '../../context/SearchContext';
import { buscarContenido } from '../../services/ContenidoApi';
import Swal from 'sweetalert2'; 
const Header = () => {
  const { updateSearchResults, updateQuery, query } = useSearch();
  const [showMenu, setShowMenu] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/');
  };

  const handlePerfilClick = () => {
    navigate('/PerfilPage');
  };

  const handleSearchClick = async () => {
    if (!query) return;

    try {
      const resultados = await buscarContenido(query);
      if (resultados.length > 0) {
        updateSearchResults(resultados);
        navigate('/BusquedaPage');
      } else {
        Swal.fire({
          icon: 'info',
          title: 'Sin resultados',
          text: 'No se encontraron contenidos relacionados con tu búsqueda.',
          confirmButtonColor: '#1db954'
        });
      }
    } catch (error) {
      console.error('Error al realizar la búsqueda:', error);
      Swal.fire({
        icon: 'error',
        title: 'Error de búsqueda',
        text: error.message,
        confirmButtonColor: '#d33'
      });
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSearchClick();
    }
  };

  const handleInputChange = (e) => {
    updateQuery(e.target.value);
  };

  return (
    <div style={styles.header}>
      <div style={styles.left}>
        <button style={styles.iconBtn}>
          <FaHome size={20} />
        </button>
        <div style={styles.searchBar}>
          <FaSearch style={styles.searchIcon} onClick={handleSearchClick} />
          <input
            type="text"
            placeholder="¿Qué quieres reproducir?"
            style={styles.input}
            value={query}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
          />
        </div>
      </div>

      <div style={styles.right}>
        <div style={styles.profileContainer}>
          <div style={styles.profile} onClick={() => setShowMenu(!showMenu)}>
            <span style={styles.profileInitial}>D</span>
            <FaChevronDown style={{ marginLeft: 5 }} />
          </div>
          {showMenu && (
            <div style={styles.dropdown}>
              <div style={styles.menuItem}>Cuenta</div>
              <div style={styles.menuItem} onClick={handlePerfilClick}>Perfil</div>
              <div style={styles.menuItem} onClick={handleLogout}>Cerrar sesión</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const styles = {
  header: {
    backgroundColor: '#000000',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '10px 20px',
    backgroundImage: 'radial-gradient(at 50% 50%, hsla(210, 100%, 16%, 0.5), hsl(220, 30%, 5%))',
    color: '#b3b3b3',
    zIndex: 100,
    position: 'relative',
  },
  left: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
  },
  searchBar: {
    backgroundColor: '#242424',
    display: 'flex',
    alignItems: 'center',
    padding: '5px 10px',
    borderRadius: '50px',
    color: '#b3b3b3',
  },
  searchIcon: {
    marginRight: 8,
    cursor: 'pointer',
  },
  input: {
    background: 'transparent',
    border: 'none',
    outline: 'none',
    color: '#fff',
  },
  right: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
  },
  profileContainer: {
    position: 'relative',
  },
  profile: {
    display: 'flex',
    alignItems: 'center',
    backgroundColor: '#1db954',
    borderRadius: '50px',
    padding: '5px 10px',
    cursor: 'pointer',
  },
  profileInitial: {
    backgroundColor: '#222',
    borderRadius: '50%',
    width: 25,
    height: 25,
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    color: '#fff',
    fontWeight: 'bold',
  },
  dropdown: {
    position: 'absolute',
    top: '40px',
    right: 0,
    backgroundColor: '#282828',
    color: '#fff',
    borderRadius: '5px',
    overflow: 'hidden',
    zIndex: 9999,
  },
  menuItem: {
    padding: '10px 15px',
    cursor: 'pointer',
    borderBottom: '1px solid #333',
  },
};

export default Header;
