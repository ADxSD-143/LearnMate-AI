import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { api, clearToken, getToken } from "../api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(Boolean(getToken()));

  async function loadUser() {
    if (!getToken()) {
      setLoading(false);
      return;
    }
    try {
      setUser(await api.me());
    } catch {
      clearToken();
      setUser(null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadUser();
    const handleUnauthorized = () => {
      setUser(null);
      setLoading(false);
    };
    window.addEventListener("learnmate:unauthorized", handleUnauthorized);
    return () => window.removeEventListener("learnmate:unauthorized", handleUnauthorized);
  }, []);

  async function login(username, password) {
    await api.login(username, password);
    await loadUser();
  }

  async function register(payload) {
    await api.register(payload);
    await login(payload.username, payload.password);
  }

  function logout() {
    clearToken();
    setUser(null);
  }

  const value = useMemo(() => ({ user, loading, login, register, logout }), [user, loading]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
