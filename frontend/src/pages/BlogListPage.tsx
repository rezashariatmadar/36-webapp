import { FormEvent, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { EmptyState } from '../components/EmptyState'
import { Pagination } from '../components/Pagination'
import { SeoHead } from '../components/SeoHead'
import { TagChip } from '../components/TagChip'
import { apiFetch } from '../lib/api/client'

type BlogTag = {
  id: number
  name: string
  slug: string
  post_count: number
}

type BlogPostCard = {
  id: number
  title: string
  slug: string
  excerpt: string
  hero_image_url: string | null
  hero_image_alt: string
  published_at: string | null
  tags: Array<{ id: number; name: string; slug: string }>
}

type BlogListResponse = {
  count: number
  page: number
  page_size: number
  results: BlogPostCard[]
}

export function BlogListPage() {
  const [q, setQ] = useState('')
  const [query, setQuery] = useState('')
  const [tag, setTag] = useState('')
  const [page, setPage] = useState(1)
  const [pageSize] = useState(9)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [tags, setTags] = useState<BlogTag[]>([])
  const [payload, setPayload] = useState<BlogListResponse>({
    count: 0,
    page: 1,
    page_size: 9,
    results: [],
  })

  useEffect(() => {
    apiFetch<{ tags: BlogTag[] }>('/api/blog/tags/')
      .then((data) => setTags(data.tags))
      .catch(() => setTags([]))
  }, [])

  useEffect(() => {
    const params = new URLSearchParams({
      page: String(page),
      page_size: String(pageSize),
    })
    if (query) params.set('q', query)
    if (tag) params.set('tag', tag)

    setLoading(true)
    setError('')
    apiFetch<BlogListResponse>(`/api/blog/posts/?${params.toString()}`)
      .then((data) => setPayload(data))
      .catch((err) => setError((err as Error).message))
      .finally(() => setLoading(false))
  }, [query, tag, page, pageSize])

  const onSearch = (event: FormEvent) => {
    event.preventDefault()
    setPage(1)
    setQuery(q.trim())
  }

  return (
    <section className="page-stack layout-flow-compact">
      <SeoHead
        title="وبلاگ | 36 Cowork"
        description="مقالات، راهنماها و تجربه‌های کاری برای رشد فردی و تیمی در ۳۶ کووورک."
        canonicalUrl={`${window.location.origin}/blog/`}
        jsonLd={{
          '@context': 'https://schema.org',
          '@type': 'Blog',
          name: '36 Cowork Blog',
          inLanguage: 'fa-IR',
          url: `${window.location.origin}/blog/`,
        }}
      />

      <header className="surface-open section-head">
        <p className="eyebrow">وبلاگ</p>
        <h2>محتوای تخصصی برای رشد حرفه‌ای</h2>
      </header>

      <form className="surface-inline blog-filter-row" onSubmit={onSearch}>
        <input value={q} onChange={(event) => setQ(event.target.value)} placeholder="جستجوی مقاله..." />
        <select
          value={tag}
          onChange={(event) => {
            setPage(1)
            setTag(event.target.value)
          }}
        >
          <option value="">همه برچسب‌ها</option>
          {tags.map((item) => (
            <option key={item.id} value={item.slug}>
              {item.name} ({item.post_count})
            </option>
          ))}
        </select>
        <button className="btn-primary" type="submit">
          جستجو
        </button>
      </form>

      {error ? <p className="error">{error}</p> : null}
      {loading ? <p>در حال بارگذاری...</p> : null}

      {!loading && payload.results.length === 0 ? (
        <EmptyState title="مقاله‌ای پیدا نشد" description="فیلترها را تغییر دهید یا بعدا دوباره بررسی کنید." />
      ) : null}

      <div className="blog-grid">
        {payload.results.map((post) => (
          <article className="surface-inline blog-card" key={post.id}>
            {post.hero_image_url ? (
              <img src={post.hero_image_url} alt={post.hero_image_alt || post.title} className="blog-card-image" loading="lazy" />
            ) : null}
            <h3>{post.title}</h3>
            <p>{post.excerpt}</p>
            <div className="row chips-wrap">
              {post.tags.map((item) => (
                <TagChip key={item.id} label={item.name} />
              ))}
            </div>
            <Link to={`/blog/${post.slug}/`} className="btn-secondary">
              مطالعه
            </Link>
          </article>
        ))}
      </div>

      <Pagination page={page} pageSize={payload.page_size} total={payload.count} onChange={setPage} />
    </section>
  )
}
