import React, { useEffect, useState } from 'react';

import { apiFetch } from '../api';

export default function CafePage({ me }) {
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
      window.location.assign(me.login_url || '/app/account');
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
