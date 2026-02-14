import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import GlareHover from '../components/GlareHover'
import { apiFetch } from '../lib/api/client'

type Seat = { id: number; name: string; status: string; capacity: number }
type Space = { id: number; name: string; status: string; zone: string; seats: Seat[]; is_nested: boolean }
type Zone = { code: string; label: string; spaces: Space[] }

export function CoworkSpacesPage() {
  const [zones, setZones] = useState<Zone[]>([])
  const [expandedZones, setExpandedZones] = useState<Record<string, boolean>>({})
  const [selectedSeatBySpace, setSelectedSeatBySpace] = useState<Record<number, Seat | null>>({})
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

  const selectSeat = (spaceId: number, seat: Seat) => {
    setSelectedSeatBySpace((prev) => ({ ...prev, [spaceId]: seat }))
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
            <div className={`cowork-grid ${zone.code === 'SHARED_DESK' ? 'cowork-grid-shared' : ''}`}>
              {zone.spaces.map((space) => (
                <article key={space.id}>
                  <GlareHover className="surface-glass cowork-card" glareColor="#400080" glareOpacity={0.8} glareSize={500}>
                    <div className="cowork-card-summary">
                      <strong>{space.name}</strong>
                      <p className={`status-pill status-${space.status.toLowerCase()} cowork-status-pill`}>{space.status}</p>
                    </div>
                    <div className="cowork-card-body">
                      {space.zone === 'SHARED_DESK' && space.seats?.length ? (
                        <>
                          <div className="cowork-seats-grid">
                            {space.seats.map((seat) => {
                              const isSelected = selectedSeatBySpace[space.id]?.id === seat.id
                              return (
                                <button
                                  key={seat.id}
                                  type="button"
                                  className={`cowork-seat-item ${isSelected ? 'is-selected' : ''}`}
                                  onClick={() => selectSeat(space.id, seat)}
                                  disabled={seat.status !== 'AVAILABLE'}
                                >
                                  <span>{seat.name}</span>
                                  <span className={`status-pill status-${seat.status.toLowerCase()}`}>{seat.status}</span>
                                </button>
                              )
                            })}
                          </div>
                          {selectedSeatBySpace[space.id] ? (
                            <p className="muted">صندلی انتخاب‌شده: {selectedSeatBySpace[space.id]!.name}</p>
                          ) : null}
                          {selectedSeatBySpace[space.id] ? (
                            <Link className="btn-secondary" to={`/cowork/book/${selectedSeatBySpace[space.id]!.id}`}>
                              رزرو این فضا
                            </Link>
                          ) : (
                            <p className="muted">برای رزرو، یک صندلی را انتخاب کنید.</p>
                          )}
                        </>
                      ) : (
                        <Link className="btn-secondary" to={`/cowork/book/${space.id}`}>
                          رزرو این فضا
                        </Link>
                      )}
                    </div>
                  </GlareHover>
                </article>
              ))}
            </div>
          ) : null}
        </article>
      ))}
    </section>
  )
}

