import { useEffect, useMemo, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import GlareHover from '../components/GlareHover'
import { apiFetch } from '../lib/api/client'

type MenuItem = { id: number; name: string; description: string; price: number }
type MenuCategory = { id: number; name: string; items: MenuItem[] }
type CartItem = { item_id: number; quantity: number }
type CartPayload = { cart_count: number; items?: CartItem[] }

export function CafeMenuPage() {
  const [categories, setCategories] = useState<MenuCategory[]>([])
  const [cartCount, setCartCount] = useState(0)
  const [busyIds, setBusyIds] = useState<number[]>([])
  const [activeCategoryId, setActiveCategoryId] = useState<number | null>(null)
  const [itemQuantities, setItemQuantities] = useState<Record<number, number>>({})
  const [categoryOverflow, setCategoryOverflow] = useState(false)
  const [canScrollCategoriesPrev, setCanScrollCategoriesPrev] = useState(false)
  const [canScrollCategoriesNext, setCanScrollCategoriesNext] = useState(false)
  const [error, setError] = useState('')

  const categorySectionRefs = useRef<Record<number, HTMLElement | null>>({})
  const stickyWrapRef = useRef<HTMLDivElement | null>(null)
  const categoryScrollerRef = useRef<HTMLDivElement | null>(null)

  const totalItems = useMemo(() => categories.reduce((acc, cat) => acc + cat.items.length, 0), [categories])

  const syncQuantitiesFromCart = (cartData: CartPayload) => {
    const next: Record<number, number> = {}
    for (const line of cartData.items || []) {
      if (line.quantity > 0) next[line.item_id] = line.quantity
    }
    setItemQuantities(next)
  }

  const load = async () => {
    try {
      const [menuData, cartData] = await Promise.all([
        apiFetch<{ categories: MenuCategory[] }>('/api/cafe/menu/'),
        apiFetch<CartPayload>('/api/cafe/cart/'),
      ])
      setCategories(menuData.categories)
      setCartCount(cartData.cart_count || 0)
      syncQuantitiesFromCart(cartData)
      if (menuData.categories.length) {
        setActiveCategoryId((prev) => prev ?? menuData.categories[0].id)
      }
    } catch (err) {
      setError((err as Error).message)
    }
  }

  const changeQty = async (menuItemId: number, delta: 1 | -1) => {
    setBusyIds((prev) => [...prev, menuItemId])
    setError('')
    try {
      const cartData = await apiFetch<CartPayload>('/api/cafe/cart/items/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ menu_item_id: menuItemId, delta }),
      })
      setCartCount(cartData.cart_count || 0)

      if (Array.isArray(cartData.items)) {
        syncQuantitiesFromCart(cartData)
      } else {
        setItemQuantities((prev) => {
          const current = prev[menuItemId] || 0
          const nextQty = Math.max(0, current + delta)
          if (!nextQty) {
            const { [menuItemId]: _removed, ...rest } = prev
            return rest
          }
          return { ...prev, [menuItemId]: nextQty }
        })
      }
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setBusyIds((prev) => prev.filter((id) => id !== menuItemId))
    }
  }

  const jumpToCategory = (categoryId: number) => {
    const node = categorySectionRefs.current[categoryId]
    if (!node) return
    const stickyOffset = stickyWrapRef.current?.offsetHeight ?? 0
    const top = node.getBoundingClientRect().top + window.scrollY - stickyOffset - 20
    window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' })
    setActiveCategoryId(categoryId)
  }

  const scrollCategoryChips = (direction: 'prev' | 'next') => {
    const scroller = categoryScrollerRef.current
    if (!scroller) return
    const delta = direction === 'next' ? -260 : 260
    scroller.scrollBy({ left: delta, behavior: 'smooth' })
  }

  useEffect(() => {
    void load()
  }, [])

  useEffect(() => {
    if (!categories.length) return

    const observer = new IntersectionObserver(
      (entries) => {
        const visibleEntries = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)
        if (!visibleEntries.length) return
        const categoryId = Number((visibleEntries[0].target as HTMLElement).dataset.categoryId)
        if (Number.isNaN(categoryId)) return
        setActiveCategoryId(categoryId)
      },
      {
        root: null,
        rootMargin: '-30% 0px -55% 0px',
        threshold: [0.1, 0.25, 0.5, 0.75],
      },
    )

    for (const category of categories) {
      const node = categorySectionRefs.current[category.id]
      if (node) observer.observe(node)
    }

    return () => observer.disconnect()
  }, [categories])

  useEffect(() => {
    if (!categories.length) return

    const syncActiveCategory = () => {
      const stickyOffset = stickyWrapRef.current?.offsetHeight ?? 0
      const probeY = stickyOffset + 120
      let nearestId = categories[0]?.id ?? null
      let nearestDistance = Number.POSITIVE_INFINITY

      for (const category of categories) {
        const node = categorySectionRefs.current[category.id]
        if (!node) continue
        const distance = Math.abs(node.getBoundingClientRect().top - probeY)
        if (distance < nearestDistance) {
          nearestDistance = distance
          nearestId = category.id
        }
      }

      if (nearestId !== null) setActiveCategoryId(nearestId)
    }

    let rafId = 0
    const onScroll = () => {
      if (rafId) return
      rafId = window.requestAnimationFrame(() => {
        syncActiveCategory()
        rafId = 0
      })
    }

    window.addEventListener('scroll', onScroll, { passive: true })
    window.addEventListener('resize', onScroll)
    syncActiveCategory()

    return () => {
      window.removeEventListener('scroll', onScroll)
      window.removeEventListener('resize', onScroll)
      if (rafId) window.cancelAnimationFrame(rafId)
    }
  }, [categories])

  useEffect(() => {
    const scroller = categoryScrollerRef.current
    if (!scroller) return

    const syncCategoryScrollState = () => {
      const maxScroll = Math.max(0, scroller.scrollWidth - scroller.clientWidth)
      const current = Math.abs(scroller.scrollLeft)
      const hasOverflow = maxScroll > 8
      setCategoryOverflow(hasOverflow)
      setCanScrollCategoriesPrev(hasOverflow && current > 8)
      setCanScrollCategoriesNext(hasOverflow && current < maxScroll - 8)
    }

    syncCategoryScrollState()
    const onScroll = () => syncCategoryScrollState()
    const onWheel = (event: WheelEvent) => {
      if (!categoryOverflow) return
      if (Math.abs(event.deltaY) <= Math.abs(event.deltaX)) return
      event.preventDefault()
      scroller.scrollBy({ left: -event.deltaY, behavior: 'auto' })
    }
    scroller.addEventListener('scroll', onScroll, { passive: true })
    scroller.addEventListener('wheel', onWheel, { passive: false })
    window.addEventListener('resize', syncCategoryScrollState)

    return () => {
      scroller.removeEventListener('scroll', onScroll)
      scroller.removeEventListener('wheel', onWheel)
      window.removeEventListener('resize', syncCategoryScrollState)
    }
  }, [categories, categoryOverflow])

  return (
    <section className="page-stack layout-flow-compact">
      <div className="menu-sticky-wrap" ref={stickyWrapRef}>
        <div className="surface-glass menu-sticky-shell">
          <div className="menu-sticky-top">
            <div className="menu-sticky-meta">
              <p className="eyebrow">Cafe</p>
              <h2>منوی کافه</h2>
              <p>
                {categories.length} دسته‌بندی · {totalItems} آیتم فعال
              </p>
            </div>
            <Link className="btn-primary menu-cart-btn" to="/cafe/cart/">
              سبد خرید ({cartCount})
            </Link>
          </div>

          {categories.length ? (
            <div className={`menu-category-carousel ${categoryOverflow ? 'is-scrollable' : ''}`}>
              <button
                type="button"
                className="menu-category-nav menu-category-nav-next"
                onClick={() => scrollCategoryChips('next')}
                disabled={!canScrollCategoriesNext}
                aria-label="اسکرول به دسته‌بندی‌های بعدی"
              >
                ◀
              </button>

              <div className="menu-category-scroller" role="tablist" aria-label="دسته‌بندی‌های منو" ref={categoryScrollerRef}>
                {categories.map((category) => (
                  <button
                    key={category.id}
                    id={`menu-chip-${category.id}`}
                    role="tab"
                    type="button"
                    className={`menu-category-chip ${activeCategoryId === category.id ? 'is-active' : ''}`}
                    onClick={() => jumpToCategory(category.id)}
                    aria-selected={activeCategoryId === category.id}
                    aria-current={activeCategoryId === category.id ? 'true' : undefined}
                    aria-controls={`menu-category-${category.id}`}
                    aria-label={`رفتن به دسته ${category.name}`}
                  >
                    <span>{category.name}</span>
                    <small>{category.items.length}</small>
                  </button>
                ))}
              </div>

              <button
                type="button"
                className="menu-category-nav menu-category-nav-prev"
                onClick={() => scrollCategoryChips('prev')}
                disabled={!canScrollCategoriesPrev}
                aria-label="اسکرول به دسته‌بندی‌های قبلی"
              >
                ▶
              </button>
            </div>
          ) : (
            <p className="menu-category-empty muted">فعلا آیتم فعالی برای نمایش وجود ندارد.</p>
          )}
        </div>
      </div>

      {error ? <p className="error">{error}</p> : null}

      {categories.map((category) => (
        <article
          key={category.id}
          id={`menu-category-${category.id}`}
          data-category-id={category.id}
          className="surface-open menu-category-section"
          role="tabpanel"
          aria-labelledby={`menu-chip-${category.id}`}
          ref={(node) => {
            categorySectionRefs.current[category.id] = node
          }}
        >
          <header className="surface-inline menu-category-header">
            <h3>{category.name}</h3>
            <span>{category.items.length} آیتم</span>
          </header>
          <div className="menu-items-grid">
            {category.items.map((item) => (
              <GlareHover
                key={item.id}
                className="surface-glass menu-card menu-item-card"
                glareColor="#400080"
                glareOpacity={0.8}
                glareSize={500}
              >
                <div className="menu-item-media" aria-hidden>
                  <div className="menu-item-placeholder">تصویر آیتم</div>
                </div>
                <div className="menu-item-head">
                  <strong>{item.name}</strong>
                  <span>{item.price.toLocaleString()} تومان</span>
                </div>
                <p className="menu-item-description">{item.description || '\u00A0'}</p>
                <div className="row menu-item-actions">
                  {(itemQuantities[item.id] || 0) === 0 ? (
                    <button
                      className="btn-primary"
                      disabled={busyIds.includes(item.id)}
                      onClick={() => changeQty(item.id, 1)}
                      type="button"
                    >
                      {busyIds.includes(item.id) ? '...' : 'افزودن'}
                    </button>
                  ) : (
                    <div className="menu-qty-control">
                      <button
                        className="btn-secondary"
                        disabled={busyIds.includes(item.id)}
                        onClick={() => changeQty(item.id, -1)}
                        type="button"
                      >
                        {busyIds.includes(item.id) ? '...' : '-'}
                      </button>
                      <span className="menu-qty-value">{itemQuantities[item.id] || 0}</span>
                      <button
                        className="btn-primary"
                        disabled={busyIds.includes(item.id)}
                        onClick={() => changeQty(item.id, 1)}
                        type="button"
                      >
                        {busyIds.includes(item.id) ? '...' : '+'}
                      </button>
                    </div>
                  )}
                </div>
              </GlareHover>
            ))}
          </div>
        </article>
      ))}
    </section>
  )
}


