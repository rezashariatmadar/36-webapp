import { useEffect, useState } from 'react'
import { apiFetch } from '../lib/api/client'

type User = {
  id: number
  phone_number: string
  full_name: string
  is_active: boolean
  roles: { is_admin: boolean; is_barista: boolean; is_customer: boolean }
}

type UserListResponse = { count: number; page: number; page_size: number; results: User[] }

export function StaffUsersPage() {
  const [users, setUsers] = useState<User[]>([])
  const [count, setCount] = useState(0)
  const [page, setPage] = useState(1)
  const [query, setQuery] = useState('')
  const [role, setRole] = useState('')
  const [isActive, setIsActive] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const load = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams({
        page: String(page),
        page_size: '20',
      })
      if (query) params.set('q', query)
      if (role) params.set('role', role)
      if (isActive) params.set('is_active', isActive)

      const data = await apiFetch<UserListResponse>(`/api/staff/users/?${params.toString()}`)
      setUsers(data.results)
      setCount(data.count)
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [page])

  const toggleStatus = async (id: number, current: boolean) => {
    await apiFetch(`/api/staff/users/${id}/status/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_active: !current }),
    })
    await load()
  }

  const changeRole = async (id: number, nextRole: string) => {
    await apiFetch(`/api/staff/users/${id}/role/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role: nextRole }),
    })
    await load()
  }

  return (
    <section className="page-stack">
      <div className="panel">
        <p className="eyebrow">پنل مدیریت</p>
        <h2>مدیریت کاربران</h2>
        <p>جستجو، تغییر نقش و فعال/غیرفعال‌سازی کاربران.</p>
      </div>
      <div className="panel row">
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="نام یا شماره" />
        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="">همه نقش‌ها</option>
          <option value="Admin">Admin</option>
          <option value="Barista">Barista</option>
          <option value="Customer">Customer</option>
        </select>
        <select value={isActive} onChange={(e) => setIsActive(e.target.value)}>
          <option value="">همه وضعیت‌ها</option>
          <option value="true">فعال</option>
          <option value="false">غیرفعال</option>
        </select>
        <button className="btn-secondary" onClick={() => { setPage(1); void load() }}>
          اعمال فیلتر
        </button>
      </div>
      {error ? <p className="error">{error}</p> : null}
      <p className="panel">تعداد کل: {count}</p>
      <div className="grid">
        {users.map((user) => (
          <article key={user.id} className="panel row">
            <strong>{user.full_name || '-'}</strong>
            <span>{user.phone_number}</span>
            <span>{user.is_active ? 'فعال' : 'غیرفعال'}</span>
            <button className="btn-secondary" onClick={() => toggleStatus(user.id, user.is_active)}>
              {user.is_active ? 'تعلیق' : 'فعال‌سازی'}
            </button>
            <button className="btn-secondary" onClick={() => changeRole(user.id, 'Admin')}>Admin</button>
            <button className="btn-secondary" onClick={() => changeRole(user.id, 'Barista')}>Barista</button>
            <button className="btn-secondary" onClick={() => changeRole(user.id, 'Customer')}>Customer</button>
          </article>
        ))}
      </div>
      <div className="row">
        <button className="btn-secondary" disabled={page <= 1 || loading} onClick={() => setPage((p) => p - 1)}>
          قبلی
        </button>
        <span>صفحه {page}</span>
        <button className="btn-secondary" disabled={users.length < 20 || loading} onClick={() => setPage((p) => p + 1)}>
          بعدی
        </button>
      </div>
    </section>
  )
}
