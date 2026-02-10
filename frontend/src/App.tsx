import { Navigate, Route, Routes } from 'react-router-dom'
import { AppShell } from './layouts/AppShell'
import { useAuth } from './lib/auth/AuthContext'
import { CafeCartPage } from './pages/CafeCartPage'
import { CafeCheckoutPage } from './pages/CafeCheckoutPage'
import { CafeMenuPage } from './pages/CafeMenuPage'
import { CafeOrdersPage } from './pages/CafeOrdersPage'
import { CoworkBookingPage } from './pages/CoworkBookingPage'
import { CoworkMyBookingsPage } from './pages/CoworkMyBookingsPage'
import { CoworkSpacesPage } from './pages/CoworkSpacesPage'
import { HomePage } from './pages/HomePage'
import { LoginPage } from './pages/LoginPage'
import { NotFoundPage } from './pages/NotFoundPage'
import { ProfilePage } from './pages/ProfilePage'
import { RegisterPage } from './pages/RegisterPage'
import { StaffAnalyticsPage } from './pages/StaffAnalyticsPage'
import { StaffLookupPage } from './pages/StaffLookupPage'
import { StaffManualOrderPage } from './pages/StaffManualOrderPage'
import { StaffMenuStockPage } from './pages/StaffMenuStockPage'
import { StaffOrdersPage } from './pages/StaffOrdersPage'
import { StaffUsersPage } from './pages/StaffUsersPage'

function StaffGuard({ children }: { children: JSX.Element }) {
  const { loading, isStaff } = useAuth()
  if (loading) return <div>Loading...</div>
  if (!isStaff) return <Navigate to="/" replace />
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
      <Routes>
        <Route path="/" element={<HomePage />} />
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
    </AppShell>
  )
}
