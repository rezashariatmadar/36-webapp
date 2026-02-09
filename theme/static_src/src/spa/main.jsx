import React, { Suspense, lazy, useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';

import './app.css';
import { apiFetch, setCsrfToken } from './api';

const APP_PREFIX = '/app';

const HomePage = lazy(() => import('./pages/home-page'));
const AccountPage = lazy(() => import('./pages/account-page'));
const CafePage = lazy(() => import('./pages/cafe-page'));
const CoworkPage = lazy(() => import('./pages/cowork-page'));
const StaffPage = lazy(() => import('./pages/staff-page'));

const stripAppPrefix = (pathname) => {
  if (!pathname.startsWith(APP_PREFIX)) return '/';
  const rest = pathname.slice(APP_PREFIX.length);
  return rest.length ? rest : '/';
};

const navItems = [
  { key: 'home', label: 'Overview', href: '/app/' },
  { key: 'account', label: 'Account', href: '/app/account' },
  { key: 'cafe', label: 'Cafe', href: '/app/cafe' },
  { key: 'cowork', label: 'Cowork', href: '/app/cowork' },
  { key: 'staff', label: 'Staff', href: '/app/staff', requiresStaff: true },
];

function App() {
  const [me, setMe] = useState({ authenticated: false, user: null, login_url: '/app/account' });
  const [routePath, setRoutePath] = useState(stripAppPrefix(window.location.pathname));
  const [error, setError] = useState('');

  const refreshSession = async () => {
    try {
      const data = await apiFetch('/api/auth/me/');
      setCsrfToken(data.csrf_token);
      setMe(data);
    } catch (fetchError) {
      setError(fetchError.message);
    }
  };

  useEffect(() => {
    refreshSession();
  }, []);

  useEffect(() => {
    const onPopState = () => {
      setRoutePath(stripAppPrefix(window.location.pathname));
    };
    const onClick = (event) => {
      const link = event.target.closest('a[data-spa-link="true"]');
      if (!link) return;
      const href = link.getAttribute('href');
      if (!href || !href.startsWith('/app')) return;
      event.preventDefault();
      if (window.location.pathname !== href) {
        window.history.pushState({}, '', href);
        setRoutePath(stripAppPrefix(href));
      }
    };

    window.addEventListener('popstate', onPopState);
    document.addEventListener('click', onClick);
    return () => {
      window.removeEventListener('popstate', onPopState);
      document.removeEventListener('click', onClick);
    };
  }, []);

  const activePage = useMemo(() => {
    if (routePath.startsWith('/account')) return 'account';
    if (routePath.startsWith('/cafe')) return 'cafe';
    if (routePath.startsWith('/cowork')) return 'cowork';
    if (routePath.startsWith('/staff')) return 'staff';
    return 'home';
  }, [routePath]);

  const isStaffUser = Boolean(me?.user?.roles?.is_admin || me?.user?.roles?.is_barista);

  const ActivePageComponent = useMemo(() => {
    if (activePage === 'account') return AccountPage;
    if (activePage === 'cafe') return CafePage;
    if (activePage === 'cowork') return CoworkPage;
    if (activePage === 'staff') return StaffPage;
    return HomePage;
  }, [activePage]);

  const activePageProps = useMemo(() => {
    if (activePage === 'account') {
      return { me, onSessionRefresh: refreshSession };
    }
    return { me };
  }, [activePage, me]);

  return (
    <div className="spa-shell text-white">
      <header className="py-6 border-b border-white/10">
        <div className="spa-container flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-2xl md:text-3xl font-black tracking-wide">36 Workspace Platform</h1>
            <p className="text-white/70 text-sm">React app shell running on top of Django APIs.</p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            {navItems
              .filter((item) => !item.requiresStaff || isStaffUser)
              .map((item) => (
                <a
                  key={item.key}
                  href={item.href}
                  data-spa-link="true"
                  className={`btn btn-sm ${activePage === item.key ? 'btn-primary' : 'btn-ghost text-white border-white/30'}`}
                >
                  {item.label}
                </a>
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
        {error ? (
          <div className="alert alert-error mb-6">{error}</div>
        ) : null}
        <Suspense
          fallback={(
            <section className="spa-card p-6 md:p-8">
              <h2 className="text-xl font-bold">Loading page...</h2>
            </section>
          )}
        >
          <ActivePageComponent {...activePageProps} />
        </Suspense>
      </main>
    </div>
  );
}

const rootNode = document.getElementById('app-root');
if (rootNode) {
  createRoot(rootNode).render(<App />);
}
