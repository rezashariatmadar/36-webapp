import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../lib/auth/AuthContext'

type NavItem = {
  to: string
  label: string
  symbol: string
}

const baseNav: NavItem[] = [
  { to: '/', label: 'خانه', symbol: 'H' },
  { to: '/cafe/menu/', label: 'منو کافه', symbol: 'C' },
  { to: '/cafe/cart/', label: 'سبد خرید', symbol: 'T' },
  { to: '/cowork/', label: 'فضای کار', symbol: 'W' },
  { to: '/cowork/my-bookings/', label: 'رزروهای من', symbol: 'B' },
  { to: '/profile/', label: 'پروفایل', symbol: 'P' },
]

const staffNav: NavItem[] = [
  { to: '/cafe/dashboard/', label: 'سفارش‌های فعال', symbol: 'O' },
  { to: '/cafe/manual-order/', label: 'ثبت سفارش دستی', symbol: 'M' },
  { to: '/cafe/manage-menu/', label: 'مدیریت منو', symbol: 'S' },
  { to: '/cafe/lookup/', label: 'جستجوی مشتری', symbol: 'L' },
  { to: '/cafe/analytics/', label: 'تحلیل‌ها', symbol: 'A' },
  { to: '/staff/users/', label: 'مدیریت کاربران', symbol: 'U' },
]

export function AppShell({ children }: { children: React.ReactNode }) {
  const location = useLocation()
  const { session, isStaff, logout } = useAuth()
  const nav = isStaff ? [...baseNav, ...staffNav] : baseNav

  return (
    <div className="app-root">
      <div className="mesh-gradient" aria-hidden />
      <aside className="sidebar shell-enter">
        <div className="brand">
          <img src="/img/36cowork/36-coworking-space.webp" alt="36 cowork" />
          <h1>36</h1>
        </div>
        <nav>
          {nav.map((item) => {
            const active = location.pathname === item.to || location.pathname.startsWith(`${item.to}/`)
            return (
              <Link key={item.to} className={`nav-link ${active ? 'active' : ''}`} to={item.to}>
                <span className="nav-icon-text" aria-hidden>
                  {item.symbol}
                </span>
                <span>{item.label}</span>
              </Link>
            )
          })}
        </nav>
        <div className="sidebar-user">
          {session?.authenticated ? (
            <>
              <strong>{session.user?.full_name || session.user?.phone_number}</strong>
              <span>{session.user?.phone_number}</span>
              <button onClick={() => logout()}>خروج</button>
            </>
          ) : (
            <>
              <span>مهمان</span>
              <Link to="/login/">ورود</Link>
              <Link to="/register/">ثبت نام</Link>
            </>
          )}
        </div>
      </aside>
      <main className="content shell-enter">
        <div className="main-frame">{children}</div>
      </main>
    </div>
  )
}
