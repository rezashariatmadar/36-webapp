import React, { useEffect, useState } from 'react';

import { apiFetch } from '../api';

export default function CoworkPage({ me }) {
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
      window.location.assign(me.login_url || '/app/account');
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
