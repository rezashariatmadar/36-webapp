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
    <section className="page-stack">
      <div className="panel">
        <p className="eyebrow">کوورک</p>
        <h2>رزروهای من</h2>
        <p>لیست همه رزروهای انجام شده و وضعیت هر رزرو.</p>
      </div>
      {error ? <p className="error">{error}</p> : null}
      {!bookings.length ? <p className="panel">رزروی موجود نیست.</p> : null}
      <div className="grid cols-3">
        {bookings.map((booking) => (
          <article className="card" key={booking.id}>
            <h3>{booking.space_name}</h3>
            <p>وضعیت: {booking.status}</p>
            <p>
              تاریخ: {booking.start_time} تا {booking.end_time}
            </p>
            <p>
              جلالی: {booking.start_time_jalali} تا {booking.end_time_jalali}
            </p>
            <p>مبلغ: {booking.price_charged.toLocaleString()} تومان</p>
          </article>
        ))}
      </div>
    </section>
  )
}
