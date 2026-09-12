export function Button({ children, variant = "primary", type = "button", ...props }) {
  return <button className={`button button-${variant}`} type={type} {...props}>{children}</button>;
}

export function PageHeader({ eyebrow, title, description, action }) {
  return (
    <div className="page-header">
      <div>
        {eyebrow && <p className="eyebrow">{eyebrow}</p>}
        <h1>{title}</h1>
        {description && <p className="page-description">{description}</p>}
      </div>
      {action}
    </div>
  );
}

export function Card({ children, className = "" }) {
  return <section className={`card ${className}`}>{children}</section>;
}

export function StatCard({ label, value, detail, tone = "blue" }) {
  return (
    <Card className={`stat-card stat-${tone}`}>
      <p className="muted">{label}</p>
      <strong>{value}</strong>
      {detail && <span>{detail}</span>}
    </Card>
  );
}

export function EmptyState({ title, description, action }) {
  return (
    <div className="empty-state">
      <div className="empty-icon">✦</div>
      <h3>{title}</h3>
      <p>{description}</p>
      {action}
    </div>
  );
}

export function LoadingState({ label = "Loading..." }) {
  return <div className="loading-state"><span className="spinner" />{label}</div>;
}

export function ErrorState({ message, onRetry }) {
  return (
    <div className="error-state">
      <strong>Something went wrong</strong>
      <p>{message}</p>
      {onRetry && <Button variant="secondary" onClick={onRetry}>Try again</Button>}
    </div>
  );
}

export function Modal({ title, onClose, children }) {
  return (
    <div className="modal-backdrop" role="presentation" onMouseDown={(event) => event.target === event.currentTarget && onClose()}>
      <div className="modal">
        <div className="modal-heading"><h2>{title}</h2><button className="icon-button" onClick={onClose} aria-label="Close">×</button></div>
        {children}
      </div>
    </div>
  );
}

export function Field({ label, children, hint }) {
  return <label className="field"><span>{label}</span>{children}{hint && <small>{hint}</small>}</label>;
}

export function formatDate(value) {
  if (!value) return "No date";
  return new Intl.DateTimeFormat(undefined, { dateStyle: "medium" }).format(new Date(value));
}
