import { useEffect, useState } from 'react'
import api from '../api'
import './Map.css'

export default function Map() {
  const [lessons, setLessons] = useState([])
  const [progress, setProgress] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      api.get('/lessons/'),
      api.get('/lessons/progress/').catch(() => ({ data: [] })),
    ]).then(([l, p]) => {
      setLessons(l.data)
      setProgress(p.data)
    }).finally(() => setLoading(false))
  }, [])

  const completedIds = new Set(progress.filter(p => p.completed).map(p => p.lesson))

  if (loading) return <div className="page-loading">Загрузка карты...</div>

  return (
    <div className="map-page">
      <h1>Мир знаний</h1>
      <div className="map-grid">
        {lessons.length === 0
          ? <p className="muted">Уроков нет. Добавь через админку!</p>
          : lessons.map(l => (
              <div className={`location-card ${completedIds.has(l.id) ? 'completed' : ''}`} key={l.id}>
                {completedIds.has(l.id) && <span className="done-badge">Пройден</span>}
                <h3>{l.title}</h3>
                <p>{l.description?.slice(0, 80) ?? 'Без описания'}</p>
                <div className="card-footer">
                  <span className="badge">+{l.xp_reward ?? 30} XP</span>
                  <button onClick={() => alert(l.title)}>Войти</button>
                </div>
              </div>
            ))
        }
      </div>
    </div>
  )
}
