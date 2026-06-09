import "./Map.css";

export default function Map() {
  const locations = [
    {
      name: "🏝️ Остров Арифметики",
      description: "Основы математики и вычислений"
    },
    {
      name: "🏰 Башня Алгебры",
      description: "Уравнения и формулы"
    },
    {
      name: "🌲 Лес Геометрии",
      description: "Фигуры и пространство"
    },
    {
      name: "⚡ Лаборатория Физики",
      description: "Законы природы"
    },
    {
      name: "💻 Долина Программирования",
      description: "Python, Java, Web"
    }
  ];

  return (
    <div className="map-page">
      <h1>🗺️ Мир знаний</h1>

      <div className="map-grid">
        {locations.map((location) => (
          <div className="location-card" key={location.name}>
            <h3>{location.name}</h3>
            <p>{location.description}</p>
            <button>Войти</button>
          </div>
        ))}
      </div>
    </div>
  );
}