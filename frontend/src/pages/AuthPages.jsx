import { Link, Navigate, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { Button, Field } from "../components/UI";

function AuthLayout({ title, description, children, footer }) {
  return (
    <main className="auth-page">
      <div className="auth-visual">
        <div className="brand brand-light"><span className="brand-mark">L</span><span>LearnMate <em>AI</em></span></div>
        <div className="visual-copy">
          <p className="eyebrow">Your learning command center</p>
          <h1>Build momentum.<br /><span>Learn with clarity.</span></h1>
          <p>Bring your subjects, focus, and academic progress into one calm workspace.</p>
        </div>
        <div className="visual-orbit orbit-one" /><div className="visual-orbit orbit-two" />
      </div>
      <section className="auth-panel">
        <div className="auth-card">
          <p className="eyebrow">Welcome to LearnMate</p>
          <h2>{title}</h2>
          <p className="muted auth-description">{description}</p>
          {children}
          <p className="auth-footer">{footer}</p>
        </div>
      </section>
    </main>
  );
}

export function LoginPage() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  if (user) return <Navigate to="/dashboard" replace />;

  async function submit(event) {
    event.preventDefault();
    setError("");
    setSaving(true);
    try {
      await login(form.username, form.password);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <AuthLayout title="Sign in" description="Pick up where you left off and keep your learning loop moving." footer={<>New to LearnMate? <Link to="/register">Create an account</Link></>}>
      <form className="stack-form" onSubmit={submit}>
        <Field label="Username or email"><input required value={form.username} onChange={(event) => setForm({ ...form, username: event.target.value })} placeholder="you@example.com" /></Field>
        <Field label="Password"><input required type="password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} placeholder="Your password" /></Field>
        {error && <div className="form-error">{error}</div>}
        <Button type="submit" disabled={saving}>{saving ? "Signing in..." : "Sign in to workspace"}</Button>
      </form>
    </AuthLayout>
  );
}

export function RegisterPage() {
  const { user, register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", email: "", password: "", semester: 1 });
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  if (user) return <Navigate to="/dashboard" replace />;

  async function submit(event) {
    event.preventDefault();
    setError("");
    setSaving(true);
    try {
      await register({ ...form, semester: Number(form.semester) });
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <AuthLayout title="Create your account" description="Start with a simple academic profile. You can add subjects and learning data as you go." footer={<>Already have an account? <Link to="/login">Sign in</Link></>}>
      <form className="stack-form" onSubmit={submit}>
        <Field label="Username"><input required minLength="3" value={form.username} onChange={(event) => setForm({ ...form, username: event.target.value })} placeholder="alex_student" /></Field>
        <Field label="Email"><input required type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} placeholder="you@example.com" /></Field>
        <Field label="Semester"><input required type="number" min="1" max="12" value={form.semester} onChange={(event) => setForm({ ...form, semester: event.target.value })} /></Field>
        <Field label="Password"><input required minLength="6" type="password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} placeholder="At least 6 characters" /></Field>
        {error && <div className="form-error">{error}</div>}
        <Button type="submit" disabled={saving}>{saving ? "Creating account..." : "Create workspace"}</Button>
      </form>
    </AuthLayout>
  );
}
