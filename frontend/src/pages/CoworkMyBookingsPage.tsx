import { useEffect, useState } from 'react'
import { apiFetch } from '../lib/api/client'

type Booking = {
  id: number
  space_name: string
  start_time: string
  end_time: string
  start_time_jalali: string
  end_time_jalali: string
  status: string
  price_charged: number
}

export function CoworkMyBookingsPage() {
  const [bookings, setBookings] = useState<Booking[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    apiFetch<{ bookings: Booking[] }>('/api/cowork/my-bookings/')
      .then((data) => setBookings(data.bookings))
      .catch((err) => setError((err as Error).message))
  }, [])

  return (
    <section className="page-stack layout-flow-compact">
      <div className="surface-open section-head">
        <p className="eyebrow">کوورک</p>
        <h2>رزروهای من</h2>
        <p>لیست همه رزروهای انجام شده و وضعیت هر رزرو.</p>
      </div>
      {error ? <p className="error">{error}</p> : null}
      {!bookings.length ? <p className="surface-inline">رزروی موجود نیست.</p> : null}
      <div className="grid cols-3 bookings-grid">
        {bookings.map((booking) => (
          <article className="surface-glass booking-card" key={booking.id}>
            <div className="booking-card-head">
              <h3>{booking.space_name}</h3>
              <span className={`status-pill status-${booking.status.toLowerCase()}`}>{booking.status}</span>
            </div>
            {booking.status === 'PENDING' ? (
              <p className="muted booking-card-note">رزرو شما ثبت شده است اما تا تایید ادمین نهایی نیست. لطفا برای تایید تماس بگیرید.</p>
            ) : null}
            <div className="booking-card-rows">
              <p>
                <strong>تاریخ:</strong> {booking.start_time} تا {booking.end_time}
              </p>
              <p>
                <strong>جلالی:</strong> {booking.start_time_jalali} تا {booking.end_time_jalali}
              </p>
            </div>
            <p className="booking-card-price">مبلغ: {booking.price_charged.toLocaleString()} تومان</p>
          </article>
        ))}
      </div>
    </section>
  )
}
