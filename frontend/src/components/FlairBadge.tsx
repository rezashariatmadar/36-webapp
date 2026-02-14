type FlairBadgeProps = {
  label: string
  color?: string
}

export function FlairBadge({ label, color }: FlairBadgeProps) {
  return (
    <span
      className="flair-badge"
      style={{
        borderColor: color || 'rgba(255,255,255,0.2)',
        background: color ? `${color}22` : undefined,
      }}
    >
      {label}
    </span>
  )
}

