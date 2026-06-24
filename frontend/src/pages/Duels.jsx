import { useEffect, useState } from 'react'
import api from '../api'

export default function Duels() {
  const [battles, setBattles] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/battles/').then(r => setBattles(r.data)).catch(console.error).finally(() => setLoading(false))
  }, [])

  const statusLabel = { pending: 'Ожидание', active: 'В бою', finished: 'Завершён' }

  if (loading) return <div className="page-loading">Загрузка...</div>

  return (
    <div className="page">
      <h1>Дуэли</h1>
      {battles.length === 0
        ? <p className="muted">Дуэлей нет. Брось вызов!</p>
        : <div className="duels-list">
            {battles.map(b => (
              <div key={b.id} className="duel-card">
                <div className="duel-players">
                  <span>{b.challenger_username ?? b.challenger}</span>
                  <span className="vs">VS</span>
                  <span>{b.opponent_username ?? b.opponent ?? '???'}</span>
                </div>
                <div className="duel-meta">
                  <span className="badge">{statusLabel[b.status] ?? b.status}</span>
                  {b.winner && <span className="badge badge-gold">Победитель: {b.winner}</span>}
                </div>
              </div>
            ))}
          </div>
      }
    </div>
  )
}
