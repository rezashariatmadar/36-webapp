import { FormEvent, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { apiFetch } from '../lib/api/client'

type Preview = {
  valid: boolean
  price: number
  start_time: string
  end_time: string
  end_time_jalali: string
}

export function CoworkBookingPage() {
  const { spaceId } = useParams()
  const [bookingType, setBookingType] = useState('DAILY')
  const [startTime, setStartTime] = useState('')
  const [preview, setPreview] = useState<Preview | null>(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const navigate = useNavigate()

  const runPreview = async () => {
    if (!spaceId) return
    setError('')
    setBusy(true)
    try {
      const params = new URLSearchParams({
        space_id: spaceId,
        booking_type: bookingType,
        start_time: startTime,
      })
      const data = await apiFetch<Preview>(`/api/cowork/bookings/preview/?${params.toString()}`)
      setPreview(data)
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setBusy(false)
    }
  }

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    if (!spaceId) return
    setError('')
    setBusy(true)
    try {
      await apiFetch('/api/cowork/bookings/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ space_id: Number(spaceId), booking_type: bookingType, start_time: startTime }),
      })
      navigate('/cowork/my-bookings/')
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <section className="page-stack">
      <div className="panel">
        <p className="eyebrow">کوورک</p>
        <h2>رزرو فضا</h2>
        <p>نوع رزرو و تاریخ شروع را وارد کنید تا قیمت نهایی محاسبه شود.</p>
      </div>
      <form className="panel grid" onSubmit={submit}>
        <select value={bookingType} onChange={(e) => setBookingType(e.target.value)}>
          <option value="DAILY">روزانه</option>
          <option value="MONTHLY">ماهانه</option>
          <option value="SIX_MONTH">شش ماهه</option>
          <option value="YEARLY">سالانه</option>
        </select>
        <input
          value={startTime}
          onChange={(e) => setStartTime(e.target.value)}
          placeholder="YYYY-MM-DD"
        />
        <div className="row">
          <button className="btn-secondary" type="button" onClick={runPreview} disabled={busy || !startTime}>
            پیش‌نمایش
          </button>
          <button className="btn-primary" type="submit" disabled={busy || !startTime}>
            ثبت رزرو
          </button>
        </div>
      </form>
      {error ? <p className="error">{error}</p> : null}
      {preview ? (
        <div className="panel grid">
          <h3>نتیجه پیش‌نمایش</h3>
          <p>قیمت: {preview.price.toLocaleString()} تومان</p>
          <p>شروع: {preview.start_time}</p>
          <p>پایان: {preview.end_time}</p>
          <p>پایان (جلالی): {preview.end_time_jalali}</p>
        </div>
      ) : null}
    </section>
  )
}
