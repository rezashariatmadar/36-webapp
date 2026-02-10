import { useEffect, useState } from 'react'
import { apiFetch } from '../lib/api/client'

type TopItem = { menu_item__name: string; total_qty: number; total_rev: number }
type TopBuyer = { user__phone_number: string; user__full_name: string; total_spent: number; total_bookings?: number }

type Overview = {
  cafe_total: number
  cafe_today: number
  cowork_total: number
  occupancy_rate: number
  active_bookings: number
  total_spaces: number
  top_items: TopItem[]
  top_cafe_buyers: TopBuyer[]
  top_cowork_members: TopBuyer[]
}

export function StaffAnalyticsPage() {
  const [data, setData] = useState<Overview | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    apiFetch<Overview>('/api/staff/analytics/overview/')
      .then(setData)
      .catch((err) => setError((err as Error).message))
  }, [])

  return (
    <section className="page-stack">
      <div className="panel">
        <p className="eyebrow">گزارش مدیریتی</p>
        <h2>آنالیز عملکرد</h2>
        <p>مرور سریع وضعیت فروش کافه و بهره‌برداری کوورک.</p>
      </div>
      {error ? <p className="error">{error}</p> : null}
      {data ? (
        <>
          <div className="grid cols-3">
            <div className="card"><h3>درآمد کافه</h3><p>{data.cafe_total.toLocaleString()} تومان</p></div>
            <div className="card"><h3>فروش امروز</h3><p>{data.cafe_today.toLocaleString()} تومان</p></div>
            <div className="card"><h3>درآمد کوورک</h3><p>{data.cowork_total.toLocaleString()} تومان</p></div>
            <div className="card"><h3>نرخ اشغال</h3><p>{data.occupancy_rate}%</p></div>
            <div className="card"><h3>رزرو فعال</h3><p>{data.active_bookings}</p></div>
            <div className="card"><h3>فضاهای فعال</h3><p>{data.total_spaces}</p></div>
          </div>
          <div className="grid cols-3">
            <article className="panel">
              <h3>آیتم‌های پرفروش</h3>
              {data.top_items.length ? data.top_items.map((item) => (
                <p key={item.menu_item__name}>{item.menu_item__name}: {item.total_qty}</p>
              )) : <p>داده‌ای موجود نیست.</p>}
            </article>
            <article className="panel">
              <h3>مشتریان برتر کافه</h3>
              {data.top_cafe_buyers.length ? data.top_cafe_buyers.map((buyer) => (
                <p key={buyer.user__phone_number}>{buyer.user__full_name || buyer.user__phone_number}: {Number(buyer.total_spent).toLocaleString()}</p>
              )) : <p>داده‌ای موجود نیست.</p>}
            </article>
            <article className="panel">
              <h3>اعضای برتر کوورک</h3>
              {data.top_cowork_members.length ? data.top_cowork_members.map((buyer) => (
                <p key={buyer.user__phone_number}>{buyer.user__full_name || buyer.user__phone_number}: {Number(buyer.total_spent).toLocaleString()}</p>
              )) : <p>داده‌ای موجود نیست.</p>}
            </article>
          </div>
        </>
      ) : null}
    </section>
  )
}
