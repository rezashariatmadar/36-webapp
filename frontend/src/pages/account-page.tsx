import { useEffect, useState } from 'react';

import { apiFetch } from '../lib/api';
import type { SessionPayload } from '../types/auth';

type AccountPageProps = {
  me: SessionPayload;
  onSessionRefresh: () => Promise<void>;
};

export default function AccountPage({ me, onSessionRefresh }: AccountPageProps) {
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [nationalId, setNationalId] = useState('');
  const [birthDate, setBirthDate] = useState(me.user?.birth_date || '');
  const [profileName, setProfileName] = useState(me.user?.full_name || '');
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    if (me.authenticated) {
      setProfileName(me.user?.full_name || '');
      setBirthDate(me.user?.birth_date || '');
    }
  }, [me]);

  const loginSubmit = async () => {
    setBusy(true);
    setError('');
    setMessage('');
    try {
      await apiFetch<SessionPayload>('/api/auth/login/', {
        method: 'POST',
        body: JSON.stringify({
          phone_number: phoneNumber,
          password,
        }),
      });
      await onSessionRefresh();
      setMessage('Signed in successfully.');
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : 'Unable to sign in.');
    } finally {
      setBusy(false);
    }
  };

  const registerSubmit = async () => {
    setBusy(true);
    setError('');
    setMessage('');
    try {
      await apiFetch<SessionPayload>('/api/auth/register/', {
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
      setError(submitError instanceof Error ? submitError.message : 'Unable to register.');
    } finally {
      setBusy(false);
    }
  };

  const profileSubmit = async () => {
    setBusy(true);
    setError('');
    setMessage('');
    try {
      await apiFetch<SessionPayload>('/api/auth/profile/', {
        method: 'PATCH',
        body: JSON.stringify({
          full_name: profileName,
          birth_date: birthDate,
        }),
      });
      await onSessionRefresh();
      setMessage('Profile updated successfully.');
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : 'Unable to update profile.');
    } finally {
      setBusy(false);
    }
  };

  const logoutSubmit = async () => {
    setBusy(true);
    setError('');
    setMessage('');
    try {
      await apiFetch<SessionPayload>('/api/auth/logout/', { method: 'POST' });
      await onSessionRefresh();
      setMode('login');
      setMessage('Signed out successfully.');
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : 'Unable to sign out.');
    } finally {
      setBusy(false);
    }
  };

  if (!me.authenticated) {
    return (
      <section className="spa-card p-6 md:p-8">
        <div className="flex items-center gap-2 mb-4">
          <button
            type="button"
            className={`btn btn-sm ${mode === 'login' ? 'btn-primary' : 'btn-outline border-white/30 text-white'}`}
            onClick={() => setMode('login')}
          >
            Login
          </button>
          <button
            type="button"
            className={`btn btn-sm ${mode === 'register' ? 'btn-primary' : 'btn-outline border-white/30 text-white'}`}
            onClick={() => setMode('register')}
          >
            Register
          </button>
        </div>
        {error ? <div className="alert alert-error mb-3">{error}</div> : null}
        {message ? <div className="alert alert-success mb-3">{message}</div> : null}
        <div className="space-y-3">
          <input
            className="input input-bordered w-full bg-white/5 border-white/20 text-white"
            placeholder="Phone Number (09xxxxxxxxx)"
            value={phoneNumber}
            onChange={(event) => setPhoneNumber(event.target.value)}
          />
          <input
            className="input input-bordered w-full bg-white/5 border-white/20 text-white"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
          {mode === 'register' ? (
            <>
              <input
                className="input input-bordered w-full bg-white/5 border-white/20 text-white"
                type="password"
                placeholder="Confirm Password"
                value={confirmPassword}
                onChange={(event) => setConfirmPassword(event.target.value)}
              />
              <input
                className="input input-bordered w-full bg-white/5 border-white/20 text-white"
                placeholder="Full Name"
                value={fullName}
                onChange={(event) => setFullName(event.target.value)}
              />
              <input
                className="input input-bordered w-full bg-white/5 border-white/20 text-white"
                placeholder="National ID (optional)"
                value={nationalId}
                onChange={(event) => setNationalId(event.target.value)}
              />
            </>
          ) : null}
          <button
            type="button"
            className="btn btn-primary w-full"
            onClick={mode === 'login' ? loginSubmit : registerSubmit}
            disabled={busy}
          >
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
        <button
          type="button"
          className="btn btn-sm btn-outline border-white/30 text-white"
          onClick={logoutSubmit}
          disabled={busy}
        >
          Logout
        </button>
      </div>
      {error ? <div className="alert alert-error mb-3">{error}</div> : null}
      {message ? <div className="alert alert-success mb-3">{message}</div> : null}
      <div className="space-y-3">
        <input
          className="input input-bordered w-full bg-white/5 border-white/20 text-white"
          value={me.user?.phone_number || ''}
          disabled
        />
        <input
          className="input input-bordered w-full bg-white/5 border-white/20 text-white"
          placeholder="Full Name"
          value={profileName}
          onChange={(event) => setProfileName(event.target.value)}
        />
        <input
          className="input input-bordered w-full bg-white/5 border-white/20 text-white"
          placeholder="Birth Date (YYYY-MM-DD)"
          value={birthDate}
          onChange={(event) => setBirthDate(event.target.value)}
        />
        <button type="button" className="btn btn-primary w-full" onClick={profileSubmit} disabled={busy}>
          Save Profile
        </button>
      </div>
    </section>
  );
}

