import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import "./Lesson.css";

const demoLesson = {
  id: 1,
  title: "What is DNA?",
  subject_name: "Biology",
  topic_title: "Genetics",
  level: "beginner",
  xp_reward: 30,
  coins_reward: 15,
  content:
    "DNA is the instruction system inside living cells. It stores genetic information, helps cells build proteins, and passes traits from parents to offspring. In genetics, DNA is the starting point for understanding how life grows, changes, and adapts.",
};

export default function Lesson() {
  const { id } = useParams();

  const [lesson, setLesson] = useState(demoLesson);
  const [loading, setLoading] = useState(true);

  const [completeResult, setCompleteResult] = useState(null);
  const [completing, setCompleting] = useState(false);
  const lessonCompleted =
    completeResult?.status === "completed" ||
    completeResult?.status === "already_completed";

  useEffect(() => {
    async function loadLesson() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/lessons/${id}/`);

        if (!response.ok) {
          throw new Error("Lesson not found");
        }

        const data = await response.json();
        setLesson({ ...demoLesson, ...(data || {}) });
      } catch {
        setLesson(demoLesson);
      } finally {
        setLoading(false);
      }
    }

    loadLesson();
  }, [id]);

  async function handleCompleteLesson() {
    if (lessonCompleted || completing) {
      return;
    }

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
        status: "completed",
        xp_gained: lesson.xp_reward || demoLesson.xp_reward,
        coins_gained: lesson.coins_reward || demoLesson.coins_reward,
      });
    } finally {
      setCompleting(false);
    }
  }

  if (loading) {
    return (
      <main className="lesson-page rpg-layout">
        <DemoSidebar active="lesson" />
        <section className="lesson-shell rpg-main">
          <p className="lesson-state">Загрузка урока...</p>
        </section>
      </main>
    );
  }

  const xpReward = lesson.xp_reward || 30;
  const coinsReward = lesson.coins_reward || 15;
  const level = lesson.level || "beginner";
  const lessonContent = lesson.content || demoLesson.content;

  return (
    <main className="lesson-page rpg-layout">
      <DemoSidebar active="lesson" />
      <section className="lesson-shell rpg-main">
        <Link className="back-link" to="/map">
          Назад к карте
        </Link>

        <div className="lesson-layout">
          <article className="lesson-card">
            <div className="lesson-header">
              <div>
                <span className="lesson-kicker">Lesson quest</span>
                <h1>{lesson.title}</h1>
              </div>

              <span className="lesson-level">{level}</span>
            </div>

            <div className="lesson-badges">
              <span className="lesson-badge">{lesson.subject_name || "EduRPG"}</span>
              <span className="lesson-badge">{lesson.topic_title || "Practice"}</span>
            </div>

            <section className="lesson-content-card">
              <span className="lesson-section-label">Learning scroll</span>
              <div className="lesson-content">
                <p>{lessonContent}</p>
              </div>
            </section>

            {completeResult && (
              <div className="complete-result">
                {completeResult.status === "completed" ? (
                  <>
                    <strong>Lesson complete</strong>
                    <p>
                      Reward collected: +{completeResult.xp_gained || xpReward} XP and +
                      {completeResult.coins_gained || coinsReward} coins.
                    </p>
                  </>
                ) : completeResult.status === "already_completed" ? (
                  <>
                    <strong>Already completed</strong>
                    <p>Reward is already saved to your profile.</p>
                  </>
                ) : (
                  <>
                    <strong>Progress saved</strong>
                    <p>Your lesson run is ready to continue.</p>
                  </>
                )}

                {completeResult.profile && (
                  <p>
                    Level: {completeResult.profile.level} | XP:{" "}
                    {completeResult.profile.xp} | Coins:{" "}
                    {completeResult.profile.coins}
                  </p>
                )}

                <Link className="complete-profile-link" to="/profile">
                  View Profile
                </Link>
              </div>
            )}
          </article>

          <aside className="lesson-side-panel">
            <div className="reward-card">
              <span>Quest reward</span>
              <strong>+{xpReward} XP</strong>
              <p>+{coinsReward} coins after completion</p>
            </div>

            <div className="lesson-checklist">
              <span>Progress</span>
              <p>Read the lesson content</p>
              <p>Complete the quest action</p>
              <p>Return to profile to view rewards</p>
            </div>

            <button
              className={lessonCompleted ? "complete-button is-complete" : "complete-button"}
              onClick={handleCompleteLesson}
              disabled={completing || lessonCompleted}
            >
              {lessonCompleted
                ? "Урок завершён"
                : completing
                  ? "Завершаем..."
                  : "Завершить урок"}
            </button>
          </aside>
        </div>
      </section>
    </main>
  );
}

function DemoSidebar({ active }) {
  return (
    <aside className="rpg-sidebar">
      <Link className="rpg-brand" to="/">
        <span className="rpg-brand-mark">E</span>
        <span>
          <strong>EduRPG</strong>
          <em>Academy hub</em>
        </span>
      </Link>

      <nav className="rpg-nav" aria-label="Demo navigation">
        <Link className={active === "home" ? "is-active" : ""} to="/">
          Dashboard
        </Link>
        <Link className={active === "map" ? "is-active" : ""} to="/map">
          Learning Map
        </Link>
        <Link className={active === "lesson" ? "is-active" : ""} to="/lessons/1">
          Current Lesson
        </Link>
        <Link to="/duels">Duels</Link>
        <Link to="/shop">Shop</Link>
        <Link className={active === "profile" ? "is-active" : ""} to="/profile">
          Profile
        </Link>
      </nav>

      <div className="rpg-user-card">
        <div className="rpg-user-avatar">d</div>
        <strong>demo</strong>
        <span>Level 1 / 30 XP</span>
        <div className="rpg-mini-meter">
          <span style={{ width: "12%" }} />
        </div>
      </div>
    </aside>
  );
}
