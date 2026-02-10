import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiFetch } from '../lib/api/client'

type Order = { id: number; status: string; total_price: number; is_paid?: boolean; created_at?: string }

export function CafeOrdersPage() {
  const [orders, setOrders] = useState<Order[]>([])
  const [error, setError] = useState('')
  const [busyOrder, setBusyOrder] = useState<number | null>(null)

  const load = async () => {
    try {
      const data = await apiFetch<{ orders: Order[] }>('/api/cafe/orders/')
      setOrders(data.orders)
    } catch (err) {
      setError((err as Error).message)
    }
  }

  const reorder = async (orderId: number) => {
    setBusyOrder(orderId)
    try {
      await apiFetch(`/api/cafe/orders/${orderId}/reorder/`, { method: 'POST' })
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setBusyOrder(null)
    }
  }

  useEffect(() => {
    load()
  }, [])

  return (
    <section className="page-stack">
      <div className="panel row">
        <h2>سفارش‌های من</h2>
        <Link className="btn-secondary" to="/cafe/menu/">
          منوی کافه
        </Link>
      </div>
      {error ? <p className="error">{error}</p> : null}
      {!orders.length ? <div className="panel">سفارشی ثبت نشده است.</div> : null}
      {orders.map((order) => (
        <article key={order.id} className="panel">
          <div className="row">
            <strong>سفارش #{order.id}</strong>
            <span>{order.status}</span>
            <span>{order.total_price?.toLocaleString?.() || order.total_price} تومان</span>
            <button disabled={busyOrder === order.id} onClick={() => reorder(order.id)}>
              تکرار سفارش
            </button>
          </div>
        </article>
      ))}
    </section>
  )
}

