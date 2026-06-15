import { Link } from "react-router-dom";
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

const demoSubjects = [
  {
    id: 1,
    name: "Biology",
    description: "Explore the living world through genetics, cells, and discovery quests.",
    icon: "biology",
    topics: [
      {
        id: 1,
        title: "Genetics",
        description: "Learn how information is stored and passed between living things.",
        lessons: [
          {
            id: 1,
            title: "What is DNA?",
            level: "beginner",
            xp_reward: 30,
            coins_reward: 15,
          },
        ],
      },
    ],
  },
];

export default function Map() {
  const [subjects, setSubjects] = useState(demoSubjects);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadSubjects() {
      try {
        const response = await fetch(API_URL);

        if (!response.ok) {
          throw new Error("Map API request failed");
        }

        const data = await response.json();
        setSubjects(Array.isArray(data) && data.length > 0 ? data : demoSubjects);
      } catch {
        setSubjects(demoSubjects);
      } finally {
        setLoading(false);
      }
    }

    loadSubjects();
  }, []);

  if (loading) {
    return (
      <div className="map-page">
        <div className="map-shell">
          <h1>Мир знаний</h1>
          <p className="map-message">Загрузка карты...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="map-page">
      <div className="map-shell">
        <header className="map-hero">
          <div>
            <span className="map-eyebrow">Learning map</span>
            <h1>Мир знаний</h1>
            <p>
              Выбери предмет, открой тему и начни следующий урок в своей RPG
              прокачке.
            </p>
          </div>

          <div className="map-summary-card">
            <span>Предметов</span>
            <strong>{subjects.length}</strong>
            <p>Активные маршруты обучения</p>
          </div>
        </header>

        {subjects.length === 0 ? (
          <p className="map-message">Карта готовится к следующему маршруту.</p>
        ) : (
          <div className="map-grid">
            {subjects.map((subject, index) => {
              const topics = subject.topics || [];
              const subjectIcon = iconMap[subject.icon] || defaultIcon;
              const lessonCount = topics.reduce((total, topic) => {
                const lessons = topic.lessons || [];
                return total + lessons.length;
              }, 0);
              const progress = Math.min(28 + topics.length * 12 + lessonCount * 7, 94);

              return (
                <article className="location-card" key={subject.id || subject.name}>
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
                      <span className="location-label">Локация {index + 1}</span>
                      <h3>{subject.name}</h3>
                    </div>
                  </div>

                  <p className="location-description">
                    {subject.description ||
                      "Готовый маршрут с темами, уроками и наградами за прогресс."}
                  </p>

                  <div className="map-progress-row">
                    <span>{topics.length} тем</span>
                    <span>{lessonCount} уроков</span>
                  </div>
                  <div className="map-progress-bar" aria-label={`${progress}% progress`}>
                    <span style={{ width: `${progress}%` }} />
                  </div>

                  {topics.length > 0 && (
                    <div className="topic-list">
                      {topics.map((topic) => {
                        const lessons = topic.lessons || [];

                        return (
                          <section className="topic-item" key={topic.id}>
                            <div className="topic-item-header">
                              <strong>{topic.title}</strong>
                              <span>{lessons.length} уроков</span>
                            </div>

                            {lessons.length > 0 && (
                              <div className="lesson-link-list">
                                {lessons.map((lesson) => (
                                  <Link
                                    className="lesson-map-link"
                                    key={lesson.id}
                                    to={`/lessons/${lesson.id}`}
                                  >
                                    <span>{lesson.title}</span>
                                    <em>+{lesson.xp_reward || 30} XP</em>
                                  </Link>
                                ))}
                              </div>
                            )}
                          </section>
                        );
                      })}
                    </div>
                  )}

                  {topics[0]?.lessons?.[0] ? (
                    <Link
                      className="map-enter-button"
                      to={`/lessons/${topics[0].lessons[0].id}`}
                    >
                      Начать маршрут
                    </Link>
                  ) : (
                    <button disabled>Нет уроков</button>
                  )}
                </article>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
