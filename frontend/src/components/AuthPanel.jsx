import React, { useState, useEffect } from 'react';
import { register as apiRegister, login as apiLogin, me as apiMe, logout as apiLogout } from '../api/auth';

export default function AuthPanel() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchMe = async () => {
    try {
      setError('');
      const data = await apiMe();
      setUser(data);
    } catch {
      setUser(null);
    }
  };

  useEffect(() => {
    fetchMe();
  }, []);

  const onRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await apiRegister(username, password);
      // auto login after register
      await apiLogin(username, password);
      await fetchMe();
      setUsername(''); setPassword('');
    } catch (err) {
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const onLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await apiLogin(username, password);
      await fetchMe();
      setUsername(''); setPassword('');
    } catch (err) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const onLogout = async () => {
    setLoading(true);
    setError('');
    try {
      await apiLogout();
      setUser(null);
    } catch (err) {
      setError(err.message || 'Logout failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md p-4 rounded-xl bg-white/70 backdrop-blur border border-gray-200 shadow">
      <h3 className="text-lg font-semibold mb-3">Account</h3>

      {user ? (
        <div className="space-y-3">
          <div className="text-sm text-gray-700">Signed in as <span className="font-medium">{user.username}</span></div>
          <button className="px-3 py-2 text-sm rounded bg-gray-900 text-white hover:bg-black disabled:opacity-50" onClick={onLogout} disabled={loading}>
            {loading ? 'Working…' : 'Log out'}
          </button>
        </div>
      ) : (
        <form className="space-y-3" onSubmit={onLogin}>
          <input
            className="w-full px-3 py-2 border rounded"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            className="w-full px-3 py-2 border rounded"
            placeholder="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {error && <div className="text-sm text-red-600">{error}</div>}
          <div className="flex gap-2">
            <button type="submit" className="px-3 py-2 text-sm rounded bg-green-600 text-white hover:bg-green-700 disabled:opacity-50" disabled={loading}>
              {loading ? 'Working…' : 'Log in'}
            </button>
            <button type="button" className="px-3 py-2 text-sm rounded border hover:bg-gray-50 disabled:opacity-50" onClick={onRegister} disabled={loading}>
              {loading ? 'Working…' : 'Register'}
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
