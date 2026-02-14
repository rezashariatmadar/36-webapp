import { Suspense, lazy, type ElementType } from 'react'
import { Link, useLocation } from 'react-router-dom'
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined'
import ArticleOutlinedIcon from '@mui/icons-material/ArticleOutlined'
import WorkOutlineOutlinedIcon from '@mui/icons-material/WorkOutlineOutlined'
import RestaurantMenuOutlinedIcon from '@mui/icons-material/RestaurantMenuOutlined'
import ShoppingCartOutlinedIcon from '@mui/icons-material/ShoppingCartOutlined'
import DeskOutlinedIcon from '@mui/icons-material/DeskOutlined'
import EventNoteOutlinedIcon from '@mui/icons-material/EventNoteOutlined'
import PersonOutlineOutlinedIcon from '@mui/icons-material/PersonOutlineOutlined'
import ReceiptLongOutlinedIcon from '@mui/icons-material/ReceiptLongOutlined'
import PointOfSaleOutlinedIcon from '@mui/icons-material/PointOfSaleOutlined'
import Inventory2OutlinedIcon from '@mui/icons-material/Inventory2Outlined'
import ManageSearchOutlinedIcon from '@mui/icons-material/ManageSearchOutlined'
import InsightsOutlinedIcon from '@mui/icons-material/InsightsOutlined'
import GroupOutlinedIcon from '@mui/icons-material/GroupOutlined'
import { useAuth } from '../lib/auth/AuthContext'

const PillNav = lazy(() => import('../components/reactbits/PillNav'))
const Silk = lazy(() => import('../components/reactbits/Silk'))

type NavItem = {
  to: string
  label: string
  icon: ElementType
}

const baseNav: NavItem[] = [
  { to: '/', label: 'خانه', icon: HomeOutlinedIcon },
  { to: '/blog/', label: 'وبلاگ', icon: ArticleOutlinedIcon },
  { to: '/freelancers/', label: 'فریلنسرها', icon: WorkOutlineOutlinedIcon },
  { to: '/cafe/menu/', label: 'منو کافه', icon: RestaurantMenuOutlinedIcon },
  { to: '/cafe/cart/', label: 'سبد خرید', icon: ShoppingCartOutlinedIcon },
  { to: '/cowork/', label: 'فضای کار', icon: DeskOutlinedIcon },
  { to: '/cowork/my-bookings/', label: 'رزروهای من', icon: EventNoteOutlinedIcon },
  { to: '/profile/', label: 'پروفایل', icon: PersonOutlineOutlinedIcon },
]

const staffNav: NavItem[] = [
  { to: '/cafe/dashboard/', label: 'سفارش‌های فعال', icon: ReceiptLongOutlinedIcon },
  { to: '/cafe/manual-order/', label: 'ثبت سفارش دستی', icon: PointOfSaleOutlinedIcon },
  { to: '/cafe/manage-menu/', label: 'مدیریت منو', icon: Inventory2OutlinedIcon },
  { to: '/cafe/lookup/', label: 'جستجوی مشتری', icon: ManageSearchOutlinedIcon },
  { to: '/cafe/analytics/', label: 'تحلیل‌ها', icon: InsightsOutlinedIcon },
  { to: '/staff/users/', label: 'مدیریت کاربران', icon: GroupOutlinedIcon },
]

const normalizePath = (value: string) => (value.length > 1 && value.endsWith('/') ? value.slice(0, -1) : value)

export function AppShell({ children }: { children: React.ReactNode }) {
  const location = useLocation()
  const { session, isStaff, logout } = useAuth()
  const nav = isStaff ? [...baseNav, ...staffNav] : baseNav
  const authRoute = location.pathname === '/login/' || location.pathname === '/register/'
  const showSilkBackground = !authRoute && location.pathname === '/'

  return (
    <div className={`app-root ${authRoute ? 'app-root-auth' : ''}`}>
      {showSilkBackground ? (
        <div className="app-bg-veil">
          <Suspense fallback={null}>
            <Silk color="#39006c" noiseIntensity={0} />
          </Suspense>
        </div>
      ) : null}

      {!authRoute ? (
        <div className="mobile-nav shell-enter">
          <Suspense fallback={null}>
            <PillNav
              logo="/img/36cowork/36-coworking-space.webp"
              logoAlt="36 cowork"
              items={nav.map((item) => ({ label: item.label, href: item.to }))}
              activeHref={location.pathname}
            />
          </Suspense>
        </div>
      ) : null}

      {!authRoute ? (
        <aside className="sidebar shell-enter">
          <div className="brand">
            <img src="/img/36cowork/36-coworking-space.webp" alt="36 cowork" />
            <h1>36</h1>
          </div>
          <nav>
            {nav.map((item) => {
              const Icon = item.icon
              const currentPath = normalizePath(location.pathname)
              const itemPath = normalizePath(item.to)
              const active = currentPath === itemPath || currentPath.startsWith(`${itemPath}/`)
              return (
                <Link key={item.to} className={`nav-link ${active ? 'active' : ''}`} to={item.to}>
                  <span className="nav-icon-text" aria-hidden>
                    <Icon fontSize="small" />
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
      ) : null}

      <main className={`content shell-enter ${authRoute ? 'content-auth' : ''}`}>
        <div className={`main-frame ${authRoute ? 'main-frame-auth layout-flow-compact' : 'layout-flow-regular'}`}>
          {children}
        </div>
      </main>
    </div>
  )
}
