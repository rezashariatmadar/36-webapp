import React, { useEffect, useState } from 'react';

import { apiFetch } from '../api';

export default function StaffPage({ me }) {
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
