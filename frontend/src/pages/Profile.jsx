import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./Profile.css";

const demoProfile = {
  username: "demo",
  level: 1,
  xp: 30,
  coins: 15,
};

export default function Profile() {
  const [profile, setProfile] = useState(demoProfile);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadProfile() {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/profile/");

        if (!response.ok) {
          throw new Error("Profile API error");
        }

        const data = await response.json();
        setProfile({ ...demoProfile, ...(data || {}) });
      } catch {
        setProfile(demoProfile);
      } finally {
        setLoading(false);
      }
    }

    loadProfile();
  }, []);

  if (loading) {
    return (
      <main className="profile-page rpg-layout">
        <DemoSidebar active="profile" />
        <section className="profile-shell rpg-main">
          <p className="profile-message">Загрузка профиля...</p>
        </section>
      </main>
    );
  }

  const xpGoal = Math.max((profile.level || 1) * 250, 250);
  const xpProgress = Math.min(Math.round(((profile.xp || 0) / xpGoal) * 100), 100);
  const achievements = ["First Quest", "Map Explorer", "XP Collector"];

  return (
    <main className="profile-page rpg-layout">
      <DemoSidebar active="profile" />
      <section className="profile-shell rpg-main">
        <header className="profile-hero">
          <div className="profile-avatar">
            {(profile.username || "H").slice(0, 1).toUpperCase()}
          </div>

          <div>
            <span className="profile-eyebrow">Player profile</span>
            <h1>{profile.username}</h1>
            <p>Arcane Scholar / Learning Guild</p>
          </div>
        </header>

        <section className="profile-grid">
          <article className="profile-card profile-main-card">
            <div className="profile-level-row">
              <div>
                <span>Level</span>
                <strong>{profile.level}</strong>
              </div>
              <div>
                <span>Coins</span>
                <strong>{profile.coins}</strong>
              </div>
              <div>
                <span>XP</span>
                <strong>{profile.xp}</strong>
              </div>
            </div>

            <div className="profile-xp-block">
              <div>
                <span>Next level progress</span>
                <strong>{xpProgress}%</strong>
              </div>
              <div className="profile-xp-bar" aria-label={`${xpProgress}% XP`}>
                <span style={{ width: `${xpProgress}%` }} />
              </div>
            </div>
          </article>

          <article className="profile-card">
            <span className="profile-card-label">Streak</span>
            <h2>1 day</h2>
            <p>Keep completing lessons to grow the streak.</p>
          </article>

          <article className="profile-card">
            <span className="profile-card-label">Achievements</span>
            <div className="achievement-list">
              {achievements.map((achievement) => (
                <span key={achievement}>{achievement}</span>
              ))}
            </div>
          </article>

          <article className="profile-card">
            <span className="profile-card-label">Stats</span>
            <div className="profile-stat-list">
              <p>Lessons completed: 1</p>
              <p>Subjects unlocked: 1</p>
              <p>Guild rank: Apprentice</p>
            </div>
          </article>
        </section>
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
