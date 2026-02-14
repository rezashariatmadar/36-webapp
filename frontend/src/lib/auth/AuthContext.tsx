import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { apiFetch } from '../api/client'

type UserRoles = {
  is_admin: boolean
  is_barista: boolean
  is_customer: boolean
}

type SessionUser = {
  id: number
  phone_number: string
  full_name: string
  national_id: string | null
  birth_date: string | null
  freelancer_profile_status?: string | null
  freelancer_public_slug?: string | null
  roles: UserRoles
}

export type SessionPayload = {
  authenticated: boolean
  csrf_token: string
  login_url: string
  logout_url?: string
  user?: SessionUser
}

type AuthContextValue = {
  session: SessionPayload | null
  loading: boolean
  refresh: () => Promise<void>
  logout: () => Promise<void>
  isStaff: boolean
}

const AuthContext = createContext<AuthContextValue | null>(null)
const FALLBACK_SESSION: SessionPayload = {
  authenticated: false,
  csrf_token: '',
  login_url: '/login/',
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<SessionPayload | null>(null)
  const [loading, setLoading] = useState(true)

  const refresh = useCallback(async () => {
    try {
      const payload = await apiFetch<SessionPayload>('/api/auth/me/')
      setSession(payload)
    } catch {
      setSession(FALLBACK_SESSION)
    }
  }, [])

  const logout = useCallback(async () => {
    try {
      await apiFetch('/api/auth/logout/', { method: 'POST' })
    } catch {
      // Keep UX responsive when backend is temporarily unavailable.
    }
    await refresh()
  }, [refresh])

  useEffect(() => {
    refresh().finally(() => setLoading(false))
  }, [refresh])

  const isStaff = Boolean(session?.user?.roles?.is_admin || session?.user?.roles?.is_barista)
  const value = useMemo(() => ({ session, loading, refresh, logout, isStaff }), [session, loading, refresh, logout, isStaff])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider')
  return ctx
}
