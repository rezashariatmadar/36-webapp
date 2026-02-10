import { FormEvent, useEffect, useState } from 'react'
import { apiFetch } from '../lib/api/client'

type Category = { id: number; name: string }
type MenuItem = { id: number; name: string; description: string; is_available: boolean; category_name: string; price: number }

export function StaffMenuStockPage() {
  const [categories, setCategories] = useState<Category[]>([])
  const [items, setItems] = useState<MenuItem[]>([])
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [price, setPrice] = useState('')
  const [categoryId, setCategoryId] = useState('')
  const [isAvailable, setIsAvailable] = useState(true)
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const load = async () => {
    const [categoriesData, itemsData] = await Promise.all([
      apiFetch<{ categories: Category[] }>('/api/cafe/staff/menu-categories/'),
      apiFetch<{ items: MenuItem[] }>('/api/cafe/staff/menu-items/'),
    ])
    setCategories(categoriesData.categories)
    setItems(itemsData.items)
  }

  useEffect(() => {
    load().catch((err) => setError((err as Error).message))
  }, [])

  const createItem = async (event: FormEvent) => {
    event.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await apiFetch('/api/cafe/staff/menu-items/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name,
          description,
          price,
          category_id: Number(categoryId),
          is_available: isAvailable,
        }),
      })
      setName('')
      setDescription('')
      setPrice('')
      setCategoryId('')
      setIsAvailable(true)
      await load()
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setSubmitting(false)
    }
  }

  const toggle = async (id: number) => {
    try {
      await apiFetch(`/api/cafe/staff/menu-items/${id}/toggle-availability/`, { method: 'POST' })
      await load()
    } catch (err) {
      setError((err as Error).message)
    }
  }

  return (
    <section className="page-stack">
      <div className="panel">
        <p className="eyebrow">پنل کافه</p>
        <h2>مدیریت منو و موجودی</h2>
        <p>آیتم جدید بسازید یا وضعیت موجودی آیتم‌ها را تغییر دهید.</p>
      </div>
      {error ? <p className="error">{error}</p> : null}
      <form className="panel grid" onSubmit={createItem}>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="نام آیتم" />
        <textarea value={description} onChange={(e) => setDescription(e.target.value)} placeholder="توضیحات" />
        <input value={price} onChange={(e) => setPrice(e.target.value)} placeholder="قیمت (تومان)" />
        <select value={categoryId} onChange={(e) => setCategoryId(e.target.value)}>
          <option value="">دسته‌بندی</option>
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </select>
        <label className="row">
          <input type="checkbox" checked={isAvailable} onChange={(e) => setIsAvailable(e.target.checked)} />
          قابل سفارش باشد
        </label>
        <button className="btn-primary" type="submit" disabled={submitting || !name || !price || !categoryId}>
          {submitting ? 'در حال افزودن...' : 'افزودن آیتم'}
        </button>
      </form>
      <div className="grid cols-3">
        {items.map((item) => (
          <article className="card" key={item.id}>
            <h3>{item.name}</h3>
            <p>{item.description || 'بدون توضیح'}</p>
            <p>{item.category_name}</p>
            <p>{item.price.toLocaleString()} تومان</p>
            <p>{item.is_available ? 'موجود' : 'ناموجود'}</p>
            <button className="btn-secondary" onClick={() => toggle(item.id)}>
              {item.is_available ? 'ناموجود کن' : 'موجود کن'}
            </button>
          </article>
        ))}
      </div>
    </section>
  )
}
