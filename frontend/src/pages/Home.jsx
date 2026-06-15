import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import "./Home.css";

const PROFILE_URL = "http://127.0.0.1:8000/api/profile/";
const SUBJECTS_URL = "http://127.0.0.1:8000/api/subjects/";

const demoProfile = {
  username: "HeroStudent",
  level: 8,
  xp: 1280,
  coins: 340,
};

const demoSubjects = [
  {
    id: 1,
    name: "Biology",
    icon: "biology",
    topics: [
      {
        id: 1,
        title: "Genetics",
        lessons: [{ id: 1, title: "What is DNA?", xp_reward: 30 }],
      },
      {
        id: 2,
        title: "Cells",
        lessons: [{ id: 2, title: "Inside the Cell", xp_reward: 35 }],
      },
    ],
  },
  {
    id: 2,
    name: "Math",
    icon: "math",
    topics: [
      {
        id: 3,
        title: "Algebra",
        lessons: [{ id: 3, title: "Linear Equations", xp_reward: 25 }],
      },
      {
        id: 4,
        title: "Functions",
        lessons: [{ id: 4, title: "Graph Basics", xp_reward: 35 }],
      },
    ],
  },
  {
    id: 3,
    name: "Programming",
    icon: "programming",
    topics: [
      {
        id: 5,
        title: "JavaScript",
        lessons: [{ id: 5, title: "Variables and Values", xp_reward: 40 }],
      },
    ],
  },
  {
    id: 4,
    name: "Physics",
    icon: "physics",
    topics: [
      {
        id: 6,
        title: "Motion",
        lessons: [{ id: 6, title: "Speed and Force", xp_reward: 45 }],
      },
    ],
  },
];

const subjectThemes = {
  biology: { shortName: "BIO", accent: "#34d399", soft: "rgba(52, 211, 153, 0.16)" },
  math: { shortName: "MTH", accent: "#facc15", soft: "rgba(250, 204, 21, 0.15)" },
  physics: { shortName: "PHY", accent: "#38bdf8", soft: "rgba(56, 189, 248, 0.16)" },
  programming: { shortName: "DEV", accent: "#a78bfa", soft: "rgba(167, 139, 250, 0.18)" },
  english: { shortName: "ENG", accent: "#fb7185", soft: "rgba(251, 113, 133, 0.15)" },
};

const fallbackThemes = [
  { shortName: "SUB", accent: "#a78bfa", soft: "rgba(167, 139, 250, 0.18)" },
  { shortName: "QST", accent: "#22d3ee", soft: "rgba(34, 211, 238, 0.16)" },
  { shortName: "ARC", accent: "#f59e0b", soft: "rgba(245, 158, 11, 0.14)" },
];

const dailyQuests = [
  {
    name: "Complete one lesson",
    detail: "Finish a topic quest before midnight",
    reward: "+30 XP",
    done: true,
  },
  {
    name: "Open the learning map",
    detail: "Choose the next subject route",
    reward: "+10 coins",
    done: false,
  },
  {
    name: "Review yesterday's topic",
    detail: "Keep the knowledge chain alive",
    reward: "+20 XP",
    done: false,
  },
];

const recentActivity = [
  "Collected coins from a practice quest",
  "Unlocked progress on the learning map",
  "Prepared the next recommended lesson",
];

async function fetchJson(url) {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("API request failed");
  }

  return response.json();
}

function countLessons(subject) {
  const topics = subject.topics || [];

  return topics.reduce((total, topic) => {
    const lessons = topic.lessons || [];
    return total + lessons.length;
  }, 0);
}

function getFirstLesson(subjects) {
  for (const subject of subjects) {
    const topics = subject.topics || [];

    for (const topic of topics) {
      const lessons = topic.lessons || [];

      if (lessons.length > 0) {
        return {
          ...lessons[0],
          subjectName: subject.name,
          topicTitle: topic.title,
        };
      }
    }
  }

  return {
    id: 1,
    title: "Start Your First Quest",
    xp_reward: 30,
    subjectName: "EduRPG",
    topicTitle: "Practice",
  };
}

function getSubjectTheme(subject, index) {
  return subjectThemes[subject.icon] || fallbackThemes[index % fallbackThemes.length];
}

export default function Home() {
  const [profile, setProfile] = useState(demoProfile);
  const [subjects, setSubjects] = useState(demoSubjects);
  const [loading, setLoading] = useState(true);
  const [usingDemoData, setUsingDemoData] = useState(false);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [profileResult, subjectsResult] = await Promise.allSettled([
          fetchJson(PROFILE_URL),
          fetchJson(SUBJECTS_URL),
        ]);

        if (profileResult.status === "fulfilled") {
          setProfile(profileResult.value || demoProfile);
        } else {
          setUsingDemoData(true);
        }

        if (
          subjectsResult.status === "fulfilled" &&
          Array.isArray(subjectsResult.value) &&
          subjectsResult.value.length > 0
        ) {
          setSubjects(subjectsResult.value);
        } else {
          setUsingDemoData(true);
        }
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  const player = {
    hearts: 5,
    streak: 12,
    title: "Arcane Scholar",
    ...profile,
  };

  const dashboardStats = useMemo(() => {
    const totalSubjects = subjects.length;
    const totalLessons = subjects.reduce(
      (total, subject) => total + countLessons(subject),
      0,
    );
    const nextLevelXp = Math.max((player.level || 1) * 250, 250);
    const currentXp = player.xp || 0;
    const xpProgress = Math.min(Math.round((currentXp / nextLevelXp) * 100), 100);
    const xpRemaining = Math.max(nextLevelXp - currentXp, 0);

    return {
      totalSubjects,
      totalLessons,
      nextLevelXp,
      xpProgress,
      xpRemaining,
    };
  }, [player.level, player.xp, subjects]);

  const recommendedLesson = getFirstLesson(subjects);
  const profileName = player.username || "Adventurer";
  const profileInitial = profileName.slice(0, 1).toUpperCase();
  const completedQuests = dailyQuests.filter((quest) => quest.done).length;
  const leaderboard = [
    { name: profileName, level: player.level || 1, rank: 1, score: "2,840 XP" },
    { name: "ManaCoder", level: 7, rank: 2, score: "2,410 XP" },
    { name: "QuizKnight", level: 6, rank: 3, score: "2,180 XP" },
  ];

  return (
    <main className="home-dashboard">
      <aside className="home-sidebar">
        <Link className="sidebar-brand" to="/">
          <span className="brand-mark">E</span>
          <span>
            <strong>EduRPG</strong>
            <em>Academy hub</em>
          </span>
        </Link>

        <nav className="sidebar-nav" aria-label="Dashboard navigation">
          <Link className="is-active" to="/">
            Dashboard
          </Link>
          <Link to="/map">Learning map</Link>
          <Link to={`/lessons/${recommendedLesson.id}`}>Current lesson</Link>
          <Link to="/profile">Hero profile</Link>
        </nav>

        <div className="sidebar-player">
          <div className="sidebar-avatar">{profileInitial}</div>
          <strong>{profileName}</strong>
          <span>{player.title}</span>
          <div className="sidebar-meter">
            <span style={{ width: `${dashboardStats.xpProgress}%` }} />
          </div>
        </div>
      </aside>

      <section className="dashboard-shell">
        <header className="dashboard-topbar">
          <div>
            <span className="eyebrow">Demo-ready learning dashboard</span>
            <h1>Continue your EduRPG run</h1>
          </div>

          <div className="top-stat-chips" aria-label="Player stats">
            <div className="stat-chip">
              <span>LVL</span>
              <strong>{player.level || 1}</strong>
            </div>
            <div className="stat-chip">
              <span>XP</span>
              <strong>{player.xp || 0}</strong>
            </div>
            <div className="stat-chip">
              <span>Coins</span>
              <strong>{player.coins || 0}</strong>
            </div>
            <div className="stat-chip">
              <span>Streak</span>
              <strong>{player.streak}</strong>
            </div>
            <div className="stat-chip">
              <span>Hearts</span>
              <strong>{player.hearts}</strong>
            </div>
          </div>
        </header>

        {loading && <p className="dashboard-note">Loading live academy data...</p>}
        {usingDemoData && !loading && (
          <p className="dashboard-note">
            Demo data is active while the local API has missing dashboard data.
          </p>
        )}

        <section className="dashboard-grid">
          <section className="dashboard-main-column">
            <article className="continue-card">
              <div className="continue-card-copy">
                <span className="mode-badge">Continue Learning</span>
                <h2>{recommendedLesson.title}</h2>
                <p>
                  {recommendedLesson.subjectName} / {recommendedLesson.topicTitle}
                </p>

                <div className="hero-progress">
                  <div>
                    <span>Level progress</span>
                    <strong>
                      {dashboardStats.xpRemaining} XP to level {(player.level || 1) + 1}
                    </strong>
                  </div>
                  <div className="xp-track" aria-label={`${dashboardStats.xpProgress}% XP`}>
                    <span style={{ width: `${dashboardStats.xpProgress}%` }} />
                  </div>
                </div>

                <div className="hero-actions">
                  <Link className="primary-action" to={`/lessons/${recommendedLesson.id}`}>
                    Start quest
                  </Link>
                  <Link className="secondary-action" to="/map">
                    View map
                  </Link>
                </div>
              </div>

              <div className="continue-card-metrics">
                <div>
                  <span>Reward</span>
                  <strong>+{recommendedLesson.xp_reward || 30} XP</strong>
                </div>
                <div>
                  <span>Subjects</span>
                  <strong>{dashboardStats.totalSubjects}</strong>
                </div>
                <div>
                  <span>Lessons</span>
                  <strong>{dashboardStats.totalLessons}</strong>
                </div>
              </div>
            </article>

            <section className="subjects-section" aria-labelledby="subjects-heading">
              <div className="section-heading">
                <div>
                  <span className="eyebrow">Subject progress</span>
                  <h2 id="subjects-heading">Active learning paths</h2>
                </div>
                <Link to="/map">Open full map</Link>
              </div>

              <div className="subject-card-grid">
                {subjects.slice(0, 4).map((subject, index) => {
                  const lessons = countLessons(subject);
                  const progress = Math.min(32 + index * 13 + lessons * 7, 96);
                  const theme = getSubjectTheme(subject, index);

                  return (
                    <article
                      className="subject-card"
                      key={subject.id || subject.name}
                      style={{
                        "--subject-accent": theme.accent,
                        "--subject-soft": theme.soft,
                      }}
                    >
                      <div className="subject-card-top">
                        <span className="subject-rune">{theme.shortName}</span>
                        <span>{progress}%</span>
                      </div>
                      <h3>{subject.name}</h3>
                      <p>{lessons} lessons across {(subject.topics || []).length} topics</p>
                      <div className="subject-bar" aria-label={`${progress}% complete`}>
                        <span style={{ width: `${progress}%` }} />
                      </div>
                    </article>
                  );
                })}
              </div>
            </section>
          </section>

          <aside className="dashboard-side-panels">
            <article className="panel-card quests-card">
              <div className="panel-heading-row">
                <div>
                  <span className="panel-kicker">Daily quests</span>
                  <h2>Today&apos;s objectives</h2>
                </div>
                <strong>
                  {completedQuests}/{dailyQuests.length}
                </strong>
              </div>
              <div className="quest-list">
                {dailyQuests.map((quest) => (
                  <div className="quest-item" key={quest.name}>
                    <span className={quest.done ? "quest-dot done" : "quest-dot"} />
                    <div>
                      <strong>{quest.name}</strong>
                      <p>{quest.detail}</p>
                    </div>
                    <em>{quest.reward}</em>
                  </div>
                ))}
              </div>
            </article>

            <article className="panel-card leaderboard-card">
              <span className="panel-kicker">Leaderboard</span>
              <h2>Guild ranking</h2>
              <div className="leaderboard-list">
                {leaderboard.map((playerRow) => (
                  <div className="leaderboard-row" key={playerRow.name}>
                    <span>#{playerRow.rank}</span>
                    <strong>{playerRow.name}</strong>
                    <em>{playerRow.score}</em>
                  </div>
                ))}
              </div>
            </article>

            <article className="panel-card activity-card">
              <span className="panel-kicker">Recent activity</span>
              <h2>Adventure feed</h2>
              <div className="activity-list">
                {recentActivity.map((activity) => (
                  <p key={activity}>{activity}</p>
                ))}
              </div>
            </article>
          </aside>
        </section>
      </section>
    </main>
  );
}
