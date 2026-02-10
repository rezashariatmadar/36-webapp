import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { apiFetch } from '../lib/api/client'

type Space = { id: number; name: string; status: string; zone: string }
type Zone = { code: string; label: string; spaces: Space[] }

export function CoworkSpacesPage() {
  const [zones, setZones] = useState<Zone[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    apiFetch<{ zones: Zone[] }>('/api/cowork/spaces/')
      .then((data) => setZones(data.zones))
      .catch((err) => setError((err as Error).message))
  }, [])

  return (
    <section className="page-stack">
      <div className="panel row">
        <h2>فضاهای کاری</h2>
        <Link className="btn-secondary" to="/cowork/my-bookings/">
          رزروهای من
        </Link>
      </div>
      {error ? <p className="error">{error}</p> : null}
      {zones.map((zone) => (
        <article key={zone.code} className="panel">
          <h3>{zone.label}</h3>
          <div className="grid">
            {zone.spaces.map((space) => (
              <div key={space.id} className="card">
                <strong>{space.name}</strong>
                <p>وضعیت: {space.status}</p>
                <Link to={`/cowork/book/${space.id}`}>رزرو این فضا</Link>
              </div>
            ))}
          </div>
        </article>
      ))}
    </section>
  )
}

