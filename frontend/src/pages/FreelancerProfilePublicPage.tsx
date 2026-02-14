import { useEffect, useMemo, useState } from 'react'
import { useParams } from 'react-router-dom'
import { EmptyState } from '../components/EmptyState'
import { FlairBadge } from '../components/FlairBadge'
import { SeoHead } from '../components/SeoHead'
import { ServiceCard, type ServiceCardData } from '../components/ServiceCard'
import { TagChip } from '../components/TagChip'
import { apiFetch } from '../lib/api/client'

type ProfilePayload = {
  profile: {
    public_slug: string
    full_name: string
    headline: string
    introduction: string
    work_types: string[]
    city: string
    province: string
    contact_cta_text: string
    contact_cta_url: string
    specialties: Array<{ id: number; name: string }>
    custom_specialties: string[]
    flairs: Array<{ id: number; name: string; color_token: string }>
    services: ServiceCardData[]
  }
}

export function FreelancerProfilePublicPage() {
  const { slug } = useParams()
  const [payload, setPayload] = useState<ProfilePayload | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!slug) return
    setLoading(true)
    setError('')
    apiFetch<ProfilePayload>(`/api/freelancers/${slug}/`)
      .then((data) => setPayload(data))
      .catch((err) => setError((err as Error).message))
      .finally(() => setLoading(false))
  }, [slug])

  const jsonLd = useMemo(() => {
    if (!payload?.profile) return null
    const profile = payload.profile
    return {
      '@context': 'https://schema.org',
      '@type': 'Person',
      name: profile.full_name || profile.public_slug,
      description: profile.headline || profile.introduction,
      address: {
        '@type': 'PostalAddress',
        addressLocality: profile.city,
        addressRegion: profile.province,
        addressCountry: 'IR',
      },
      knowsAbout: [
        ...profile.specialties.map((item) => item.name),
        ...(profile.custom_specialties || []),
      ],
      url: `${window.location.origin}/freelancers/${profile.public_slug}/`,
    }
  }, [payload])

  if (loading) return <p>در حال بارگذاری...</p>
  if (error) return <p className="error">{error}</p>
  if (!payload) return <EmptyState title="پروفایل یافت نشد" />

  const profile = payload.profile
  return (
    <section className="page-stack">
      <SeoHead
        title={`${profile.full_name || profile.public_slug} | فریلنسر`}
        description={profile.headline || profile.introduction}
        canonicalUrl={`${window.location.origin}/freelancers/${profile.public_slug}/`}
        jsonLd={jsonLd}
      />
      <div className="panel">
        <p className="eyebrow">Freelancer Profile</p>
        <h2>{profile.full_name || profile.public_slug}</h2>
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
        {profile.contact_cta_url ? (
          <a className="btn-primary" href={profile.contact_cta_url} target="_blank" rel="noreferrer">
            {profile.contact_cta_text || 'تماس'}
          </a>
        ) : null}
      </div>

      <div className="panel">
        <h3>خدمات</h3>
        {profile.services.length === 0 ? (
          <EmptyState title="خدمتی ثبت نشده است." />
        ) : (
          <div className="services-grid">
            {profile.services.map((item) => (
              <ServiceCard key={item.id} service={item} />
            ))}
          </div>
        )}
      </div>
    </section>
  )
}

