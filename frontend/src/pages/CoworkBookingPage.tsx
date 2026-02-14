import { FormEvent, useEffect, useMemo, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import DatePicker from 'react-multi-date-picker'
import DateObject from 'react-date-object'
import persian from 'react-date-object/calendars/persian'
import gregorian from 'react-date-object/calendars/gregorian'
import persian_fa from 'react-date-object/locales/persian_fa'
import gregorian_en from 'react-date-object/locales/gregorian_en'
import { apiFetch } from '../lib/api/client'

type Preview = {
  valid: boolean
  price: number
  start_time: string
  end_time: string
  end_time_jalali: string
}

type SpaceSummary = {
  id: number
  zone: string
  name: string
  seats?: { id: number; name: string }[]
}

type ZonePayload = {
  spaces: SpaceSummary[]
}

type CreateBookingResponse = {
  detail?: string
  requires_admin_approval?: boolean
}

const BOOKING_LABELS: Record<string, string> = {
  HOURLY: 'ساعتی',
  DAILY: 'روزانه',
  MONTHLY: 'ماهانه',
  SIX_MONTH: 'شش ماهه',
  YEARLY: 'سالانه',
}

const bookingTypesByZone: Record<string, string[]> = {
  LONG_TABLE: ['DAILY'],
  SHARED_DESK: ['MONTHLY'],
  PRIVATE_2: ['DAILY', 'MONTHLY', 'SIX_MONTH', 'YEARLY'],
  PRIVATE_3: ['DAILY', 'MONTHLY', 'SIX_MONTH', 'YEARLY'],
  MEETING_ROOM: ['HOURLY', 'DAILY', 'MONTHLY'],
  DESK: ['DAILY', 'MONTHLY'],
}

export function CoworkBookingPage() {
  const { spaceId } = useParams()
  const [bookingType, setBookingType] = useState('DAILY')
  const [startTime, setStartTime] = useState('')
  const [jalaliDateValue, setJalaliDateValue] = useState<DateObject | null>(null)
  const [spaceZone, setSpaceZone] = useState<string>('')
  const [spaceName, setSpaceName] = useState<string>('')
  const [preview, setPreview] = useState<Preview | null>(null)
  const [error, setError] = useState('')
  const [successNotice, setSuccessNotice] = useState('')
  const [busy, setBusy] = useState(false)
  const navigate = useNavigate()

  const availableBookingTypes = useMemo(() => {
    if (!spaceZone) return ['DAILY', 'MONTHLY', 'SIX_MONTH', 'YEARLY']
    return bookingTypesByZone[spaceZone] || ['DAILY']
  }, [spaceZone])

  useEffect(() => {
    if (!spaceId) return
    apiFetch<{ zones: ZonePayload[] }>('/api/cowork/spaces/')
      .then((payload) => {
        const targetId = Number(spaceId)
        for (const zone of payload.zones) {
          for (const space of zone.spaces || []) {
            if (space.id === targetId) {
              setSpaceZone(space.zone)
              setSpaceName(space.name)
              return
            }
            const matchedSeat = (space.seats || []).find((seat) => seat.id === targetId)
            if (matchedSeat) {
              setSpaceZone(space.zone)
              setSpaceName(matchedSeat.name)
              return
            }
          }
        }
      })
      .catch(() => {})
  }, [spaceId])

  useEffect(() => {
    if (!availableBookingTypes.includes(bookingType)) {
      setBookingType(availableBookingTypes[0])
    }
  }, [availableBookingTypes, bookingType])

  const onJalaliDateChange = (value: DateObject | DateObject[] | null) => {
    const dateValue = Array.isArray(value) ? value[0] : value
    if (!dateValue) {
      setJalaliDateValue(null)
      setStartTime('')
      return
    }

    const jalali = dateValue instanceof DateObject ? dateValue : new DateObject(dateValue)
    setJalaliDateValue(jalali)
    const gregorianDate = new DateObject(jalali).convert(gregorian, gregorian_en).format('YYYY-MM-DD')
    setStartTime(gregorianDate)
    setError('')
  }

  const runPreview = async () => {
    if (!spaceId) return
    if (!startTime.trim()) {
      setError('لطفا تاریخ شروع را وارد کنید.')
      return
    }
    setError('')
    setSuccessNotice('')
    setBusy(true)
    try {
      const params = new URLSearchParams({
        space_id: spaceId,
        booking_type: bookingType,
        start_time: startTime,
      })
      const data = await apiFetch<Preview>(`/api/cowork/bookings/preview/?${params.toString()}`)
      setPreview(data)
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setBusy(false)
    }
  }

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    if (!spaceId) return
    if (!startTime.trim()) {
      setError('لطفا تاریخ شروع را وارد کنید.')
      return
    }
    setError('')
    setBusy(true)
    try {
      const response = await apiFetch<CreateBookingResponse>('/api/cowork/bookings/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ space_id: Number(spaceId), booking_type: bookingType, start_time: startTime }),
      })
      setSuccessNotice(
        response.detail || 'رزرو ثبت شد اما تا تایید ادمین نهایی نیست. برای تایید نهایی لطفا تماس بگیرید.',
      )
      setPreview(null)
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <section className="page-stack layout-flow-compact">
      <div className="surface-open section-head">
        <p className="eyebrow">کوورک</p>
        <h2>رزرو فضا</h2>
        <p>نوع رزرو و تاریخ شروع را وارد کنید تا قیمت نهایی محاسبه شود.</p>
        {spaceName ? <p className="muted">فضای انتخابی: {spaceName}</p> : null}
      </div>
      <form className="surface-inline grid booking-form" onSubmit={submit}>
        <select value={bookingType} onChange={(e) => setBookingType(e.target.value)}>
          {availableBookingTypes.map((value) => (
            <option key={value} value={value}>
              {BOOKING_LABELS[value] || value}
            </option>
          ))}
        </select>
        <input
          value={startTime}
          onChange={(e) => {
            setStartTime(e.target.value)
            setError('')
          }}
          placeholder="YYYY-MM-DD"
        />
        <div className="booking-jalali-picker">
          <DatePicker
            value={jalaliDateValue}
            onChange={onJalaliDateChange}
            calendar={persian}
            locale={persian_fa}
            format="YYYY/MM/DD"
            calendarPosition="bottom-right"
            placeholder="انتخاب تاریخ جلالی"
            containerClassName="booking-jalali-container"
            inputClass="booking-jalali-input"
          />
          <small className="muted">با انتخاب از تقویم جلالی، تاریخ میلادی برای رزرو به‌صورت خودکار ثبت می‌شود.</small>
        </div>
        <div className="row booking-actions">
          <button className="btn-secondary" type="button" onClick={runPreview} disabled={busy}>
            {busy ? '...' : 'پیش‌نمایش'}
          </button>
          <button className="btn-primary" type="submit" disabled={busy}>
            {busy ? '...' : 'ثبت رزرو'}
          </button>
        </div>
      </form>
      {error ? <p className="error">{error}</p> : null}
      {successNotice ? (
        <div className="surface-strip booking-notice">
          <p>{successNotice}</p>
          <div className="row booking-actions">
            <Link className="btn-secondary" to="/cowork/my-bookings/">
              مشاهده رزروهای من
            </Link>
            <button className="btn-primary" type="button" onClick={() => navigate('/cowork/')}>
              بازگشت به فضاها
            </button>
          </div>
        </div>
      ) : null}
      {preview ? (
        <div className="surface-glass grid booking-preview">
          <h3>نتیجه پیش‌نمایش</h3>
          <p>قیمت: {preview.price.toLocaleString()} تومان</p>
          <p>شروع: {preview.start_time}</p>
          <p>پایان: {preview.end_time}</p>
          <p>پایان (جلالی): {preview.end_time_jalali}</p>
        </div>
      ) : null}
    </section>
  )
}
