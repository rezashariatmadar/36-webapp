import { Suspense, lazy, useCallback, useEffect, useMemo, useState } from 'react';
import { BrowserRouter, NavLink, Navigate, Route, Routes } from 'react-router-dom';

import { apiFetch, ensureCsrfCookie, setCsrfToken } from './lib/api';
import type { SessionPayload } from './types/auth';

const HomePage = lazy(() => import('./pages/home-page'));
const AccountPage = lazy(() => import('./pages/account-page'));
const CafePage = lazy(() => import('./pages/cafe-page'));
const CoworkPage = lazy(() => import('./pages/cowork-page'));
const StaffPage = lazy(() => import('./pages/staff-page'));

type NavItem = {
  key: 'home' | 'account' | 'cafe' | 'cowork' | 'staff';
  label: string;
  to: string;
  requiresStaff?: boolean;
};

const navItems: NavItem[] = [
  { key: 'home', label: 'Overview', to: '/' },
  { key: 'account', label: 'Account', to: '/account' },
  { key: 'cafe', label: 'Cafe', to: '/cafe' },
  { key: 'cowork', label: 'Cowork', to: '/cowork' },
  { key: 'staff', label: 'Staff', to: '/staff', requiresStaff: true },
];

const initialSessionState: SessionPayload = {
  authenticated: false,
  login_url: '/app/account',
  user: null,
};

function AppShell() {
  const [me, setMe] = useState<SessionPayload>(initialSessionState);
  const [error, setError] = useState('');

  const refreshSession = useCallback(async () => {
    try {
      const data = await apiFetch<SessionPayload>('/api/auth/me/');
      setCsrfToken(data.csrf_token);
      setMe({
        ...data,
        login_url: data.login_url || '/app/account',
      });
    } catch (fetchError) {
      setError(fetchError instanceof Error ? fetchError.message : 'Unable to refresh session.');
    }
  }, []);

  useEffect(() => {
    const initialize = async () => {
      try {
        await ensureCsrfCookie();
      } catch (csrfError) {
        setError(csrfError instanceof Error ? csrfError.message : 'Unable to initialize CSRF.');
      }
      await refreshSession();
    };

    void initialize();
  }, [refreshSession]);

  const isStaffUser = Boolean(me.user?.roles?.is_admin || me.user?.roles?.is_barista);

  const visibleNavItems = useMemo(
    () => navItems.filter((item) => !item.requiresStaff || isStaffUser),
    [isStaffUser],
  );

  return (
    <div className="spa-shell text-white">
      <header className="py-6 border-b border-white/10">
        <div className="spa-container flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-2xl md:text-3xl font-black tracking-wide">36 Workspace Platform</h1>
            <p className="text-white/70 text-sm">React app shell running on top of Django APIs.</p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            {visibleNavItems.map((item) => (
              <NavLink
                key={item.key}
                to={item.to}
                end={item.to === '/'}
                className={({ isActive }) =>
                  `btn btn-sm ${isActive ? 'btn-primary' : 'btn-ghost text-white border-white/30'}`
                }
              >
                {item.label}
              </NavLink>
            ))}
            {me.authenticated ? (
              <a href={me.logout_url || '/logout/'} className="btn btn-sm btn-outline border-white/30 text-white">
                Logout
              </a>
            ) : (
              <a href={me.login_url || '/app/account'} className="btn btn-sm btn-outline border-white/30 text-white">
                Login
              </a>
            )}
          </div>
        </div>
      </header>

      <main className="spa-container py-8">
        {error ? <div className="alert alert-error mb-6">{error}</div> : null}
        <Suspense
          fallback={(
            <section className="spa-card p-6 md:p-8">
              <h2 className="text-xl font-bold">Loading page...</h2>
            </section>
          )}
        >
          <Routes>
            <Route path="/" element={<HomePage me={me} />} />
            <Route path="/account" element={<AccountPage me={me} onSessionRefresh={refreshSession} />} />
            <Route path="/cafe" element={<CafePage me={me} />} />
            <Route path="/cowork" element={<CoworkPage me={me} />} />
            <Route path="/staff" element={<StaffPage me={me} />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Suspense>
      </main>
    </div>
  );
}

export function App() {
  return (
    <BrowserRouter basename="/app">
      <AppShell />
    </BrowserRouter>
  );
}

