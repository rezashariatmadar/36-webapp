import { cleanup, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Route, Routes, MemoryRouter } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { CafeCheckoutPage } from './pages/CafeCheckoutPage'
import { CoworkBookingPage } from './pages/CoworkBookingPage'
import { LoginPage } from './pages/LoginPage'
import { ProfilePage } from './pages/ProfilePage'
import { RegisterPage } from './pages/RegisterPage'

const apiFetchMock = vi.fn()
const refreshMock = vi.fn()

vi.mock('./lib/api/client', () => ({
  apiFetch: (...args: unknown[]) => apiFetchMock(...args),
}))

vi.mock('./lib/auth/AuthContext', () => ({
  useAuth: () => ({
    refresh: refreshMock,
    session: {
      authenticated: true,
      user: {
        phone_number: '09121234567',
        full_name: 'Test User',
        birth_date: '2025-01-01',
      },
    },
  }),
}))

describe('forms surface api errors', () => {
  beforeEach(() => {
    apiFetchMock.mockReset()
    refreshMock.mockReset()
  })
  afterEach(() => {
    cleanup()
  })

  it('shows login api errors', async () => {
    apiFetchMock.mockRejectedValueOnce(new Error('invalid credentials'))
    const user = userEvent.setup()

    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>,
    )

    const [phoneInput] = screen.getAllByRole('textbox')
    await user.type(phoneInput, '09121234567')
    await user.type(screen.getByPlaceholderText('رمز عبور'), 'badpass')
    await user.click(screen.getByRole('button', { name: 'ورود' }))

    expect(await screen.findByText('invalid credentials')).toBeInTheDocument()
  })

  it('shows register api errors', async () => {
    apiFetchMock.mockRejectedValueOnce(new Error('registration failed'))
    const user = userEvent.setup()

    render(
      <MemoryRouter>
        <RegisterPage />
      </MemoryRouter>,
    )

    await user.type(screen.getByPlaceholderText('شماره موبایل'), '09121234567')
    await user.click(screen.getByRole('button', { name: 'مرحله بعد' }))
    await user.type(await screen.findByPlaceholderText('نام کامل'), 'Test User')
    await user.type(screen.getByPlaceholderText('کد ملی'), '0011223344')
    await user.click(screen.getByRole('button', { name: 'مرحله بعد' }))
    await user.type(await screen.findByPlaceholderText('رمز عبور'), 'password123')
    await user.type(screen.getByPlaceholderText('تکرار رمز عبور'), 'password123')
    await user.click(screen.getByRole('button', { name: 'مرحله بعد' }))
    await user.click(screen.getByRole('button', { name: 'ایجاد حساب' }))

    expect(await screen.findByText('registration failed')).toBeInTheDocument()
  })

  it('shows profile save errors', async () => {
    apiFetchMock
      .mockResolvedValueOnce({
        profile: {
          public_slug: 'freelancer-1',
          headline: '',
          introduction: '',
          work_types: [],
          city: '',
          province: '',
          is_public: true,
          status: 'draft',
          moderation_note: '',
          contact_cta_text: 'Contact me',
          contact_cta_url: '',
          specialty_ids: [],
          flair_ids: [],
          custom_specialties: [],
          specialties: [],
          flairs: [],
          services: [],
        },
      })
      .mockResolvedValueOnce({ specialties: [] })
      .mockResolvedValueOnce({ flairs: [] })
      .mockRejectedValueOnce(new Error('profile update failed'))
    const user = userEvent.setup()

    render(
      <MemoryRouter>
        <ProfilePage />
      </MemoryRouter>,
    )

    await user.clear(screen.getByPlaceholderText('نام کامل'))
    await user.type(screen.getByPlaceholderText('نام کامل'), 'Updated User')
    await user.click(screen.getByRole('button', { name: 'ذخیره' }))

    expect(await screen.findByText('profile update failed')).toBeInTheDocument()
  })

  it('shows checkout api errors', async () => {
    apiFetchMock.mockRejectedValueOnce(new Error('checkout failed'))
    const user = userEvent.setup()

    render(
      <MemoryRouter>
        <CafeCheckoutPage />
      </MemoryRouter>,
    )

    await user.type(screen.getByPlaceholderText('توضیحات سفارش'), 'note')
    await user.click(screen.getByRole('button', { name: 'ثبت سفارش' }))

    expect(await screen.findByText('checkout failed')).toBeInTheDocument()
  })

  it('shows booking preview errors', async () => {
    apiFetchMock
      .mockResolvedValueOnce({ zones: [] })
      .mockRejectedValueOnce(new Error('preview failed'))
    const user = userEvent.setup()

    render(
      <MemoryRouter initialEntries={['/cowork/book/7']}>
        <Routes>
          <Route path="/cowork/book/:spaceId" element={<CoworkBookingPage />} />
        </Routes>
      </MemoryRouter>,
    )

    await user.type(screen.getByPlaceholderText('YYYY-MM-DD'), '2026-03-01')
    await user.click(screen.getByRole('button', { name: 'پیش‌نمایش' }))

    expect(await screen.findByText('preview failed')).toBeInTheDocument()
  })
})
