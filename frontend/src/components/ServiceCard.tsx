import { FormEvent, useState } from 'react'

export type ServiceCardData = {
  id: number
  title: string
  description: string
  delivery_mode: string
  starting_price: number
  response_time_hours: number
  is_active: boolean
  sort_order: number
}

type ServiceCardProps = {
  service: ServiceCardData
  onSave?: (serviceId: number, patch: Partial<ServiceCardData>) => Promise<void>
  onDelete?: (serviceId: number) => Promise<void>
}

export function ServiceCard({ service, onSave, onDelete }: ServiceCardProps) {
  const readOnly = !onSave && !onDelete
  const [title, setTitle] = useState(service.title)
  const [description, setDescription] = useState(service.description)
  const [deliveryMode, setDeliveryMode] = useState(service.delivery_mode)
  const [startingPrice, setStartingPrice] = useState(String(service.starting_price))
  const [responseTime, setResponseTime] = useState(String(service.response_time_hours))
  const [isActive, setIsActive] = useState(service.is_active)
  const [saving, setSaving] = useState(false)

  const handleSave = async (event: FormEvent) => {
    event.preventDefault()
    if (!onSave) return
    setSaving(true)
    try {
      await onSave(service.id, {
        title,
        description,
        delivery_mode: deliveryMode,
        starting_price: Number(startingPrice || 0),
        response_time_hours: Number(responseTime || 24),
        is_active: isActive,
      })
    } finally {
      setSaving(false)
    }
  }

  if (readOnly) {
    return (
      <article className="service-card">
        <h4>{service.title}</h4>
        <p>{service.description}</p>
        <div className="service-row">
          <span>{service.delivery_mode}</span>
          <span>از {service.starting_price.toLocaleString()} تومان</span>
          <span>پاسخ: {service.response_time_hours} ساعت</span>
        </div>
      </article>
    )
  }

  return (
    <form className="service-card" onSubmit={handleSave}>
      <div className="service-row">
        <input value={title} onChange={(event) => setTitle(event.target.value)} placeholder="عنوان خدمت" />
        <select value={deliveryMode} onChange={(event) => setDeliveryMode(event.target.value)}>
          <option value="remote">Remote</option>
          <option value="onsite">Onsite</option>
          <option value="hybrid">Hybrid</option>
        </select>
      </div>
      <textarea value={description} onChange={(event) => setDescription(event.target.value)} placeholder="توضیح کوتاه خدمت" />
      <div className="service-row">
        <input
          type="number"
          min={0}
          value={startingPrice}
          onChange={(event) => setStartingPrice(event.target.value)}
          placeholder="قیمت شروع"
        />
        <input
          type="number"
          min={1}
          max={168}
          value={responseTime}
          onChange={(event) => setResponseTime(event.target.value)}
          placeholder="زمان پاسخ (ساعت)"
        />
      </div>
      <label className="check-row">
        <input type="checkbox" checked={isActive} onChange={(event) => setIsActive(event.target.checked)} />
        <span>فعال</span>
      </label>
      <div className="row service-actions">
        {onSave ? (
          <button className="btn-secondary" type="submit" disabled={saving}>
            {saving ? 'در حال ذخیره...' : 'ذخیره خدمت'}
          </button>
        ) : null}
        {onDelete ? (
          <button
            className="btn-ghost"
            type="button"
            onClick={() => {
              void onDelete(service.id)
            }}
          >
            حذف
          </button>
        ) : null}
      </div>
    </form>
  )
}
