import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiFetch } from '../lib/api/client'
import { useAuth } from '../lib/auth/AuthContext'

export function RegisterPage() {
  const [phoneNumber, setPhoneNumber] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [nationalId, setNationalId] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const { refresh } = useAuth()
  const navigate = useNavigate()

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await apiFetch('/api/auth/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          phone_number: phoneNumber,
          password,
          confirm_password: confirmPassword,
          full_name: fullName,
          national_id: nationalId,
        }),
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
        <p className="eyebrow">شروع حساب</p>
        <h2>ثبت نام</h2>
        <p>اطلاعات اولیه را وارد کنید تا حساب مشتری ساخته شود.</p>
      </div>
      <form className="panel grid" onSubmit={onSubmit}>
        <input
          autoComplete="tel"
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          placeholder="شماره موبایل"
        />
        <input
          autoComplete="name"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          placeholder="نام کامل"
        />
        <input
          value={nationalId}
          onChange={(e) => setNationalId(e.target.value)}
          placeholder="کد ملی"
        />
        <input
          type="password"
          autoComplete="new-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="رمز عبور"
        />
        <input
          type="password"
          autoComplete="new-password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="تکرار رمز عبور"
        />
        {error ? <p className="error">{error}</p> : null}
        <button className="btn-primary" type="submit" disabled={submitting}>
          {submitting ? 'در حال ثبت...' : 'ایجاد حساب'}
        </button>
      </form>
      <div className="panel">
        <p>
          قبلا ثبت نام کرده‌اید؟ <a href="/login/">ورود</a>
        </p>
      </div>
    </section>
  )
}
