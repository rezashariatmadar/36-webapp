import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';

import './app.css';

const APP_PREFIX = '/app';

let csrfTokenCache = '';

const getCookie = (name) => {
  const cookie = `; ${document.cookie}`;
  const chunks = cookie.split(`; ${name}=`);
  if (chunks.length !== 2) return '';
  return chunks.pop().split(';').shift() || '';
};

const apiFetch = async (path, options = {}) => {
  const method = options.method || 'GET';
  const headers = new Headers(options.headers || {});
  headers.set('Accept', 'application/json');
  const isWrite = !['GET', 'HEAD', 'OPTIONS'].includes(method.toUpperCase());

  if (isWrite && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }
  if (isWrite && !headers.has('X-CSRFToken')) {
    headers.set('X-CSRFToken', csrfTokenCache || getCookie('csrftoken'));
  }

  const response = await fetch(path, {
    ...options,
    method,
    headers,
    credentials: 'same-origin',
  });

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    const detail = payload?.detail || payload?.errors || `HTTP ${response.status}`;
    throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail));
  }
  return payload;
};

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
  const [me, setMe] = useState({ authenticated: false, user: null, login_url: '/login/' });
  const [routePath, setRoutePath] = useState(stripAppPrefix(window.location.pathname));
  const [error, setError] = useState('');
  const refreshSession = async () => {
    try {
      const data = await apiFetch('/api/auth/me/');
      csrfTokenCache = data.csrf_token || csrfTokenCache;
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
              <a href={me.login_url || '/login/'} className="btn btn-sm btn-outline border-white/30 text-white">
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
        {activePage === 'home' ? <HomePage me={me} /> : null}
        {activePage === 'account' ? <AccountPage me={me} onSessionRefresh={refreshSession} /> : null}
        {activePage === 'cafe' ? <CafePage me={me} /> : null}
        {activePage === 'cowork' ? <CoworkPage me={me} /> : null}
        {activePage === 'staff' ? <StaffPage me={me} /> : null}
      </main>
    </div>
  );
}

function HomePage({ me }) {
  return (
    <section className="spa-card p-6 md:p-8">
      <h2 className="text-xl font-bold">Migration Entry Point</h2>
      <p className="mt-2 text-white/75">
        This route is the new React shell. Legacy Django templates still run in parallel while feature cutover is in progress.
      </p>
      <div className="mt-5 spa-grid md:grid-cols-2">
        <a href="/app/account" data-spa-link="true" className="spa-card p-5 hover:bg-white/10 transition-colors">
          <h3 className="font-semibold">Account Workflow</h3>
          <p className="text-sm text-white/70 mt-1">Session login/register and profile update in SPA.</p>
        </a>
        <a href="/app/cafe" data-spa-link="true" className="spa-card p-5 hover:bg-white/10 transition-colors">
          <h3 className="font-semibold">Cafe Workflow</h3>
          <p className="text-sm text-white/70 mt-1">Menu, cart, checkout, and previous orders.</p>
        </a>
        <a href="/app/cowork" data-spa-link="true" className="spa-card p-5 hover:bg-white/10 transition-colors">
          <h3 className="font-semibold">Cowork Workflow</h3>
          <p className="text-sm text-white/70 mt-1">Spaces list, pricing preview, booking, and my bookings.</p>
        </a>
      </div>
      <div className="mt-6 text-sm text-white/70">
        Session: {me.authenticated ? `Signed in as ${me.user?.full_name || me.user?.phone_number}` : 'Anonymous'}
      </div>
    </section>
  );
}

function AccountPage({ me, onSessionRefresh }) {
  const [mode, setMode] = useState('login');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [nationalId, setNationalId] = useState('');
  const [birthDate, setBirthDate] = useState(me?.user?.birth_date || '');
  const [profileName, setProfileName] = useState(me?.user?.full_name || '');
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    if (me?.authenticated) {
      setProfileName(me.user?.full_name || '');
      setBirthDate(me.user?.birth_date || '');
    }
  }, [me]);

  const loginSubmit = async () => {
    setBusy(true);
    setError('');
    setMessage('');
    try {
      await apiFetch('/api/auth/login/', {
        method: 'POST',
        body: JSON.stringify({
          phone_number: phoneNumber,
          password,
        }),
      });
      await onSessionRefresh();
      setMessage('Signed in successfully.');
    } catch (submitError) {
      setError(submitError.message);
    } finally {
      setBusy(false);
    }
  };

  const registerSubmit = async () => {
    setBusy(true);
    setError('');
    setMessage('');
    try {
      await apiFetch('/api/auth/register/', {
        method: 'POST',
        body: JSON.stringify({
          phone_number: phoneNumber,
          password,
          confirm_password: confirmPassword,
          full_name: fullName,
          national_id: nationalId,
        }),
      });
      await onSessionRefresh();
      setMessage('Registered and signed in successfully.');
    } catch (submitError) {
      setError(submitError.message);
    } finally {
      setBusy(false);
    }
  };

  const profileSubmit = async () => {
    setBusy(true);
    setError('');
    setMessage('');
    try {
      await apiFetch('/api/auth/profile/', {
        method: 'PATCH',
        body: JSON.stringify({
          full_name: profileName,
          birth_date: birthDate,
        }),
      });
      await onSessionRefresh();
      setMessage('Profile updated successfully.');
    } catch (submitError) {
      setError(submitError.message);
    } finally {
      setBusy(false);
    }
  };

  const logoutSubmit = async () => {
    setBusy(true);
    setError('');
    setMessage('');
    try {
      await apiFetch('/api/auth/logout/', { method: 'POST' });
      await onSessionRefresh();
      setMode('login');
      setMessage('Signed out successfully.');
    } catch (submitError) {
      setError(submitError.message);
    } finally {
      setBusy(false);
    }
  };

  if (!me?.authenticated) {
    return (
      <section className="spa-card p-6 md:p-8">
        <div className="flex items-center gap-2 mb-4">
          <button type="button" className={`btn btn-sm ${mode === 'login' ? 'btn-primary' : 'btn-outline border-white/30 text-white'}`} onClick={() => setMode('login')}>
            Login
          </button>
          <button type="button" className={`btn btn-sm ${mode === 'register' ? 'btn-primary' : 'btn-outline border-white/30 text-white'}`} onClick={() => setMode('register')}>
            Register
          </button>
        </div>
        {error ? <div className="alert alert-error mb-3">{error}</div> : null}
        {message ? <div className="alert alert-success mb-3">{message}</div> : null}
        <div className="space-y-3">
          <input className="input input-bordered w-full bg-white/5 border-white/20 text-white" placeholder="Phone Number (09xxxxxxxxx)" value={phoneNumber} onChange={(event) => setPhoneNumber(event.target.value)} />
          <input className="input input-bordered w-full bg-white/5 border-white/20 text-white" type="password" placeholder="Password" value={password} onChange={(event) => setPassword(event.target.value)} />
          {mode === 'register' ? (
            <>
              <input className="input input-bordered w-full bg-white/5 border-white/20 text-white" type="password" placeholder="Confirm Password" value={confirmPassword} onChange={(event) => setConfirmPassword(event.target.value)} />
              <input className="input input-bordered w-full bg-white/5 border-white/20 text-white" placeholder="Full Name" value={fullName} onChange={(event) => setFullName(event.target.value)} />
              <input className="input input-bordered w-full bg-white/5 border-white/20 text-white" placeholder="National ID (optional)" value={nationalId} onChange={(event) => setNationalId(event.target.value)} />
            </>
          ) : null}
          <button type="button" className="btn btn-primary w-full" onClick={mode === 'login' ? loginSubmit : registerSubmit} disabled={busy}>
            {mode === 'login' ? 'Sign In' : 'Create Account'}
          </button>
        </div>
      </section>
    );
  }

  return (
    <section className="spa-card p-6 md:p-8">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold">Account Profile</h2>
        <button type="button" className="btn btn-sm btn-outline border-white/30 text-white" onClick={logoutSubmit} disabled={busy}>
          Logout
        </button>
      </div>
      {error ? <div className="alert alert-error mb-3">{error}</div> : null}
      {message ? <div className="alert alert-success mb-3">{message}</div> : null}
      <div className="space-y-3">
        <input className="input input-bordered w-full bg-white/5 border-white/20 text-white" value={me.user?.phone_number || ''} disabled />
        <input className="input input-bordered w-full bg-white/5 border-white/20 text-white" placeholder="Full Name" value={profileName} onChange={(event) => setProfileName(event.target.value)} />
        <input className="input input-bordered w-full bg-white/5 border-white/20 text-white" placeholder="Birth Date (YYYY-MM-DD)" value={birthDate} onChange={(event) => setBirthDate(event.target.value)} />
        <button type="button" className="btn btn-primary w-full" onClick={profileSubmit} disabled={busy}>
          Save Profile
        </button>
      </div>
    </section>
  );
}

function CafePage({ me }) {
  const [menu, setMenu] = useState([]);
  const [cart, setCart] = useState({ items: [], total: 0, cart_count: 0 });
  const [orders, setOrders] = useState([]);
  const [notes, setNotes] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const loadCart = async () => {
    const data = await apiFetch('/api/cafe/cart/');
    setCart(data);
  };

  const loadMenu = async () => {
    const data = await apiFetch('/api/cafe/menu/');
    setMenu(data.categories || []);
  };

  const loadOrders = async () => {
    if (!me.authenticated) {
      setOrders([]);
      return;
    }
    const data = await apiFetch('/api/cafe/orders/');
    setOrders(data.orders || []);
  };

  const loadAll = async () => {
    setBusy(true);
    setError('');
    try {
      await Promise.all([loadMenu(), loadCart(), loadOrders()]);
    } catch (loadError) {
      setError(loadError.message);
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    loadAll();
  }, [me.authenticated]);

  const changeQuantity = async (menuItemId, delta) => {
    setError('');
    try {
      const data = await apiFetch('/api/cafe/cart/items/', {
        method: 'POST',
        body: JSON.stringify({ menu_item_id: menuItemId, delta }),
      });
      setCart(data);
      setMessage('Cart updated');
      window.setTimeout(() => setMessage(''), 1200);
    } catch (cartError) {
      setError(cartError.message);
    }
  };

  const checkout = async () => {
    if (!me.authenticated) {
      window.location.assign(me.login_url || '/login/');
      return;
    }
    setError('');
    setBusy(true);
    try {
      await apiFetch('/api/cafe/checkout/', {
        method: 'POST',
        body: JSON.stringify({ notes }),
      });
      setNotes('');
      await Promise.all([loadCart(), loadOrders()]);
      setMessage('Checkout completed');
    } catch (checkoutError) {
      setError(checkoutError.message);
    } finally {
      setBusy(false);
    }
  };

  const reorder = async (orderId) => {
    setError('');
    try {
      const updatedCart = await apiFetch(`/api/cafe/orders/${orderId}/reorder/`, { method: 'POST' });
      setCart(updatedCart);
      setMessage('Order copied to cart');
      window.setTimeout(() => setMessage(''), 1200);
    } catch (reorderError) {
      setError(reorderError.message);
    }
  };

  return (
    <section className="spa-grid spa-grid-2">
      <div className="spa-card p-5 md:p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold">Cafe Menu</h2>
          <button type="button" className="btn btn-sm btn-outline border-white/30 text-white" onClick={loadAll} disabled={busy}>
            Refresh
          </button>
        </div>
        {error ? <div className="alert alert-error mb-4">{error}</div> : null}
        {message ? <div className="alert alert-success mb-4">{message}</div> : null}
        {busy && !menu.length ? <div className="text-white/60">Loading...</div> : null}
        <div className="space-y-5">
          {menu.map((category) => (
            <article key={category.id}>
              <h3 className="font-semibold text-white/90 mb-2">{category.name}</h3>
              <div className="spa-grid md:grid-cols-2">
                {(category.items || []).map((item) => (
                  <div key={item.id} className="spa-card p-4">
                    <div className="font-medium">{item.name}</div>
                    <div className="text-sm text-white/60 mt-1">{item.description || 'No description'}</div>
                    <div className="mt-2 text-sm font-semibold">{item.price.toLocaleString()} toman</div>
                    <div className="mt-3 flex items-center gap-2">
                      <button type="button" className="btn btn-xs btn-outline border-white/30 text-white" onClick={() => changeQuantity(item.id, -1)}>
                        -
                      </button>
                      <button type="button" className="btn btn-xs btn-primary" onClick={() => changeQuantity(item.id, 1)}>
                        Add
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </article>
          ))}
        </div>
      </div>

      <aside className="spa-grid">
        <div className="spa-card p-5">
          <h2 className="text-lg font-bold">Cart ({cart.cart_count || 0})</h2>
          <div className="mt-3 space-y-2 max-h-80 overflow-auto pr-1">
            {(cart.items || []).length ? (
              cart.items.map((item) => (
                <div key={`${item.item_id}-${item.quantity}`} className="flex items-center justify-between text-sm">
                  <span>{item.name} x {item.quantity}</span>
                  <span>{item.subtotal.toLocaleString()}</span>
                </div>
              ))
            ) : (
              <div className="text-white/60 text-sm">Cart is empty</div>
            )}
          </div>
          <div className="mt-3 font-semibold">Total: {(cart.total || 0).toLocaleString()} toman</div>
          <textarea
            className="textarea textarea-bordered w-full mt-3 bg-white/5 border-white/20 text-white"
            rows={3}
            value={notes}
            onChange={(event) => setNotes(event.target.value)}
            placeholder="Order notes"
          />
          <button type="button" className="btn btn-primary w-full mt-3" onClick={checkout} disabled={busy || !(cart.items || []).length}>
            Checkout
          </button>
        </div>

        <div className="spa-card p-5">
          <h2 className="text-lg font-bold">My Orders</h2>
          {!me.authenticated ? (
            <p className="text-sm text-white/60 mt-2">Sign in to view order history.</p>
          ) : !(orders || []).length ? (
            <p className="text-sm text-white/60 mt-2">No orders yet.</p>
          ) : (
            <div className="mt-3 space-y-3">
              {orders.map((order) => (
                <div key={order.id} className="spa-card p-3">
                  <div className="flex items-center justify-between text-sm">
                    <span>Order #{order.id}</span>
                    <span>{order.status}</span>
                  </div>
                  <div className="text-xs text-white/60 mt-1">Total: {(order.total_price || 0).toLocaleString()} toman</div>
                  <button type="button" className="btn btn-xs btn-outline border-white/30 text-white mt-2" onClick={() => reorder(order.id)}>
                    Reorder
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </aside>
    </section>
  );
}

function CoworkPage({ me }) {
  const [zones, setZones] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [selectedSpace, setSelectedSpace] = useState('');
  const [bookingType, setBookingType] = useState('DAILY');
  const [startTime, setStartTime] = useState('');
  const [preview, setPreview] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const loadSpaces = async () => {
    const data = await apiFetch('/api/cowork/spaces/');
    setZones(data.zones || []);
  };

  const loadBookings = async () => {
    if (!me.authenticated) {
      setBookings([]);
      return;
    }
    const data = await apiFetch('/api/cowork/my-bookings/');
    setBookings(data.bookings || []);
  };

  const refresh = async () => {
    setBusy(true);
    setError('');
    try {
      await Promise.all([loadSpaces(), loadBookings()]);
    } catch (loadError) {
      setError(loadError.message);
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    refresh();
  }, [me.authenticated]);

  const runPreview = async () => {
    if (!selectedSpace || !startTime || !bookingType) {
      setError('Select a space, booking type, and start date first.');
      return;
    }
    setError('');
    try {
      const query = new URLSearchParams({
        space_id: selectedSpace,
        booking_type: bookingType,
        start_time: startTime,
      });
      const data = await apiFetch(`/api/cowork/bookings/preview/?${query.toString()}`);
      setPreview(data);
    } catch (previewError) {
      setPreview(null);
      setError(previewError.message);
    }
  };

  const book = async () => {
    if (!me.authenticated) {
      window.location.assign(me.login_url || '/login/');
      return;
    }
    setBusy(true);
    setError('');
    try {
      await apiFetch('/api/cowork/bookings/', {
        method: 'POST',
        body: JSON.stringify({
          space_id: selectedSpace,
          booking_type: bookingType,
          start_time: startTime,
        }),
      });
      setPreview(null);
      await refresh();
    } catch (bookingError) {
      setError(bookingError.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <section className="spa-grid spa-grid-2">
      <div className="spa-card p-5 md:p-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold">Cowork Spaces</h2>
          <button type="button" className="btn btn-sm btn-outline border-white/30 text-white" onClick={refresh} disabled={busy}>
            Refresh
          </button>
        </div>
        {error ? <div className="alert alert-error mt-4">{error}</div> : null}
        <div className="mt-4 space-y-5">
          {zones.map((zone) => (
            <article key={zone.code}>
              <h3 className="font-semibold text-white/90 mb-2">{zone.label}</h3>
              <div className="spa-grid md:grid-cols-2">
                {(zone.spaces || []).map((space) => (
                  <button
                    type="button"
                    key={space.id}
                    className={`spa-card p-4 text-right transition-colors ${String(selectedSpace) === String(space.id) ? 'border-primary' : ''}`}
                    onClick={() => setSelectedSpace(String(space.id))}
                  >
                    <div className="font-medium">{space.name}</div>
                    <div className="text-sm text-white/60 mt-1">Status: {space.status}</div>
                    <div className="text-sm text-white/60">Zone: {space.zone}</div>
                  </button>
                ))}
              </div>
            </article>
          ))}
        </div>
      </div>

      <aside className="spa-grid">
        <div className="spa-card p-5">
          <h2 className="text-lg font-bold">Booking Preview</h2>
          <div className="space-y-3 mt-3">
            <label className="form-control">
              <span className="label-text text-white/70">Booking Type</span>
              <select className="select select-bordered bg-white/5 border-white/20 text-white" value={bookingType} onChange={(event) => setBookingType(event.target.value)}>
                <option value="DAILY">Daily</option>
                <option value="MONTHLY">Monthly</option>
                <option value="SIX_MONTH">Six-Month</option>
                <option value="YEARLY">Yearly</option>
              </select>
            </label>
            <label className="form-control">
              <span className="label-text text-white/70">Start Date (YYYY-MM-DD)</span>
              <input className="input input-bordered bg-white/5 border-white/20 text-white" value={startTime} onChange={(event) => setStartTime(event.target.value)} placeholder="1404-12-01" />
            </label>
            <div className="flex gap-2">
              <button type="button" className="btn btn-outline border-white/30 text-white flex-1" onClick={runPreview}>
                Preview
              </button>
              <button type="button" className="btn btn-primary flex-1" onClick={book} disabled={busy || !selectedSpace}>
                Book
              </button>
            </div>
            {preview ? (
              <div className="spa-card p-3 text-sm">
                <div>Price: {preview.price.toLocaleString()} toman</div>
                <div>End Date: {preview.end_time}</div>
                <div>Jalali End: {preview.end_time_jalali}</div>
              </div>
            ) : null}
          </div>
        </div>

        <div className="spa-card p-5">
          <h2 className="text-lg font-bold">My Bookings</h2>
          {!me.authenticated ? (
            <p className="text-sm text-white/60 mt-2">Sign in to see your bookings.</p>
          ) : !(bookings || []).length ? (
            <p className="text-sm text-white/60 mt-2">No active bookings.</p>
          ) : (
            <div className="mt-3 space-y-2">
              {bookings.map((booking) => (
                <div key={booking.id} className="spa-card p-3 text-sm">
                  <div className="font-medium">{booking.space_name}</div>
                  <div className="text-white/70">{booking.start_time} {'->'} {booking.end_time}</div>
                  <div className="text-white/70">Price: {(booking.price_charged || 0).toLocaleString()} toman</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </aside>
    </section>
  );
}

function StaffPage({ me }) {
  const [orders, setOrders] = useState([]);
  const [menuItems, setMenuItems] = useState([]);
  const [lookup, setLookup] = useState('');
  const [customers, setCustomers] = useState([]);
  const [platformUsers, setPlatformUsers] = useState([]);
  const [busy, setBusy] = useState(false);
  const [usersBusy, setUsersBusy] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const isStaffUser = Boolean(me?.user?.roles?.is_admin || me?.user?.roles?.is_barista);
  const isAdminUser = Boolean(me?.user?.roles?.is_admin);

  const loadCafeData = async () => {
    const [ordersData, menuData] = await Promise.all([
      apiFetch('/api/cafe/staff/orders/'),
      apiFetch('/api/cafe/staff/menu-items/'),
    ]);
    setOrders(ordersData.orders || []);
    setMenuItems(menuData.items || []);
  };

  const loadPlatformUsers = async () => {
    if (!isAdminUser) {
      setPlatformUsers([]);
      return;
    }
    const data = await apiFetch('/api/auth/staff/users/?page=1&page_size=100');
    setPlatformUsers(data.results || data || []);
  };

  const loadAll = async () => {
    setBusy(true);
    setError('');
    setMessage('');
    try {
      await Promise.all([loadCafeData(), loadPlatformUsers()]);
    } catch (loadError) {
      setError(loadError.message);
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    if (isStaffUser) {
      loadAll();
    }
  }, [isStaffUser]);

  const setOrderStatus = async (orderId, statusValue) => {
    setError('');
    setMessage('');
    try {
      await apiFetch(`/api/cafe/staff/orders/${orderId}/status/`, {
        method: 'POST',
        body: JSON.stringify({ status: statusValue }),
      });
      await loadAll();
      setMessage('Order status updated.');
    } catch (statusError) {
      setError(statusError.message);
    }
  };

  const togglePayment = async (orderId) => {
    setError('');
    setMessage('');
    try {
      await apiFetch(`/api/cafe/staff/orders/${orderId}/toggle-payment/`, { method: 'POST' });
      await loadAll();
      setMessage('Payment state updated.');
    } catch (paymentError) {
      setError(paymentError.message);
    }
  };

  const toggleItemAvailability = async (itemId) => {
    setError('');
    setMessage('');
    try {
      await apiFetch(`/api/cafe/staff/menu-items/${itemId}/toggle-availability/`, { method: 'POST' });
      await loadAll();
      setMessage('Menu availability updated.');
    } catch (toggleError) {
      setError(toggleError.message);
    }
  };

  const runLookup = async () => {
    if (!lookup.trim()) {
      setCustomers([]);
      return;
    }
    setError('');
    try {
      const data = await apiFetch(`/api/cafe/staff/customer-lookup/?q=${encodeURIComponent(lookup.trim())}`);
      setCustomers(data.customers || []);
    } catch (lookupError) {
      setError(lookupError.message);
    }
  };

  const toggleUserStatus = async (userId) => {
    setError('');
    setMessage('');
    setUsersBusy(true);
    try {
      await apiFetch(`/api/auth/staff/users/${userId}/status/`, {
        method: 'PATCH',
        body: JSON.stringify({}),
      });
      await loadPlatformUsers();
      setMessage('User status updated.');
    } catch (statusError) {
      setError(statusError.message);
    } finally {
      setUsersBusy(false);
    }
  };

  const setUserRole = async (userId, role) => {
    setError('');
    setMessage('');
    setUsersBusy(true);
    try {
      await apiFetch(`/api/auth/staff/users/${userId}/role/`, {
        method: 'PATCH',
        body: JSON.stringify({ role }),
      });
      await loadPlatformUsers();
      setMessage('User role updated.');
    } catch (roleError) {
      setError(roleError.message);
    } finally {
      setUsersBusy(false);
    }
  };

  if (!me.authenticated) {
    return (
      <section className="spa-card p-6">
        <h2 className="text-xl font-bold">Staff Dashboard</h2>
        <p className="text-white/70 mt-2">Sign in with a staff account to access this page.</p>
      </section>
    );
  }

  if (!isStaffUser) {
    return (
      <section className="spa-card p-6">
        <h2 className="text-xl font-bold">Staff Dashboard</h2>
        <p className="text-white/70 mt-2">This section is restricted to Barista and Admin roles.</p>
      </section>
    );
  }

  return (
    <section className="spa-grid spa-grid-2">
      <div className="spa-card p-5 md:p-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold">Active Orders</h2>
          <button type="button" className="btn btn-sm btn-outline border-white/30 text-white" onClick={loadAll} disabled={busy}>
            Refresh
          </button>
        </div>
        {error ? <div className="alert alert-error mt-4">{error}</div> : null}
        {message ? <div className="alert alert-success mt-4">{message}</div> : null}
        <div className="mt-4 space-y-3">
          {!orders.length ? (
            <p className="text-sm text-white/60">No active orders.</p>
          ) : (
            orders.map((order) => (
              <div key={order.id} className="spa-card p-4">
                <div className="flex items-center justify-between text-sm">
                  <span>Order #{order.id}</span>
                  <span>{order.status}</span>
                </div>
                <div className="text-xs text-white/70 mt-1">
                  {order.customer ? `${order.customer.full_name || order.customer.phone_number}` : 'Walk-in guest'}
                </div>
                <div className="text-xs text-white/70">Total: {(order.total_price || 0).toLocaleString()} toman</div>
                <div className="flex flex-wrap gap-2 mt-3">
                  <button type="button" className="btn btn-xs btn-outline border-white/30 text-white" onClick={() => setOrderStatus(order.id, 'PREPARING')}>
                    Preparing
                  </button>
                  <button type="button" className="btn btn-xs btn-outline border-white/30 text-white" onClick={() => setOrderStatus(order.id, 'READY')}>
                    Ready
                  </button>
                  <button type="button" className="btn btn-xs btn-outline border-white/30 text-white" onClick={() => setOrderStatus(order.id, 'DELIVERED')}>
                    Delivered
                  </button>
                  <button type="button" className="btn btn-xs btn-outline border-white/30 text-white" onClick={() => setOrderStatus(order.id, 'CANCELLED')}>
                    Cancel
                  </button>
                  <button type="button" className="btn btn-xs btn-primary" onClick={() => togglePayment(order.id)}>
                    {order.is_paid ? 'Mark Unpaid' : 'Mark Paid'}
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      <aside className="spa-grid">
        <div className="spa-card p-5">
          <h2 className="text-lg font-bold">Menu Stock</h2>
          <div className="mt-3 space-y-2 max-h-80 overflow-auto pr-1">
            {!menuItems.length ? (
              <p className="text-sm text-white/60">No menu items found.</p>
            ) : (
              menuItems.map((item) => (
                <div key={item.id} className="flex items-center justify-between text-sm gap-2">
                  <span className="truncate">{item.name}</span>
                  <button type="button" className="btn btn-xs btn-outline border-white/30 text-white" onClick={() => toggleItemAvailability(item.id)}>
                    {item.is_available ? 'Disable' : 'Enable'}
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="spa-card p-5">
          <h2 className="text-lg font-bold">Customer Lookup</h2>
          <div className="flex gap-2 mt-3">
            <input
              className="input input-bordered flex-1 bg-white/5 border-white/20 text-white"
              value={lookup}
              onChange={(event) => setLookup(event.target.value)}
              placeholder="Phone or name"
            />
            <button type="button" className="btn btn-outline border-white/30 text-white" onClick={runLookup}>
              Search
            </button>
          </div>
          <div className="mt-3 space-y-2">
            {!customers.length ? (
              <p className="text-sm text-white/60">No results.</p>
            ) : (
              customers.map((customer) => (
                <div key={customer.id} className="spa-card p-3 text-sm">
                  <div>{customer.full_name || '-'}</div>
                  <div className="text-white/70">{customer.phone_number}</div>
                </div>
              ))
            )}
          </div>
        </div>

        {isAdminUser ? (
          <div className="spa-card p-5">
            <h2 className="text-lg font-bold">Platform Users</h2>
            <div className="mt-3 space-y-2 max-h-96 overflow-auto pr-1">
              {!platformUsers.length ? (
                <p className="text-sm text-white/60">No users found.</p>
              ) : (
                platformUsers.map((userRecord) => (
                  <div key={userRecord.id} className="spa-card p-3 text-sm">
                    <div className="font-medium">{userRecord.full_name || '-'}</div>
                    <div className="text-white/70">{userRecord.phone_number}</div>
                    <div className="text-white/70">Role: {userRecord.role || 'Unassigned'}</div>
                    <div className="text-white/70">Status: {userRecord.is_active ? 'Active' : 'Inactive'}</div>
                    <div className="flex flex-wrap gap-2 mt-2">
                      <button type="button" className="btn btn-xs btn-outline border-white/30 text-white" onClick={() => setUserRole(userRecord.id, 'Admin')} disabled={usersBusy}>
                        Admin
                      </button>
                      <button type="button" className="btn btn-xs btn-outline border-white/30 text-white" onClick={() => setUserRole(userRecord.id, 'Barista')} disabled={usersBusy}>
                        Barista
                      </button>
                      <button type="button" className="btn btn-xs btn-outline border-white/30 text-white" onClick={() => setUserRole(userRecord.id, 'Customer')} disabled={usersBusy}>
                        Customer
                      </button>
                      <button type="button" className="btn btn-xs btn-primary" onClick={() => toggleUserStatus(userRecord.id)} disabled={usersBusy}>
                        {userRecord.is_active ? 'Deactivate' : 'Activate'}
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        ) : null}
      </aside>
    </section>
  );
}

const rootNode = document.getElementById('app-root');
if (rootNode) {
  createRoot(rootNode).render(<App />);
}
