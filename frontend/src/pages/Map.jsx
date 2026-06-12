import { useEffect, useState } from "react";
import "./Map.css";

const API_URL = "http://127.0.0.1:8000/api/subjects/";

export default function Map() {
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadSubjects() {
      try {
        const response = await fetch(API_URL);

        if (!response.ok) {
          throw new Error("Backend returned an error");
        }

        const data = await response.json();
        setSubjects(data);
      } catch (err) {
        setError("Не удалось загрузить карту знаний. Проверь backend.");
      } finally {
        setLoading(false);
      }
    }

    loadSubjects();
  }, []);

  if (loading) {
    return (
      <div className="map-page">
        <h1>🗺️ Мир знаний</h1>
        <p className="map-message">Загрузка карты...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="map-page">
        <h1>🗺️ Мир знаний</h1>
        <p className="map-message">{error}</p>
      </div>
    );
  }

  return (
    <div className="map-page">
      <h1>🗺️ Мир знаний</h1>

      {subjects.length === 0 ? (
        <p className="map-message">
          Пока нет предметов. Добавь их через Django Admin.
        </p>
      ) : (
        <div className="map-grid">
          {subjects.map((subject) => (
            <div className="location-card" key={subject.id}>
              <h3>
                {subject.icon || "📚"} {subject.name}
              </h3>

              <p>{subject.description || "Описание пока не добавлено."}</p>
              <p>Тем: {subject.topics.length}</p>

              {subject.topics.length > 0 && (
                <div className="topic-list">
                  {subject.topics.map((topic) => (
                    <div className="topic-item" key={topic.id}>
                      <strong>{topic.title}</strong>
                      <p>Уроков: {topic.lessons.length}</p>
                    </div>
                  ))}
                </div>
              )}

              <button>Войти</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}