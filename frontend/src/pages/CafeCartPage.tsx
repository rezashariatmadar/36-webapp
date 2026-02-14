import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { apiFetch } from '../lib/api/client'

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
    void load()
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
    <section className="page-stack layout-flow-compact">
      <header className="surface-open section-head row">
        <div>
          <p className="eyebrow">Cart</p>
          <h2>سبد خرید ({cart.cart_count})</h2>
          <p className="muted">اقلام انتخاب‌شده را بررسی کنید و سپس تسویه را انجام دهید.</p>
        </div>
        <div className="row cart-head-actions">
          <Link className="btn-secondary" to="/cafe/menu/">
            بازگشت به منو
          </Link>
          <button className="btn-primary" disabled={!cart.items.length} onClick={() => navigate('/cafe/checkout/')}>
            تسویه
          </button>
        </div>
      </header>

      {error ? <p className="error">{error}</p> : null}

      {!cart.items.length ? (
        <div className="surface-inline cart-empty">
          <p>سبد خرید خالی است.</p>
          <Link to="/cafe/menu/">بازگشت به منو</Link>
        </div>
      ) : null}

      <div className="grid cart-lines">
        {cart.items.map((item) => (
          <article key={item.item_id} className="surface-glass cart-line-item">
            <div className="cart-line-main">
              <strong>{item.name}</strong>
              <span className="cart-line-price">{item.subtotal.toLocaleString()} تومان</span>
            </div>
            <div className="row cart-line-actions">
              <button
                className="btn-secondary cart-qty-btn"
                disabled={busy === item.item_id}
                onClick={() => changeQty(item.item_id, -1)}
                type="button"
              >
                -
              </button>
              <span className="qty-pill">{item.quantity}</span>
              <button
                className="btn-primary cart-qty-btn"
                disabled={busy === item.item_id}
                onClick={() => changeQty(item.item_id, 1)}
                type="button"
              >
                +
              </button>
            </div>
          </article>
        ))}
      </div>

      <div className="surface-strip cart-summary">
        <div className="row cart-total-row">
          <strong>جمع کل</strong>
          <span>{cart.total.toLocaleString()} تومان</span>
        </div>
        <div className="row cart-summary-actions">
          <Link className="btn-secondary" to="/cafe/menu/">
            افزودن آیتم بیشتر
          </Link>
          <button className="btn-primary" disabled={!cart.items.length} onClick={() => navigate('/cafe/checkout/')}>
            ادامه تسویه
          </button>
        </div>
      </div>
    </section>
  )
}
