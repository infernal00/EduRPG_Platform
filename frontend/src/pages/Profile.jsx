import { useEffect, useState } from 'react'
import api from '../api'

export default function Profile() {
  const [user, setUser] = useState(null)
  const [achievements, setAchievements] = useState([])

  useEffect(() => {
    api.get('/users/me/').then(r => setUser(r.data)).catch(console.error)
    api.get('/users/me/achievements/').then(r => setAchievements(r.data)).catch(() => {})
  }, [])

  if (!user) return <div className="page-loading">Загрузка...</div>

  return (
    <div className="page">
      <h1>Профиль</h1>
      <div className="profile-card">
        <div className="avatar">{user.username[0].toUpperCase()}</div>
        <div>
          <h2 style={{ margin: 0 }}>{user.username}</h2>
          <p className="muted">{user.character_class ?? 'Новичок'}</p>
        </div>
      </div>
      <div className="stats-grid">
        <div className="stat-card"><span className="stat-label">Уровень</span><span className="stat-value">{user.level}</span></div>
        <div className="stat-card"><span className="stat-label">XP</span><span className="stat-value">{user.xp}</span></div>
        <div className="stat-card"><span className="stat-label">Монеты</span><span className="stat-value">{user.coins}</span></div>
        <div className="stat-card"><span className="stat-label">Здоровье</span><span className="stat-value">{user.health}</span></div>
      </div>
      <h2>Достижения</h2>
      {achievements.length === 0
        ? <p className="muted">Пока нет — учись и сражайся!</p>
        : <div className="achievements-grid">
            {achievements.map(a => (
              <div key={a.id} className="achievement-card">
                <span className="ach-icon">{a.icon ?? '🏅'}</span>
                <span className="ach-name">{a.name}</span>
              </div>
            ))}
          </div>
      }
    </div>
  )
}
