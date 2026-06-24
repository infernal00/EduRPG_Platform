import { BrowserRouter, Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom'
import './App.css'
import Home from './pages/Home'
import Map from './pages/Map'
import Duels from './pages/Duels'
import Shop from './pages/Shop'
import Profile from './pages/Profile'
import Login from './pages/Login'
import Register from './pages/Register'

function PrivateRoute({ children }) {
  const token = localStorage.getItem('access_token')
  return token ? children : <Navigate to="/login" replace />
}

function Navbar() {
  const navigate = useNavigate()
  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    navigate('/login')
  }
  return (
    <nav className="navbar">
      <h2>EduRPG</h2>
      <div>
        <Link to="/">Главная</Link>
        <Link to="/map">Карта</Link>
        <Link to="/duels">Дуэли</Link>
        <Link to="/shop">Магазин</Link>
        <Link to="/profile">Профиль</Link>
        <button onClick={logout} className="btn-logout">Выйти</button>
      </div>
    </nav>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/*" element={
          <PrivateRoute>
            <div className="app">
              <Navbar />
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/map" element={<Map />} />
                <Route path="/duels" element={<Duels />} />
                <Route path="/shop" element={<Shop />} />
                <Route path="/profile" element={<Profile />} />
              </Routes>
            </div>
          </PrivateRoute>
        } />
      </Routes>
    </BrowserRouter>
  )
}
