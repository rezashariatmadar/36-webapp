import { useEffect, useState } from 'react'
import { apiFetch } from '../lib/api/client'

type Order = { id: number; status: string; is_paid: boolean; total_price: number }

export function StaffOrdersPage() {
  const [orders, setOrders] = useState<Order[]>([])
  const [error, setError] = useState('')
  const [busy, setBusy] = useState<number | null>(null)

  const load = async () => {
    try {
      const data = await apiFetch<{ orders: Order[] }>('/api/cafe/staff/orders/')
      setOrders(data.orders)
    } catch (err) {
      setError((err as Error).message)
    }
  }

  useEffect(() => {
    load()
  }, [])

  const mutate = async (orderId: number, action: 'payment' | 'status', status?: string) => {
    setBusy(orderId)
    setError('')
    try {
      if (action === 'payment') {
        await apiFetch(`/api/cafe/staff/orders/${orderId}/toggle-payment/`, { method: 'POST' })
      } else {
        await apiFetch(`/api/cafe/staff/orders/${orderId}/status/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ status }),
        })
      }
      await load()
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setBusy(null)
    }
  }

  return (
    <section className="page-stack">
      <div className="panel row">
        <h2>داشبورد سفارشات جاری</h2>
        <button onClick={load}>بروزرسانی</button>
      </div>
      {error ? <p className="error">{error}</p> : null}
      {!orders.length ? <div className="panel">سفارش فعالی وجود ندارد.</div> : null}
      {orders.map((order) => (
        <article key={order.id} className="panel">
          <div className="row">
            <strong>#{order.id}</strong>
            <span>{order.status}</span>
            <span>{order.total_price.toLocaleString()} تومان</span>
            <span>{order.is_paid ? 'پرداخت‌شده' : 'پرداخت‌نشده'}</span>
          </div>
          <div className="row">
            <button disabled={busy === order.id} onClick={() => mutate(order.id, 'status', 'PREPARING')}>
              شروع تهیه
            </button>
            <button disabled={busy === order.id} onClick={() => mutate(order.id, 'status', 'READY')}>
              آماده شد
            </button>
            <button disabled={busy === order.id} onClick={() => mutate(order.id, 'status', 'DELIVERED')}>
              تحویل شد
            </button>
            <button disabled={busy === order.id} onClick={() => mutate(order.id, 'status', 'CANCELLED')}>
              لغو
            </button>
            <button disabled={busy === order.id} onClick={() => mutate(order.id, 'payment')}>
              {order.is_paid ? 'لغو پرداخت' : 'تایید پرداخت'}
            </button>
          </div>
        </article>
      ))}
    </section>
  )
}

