import { FormEvent, useEffect, useState } from 'react'
import { EmptyState } from '../components/EmptyState'
import { FlairBadge } from '../components/FlairBadge'
import { ServiceCard, type ServiceCardData } from '../components/ServiceCard'
import { TagChip } from '../components/TagChip'
import { apiFetch } from '../lib/api/client'
import { useAuth } from '../lib/auth/AuthContext'

type Specialty = { id: number; name: string; slug: string }
type Flair = { id: number; name: string; slug: string; color_token: string; icon_name?: string }

type FreelancerProfile = {
  id: number
  public_slug: string
  headline: string
  introduction: string
  work_types: string[]
  city: string
  province: string
  is_public: boolean
  status: string
  moderation_note: string
  contact_cta_text: string
  contact_cta_url: string
  specialty_ids: number[]
  flair_ids: number[]
  custom_specialties: string[]
  specialties: Specialty[]
  flairs: Flair[]
  services: ServiceCardData[]
}

const WORK_TYPES = [
  { key: 'remote', label: 'Remote' },
  { key: 'onsite', label: 'Onsite' },
  { key: 'hybrid', label: 'Hybrid' },
  { key: 'project_based', label: 'Project Based' },
]

export function ProfilePage() {
  const { session, refresh } = useAuth()
  const [fullName, setFullName] = useState('')
  const [birthDate, setBirthDate] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const [freelancer, setFreelancer] = useState<FreelancerProfile | null>(null)
  const [specialties, setSpecialties] = useState<Specialty[]>([])
  const [flairs, setFlairs] = useState<Flair[]>([])
  const [freelancerLoading, setFreelancerLoading] = useState(false)
  const [freelancerError, setFreelancerError] = useState('')
  const [freelancerMessage, setFreelancerMessage] = useState('')
  const [freelancerSubmitting, setFreelancerSubmitting] = useState(false)
  const [serviceSubmitting, setServiceSubmitting] = useState(false)

  const [publicSlug, setPublicSlug] = useState('')
  const [headline, setHeadline] = useState('')
  const [introduction, setIntroduction] = useState('')
  const [workTypes, setWorkTypes] = useState<string[]>([])
  const [city, setCity] = useState('')
  const [province, setProvince] = useState('')
  const [isPublic, setIsPublic] = useState(true)
  const [contactCtaText, setContactCtaText] = useState('Contact me')
  const [contactCtaUrl, setContactCtaUrl] = useState('')
  const [specialtyIds, setSpecialtyIds] = useState<number[]>([])
  const [flairIds, setFlairIds] = useState<number[]>([])
  const [customSpecialtiesText, setCustomSpecialtiesText] = useState('')

  const [serviceTitle, setServiceTitle] = useState('')
  const [serviceDescription, setServiceDescription] = useState('')
  const [serviceDeliveryMode, setServiceDeliveryMode] = useState('remote')
  const [serviceStartingPrice, setServiceStartingPrice] = useState('0')
  const [serviceResponseTime, setServiceResponseTime] = useState('24')

  useEffect(() => {
    setFullName(session?.user?.full_name ?? '')
    setBirthDate(session?.user?.birth_date ?? '')
  }, [session?.user?.full_name, session?.user?.birth_date])

  const mapFreelancer = (profile: FreelancerProfile) => {
    setFreelancer(profile)
    setPublicSlug(profile.public_slug || '')
    setHeadline(profile.headline || '')
    setIntroduction(profile.introduction || '')
    setWorkTypes(profile.work_types || [])
    setCity(profile.city || '')
    setProvince(profile.province || '')
    setIsPublic(profile.is_public ?? true)
    setContactCtaText(profile.contact_cta_text || 'Contact me')
    setContactCtaUrl(profile.contact_cta_url || '')
    setSpecialtyIds(profile.specialty_ids || [])
    setFlairIds(profile.flair_ids || [])
    setCustomSpecialtiesText((profile.custom_specialties || []).join(', '))
  }

  const loadFreelancer = async () => {
    setFreelancerLoading(true)
    setFreelancerError('')
    try {
      const [profileData, specialtiesData, flairsData] = await Promise.all([
        apiFetch<{ profile: FreelancerProfile }>('/api/auth/freelancer-profile/'),
        apiFetch<{ specialties: Specialty[] }>('/api/auth/freelancer-specialties/'),
        apiFetch<{ flairs: Flair[] }>('/api/auth/freelancer-flairs/'),
      ])
      mapFreelancer(profileData.profile)
      setSpecialties(specialtiesData.specialties)
      setFlairs(flairsData.flairs)
    } catch (err) {
      setFreelancerError((err as Error).message)
    } finally {
      setFreelancerLoading(false)
    }
  }

  useEffect(() => {
    if (!session?.authenticated) return
    void loadFreelancer()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session?.authenticated])

  if (!session?.authenticated) {
    return (
      <section className="surface-inline">
        <h2>پروفایل</h2>
        <p>برای مشاهده پروفایل ابتدا وارد شوید.</p>
      </section>
    )
  }

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setError('')
    setMessage('')
    setSubmitting(true)
    try {
      await apiFetch('/api/auth/profile/', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ full_name: fullName, birth_date: birthDate }),
      })
      await refresh()
      setMessage('پروفایل ذخیره شد.')
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setSubmitting(false)
    }
  }

  const onSaveFreelancer = async (event: FormEvent) => {
    event.preventDefault()
    setFreelancerError('')
    setFreelancerMessage('')
    setFreelancerSubmitting(true)
    const customSpecialties = customSpecialtiesText
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean)

    try {
      const data = await apiFetch<{ profile: FreelancerProfile }>('/api/auth/freelancer-profile/', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          public_slug: publicSlug,
          headline,
          introduction,
          work_types: workTypes,
          city,
          province,
          is_public: isPublic,
          contact_cta_text: contactCtaText,
          contact_cta_url: contactCtaUrl,
          specialty_ids: specialtyIds,
          flair_ids: flairIds,
          custom_specialties: customSpecialties,
        }),
      })
      mapFreelancer(data.profile)
      await refresh()
      setFreelancerMessage('پروفایل فریلنسر ذخیره شد.')
    } catch (err) {
      setFreelancerError((err as Error).message)
    } finally {
      setFreelancerSubmitting(false)
    }
  }

  const onSubmitForApproval = async () => {
    setFreelancerError('')
    setFreelancerMessage('')
    try {
      const data = await apiFetch<{ profile: FreelancerProfile }>('/api/auth/freelancer-profile/submit/', { method: 'POST' })
      mapFreelancer(data.profile)
      await refresh()
      setFreelancerMessage('پروفایل برای تایید ارسال شد.')
    } catch (err) {
      setFreelancerError((err as Error).message)
    }
  }

  const onAddService = async (event: FormEvent) => {
    event.preventDefault()
    setFreelancerError('')
    setFreelancerMessage('')
    setServiceSubmitting(true)
    try {
      await apiFetch('/api/auth/freelancer-services/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: serviceTitle,
          description: serviceDescription,
          delivery_mode: serviceDeliveryMode,
          starting_price: Number(serviceStartingPrice || 0),
          response_time_hours: Number(serviceResponseTime || 24),
          is_active: true,
        }),
      })
      setServiceTitle('')
      setServiceDescription('')
      setServiceDeliveryMode('remote')
      setServiceStartingPrice('0')
      setServiceResponseTime('24')
      await loadFreelancer()
      setFreelancerMessage('خدمت جدید ثبت شد.')
    } catch (err) {
      setFreelancerError((err as Error).message)
    } finally {
      setServiceSubmitting(false)
    }
  }

  const onSaveService = async (serviceId: number, patch: Partial<ServiceCardData>) => {
    setFreelancerError('')
    await apiFetch(`/api/auth/freelancer-services/${serviceId}/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(patch),
    })
    await loadFreelancer()
  }

  const onDeleteService = async (serviceId: number) => {
    setFreelancerError('')
    await apiFetch(`/api/auth/freelancer-services/${serviceId}/`, { method: 'DELETE' })
    await loadFreelancer()
  }

  return (
    <section className="page-stack layout-flow-compact profile-page">
      <div className="surface-open section-head">
        <p className="eyebrow">حساب من</p>
        <h2>پروفایل</h2>
        <p>{session.user?.phone_number}</p>
      </div>

      <form className="surface-inline grid profile-form" onSubmit={onSubmit}>
        <input autoComplete="name" value={fullName} onChange={(event) => setFullName(event.target.value)} placeholder="نام کامل" />
        <input value={birthDate} onChange={(event) => setBirthDate(event.target.value)} placeholder="YYYY-MM-DD" />
        {error ? <p className="error">{error}</p> : null}
        {message ? <p className="ok">{message}</p> : null}
        <button className="btn-primary" type="submit" disabled={submitting}>
          {submitting ? 'در حال ذخیره...' : 'ذخیره'}
        </button>
      </form>

      <div className="surface-strip">
        <p className="eyebrow">Freelancer</p>
        <h2>پروفایل حرفه‌ای</h2>
        {freelancerLoading ? <p>در حال بارگذاری اطلاعات فریلنسر...</p> : null}
        {freelancer ? (
          <>
            <div className="row chips-wrap">
              <TagChip label={`وضعیت: ${freelancer.status}`} />
              {freelancer.public_slug ? <TagChip label={`slug: ${freelancer.public_slug}`} /> : null}
              {freelancer.flairs.map((item) => (
                <FlairBadge key={item.id} label={item.name} color={item.color_token} />
              ))}
            </div>
            {freelancer.moderation_note ? <p className="muted">یادداشت ادمین: {freelancer.moderation_note}</p> : null}
          </>
        ) : null}
      </div>

      <form className="surface-inline grid profile-form" onSubmit={onSaveFreelancer}>
        <input value={publicSlug} onChange={(event) => setPublicSlug(event.target.value)} placeholder="public slug (مثال: ali-designer)" />
        <input value={headline} onChange={(event) => setHeadline(event.target.value)} placeholder="تیتر حرفه‌ای" />
        <textarea value={introduction} onChange={(event) => setIntroduction(event.target.value)} placeholder="معرفی کوتاه" />
        <div className="grid grid-two">
          <input value={city} onChange={(event) => setCity(event.target.value)} placeholder="شهر" />
          <input value={province} onChange={(event) => setProvince(event.target.value)} placeholder="استان" />
        </div>
        <div className="grid grid-two">
          <input value={contactCtaText} onChange={(event) => setContactCtaText(event.target.value)} placeholder="متن CTA تماس" />
          <input value={contactCtaUrl} onChange={(event) => setContactCtaUrl(event.target.value)} placeholder="لینک CTA تماس" />
        </div>

        <div className="panel-section">
          <strong>نوع همکاری</strong>
          <div className="option-grid">
            {WORK_TYPES.map((item) => (
              <label key={item.key} className="check-row">
                <input
                  type="checkbox"
                  checked={workTypes.includes(item.key)}
                  onChange={(event) => {
                    if (event.target.checked) {
                      setWorkTypes((prev) => [...prev, item.key])
                    } else {
                      setWorkTypes((prev) => prev.filter((value) => value !== item.key))
                    }
                  }}
                />
                <span>{item.label}</span>
              </label>
            ))}
          </div>
        </div>

        <div className="panel-section">
          <strong>تخصص‌های استاندارد</strong>
          <div className="option-grid">
            {specialties.map((item) => (
              <label key={item.id} className="check-row">
                <input
                  type="checkbox"
                  checked={specialtyIds.includes(item.id)}
                  onChange={(event) => {
                    if (event.target.checked) {
                      setSpecialtyIds((prev) => [...prev, item.id])
                    } else {
                      setSpecialtyIds((prev) => prev.filter((id) => id !== item.id))
                    }
                  }}
                />
                <span>{item.name}</span>
              </label>
            ))}
          </div>
        </div>

        <div className="panel-section">
          <strong>فلرها</strong>
          <div className="option-grid">
            {flairs.map((item) => (
              <label key={item.id} className="check-row">
                <input
                  type="checkbox"
                  checked={flairIds.includes(item.id)}
                  onChange={(event) => {
                    if (event.target.checked) {
                      setFlairIds((prev) => [...prev, item.id])
                    } else {
                      setFlairIds((prev) => prev.filter((id) => id !== item.id))
                    }
                  }}
                />
                <FlairBadge label={item.name} color={item.color_token} />
              </label>
            ))}
          </div>
        </div>

        <textarea
          value={customSpecialtiesText}
          onChange={(event) => setCustomSpecialtiesText(event.target.value)}
          placeholder="تخصص‌های سفارشی (با کاما جدا کنید)"
        />

        <label className="check-row">
          <input type="checkbox" checked={isPublic} onChange={(event) => setIsPublic(event.target.checked)} />
          <span>نمایش عمومی پروفایل</span>
        </label>

        {freelancerError ? <p className="error">{freelancerError}</p> : null}
        {freelancerMessage ? <p className="ok">{freelancerMessage}</p> : null}
        <div className="row">
          <button className="btn-primary" type="submit" disabled={freelancerSubmitting}>
            {freelancerSubmitting ? 'در حال ذخیره...' : 'ذخیره پروفایل فریلنسر'}
          </button>
          <button className="btn-secondary" type="button" onClick={onSubmitForApproval}>
            ارسال برای تایید
          </button>
        </div>
      </form>

      <form className="surface-inline grid profile-form" onSubmit={onAddService}>
        <p className="eyebrow">Service Offerings</p>
        <h3>افزودن خدمت جدید</h3>
        <input value={serviceTitle} onChange={(event) => setServiceTitle(event.target.value)} placeholder="عنوان خدمت" />
        <textarea value={serviceDescription} onChange={(event) => setServiceDescription(event.target.value)} placeholder="توضیح خدمت" />
        <div className="grid grid-two">
          <select value={serviceDeliveryMode} onChange={(event) => setServiceDeliveryMode(event.target.value)}>
            <option value="remote">Remote</option>
            <option value="onsite">Onsite</option>
            <option value="hybrid">Hybrid</option>
          </select>
          <input
            type="number"
            min={0}
            value={serviceStartingPrice}
            onChange={(event) => setServiceStartingPrice(event.target.value)}
            placeholder="قیمت شروع"
          />
        </div>
        <input
          type="number"
          min={1}
          max={168}
          value={serviceResponseTime}
          onChange={(event) => setServiceResponseTime(event.target.value)}
          placeholder="زمان پاسخ (ساعت)"
        />
        <button className="btn-primary" type="submit" disabled={serviceSubmitting}>
          {serviceSubmitting ? 'در حال افزودن...' : 'افزودن خدمت'}
        </button>
      </form>

      <div className="surface-strip">
        <h3>خدمات ثبت‌شده</h3>
        {!freelancer?.services?.length ? (
          <EmptyState title="هنوز خدمتی ثبت نشده است." />
        ) : (
          <div className="services-grid">
            {freelancer.services.map((service) => (
              <ServiceCard key={service.id} service={service} onSave={onSaveService} onDelete={onDeleteService} />
            ))}
          </div>
        )}
      </div>
    </section>
  )
}
