import './DarkVeil.css'

type DarkVeilProps = {
  className?: string
}

export default function DarkVeil({ className = '' }: DarkVeilProps) {
  return (
    <div className={`rb-dark-veil ${className}`.trim()} aria-hidden>
      <div className="rb-dark-veil-layer rb-dark-veil-layer-a" />
      <div className="rb-dark-veil-layer rb-dark-veil-layer-b" />
      <div className="rb-dark-veil-grain" />
    </div>
  )
}

