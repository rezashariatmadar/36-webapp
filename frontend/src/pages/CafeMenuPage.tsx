import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiFetch } from '../lib/api/client'

type MenuItem = { id: number; name: string; description: string; price: number }
type MenuCategory = { id: number; name: string; items: MenuItem[] }
type CartPayload = { cart_count: number }

export function CafeMenuPage() {
  const [categories, setCategories] = useState<MenuCategory[]>([])
  const [cartCount, setCartCount] = useState(0)
  const [busyIds, setBusyIds] = useState<number[]>([])
  const [error, setError] = useState('')

  const totalItems = useMemo(() => categories.reduce((acc, cat) => acc + cat.items.length, 0), [categories])

  const load = async () => {
    try {
      const [menuData, cartData] = await Promise.all([
        apiFetch<{ categories: MenuCategory[] }>('/api/cafe/menu/'),
        apiFetch<CartPayload>('/api/cafe/cart/'),
      ])
      setCategories(menuData.categories)
      setCartCount(cartData.cart_count || 0)
    } catch (err) {
      setError((err as Error).message)
    }
  }

  const changeQty = async (menuItemId: number, delta: 1 | -1) => {
    setBusyIds((prev) => [...prev, menuItemId])
    setError('')
    try {
      const cartData = await apiFetch<CartPayload>('/api/cafe/cart/items/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ menu_item_id: menuItemId, delta }),
      })
      setCartCount(cartData.cart_count || 0)
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setBusyIds((prev) => prev.filter((id) => id !== menuItemId))
    }
  }

  useEffect(() => {
    load()
  }, [])

  return (
    <section className="page-stack">
      <div className="panel row">
        <div>
          <h2>منوی کافه</h2>
          <p>{totalItems} آیتم فعال</p>
        </div>
        <Link className="btn-primary" to="/cafe/cart/">
          سبد خرید ({cartCount})
        </Link>
      </div>
      {error ? <p className="error">{error}</p> : null}
      {categories.map((category) => (
        <article key={category.id} className="panel">
          <h3>{category.name}</h3>
          <div className="grid">
            {category.items.map((item) => (
              <div key={item.id} className="card">
                <strong>{item.name}</strong>
                <p>{item.description || 'بدون توضیح'}</p>
                <span>{item.price.toLocaleString()} تومان</span>
                <div className="row">
                  <button disabled={busyIds.includes(item.id)} onClick={() => changeQty(item.id, -1)}>
                    -
                  </button>
                  <button disabled={busyIds.includes(item.id)} onClick={() => changeQty(item.id, 1)}>
                    افزودن
                  </button>
                </div>
              </div>
            ))}
          </div>
        </article>
      ))}
    </section>
  )
}

