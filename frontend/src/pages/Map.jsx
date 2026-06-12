import { useEffect, useState } from "react";
import biologyIcon from "../assets/subjects/biology.svg";
import defaultIcon from "../assets/subjects/default.svg";
import englishIcon from "../assets/subjects/english.svg";
import mathIcon from "../assets/subjects/math.svg";
import physicsIcon from "../assets/subjects/physics.svg";
import programmingIcon from "../assets/subjects/programming.svg";
import "./Map.css";

const API_URL = "http://127.0.0.1:8000/api/subjects/";

const iconMap = {
  biology: biologyIcon,
  math: mathIcon,
  physics: physicsIcon,
  programming: programmingIcon,
  english: englishIcon,
  default: defaultIcon,
};

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
      } catch {
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
          {subjects.map((subject) => {
            const topics = subject.topics || [];
            const subjectIcon = iconMap[subject.icon] || defaultIcon;

            return (
              <div className="location-card" key={subject.id}>
                <div className="location-card-header">
                  <div className="subject-icon-frame">
                    <img
                      className="subject-icon"
                      src={subjectIcon}
                      alt=""
                      aria-hidden="true"
                    />
                  </div>

                  <div>
                    <span className="location-label">Локация</span>
                    <h3>{subject.name}</h3>
                  </div>
                </div>

                <p className="location-description">
                  {subject.description || "Описание пока не добавлено."}
                </p>
                <p className="topic-count">Тем: {topics.length}</p>

                {topics.length > 0 && (
                  <div className="topic-list">
                    {topics.map((topic) => {
                      const lessons = topic.lessons || [];

                      return (
                        <div className="topic-item" key={topic.id}>
                          <strong>{topic.title}</strong>
                          <span>Уроков: {lessons.length}</span>
                        </div>
                      );
                    })}
                  </div>
                )}

                <button>Войти</button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
