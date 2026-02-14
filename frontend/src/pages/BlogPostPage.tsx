import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { SeoHead } from '../components/SeoHead'
import { TagChip } from '../components/TagChip'
import { apiFetch } from '../lib/api/client'

type ContentBlock =
  | { type: 'paragraph'; text: string }
  | { type: 'heading'; text: string }
  | { type: 'quote'; text: string; author?: string }
  | { type: 'image'; url: string; alt?: string; caption?: string }
  | { type: 'list'; items: string[] }

type BlogPost = {
  id: number
  title: string
  slug: string
  excerpt: string
  hero_image_url: string | null
  hero_image_alt: string
  content_blocks: ContentBlock[]
  canonical_url?: string
  og_image_url?: string | null
  author_name?: string
  published_at?: string | null
  tags: Array<{ id: number; name: string; slug: string }>
}

type Payload = {
  post: BlogPost
  related: Array<{ id: number; title: string; slug: string }>
}

export function BlogPostPage() {
  const { slug } = useParams()
  const [payload, setPayload] = useState<Payload | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!slug) return
    setLoading(true)
    setError('')
    apiFetch<Payload>(`/api/blog/posts/${slug}/`)
      .then((data) => setPayload(data))
      .catch((err) => setError((err as Error).message))
      .finally(() => setLoading(false))
  }, [slug])

  const jsonLd = useMemo(() => {
    if (!payload?.post) return null
    return {
      '@context': 'https://schema.org',
      '@type': 'Article',
      headline: payload.post.title,
      description: payload.post.excerpt,
      inLanguage: 'fa-IR',
      datePublished: payload.post.published_at,
      image: payload.post.og_image_url || payload.post.hero_image_url || undefined,
      author: payload.post.author_name
        ? {
            '@type': 'Person',
            name: payload.post.author_name,
          }
        : undefined,
      mainEntityOfPage: payload.post.canonical_url || `${window.location.origin}/blog/${payload.post.slug}/`,
    }
  }, [payload])

  if (loading) return <p>در حال بارگذاری...</p>
  if (error) return <p className="error">{error}</p>
  if (!payload) return <p className="error">مقاله یافت نشد.</p>

  const { post } = payload
  return (
    <section className="page-stack">
      <SeoHead
        title={`${post.title} | 36 Cowork`}
        description={post.excerpt}
        canonicalUrl={post.canonical_url || `${window.location.origin}/blog/${post.slug}/`}
        ogImage={post.og_image_url || post.hero_image_url || undefined}
        jsonLd={jsonLd}
      />
      <article className="panel blog-post">
        <p className="eyebrow">وبلاگ</p>
        <h2>{post.title}</h2>
        <p>{post.excerpt}</p>
        {post.hero_image_url ? <img src={post.hero_image_url} alt={post.hero_image_alt || post.title} className="blog-hero-image" /> : null}
        <div className="row chips-wrap">
          {post.tags.map((tag) => (
            <TagChip key={tag.id} label={tag.name} />
          ))}
        </div>
        <div className="blog-content-blocks">
          {post.content_blocks.map((block, index) => {
            if (block.type === 'heading') return <h3 key={index}>{block.text}</h3>
            if (block.type === 'paragraph') return <p key={index}>{block.text}</p>
            if (block.type === 'quote') {
              return (
                <blockquote key={index}>
                  {block.text}
                  {block.author ? <cite>{block.author}</cite> : null}
                </blockquote>
              )
            }
            if (block.type === 'image') {
              return (
                <figure key={index} className="blog-inline-image">
                  <img src={block.url} alt={block.alt || post.title} loading="lazy" />
                  {block.caption ? <figcaption>{block.caption}</figcaption> : null}
                </figure>
              )
            }
            if (block.type === 'list') {
              return (
                <ul key={index}>
                  {block.items.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              )
            }
            return null
          })}
        </div>
      </article>

      {payload.related.length ? (
        <div className="panel">
          <h3>مطالب مرتبط</h3>
          <div className="blog-related-list">
            {payload.related.map((item) => (
              <Link key={item.id} to={`/blog/${item.slug}/`} className="nav-link">
                {item.title}
              </Link>
            ))}
          </div>
        </div>
      ) : null}
    </section>
  )
}

