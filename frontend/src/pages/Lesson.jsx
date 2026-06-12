import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import "./Lesson.css";

export default function Lesson() {
  const { id } = useParams();

  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [completeResult, setCompleteResult] = useState(null);
  const [completing, setCompleting] = useState(false);

  useEffect(() => {
    async function loadLesson() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/lessons/${id}/`);

        if (!response.ok) {
          throw new Error("Lesson not found");
        }

        const data = await response.json();
        setLesson(data);
      } catch {
        setError("Не удалось загрузить урок. Проверь backend или ID урока.");
      } finally {
        setLoading(false);
      }
    }

    loadLesson();
  }, [id]);

  async function handleCompleteLesson() {
    setCompleting(true);
    setCompleteResult(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/lessons/${id}/complete/`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to complete lesson");
      }

      const data = await response.json();
      setCompleteResult(data);
    } catch {
      setCompleteResult({
        status: "error",
        message: "Не удалось завершить урок. Проверь backend.",
      });
    } finally {
      setCompleting(false);
    }
  }

  if (loading) {
    return (
      <div className="lesson-page">
        <p>Загрузка урока...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="lesson-page">
        <p>{error}</p>
        <Link to="/map">Вернуться к карте</Link>
      </div>
    );
  }

  return (
    <div className="lesson-page">
      <Link className="back-link" to="/map">
        ← Назад к карте
      </Link>

      <div className="lesson-card">
        <div className="lesson-header">
          <div>
            <span className="lesson-badge">{lesson.subject_name}</span>
            <span className="lesson-badge">{lesson.topic_title}</span>
          </div>

          <span className="lesson-level">{lesson.level}</span>
        </div>

        <h1>{lesson.title}</h1>

        <div className="lesson-rewards">
          <span>⭐ {lesson.xp_reward} XP</span>
          <span>🪙 {lesson.coins_reward} coins</span>
        </div>

        <div className="lesson-content">
          {lesson.content ? (
            <p>{lesson.content}</p>
          ) : (
            <p>
              Контент урока пока не добавлен. Добавь текст через Django Admin.
            </p>
          )}
        </div>

        <button
          className="complete-button"
          onClick={handleCompleteLesson}
          disabled={completing}
        >
          {completing ? "Завершаем..." : "Завершить урок"}
        </button>

        {completeResult && (
          <div className="complete-result">
            {completeResult.status === "completed" ? (
              <p>
                Урок завершён! +{completeResult.xp_gained} XP и +
                {completeResult.coins_gained} coins.
              </p>
            ) : completeResult.status === "already_completed" ? (
              <p>Этот урок уже был завершён. Награда уже получена.</p>
            ) : (
              <p>{completeResult.message}</p>
            )}

            {completeResult.profile && (
              <p>
                Level: {completeResult.profile.level} | XP:{" "}
                {completeResult.profile.xp} | Coins:{" "}
                {completeResult.profile.coins}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}