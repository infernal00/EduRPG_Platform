import './App.css'

function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <h2>EduRPG</h2>
        <div>
          <a href="#">Главная</a>
          <a href="#">Карта</a>
          <a href="#">Дуэли</a>
          <a href="#">Магазин</a>
          <a href="#">Профиль</a>
        </div>
      </nav>

      <section className="hero">
        <h1>EduRPG Platform</h1>
        <p>Образовательная RPG-платформа с квестами, XP, дуэлями и магазином.</p>
        <button>Начать приключение</button>
      </section>

      <section className="cards">
        <div className="card">
          <h3>🗺️ Карта мира</h3>
          <p>Учебные темы представлены как зоны и локации.</p>
        </div>

        <div className="card">
          <h3>⚔️ Дуэли</h3>
          <p>Игроки соревнуются в знаниях и получают монеты.</p>
        </div>

        <div className="card">
          <h3>🛒 Магазин</h3>
          <p>Монеты можно тратить на аватары, рамки и значки.</p>
        </div>
      </section>
    </div>
  )
}

export default App