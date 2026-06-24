import { useEffect, useState } from 'react'
import api from '../api'

export default function Shop() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [msg, setMsg] = useState(null)

  useEffect(() => {
    api.get('/flashcards/').then(r => setItems(r.data)).catch(console.error).finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="page-loading">Загрузка...</div>

  return (
    <div className="page">
      <h1>Магазин</h1>
      {msg && <div className="toast">{msg}</div>}
      {items.length === 0
        ? <p className="muted">Пусто. Добавь колоды через админку!</p>
        : <div className="shop-grid">
            {items.map(item => (
              <div key={item.id} className="shop-card">
                <h3>{item.title ?? item.name}</h3>
                <p className="muted">{item.description?.slice(0, 80)}</p>
                <button className="btn-primary" onClick={() => { setMsg(`Открыто: ${item.title ?? item.name}`); setTimeout(() => setMsg(null), 3000) }}>Открыть</button>
              </div>
            ))}
          </div>
      }
    </div>
  )
}
