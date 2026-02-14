import { FormEvent, useEffect, useMemo, useState } from 'react'
import { apiFetch } from '../lib/api/client'

type ManualOrderItem = { menu_item_id: number; quantity: number }
type StaffMenuItem = {
  id: number
  name: string
  price: number
  is_available: boolean
  category_name: string
}
type StaffCustomer = {
  id: number
  phone_number: string
  full_name: string
  is_active: boolean
}
type SelectedItem = { menu_item_id: number; quantity: number; menu_item_name: string; unit_price: number }
type TopItem = { menu_item__name: string; total_qty: number; total_rev: number }
type StaffAnalyticsOverview = { top_items: TopItem[] }

const CUSTOMER_TYPES = [
  { value: 'walk_in', label: 'حضوری' },
  { value: 'member', label: 'عضو' },
  { value: 'vip', label: 'VIP' },
]

function toLatinDigits(value: string) {
  return value
    .replace(/[۰-۹]/g, (digit) => String(digit.charCodeAt(0) - 1776))
    .replace(/[٠-٩]/g, (digit) => String(digit.charCodeAt(0) - 1632))
}

function normalizePhoneCandidate(value: string) {
  return toLatinDigits(value).replace(/[^\d+]/g, '')
}

export function StaffManualOrderPage() {
  const [menuItems, setMenuItems] = useState<StaffMenuItem[]>([])
  const [customerQuery, setCustomerQuery] = useState('')
  const [customerSuggestions, setCustomerSuggestions] = useState<StaffCustomer[]>([])
  const [selectedCustomer, setSelectedCustomer] = useState<StaffCustomer | null>(null)
  const [itemQuery, setItemQuery] = useState('')
  const [selectedItems, setSelectedItems] = useState<SelectedItem[]>([])
  const [salesRankByName, setSalesRankByName] = useState<Record<string, number>>({})
  const [customerType, setCustomerType] = useState(CUSTOMER_TYPES[0].value)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    const loadMenuItems = async () => {
      try {
        const data = await apiFetch<{ items: StaffMenuItem[] }>('/api/cafe/staff/menu-items/')
        const availableItems = data.items.filter((item) => item.is_available)
        setMenuItems(availableItems)
      } catch (err) {
        setError((err as Error).message)
      }
    }
    void loadMenuItems()
  }, [])

  useEffect(() => {
    const loadTopItems = async () => {
      try {
        const data = await apiFetch<StaffAnalyticsOverview>('/api/staff/analytics/overview/')
        const rank = (data.top_items || []).reduce<Record<string, number>>((acc, item) => {
          const key = (item.menu_item__name || '').trim().toLowerCase()
          if (key) {
            acc[key] = Number(item.total_qty) || 0
          }
          return acc
        }, {})
        setSalesRankByName(rank)
      } catch {
        setSalesRankByName({})
      }
    }
    void loadTopItems()
  }, [])

  useEffect(() => {
    const query = customerQuery.trim()
    if (!query) {
      setCustomerSuggestions([])
      if (selectedCustomer) {
        setSelectedCustomer(null)
      }
      return
    }
    const timer = window.setTimeout(async () => {
      try {
        const params = new URLSearchParams({ q: query })
        const data = await apiFetch<{ customers: StaffCustomer[] }>(`/api/cafe/staff/customer-lookup/?${params.toString()}`)
        setCustomerSuggestions(data.customers)
      } catch {
        setCustomerSuggestions([])
      }
    }, 220)
    return () => window.clearTimeout(timer)
  }, [customerQuery, selectedCustomer])

  const availableItemSuggestions = useMemo(() => {
    const normalized = itemQuery.trim().toLowerCase()
    const filtered = normalized
      ? menuItems.filter(
          (item) =>
            item.name.toLowerCase().includes(normalized) ||
            item.category_name.toLowerCase().includes(normalized) ||
            String(item.id).includes(normalized),
        )
      : menuItems

    const sorted = [...filtered].sort((a, b) => {
      const aScore = salesRankByName[a.name.trim().toLowerCase()] || 0
      const bScore = salesRankByName[b.name.trim().toLowerCase()] || 0
      if (bScore !== aScore) {
        return bScore - aScore
      }
      return a.name.localeCompare(b.name, 'fa')
    })
    return sorted.slice(0, 12)
  }, [itemQuery, menuItems, salesRankByName])

  const totalPrice = useMemo(
    () => selectedItems.reduce((sum, item) => sum + item.unit_price * item.quantity, 0),
    [selectedItems],
  )

  const customerTypeLabel = useMemo(
    () => CUSTOMER_TYPES.find((type) => type.value === customerType)?.label ?? CUSTOMER_TYPES[0].label,
    [customerType],
  )

  const addMenuItem = (item: StaffMenuItem) => {
    setSelectedItems((prev) => {
      const existingIndex = prev.findIndex((entry) => entry.menu_item_id === item.id)
      if (existingIndex >= 0) {
        return prev.map((entry, index) =>
          index === existingIndex ? { ...entry, quantity: entry.quantity + 1 } : entry,
        )
      }
      return [...prev, { menu_item_id: item.id, quantity: 1, menu_item_name: item.name, unit_price: item.price }]
    })
    setItemQuery('')
  }

  const updateQuantity = (menuItemId: number, delta: number) => {
    setSelectedItems((prev) =>
      prev
        .map((entry) =>
          entry.menu_item_id === menuItemId ? { ...entry, quantity: Math.max(0, entry.quantity + delta) } : entry,
        )
        .filter((entry) => entry.quantity > 0),
    )
  }

  const removeItem = (menuItemId: number) => {
    setSelectedItems((prev) => prev.filter((entry) => entry.menu_item_id !== menuItemId))
  }

  const chooseCustomer = (customer: StaffCustomer) => {
    setSelectedCustomer(customer)
    setCustomerQuery(`${customer.full_name || 'بدون نام'} - ${customer.phone_number}`)
    setCustomerSuggestions([])
  }

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    setError('')
    setMessage('')
    setSubmitting(true)
    try {
      const items: ManualOrderItem[] = selectedItems.map((item) => ({
        menu_item_id: item.menu_item_id,
        quantity: item.quantity,
      }))

      const rawPhone = selectedCustomer?.phone_number || normalizePhoneCandidate(customerQuery)
      const phone_number = /^(\+?\d{7,15})$/.test(rawPhone) ? rawPhone : ''
      const notes = `نوع مشتری: ${customerTypeLabel}`

      const data = await apiFetch<{ order_id: number; total_price: number }>('/api/cafe/staff/manual-orders/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone_number, notes, items }),
      })
      setMessage(`سفارش ${data.order_id} ثبت شد. مبلغ: ${data.total_price.toLocaleString()} تومان`)
      setSelectedItems([])
      setItemQuery('')
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section className="page-stack layout-flow-compact">
      <header className="surface-open section-head">
        <p className="eyebrow">پنل کافه</p>
        <h2>ثبت سفارش حضوری</h2>
        <p className="muted">شماره موبایل اختیاری است. می‌توانید مشتری را با شماره یا نام پیدا کنید.</p>
      </header>

      <form className="surface-glass grid manual-order-form" onSubmit={submit}>
        <label className="manual-order-field">
          <span>مشتری (اختیاری): جستجو با نام یا شماره</span>
          <input
            value={customerQuery}
            onChange={(event) => {
              setCustomerQuery(event.target.value)
              setSelectedCustomer(null)
            }}
            placeholder="مثال: علی یا 09xxxxxxxxx"
          />
          {customerSuggestions.length ? (
            <div className="manual-order-suggestions">
              {customerSuggestions.map((customer) => (
                <button key={customer.id} type="button" className="manual-order-suggestion" onClick={() => chooseCustomer(customer)}>
                  <strong>{customer.full_name || 'بدون نام'}</strong>
                  <span dir="ltr">{customer.phone_number}</span>
                </button>
              ))}
            </div>
          ) : null}
        </label>

        <label className="manual-order-field">
          <span>افزودن آیتم منو</span>
          <input
            value={itemQuery}
            onChange={(event) => setItemQuery(event.target.value)}
            placeholder="جستجو با نام آیتم یا دسته‌بندی"
          />
          {availableItemSuggestions.length ? (
            <div className="manual-order-suggestions">
              {availableItemSuggestions.map((item) => (
                <button key={item.id} type="button" className="manual-order-suggestion" onClick={() => addMenuItem(item)}>
                  <strong>{item.name}</strong>
                  <span>
                    {item.category_name} - {item.price.toLocaleString()} تومان
                  </span>
                </button>
              ))}
            </div>
          ) : null}
        </label>

        <div className="manual-order-field">
          <span>آیتم‌های انتخاب‌شده</span>
          {!selectedItems.length ? (
            <p className="muted">هنوز آیتمی اضافه نشده است.</p>
          ) : (
            <div className="manual-order-items">
              {selectedItems.map((item) => (
                <article key={item.menu_item_id} className="manual-order-item">
                  <div>
                    <strong>{item.menu_item_name}</strong>
                    <p>{item.unit_price.toLocaleString()} تومان</p>
                  </div>
                  <div className="manual-order-qty">
                    <button type="button" className="btn-secondary" onClick={() => updateQuantity(item.menu_item_id, -1)}>
                      -
                    </button>
                    <span>{item.quantity}</span>
                    <button type="button" className="btn-secondary" onClick={() => updateQuantity(item.menu_item_id, 1)}>
                      +
                    </button>
                    <button type="button" className="btn-secondary" onClick={() => removeItem(item.menu_item_id)}>
                      حذف
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </div>

        <label className="manual-order-field">
          <span>نوع مشتری</span>
          <select value={customerType} onChange={(event) => setCustomerType(event.target.value)}>
            {CUSTOMER_TYPES.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>

        <div className="manual-order-summary row">
          <p>مجموع: {totalPrice.toLocaleString()} تومان</p>
        </div>

        {error ? <p className="error">{error}</p> : null}
        {message ? <p className="ok">{message}</p> : null}

        <button className="btn-primary" type="submit" disabled={submitting || !selectedItems.length}>
          {submitting ? 'در حال ثبت...' : 'ثبت سفارش'}
        </button>
      </form>
    </section>
  )
}
