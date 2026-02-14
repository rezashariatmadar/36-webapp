import { cleanup, render, screen } from '@testing-library/react'
import type { ReactNode } from 'react'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { App } from './App'

const useAuthMock = vi.fn()

vi.mock('./lib/auth/AuthContext', () => ({
  useAuth: () => useAuthMock(),
}))

vi.mock('./layouts/AppShell', () => ({
  AppShell: ({ children }: { children: ReactNode }) => <div>{children}</div>,
}))

vi.mock('./pages/HomePage', () => ({ HomePage: () => <div>HomePage</div> }))
vi.mock('./pages/BlogListPage', () => ({ BlogListPage: () => <div>BlogListPage</div> }))
vi.mock('./pages/BlogPostPage', () => ({ BlogPostPage: () => <div>BlogPostPage</div> }))
vi.mock('./pages/FreelancersListPage', () => ({ FreelancersListPage: () => <div>FreelancersListPage</div> }))
vi.mock('./pages/FreelancerProfilePublicPage', () => ({ FreelancerProfilePublicPage: () => <div>FreelancerProfilePublicPage</div> }))
vi.mock('./pages/LoginPage', () => ({ LoginPage: () => <div>LoginPage</div> }))
vi.mock('./pages/RegisterPage', () => ({ RegisterPage: () => <div>RegisterPage</div> }))
vi.mock('./pages/ProfilePage', () => ({ ProfilePage: () => <div>ProfilePage</div> }))
vi.mock('./pages/CafeMenuPage', () => ({ CafeMenuPage: () => <div>CafeMenuPage</div> }))
vi.mock('./pages/CafeCartPage', () => ({ CafeCartPage: () => <div>CafeCartPage</div> }))
vi.mock('./pages/CafeCheckoutPage', () => ({ CafeCheckoutPage: () => <div>CafeCheckoutPage</div> }))
vi.mock('./pages/CafeOrdersPage', () => ({ CafeOrdersPage: () => <div>CafeOrdersPage</div> }))
vi.mock('./pages/CoworkSpacesPage', () => ({ CoworkSpacesPage: () => <div>CoworkSpacesPage</div> }))
vi.mock('./pages/CoworkBookingPage', () => ({ CoworkBookingPage: () => <div>CoworkBookingPage</div> }))
vi.mock('./pages/CoworkMyBookingsPage', () => ({ CoworkMyBookingsPage: () => <div>CoworkMyBookingsPage</div> }))
vi.mock('./pages/StaffOrdersPage', () => ({ StaffOrdersPage: () => <div>StaffOrdersPage</div> }))
vi.mock('./pages/StaffManualOrderPage', () => ({ StaffManualOrderPage: () => <div>StaffManualOrderPage</div> }))
vi.mock('./pages/StaffMenuStockPage', () => ({ StaffMenuStockPage: () => <div>StaffMenuStockPage</div> }))
vi.mock('./pages/StaffLookupPage', () => ({ StaffLookupPage: () => <div>StaffLookupPage</div> }))
vi.mock('./pages/StaffAnalyticsPage', () => ({ StaffAnalyticsPage: () => <div>StaffAnalyticsPage</div> }))
vi.mock('./pages/StaffUsersPage', () => ({ StaffUsersPage: () => <div>StaffUsersPage</div> }))
vi.mock('./pages/NotFoundPage', () => ({ NotFoundPage: () => <div>NotFoundPage</div> }))

type AuthState = {
  loading: boolean
  isStaff: boolean
  session: { authenticated: boolean } | null
}

const defaultAuth: AuthState = {
  loading: false,
  isStaff: true,
  session: { authenticated: true },
}

function renderPath(path: string, auth: Partial<AuthState> = {}) {
  useAuthMock.mockReturnValue({ ...defaultAuth, ...auth })
  return render(
    <MemoryRouter initialEntries={[path]}>
      <App />
    </MemoryRouter>,
  )
}

describe('app routes and guards', () => {
  beforeEach(() => {
    useAuthMock.mockReset()
  })
  afterEach(() => {
    cleanup()
  })

  it('renders public routes', async () => {
    const routeMap = [
      ['/', 'HomePage'],
      ['/blog/', 'BlogListPage'],
      ['/blog/post-slug/', 'BlogPostPage'],
      ['/freelancers/', 'FreelancersListPage'],
      ['/freelancers/ali-designer/', 'FreelancerProfilePublicPage'],
      ['/login/', 'LoginPage'],
      ['/register/', 'RegisterPage'],
      ['/cafe/menu/', 'CafeMenuPage'],
      ['/cafe/cart/', 'CafeCartPage'],
      ['/cowork/', 'CoworkSpacesPage'],
    ] as const

    for (const [path, page] of routeMap) {
      const view = renderPath(path)
      expect(await screen.findByText(page)).toBeInTheDocument()
      view.unmount()
    }
  })

  it('renders protected customer routes when authenticated', async () => {
    const routeMap = [
      ['/profile/', 'ProfilePage'],
      ['/cafe/checkout/', 'CafeCheckoutPage'],
      ['/cafe/orders/', 'CafeOrdersPage'],
      ['/cowork/book/9', 'CoworkBookingPage'],
      ['/cowork/my-bookings/', 'CoworkMyBookingsPage'],
    ] as const

    for (const [path, page] of routeMap) {
      const view = renderPath(path, { session: { authenticated: true } })
      expect(await screen.findByText(page)).toBeInTheDocument()
      view.unmount()
    }
  })

  it('redirects unauthenticated users from customer protected routes to login', async () => {
    renderPath('/profile/', { session: { authenticated: false } })
    expect(await screen.findByText('LoginPage')).toBeInTheDocument()
  })

  it('renders staff routes for staff users', async () => {
    const routeMap = [
      ['/cafe/dashboard/', 'StaffOrdersPage'],
      ['/cafe/manual-order/', 'StaffManualOrderPage'],
      ['/cafe/manage-menu/', 'StaffMenuStockPage'],
      ['/cafe/lookup/', 'StaffLookupPage'],
      ['/cafe/analytics/', 'StaffAnalyticsPage'],
      ['/staff/users/', 'StaffUsersPage'],
    ] as const

    for (const [path, page] of routeMap) {
      const view = renderPath(path, { isStaff: true, session: { authenticated: true } })
      expect(await screen.findByText(page)).toBeInTheDocument()
      view.unmount()
    }
  })

  it('redirects non-staff users from staff routes to login', async () => {
    renderPath('/staff/users/', { isStaff: false, session: { authenticated: true } })
    expect(await screen.findByText('LoginPage')).toBeInTheDocument()
  })
})
