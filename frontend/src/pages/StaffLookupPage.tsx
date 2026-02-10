import { useState } from 'react'
import { apiFetch } from '../lib/api/client'

type Customer = { id: number; phone_number: string; full_name: string; is_active: boolean }

export function StaffLookupPage() {
  const [query, setQuery] = useState('')
  const [customers, setCustomers] = useState<Customer[]>([])
  const [error, setError] = useState('')

  const search = async () => {
    setError('')
    try {
      const data = await apiFetch<{ customers: Customer[] }>(`/api/cafe/staff/customer-lookup/?q=${encodeURIComponent(query)}`)
      setCustomers(data.customers)
    } catch (err) {
      setError((err as Error).message)
    }
  }

  return (
    <section className="page-stack">
      <div className="panel">
        <p className="eyebrow">پنل کافه</p>
        <h2>جستجوی مشتری</h2>
        <p>برای ثبت سفارش حضوری یا پیگیری سابقه، مشتری را پیدا کنید.</p>
      </div>
      <div className="panel row">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="نام یا شماره مشتری"
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              e.preventDefault()
              void search()
            }
          }}
        />
        <button className="btn-primary" onClick={() => void search()}>
          جستجو
        </button>
      </div>
      {error ? <p className="error">{error}</p> : null}
      <div className="grid cols-3">
        {customers.map((customer) => (
          <article className="card" key={customer.id}>
            <h3>{customer.full_name || 'بدون نام'}</h3>
            <p>{customer.phone_number}</p>
            <p>{customer.is_active ? 'فعال' : 'غیرفعال'}</p>
          </article>
        ))}
      </div>
    </section>
  )
}
