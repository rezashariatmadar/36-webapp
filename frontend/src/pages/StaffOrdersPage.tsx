import { useEffect, useMemo, useState } from 'react'
import { apiFetch } from '../lib/api/client'

type Order = { id: number; status: string; is_paid: boolean; total_price: number }

const statusLabel: Record<string, string> = {
  PENDING: 'در انتظار',
  PREPARING: 'در حال آماده‌سازی',
  READY: 'آماده تحویل',
  DELIVERED: 'تحویل شده',
  CANCELLED: 'لغو شده',
}

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
    void load()
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

  const metrics = useMemo(() => {
    const pending = orders.filter((order) => order.status === 'PENDING').length
    const preparing = orders.filter((order) => order.status === 'PREPARING').length
    const ready = orders.filter((order) => order.status === 'READY').length
    const paid = orders.filter((order) => order.is_paid).length
    return { pending, preparing, ready, paid }
  }, [orders])

  return (
    <section className="page-stack layout-flow-compact">
      <header className="surface-open section-head row">
        <div>
          <p className="eyebrow">Staff</p>
          <h2>داشبورد سفارش‌های جاری</h2>
          <p className="muted">عملیات سفارش‌های فعال را سریع و دقیق مدیریت کنید.</p>
        </div>
        <button className="btn-secondary" onClick={() => void load()} type="button">
          بروزرسانی
        </button>
      </header>

      <div className="grid dashboard-metrics">
        <article className="surface-inline dashboard-metric-card">
          <strong>{orders.length}</strong>
          <span>کل سفارش‌های فعال</span>
        </article>
        <article className="surface-inline dashboard-metric-card">
          <strong>{metrics.pending}</strong>
          <span>در انتظار</span>
        </article>
        <article className="surface-inline dashboard-metric-card">
          <strong>{metrics.preparing}</strong>
          <span>در حال آماده‌سازی</span>
        </article>
        <article className="surface-inline dashboard-metric-card">
          <strong>{metrics.ready}</strong>
          <span>آماده تحویل</span>
        </article>
        <article className="surface-inline dashboard-metric-card">
          <strong>{metrics.paid}</strong>
          <span>پرداخت شده</span>
        </article>
      </div>

      {error ? <p className="error">{error}</p> : null}

      {!orders.length ? (
        <div className="surface-inline dashboard-empty">
          <p>در حال حاضر سفارش فعالی وجود ندارد.</p>
        </div>
      ) : null}

      <div className="grid dashboard-orders-grid">
        {orders.map((order) => (
          <article key={order.id} className="surface-glass dashboard-order-card">
            <div className="dashboard-order-head">
              <strong>سفارش #{order.id}</strong>
              <span className={`status-pill status-${order.status.toLowerCase()}`}>{statusLabel[order.status] || order.status}</span>
            </div>

            <div className="dashboard-order-meta">
              <p>
                <span className="muted">مبلغ:</span> {order.total_price.toLocaleString()} تومان
              </p>
              <p>
                <span className="muted">پرداخت:</span>{' '}
                <span className={`status-pill ${order.is_paid ? 'status-available' : 'status-occupied'}`}>
                  {order.is_paid ? 'پرداخت‌شده' : 'پرداخت‌نشده'}
                </span>
              </p>
            </div>

            <div className="dashboard-order-actions">
              <div className="row dashboard-status-actions">
                <button className="btn-secondary" disabled={busy === order.id} onClick={() => mutate(order.id, 'status', 'PREPARING')} type="button">
                  شروع تهیه
                </button>
                <button className="btn-secondary" disabled={busy === order.id} onClick={() => mutate(order.id, 'status', 'READY')} type="button">
                  آماده شد
                </button>
                <button className="btn-secondary" disabled={busy === order.id} onClick={() => mutate(order.id, 'status', 'DELIVERED')} type="button">
                  تحویل شد
                </button>
                <button className="btn-secondary btn-danger-soft" disabled={busy === order.id} onClick={() => mutate(order.id, 'status', 'CANCELLED')} type="button">
                  لغو
                </button>
              </div>
              <button className="btn-primary dashboard-payment-btn" disabled={busy === order.id} onClick={() => mutate(order.id, 'payment')} type="button">
                {order.is_paid ? 'لغو پرداخت' : 'تایید پرداخت'}
              </button>
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}
