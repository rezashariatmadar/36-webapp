import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiFetch } from '../lib/api/client'

export function CafeCheckoutPage() {
  const [notes, setNotes] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const navigate = useNavigate()

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await apiFetch('/api/cafe/checkout/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ notes }),
      })
      navigate('/cafe/orders/')
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section className="page-stack">
      <div className="panel">
        <p className="eyebrow">تکمیل خرید</p>
        <h2>ثبت نهایی سفارش</h2>
        <p>یادداشت سفارش را ثبت کنید و به صفحه سفارش‌ها بروید.</p>
      </div>
      <form className="panel grid" onSubmit={submit}>
        <textarea value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="توضیحات سفارش" />
        {error ? <p className="error">{error}</p> : null}
        <button className="btn-primary" type="submit" disabled={submitting}>
          {submitting ? 'در حال ثبت...' : 'ثبت سفارش'}
        </button>
      </form>
    </section>
  )
}
