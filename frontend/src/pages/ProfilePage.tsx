import { FormEvent, useEffect, useState } from 'react'
import { apiFetch } from '../lib/api/client'
import { useAuth } from '../lib/auth/AuthContext'

export function ProfilePage() {
  const { session, refresh } = useAuth()
  const [fullName, setFullName] = useState('')
  const [birthDate, setBirthDate] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    setFullName(session?.user?.full_name ?? '')
    setBirthDate(session?.user?.birth_date ?? '')
  }, [session?.user?.full_name, session?.user?.birth_date])

  if (!session?.authenticated) {
    return (
      <section className="panel">
        <h2>پروفایل</h2>
        <p>برای مشاهده پروفایل ابتدا وارد شوید.</p>
      </section>
    )
  }

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setError('')
    setMessage('')
    setSubmitting(true)
    try {
      await apiFetch('/api/auth/profile/', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ full_name: fullName, birth_date: birthDate }),
      })
      await refresh()
      setMessage('پروفایل ذخیره شد.')
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section className="page-stack">
      <div className="panel">
        <p className="eyebrow">حساب من</p>
        <h2>پروفایل</h2>
        <p>{session.user?.phone_number}</p>
      </div>
      <form className="panel grid" onSubmit={onSubmit}>
        <input
          autoComplete="name"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          placeholder="نام کامل"
        />
        <input
          value={birthDate}
          onChange={(e) => setBirthDate(e.target.value)}
          placeholder="YYYY-MM-DD"
        />
        {error ? <p className="error">{error}</p> : null}
        {message ? <p className="ok">{message}</p> : null}
        <button className="btn-primary" type="submit" disabled={submitting}>
          {submitting ? 'در حال ذخیره...' : 'ذخیره'}
        </button>
      </form>
    </section>
  )
}
