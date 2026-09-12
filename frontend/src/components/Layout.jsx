import { NavLink, useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "../context/AuthContext";

const navigation = [
  ["Dashboard", "/dashboard", "⌂"],
  ["Subjects", "/subjects", "◈"],
  ["Tasks", "/tasks", "✓"],
  ["Timetable", "/timetable", "▦"],
  ["Attendance", "/attendance", "◒"],
  ["Materials", "/materials", "▤"],
  ["Quizzes", "/quizzes", "✎"],
  ["Recommendations", "/recommendations", "✦"],
  ["Study Plan", "/study-plan", "◷"],
];

export function AppShell({ children }) {
  const [open, setOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  function signOut() {
    logout();
    navigate("/login");
  }

  return (
    <div className="app-shell">
      <aside className={`sidebar ${open ? "sidebar-open" : ""}`}>
        <div className="brand"><span className="brand-mark">L</span><span>LearnMate <em>AI</em></span></div>
        <nav className="side-nav">
          <p className="nav-label">Workspace</p>
          {navigation.map(([label, path, icon]) => (
            <NavLink key={path} to={path} onClick={() => setOpen(false)} className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}>
              <span className="nav-icon">{icon}</span><span>{label}</span>
            </NavLink>
          ))}
          <p className="nav-label nav-label-spaced">Account</p>
          <NavLink to="/profile" onClick={() => setOpen(false)} className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}>
            <span className="nav-icon">◉</span><span>Profile</span>
          </NavLink>
          <NavLink to="/predictions" onClick={() => setOpen(false)} className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}>
            <span className="nav-icon">⌁</span><span>Performance baseline</span>
          </NavLink>
        </nav>
        <div className="sidebar-user">
          <div className="avatar">{user?.username?.slice(0, 1).toUpperCase()}</div>
          <div className="user-meta"><strong>{user?.username}</strong><span>{user?.email}</span></div>
          <button className="icon-button" onClick={signOut} title="Log out">↪</button>
        </div>
      </aside>
      {open && <button className="mobile-overlay" onClick={() => setOpen(false)} aria-label="Close menu" />}
      <main className="main-area">
        <header className="topbar">
          <button className="menu-button" onClick={() => setOpen(true)} aria-label="Open menu">☰</button>
          <div className="breadcrumb">LearnMate <span>/</span> <strong>{navigation.find(([, path]) => location.pathname.startsWith(path))?.[0] || "Profile"}</strong></div>
          <div className="topbar-actions"><span className="status-dot" /> Live workspace</div>
        </header>
        <div className="content">{children}</div>
      </main>
    </div>
  );
}
