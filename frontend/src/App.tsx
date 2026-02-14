import { Suspense, lazy } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import { AppShell } from './layouts/AppShell'
import { useAuth } from './lib/auth/AuthContext'

const HomePage = lazy(() => import('./pages/HomePage').then((m) => ({ default: m.HomePage })))
const BlogListPage = lazy(() => import('./pages/BlogListPage').then((m) => ({ default: m.BlogListPage })))
const BlogPostPage = lazy(() => import('./pages/BlogPostPage').then((m) => ({ default: m.BlogPostPage })))
const FreelancersListPage = lazy(() =>
  import('./pages/FreelancersListPage').then((m) => ({ default: m.FreelancersListPage })),
)
const FreelancerProfilePublicPage = lazy(() =>
  import('./pages/FreelancerProfilePublicPage').then((m) => ({ default: m.FreelancerProfilePublicPage })),
)
const LoginPage = lazy(() => import('./pages/LoginPage').then((m) => ({ default: m.LoginPage })))
const RegisterPage = lazy(() => import('./pages/RegisterPage').then((m) => ({ default: m.RegisterPage })))
const ProfilePage = lazy(() => import('./pages/ProfilePage').then((m) => ({ default: m.ProfilePage })))
const CafeMenuPage = lazy(() => import('./pages/CafeMenuPage').then((m) => ({ default: m.CafeMenuPage })))
const CafeCartPage = lazy(() => import('./pages/CafeCartPage').then((m) => ({ default: m.CafeCartPage })))
const CafeCheckoutPage = lazy(() =>
  import('./pages/CafeCheckoutPage').then((m) => ({ default: m.CafeCheckoutPage })),
)
const CafeOrdersPage = lazy(() => import('./pages/CafeOrdersPage').then((m) => ({ default: m.CafeOrdersPage })))
const CoworkSpacesPage = lazy(() =>
  import('./pages/CoworkSpacesPage').then((m) => ({ default: m.CoworkSpacesPage })),
)
const CoworkBookingPage = lazy(() =>
  import('./pages/CoworkBookingPage').then((m) => ({ default: m.CoworkBookingPage })),
)
const CoworkMyBookingsPage = lazy(() =>
  import('./pages/CoworkMyBookingsPage').then((m) => ({ default: m.CoworkMyBookingsPage })),
)
const StaffOrdersPage = lazy(() =>
  import('./pages/StaffOrdersPage').then((m) => ({ default: m.StaffOrdersPage })),
)
const StaffManualOrderPage = lazy(() =>
  import('./pages/StaffManualOrderPage').then((m) => ({ default: m.StaffManualOrderPage })),
)
const StaffMenuStockPage = lazy(() =>
  import('./pages/StaffMenuStockPage').then((m) => ({ default: m.StaffMenuStockPage })),
)
const StaffLookupPage = lazy(() => import('./pages/StaffLookupPage').then((m) => ({ default: m.StaffLookupPage })))
const StaffAnalyticsPage = lazy(() =>
  import('./pages/StaffAnalyticsPage').then((m) => ({ default: m.StaffAnalyticsPage })),
)
const StaffUsersPage = lazy(() => import('./pages/StaffUsersPage').then((m) => ({ default: m.StaffUsersPage })))
const NotFoundPage = lazy(() => import('./pages/NotFoundPage').then((m) => ({ default: m.NotFoundPage })))

function StaffGuard({ children }: { children: JSX.Element }) {
  const { loading, isStaff } = useAuth()
  if (loading) return <div>Loading...</div>
  if (!isStaff) return <Navigate to="/login/" replace />
  return children
}

function AuthGuard({ children }: { children: JSX.Element }) {
  const { loading, session } = useAuth()
  if (loading) return <div>Loading...</div>
  if (!session?.authenticated) return <Navigate to="/login/" replace />
  return children
}

export function App() {
  return (
    <AppShell>
      <Suspense fallback={<div>Loading...</div>}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/blog/" element={<BlogListPage />} />
          <Route path="/blog/:slug/" element={<BlogPostPage />} />
          <Route path="/freelancers/" element={<FreelancersListPage />} />
          <Route path="/freelancers/:slug/" element={<FreelancerProfilePublicPage />} />
          <Route path="/login/" element={<LoginPage />} />
          <Route path="/register/" element={<RegisterPage />} />
          <Route
            path="/profile/"
            element={
              <AuthGuard>
                <ProfilePage />
              </AuthGuard>
            }
          />
          <Route path="/cafe/menu/" element={<CafeMenuPage />} />
          <Route path="/cafe/cart/" element={<CafeCartPage />} />
          <Route
            path="/cafe/checkout/"
            element={
              <AuthGuard>
                <CafeCheckoutPage />
              </AuthGuard>
            }
          />
          <Route
            path="/cafe/orders/"
            element={
              <AuthGuard>
                <CafeOrdersPage />
              </AuthGuard>
            }
          />
          <Route path="/cowork/" element={<CoworkSpacesPage />} />
          <Route
            path="/cowork/book/:spaceId"
            element={
              <AuthGuard>
                <CoworkBookingPage />
              </AuthGuard>
            }
          />
          <Route
            path="/cowork/my-bookings/"
            element={
              <AuthGuard>
                <CoworkMyBookingsPage />
              </AuthGuard>
            }
          />
          <Route
            path="/cafe/dashboard/"
            element={
              <StaffGuard>
                <StaffOrdersPage />
              </StaffGuard>
            }
          />
          <Route
            path="/cafe/manual-order/"
            element={
              <StaffGuard>
                <StaffManualOrderPage />
              </StaffGuard>
            }
          />
          <Route
            path="/cafe/manage-menu/"
            element={
              <StaffGuard>
                <StaffMenuStockPage />
              </StaffGuard>
            }
          />
          <Route
            path="/cafe/lookup/"
            element={
              <StaffGuard>
                <StaffLookupPage />
              </StaffGuard>
            }
          />
          <Route
            path="/cafe/analytics/"
            element={
              <StaffGuard>
                <StaffAnalyticsPage />
              </StaffGuard>
            }
          />
          <Route
            path="/staff/users/"
            element={
              <StaffGuard>
                <StaffUsersPage />
              </StaffGuard>
            }
          />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Suspense>
    </AppShell>
  )
}
