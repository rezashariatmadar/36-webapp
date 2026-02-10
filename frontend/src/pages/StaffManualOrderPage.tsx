import { FormEvent, useState } from 'react'
import { apiFetch } from '../lib/api/client'

type ManualOrderItem = { menu_item_id: number; quantity: number }

export function StaffManualOrderPage() {
  const [phoneNumber, setPhoneNumber] = useState('')
  const [notes, setNotes] = useState('Walk-in Guest')
  const [itemId, setItemId] = useState('')
  const [quantity, setQuantity] = useState('1')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    setError('')
    setMessage('')
    setSubmitting(true)
    try {
      const items: ManualOrderItem[] = [{ menu_item_id: Number(itemId), quantity: Number(quantity) }]
      const data = await apiFetch<{ order_id: number; total_price: number }>('/api/cafe/staff/manual-orders/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone_number: phoneNumber, notes, items }),
      })
      setMessage(`سفارش ${data.order_id} ثبت شد. مبلغ: ${data.total_price.toLocaleString()} تومان`)
      setItemId('')
      setQuantity('1')
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section className="page-stack">
      <div className="panel">
        <p className="eyebrow">پنل کافه</p>
        <h2>ثبت سفارش حضوری</h2>
        <p>برای مشتریان حضوری سفارش پرداخت‌شده ثبت کنید.</p>
      </div>
      <form className="panel grid" onSubmit={submit}>
        <input
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          placeholder="شماره مشتری (اختیاری)"
        />
        <input value={itemId} onChange={(e) => setItemId(e.target.value)} placeholder="شناسه آیتم" />
        <input value={quantity} onChange={(e) => setQuantity(e.target.value)} placeholder="تعداد" />
        <textarea value={notes} onChange={(e) => setNotes(e.target.value)} />
        {error ? <p className="error">{error}</p> : null}
        {message ? <p className="ok">{message}</p> : null}
        <button className="btn-primary" type="submit" disabled={submitting || !itemId}>
          {submitting ? 'در حال ثبت...' : 'ثبت سفارش'}
        </button>
      </form>
    </section>
  )
}
