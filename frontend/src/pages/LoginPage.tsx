import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiFetch } from '../lib/api/client'
import { useAuth } from '../lib/auth/AuthContext'

export function LoginPage() {
  const [phoneNumber, setPhoneNumber] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const { refresh } = useAuth()
  const navigate = useNavigate()

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await apiFetch('/api/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone_number: phoneNumber, password }),
      })
      await refresh()
      navigate('/')
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section className="page-stack">
      <div className="panel">
        <p className="eyebrow">حساب کاربری</p>
        <h2>ورود</h2>
        <p>برای ثبت سفارش و رزرو، با شماره موبایل وارد شوید.</p>
      </div>
      <form className="panel grid" onSubmit={onSubmit}>
        <input
          autoComplete="tel"
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          placeholder="09xxxxxxxxx"
        />
        <input
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="رمز عبور"
        />
        {error ? <p className="error">{error}</p> : null}
        <button className="btn-primary" type="submit" disabled={submitting}>
          {submitting ? 'در حال ورود...' : 'ورود'}
        </button>
      </form>
      <div className="panel">
        <p>
          حساب ندارید؟ <a href="/register/">ثبت نام</a>
        </p>
      </div>
    </section>
  )
}
