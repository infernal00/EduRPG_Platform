import { BrowserRouter, Routes, Route, Link, useLocation } from "react-router-dom";
import "./App.css";

import Lesson from "./pages/Lesson";
import Home from "./pages/Home";
import Map from "./pages/Map";
import Duels from "./pages/Duels";
import Shop from "./pages/Shop";
import Profile from "./pages/Profile";

function AppShell() {
  const location = useLocation();
  const hasDemoShell =
    location.pathname === "/" ||
    location.pathname === "/map" ||
    location.pathname === "/profile" ||
    location.pathname.startsWith("/lessons/");

  return (
    <div className="app">
      {!hasDemoShell && (
        <nav className="navbar">
          <h2>EduRPG</h2>

          <div>
            <Link to="/">Главная</Link>
            <Link to="/map">Карта</Link>
            <Link to="/duels">Дуэли</Link>
            <Link to="/shop">Магазин</Link>
            <Link to="/profile">Профиль</Link>
          </div>
        </nav>
      )}

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/map" element={<Map />} />
        <Route path="/duels" element={<Duels />} />
        <Route path="/shop" element={<Shop />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/lessons/:id" element={<Lesson />} />
      </Routes>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppShell />
    </BrowserRouter>
  );
}

export default App;
