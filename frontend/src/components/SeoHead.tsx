import { useEffect } from 'react'

type SeoHeadProps = {
  title: string
  description?: string
  canonicalUrl?: string
  ogImage?: string
  jsonLd?: Record<string, unknown> | null
}

const upsertMeta = (name: string, content: string, attr: 'name' | 'property' = 'name') => {
  let meta = document.head.querySelector<HTMLMetaElement>(`meta[${attr}="${name}"]`)
  if (!meta) {
    meta = document.createElement('meta')
    meta.setAttribute(attr, name)
    document.head.appendChild(meta)
  }
  meta.setAttribute('content', content)
}

export function SeoHead({ title, description, canonicalUrl, ogImage, jsonLd }: SeoHeadProps) {
  useEffect(() => {
    const previousTitle = document.title
    document.title = title

    if (description) {
      upsertMeta('description', description)
      upsertMeta('og:description', description, 'property')
    }
    upsertMeta('og:title', title, 'property')
    if (ogImage) upsertMeta('og:image', ogImage, 'property')

    let canonicalElement: HTMLLinkElement | null = null
    if (canonicalUrl) {
      canonicalElement = document.head.querySelector<HTMLLinkElement>('link[rel="canonical"]')
      if (!canonicalElement) {
        canonicalElement = document.createElement('link')
        canonicalElement.setAttribute('rel', 'canonical')
        document.head.appendChild(canonicalElement)
      }
      canonicalElement.setAttribute('href', canonicalUrl)
    }

    let scriptElement: HTMLScriptElement | null = null
    if (jsonLd) {
      scriptElement = document.head.querySelector<HTMLScriptElement>('script[data-seo-jsonld="true"]')
      if (!scriptElement) {
        scriptElement = document.createElement('script')
        scriptElement.setAttribute('type', 'application/ld+json')
        scriptElement.dataset.seoJsonld = 'true'
        document.head.appendChild(scriptElement)
      }
      scriptElement.textContent = JSON.stringify(jsonLd)
    }

    return () => {
      document.title = previousTitle
      if (canonicalElement && canonicalElement.getAttribute('href') === canonicalUrl) {
        canonicalElement.remove()
      }
      if (scriptElement) {
        scriptElement.remove()
      }
    }
  }, [title, description, canonicalUrl, ogImage, jsonLd])

  return null
}

