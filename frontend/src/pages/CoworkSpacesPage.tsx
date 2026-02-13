import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiFetch } from '../lib/api/client'

type Seat = { id: number; name: string; status: string; capacity: number }
type Space = { id: number; name: string; status: string; zone: string; seats: Seat[]; is_nested: boolean }
type Zone = { code: string; label: string; spaces: Space[] }

export function CoworkSpacesPage() {
  const [zones, setZones] = useState<Zone[]>([])
  const [expandedZones, setExpandedZones] = useState<Record<string, boolean>>({})
  const [error, setError] = useState('')

  useEffect(() => {
    apiFetch<{ zones: Zone[] }>('/api/cowork/spaces/')
      .then((data) => {
        setZones(data.zones)
        setExpandedZones(
          data.zones.reduce<Record<string, boolean>>((acc, zone) => {
            acc[zone.code] = false
            return acc
          }, {})
        )
      })
      .catch((err) => setError((err as Error).message))
  }, [])

  const toggleZone = (zoneCode: string) => {
    setExpandedZones((prev) => ({ ...prev, [zoneCode]: !prev[zoneCode] }))
  }

  return (
    <section className="page-stack layout-flow-compact">
      <header className="surface-open section-head row">
        <div>
          <p className="eyebrow">Cowork</p>
          <h2>فضاهای کاری</h2>
        </div>
        <Link className="btn-secondary" to="/cowork/my-bookings/">
          رزروهای من
        </Link>
      </header>

      {error ? <p className="error">{error}</p> : null}

      {zones.map((zone) => (
        <article key={zone.code} className="surface-strip cowork-zone">
          <button
            className="surface-open section-head row cowork-zone-head cowork-zone-toggle"
            type="button"
            onClick={() => toggleZone(zone.code)}
            aria-expanded={Boolean(expandedZones[zone.code])}
          >
            <h3>{zone.label}</h3>
            <span className="muted">
              {zone.spaces.length} فضا
              <span className="cowork-zone-chevron" aria-hidden>
                {expandedZones[zone.code] ? '▾' : '▸'}
              </span>
            </span>
          </button>
          {expandedZones[zone.code] ? (
            <div className="cowork-grid">
              {zone.spaces.map((space) => (
                <article key={space.id} className="surface-glass cowork-card">
                  <div className="cowork-card-summary">
                    <strong>{space.name}</strong>
                    <p className={`status-pill status-${space.status.toLowerCase()} cowork-status-pill`}>{space.status}</p>
                  </div>
                  <div className="cowork-card-body">
                    {space.zone === 'SHARED_DESK' && space.seats?.length ? (
                      <div className="cowork-seats-grid">
                        {space.seats.map((seat) => (
                          <div key={seat.id} className="cowork-seat-item">
                            <span>{seat.name}</span>
                            <span className={`status-pill status-${seat.status.toLowerCase()}`}>{seat.status}</span>
                          </div>
                        ))}
                      </div>
                    ) : null}
                    <Link className="btn-secondary" to={`/cowork/book/${space.id}`}>
                      رزرو این فضا
                    </Link>
                  </div>
                </article>
              ))}
            </div>
          ) : null}
        </article>
      ))}
    </section>
  )
}
