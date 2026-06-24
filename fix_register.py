content = """import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

export default function Register() {
  const [form, setForm] = useState({ username: '', email: '', password: '', password2: '' })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handle = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const submit = async (e) => {
    e.preventDefault()
    if (form.password !== form.password2) { setError('Пароли не совпадают'); return }
    setLoading(true)
    setError(null)
    try {
      const res = await axios.post('/api/auth/register/', {
        username: form.username,
        email: form.email,
        password: form.password,
      })
      localStorage.setItem('access_token', res.data.access)
      localStorage.setItem('refresh_token', res.data.refresh)
      navigate('/')
    } catch (err) {
      const data = err.response?.data
      setError(typeof data === 'object' ? Object.values(data).flat().join(' ') : 'Ошибка регистрации')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>EduRPG</h1>
        <p className="muted">Создай аккаунт</p>
        {error && <div className="error-box">{error}</div>}
        <form onSubmit={submit}>
          <div className="field">
            <label>Логин</label>
            <input name="username" value={form.username} onChange={handle} placeholder="username" required />
          </div>
          <div className="field">
            <label>Email</label>
            <input name="email" type="email" value={form.email} onChange={handle} placeholder="you@example.com" required />
          </div>
          <div className="field">
            <label>Пароль</label>
            <input type="password" name="password" value={form.password} onChange={handle} placeholder="password" required />
          </div>
          <div className="field">
            <label>Повтори пароль</label>
            <input type="password" name="password2" value={form.password2} onChange={handle} placeholder="password" required />
          </div>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Создаём...' : 'Зарегистрироваться'}
          </button>
        </form>
        <p style={{ marginTop: '1rem', textAlign: 'center' }}>
          Уже есть аккаунт? <a href="/login" style={{ color: '#a78bfa' }}>Войти</a>
        </p>
      </div>
    </div>
  )
}"""
with open('frontend/src/pages/Register.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')
