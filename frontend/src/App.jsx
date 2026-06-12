import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import "./App.css";

import Lesson from "./pages/Lesson";
import Home from "./pages/Home";
import Map from "./pages/Map";
import Duels from "./pages/Duels";
import Shop from "./pages/Shop";
import Profile from "./pages/Profile";

function App() {
  return (
    <BrowserRouter>
      <div className="app">
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

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/map" element={<Map />} />
          <Route path="/duels" element={<Duels />} />
          <Route path="/shop" element={<Shop />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/lessons/:id" element={<Lesson />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;