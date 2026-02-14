import { FormEvent, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { EmptyState } from '../components/EmptyState'
import { FlairBadge } from '../components/FlairBadge'
import { Pagination } from '../components/Pagination'
import { SeoHead } from '../components/SeoHead'
import { TagChip } from '../components/TagChip'
import { apiFetch } from '../lib/api/client'

type Specialty = { id: number; name: string; slug: string }
type Flair = { id: number; name: string; slug: string; color_token: string; icon_name?: string }
type Service = { id: number; title: string }

type ProfileCard = {
  id: number
  public_slug: string
  full_name: string
  headline: string
  introduction: string
  city: string
  province: string
  work_types: string[]
  specialties: Specialty[]
  custom_specialties: string[]
  flairs: Flair[]
  services: Service[]
}

type ListPayload = {
  count: number
  page: number
  page_size: number
  results: ProfileCard[]
}

export function FreelancersListPage() {
  const [q, setQ] = useState('')
  const [query, setQuery] = useState('')
  const [city, setCity] = useState('')
  const [tag, setTag] = useState('')
  const [flair, setFlair] = useState('')
  const [workType, setWorkType] = useState('')
  const [specialties, setSpecialties] = useState<Specialty[]>([])
  const [flairs, setFlairs] = useState<Flair[]>([])
  const [payload, setPayload] = useState<ListPayload>({ count: 0, page: 1, page_size: 12, results: [] })
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    apiFetch<{ specialties: Specialty[] }>('/api/freelancers/specialties/')
      .then((data) => setSpecialties(data.specialties))
      .catch(() => setSpecialties([]))
    apiFetch<{ flairs: Flair[] }>('/api/freelancers/flairs/')
      .then((data) => setFlairs(data.flairs))
      .catch(() => setFlairs([]))
  }, [])

  useEffect(() => {
    const params = new URLSearchParams({ page: String(page), page_size: '12' })
    if (query) params.set('q', query)
    if (city) params.set('city', city)
    if (tag) params.set('tag', tag)
    if (flair) params.set('flair', flair)
    if (workType) params.set('work_type', workType)

    setLoading(true)
    setError('')
    apiFetch<ListPayload>(`/api/freelancers/?${params.toString()}`)
      .then((data) => setPayload(data))
      .catch((err) => setError((err as Error).message))
      .finally(() => setLoading(false))
  }, [query, city, tag, flair, workType, page])

  const onSearch = (event: FormEvent) => {
    event.preventDefault()
    setPage(1)
    setQuery(q.trim())
  }

  return (
    <section className="page-stack layout-flow-compact">
      <SeoHead
        title="فریلنسرها | 36 Cowork"
        description="فهرست فریلنسرهای تاییدشده برای همکاری پروژه‌ای و حرفه‌ای."
        canonicalUrl={`${window.location.origin}/freelancers/`}
        jsonLd={{
          '@context': 'https://schema.org',
          '@type': 'ItemList',
          name: 'Freelancers',
          inLanguage: 'fa-IR',
          url: `${window.location.origin}/freelancers/`,
        }}
      />

      <header className="surface-open section-head">
        <p className="eyebrow">Freelancers</p>
        <h2>فریلنسرهای تاییدشده</h2>
      </header>

      <form className="surface-inline freelancers-filters" onSubmit={onSearch}>
        <input value={q} onChange={(event) => setQ(event.target.value)} placeholder="جستجو براساس نام یا تخصص..." />
        <input value={city} onChange={(event) => setCity(event.target.value)} placeholder="شهر" />
        <select value={tag} onChange={(event) => setTag(event.target.value)}>
          <option value="">همه تخصص‌ها</option>
          {specialties.map((item) => (
            <option key={item.id} value={item.slug}>
              {item.name}
            </option>
          ))}
        </select>
        <select value={flair} onChange={(event) => setFlair(event.target.value)}>
          <option value="">همه فلرها</option>
          {flairs.map((item) => (
            <option key={item.id} value={item.slug}>
              {item.name}
            </option>
          ))}
        </select>
        <select value={workType} onChange={(event) => setWorkType(event.target.value)}>
          <option value="">همه حالت‌های همکاری</option>
          <option value="remote">Remote</option>
          <option value="onsite">Onsite</option>
          <option value="hybrid">Hybrid</option>
          <option value="project_based">Project Based</option>
        </select>
        <button className="btn-primary" type="submit">
          اعمال فیلتر
        </button>
      </form>

      {error ? <p className="error">{error}</p> : null}
      {loading ? <p>در حال بارگذاری...</p> : null}
      {!loading && payload.results.length === 0 ? <EmptyState title="پروفایلی یافت نشد" /> : null}

      <div className="freelancers-grid">
        {payload.results.map((profile) => (
          <article key={profile.id} className="surface-inline freelancer-card">
            <h3>{profile.full_name || profile.public_slug}</h3>
            <p className="freelancer-headline">{profile.headline}</p>
            <p>{profile.introduction}</p>
            <p className="muted">
              {profile.city}
              {profile.city && profile.province ? ' - ' : ''}
              {profile.province}
            </p>
            <div className="row chips-wrap">
              {profile.specialties.map((item) => (
                <TagChip key={item.id} label={item.name} />
              ))}
              {profile.custom_specialties.map((item) => (
                <TagChip key={item} label={item} />
              ))}
            </div>
            <div className="row chips-wrap">
              {profile.flairs.map((item) => (
                <FlairBadge key={item.id} label={item.name} color={item.color_token} />
              ))}
            </div>
            <Link className="btn-secondary" to={`/freelancers/${profile.public_slug}/`}>
              مشاهده پروفایل
            </Link>
          </article>
        ))}
      </div>

      <Pagination page={page} pageSize={payload.page_size} total={payload.count} onChange={setPage} />
    </section>
  )
}
