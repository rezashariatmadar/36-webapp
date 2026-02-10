import { Link, useNavigate } from 'react-router-dom'
import { apiFetch } from '../lib/api/client'
import { useEffect, useState } from 'react'

type CartItem = { item_id: number; name: string; quantity: number; subtotal: number }
type CartPayload = { items: CartItem[]; total: number; cart_count: number }

export function CafeCartPage() {
  const [cart, setCart] = useState<CartPayload>({ items: [], total: 0, cart_count: 0 })
  const [error, setError] = useState('')
  const [busy, setBusy] = useState<number | null>(null)
  const navigate = useNavigate()

  const load = async () => {
    try {
      const data = await apiFetch<CartPayload>('/api/cafe/cart/')
      setCart(data)
    } catch (err) {
      setError((err as Error).message)
    }
  }

  useEffect(() => {
    load()
  }, [])

  const changeQty = async (menuItemId: number, delta: 1 | -1) => {
    setBusy(menuItemId)
    setError('')
    try {
      const data = await apiFetch<CartPayload>('/api/cafe/cart/items/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ menu_item_id: menuItemId, delta }),
      })
      setCart(data)
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setBusy(null)
    }
  }

  return (
    <section className="page-stack">
      <div className="panel row">
        <h2>سبد خرید ({cart.cart_count})</h2>
        <button className="btn-primary" disabled={!cart.items.length} onClick={() => navigate('/cafe/checkout/')}>
          تسویه
        </button>
      </div>
      {error ? <p className="error">{error}</p> : null}
      {!cart.items.length ? (
        <div className="panel">
          <p>سبد خرید خالی است.</p>
          <Link to="/cafe/menu/">بازگشت به منو</Link>
        </div>
      ) : null}
      {cart.items.map((item) => (
        <div key={item.item_id} className="panel row">
          <strong>{item.name}</strong>
          <div className="row">
            <button disabled={busy === item.item_id} onClick={() => changeQty(item.item_id, -1)}>
              -
            </button>
            <span>{item.quantity}</span>
            <button disabled={busy === item.item_id} onClick={() => changeQty(item.item_id, 1)}>
              +
            </button>
          </div>
          <span>{item.subtotal.toLocaleString()} تومان</span>
        </div>
      ))}
      <div className="panel row">
        <strong>جمع کل:</strong>
        <span>{cart.total.toLocaleString()} تومان</span>
      </div>
    </section>
  )
}

