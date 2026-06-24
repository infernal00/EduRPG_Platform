import { useEffect, useState } from 'react'
import api from '../api'

export default function Home() {
  const [user, setUser] = useState(null)
  const [lessons, setLessons] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      api.get('/users/me/'),
      api.get('/lessons/'),
    ]).then(([u, l]) => {
      setUser(u.data)
      setLessons(l.data.slice(0, 3))
    }).catch(console.error).finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="page-loading">Загрузка...</div>

  const xpForNextLevel = Math.floor(100 * Math.pow(1.5, (user?.level ?? 1) - 1))
  const xpProgress = Math.min(100, Math.round(((user?.xp ?? 0) / xpForNextLevel) * 100))

  return (
    <div className="page">
      <h1>Привет, {user?.username}!</h1>
      <div className="stats-grid">
        <div className="stat-card"><span className="stat-label">Уровень</span><span className="stat-value">{user?.level ?? 1}</span></div>
        <div className="stat-card"><span className="stat-label">Опыт</span><span className="stat-value">{user?.xp ?? 0}</span></div>
        <div className="stat-card"><span className="stat-label">Монеты</span><span className="stat-value">{user?.coins ?? 0}</span></div>
        <div className="stat-card"><span className="stat-label">Здоровье</span><span className="stat-value">{user?.health ?? 100}</span></div>
      </div>
      <div className="xp-bar-wrap">
        <div className="xp-bar-label">До уровня {(user?.level ?? 1) + 1}: {user?.xp ?? 0} / {xpForNextLevel} XP</div>
        <div className="xp-bar"><div className="xp-bar-fill" style={{ width: `${xpProgress}%` }} /></div>
      </div>
      <h2>Последние уроки</h2>
      {lessons.length === 0
        ? <p className="muted">Уроков нет — зайди на Карту!</p>
        : <div className="lessons-list">
            {lessons.map(l => (
              <div key={l.id} className="lesson-card">
                <h3>{l.title}</h3>
                <p className="muted">{l.description?.slice(0, 100)}</p>
                <span className="badge">+{l.xp_reward ?? 30} XP</span>
              </div>
            ))}
          </div>
      }
    </div>
  )
}
