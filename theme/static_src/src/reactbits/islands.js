import React from 'react';
import { createRoot } from 'react-dom/client';
import { flushSync } from 'react-dom';

import GooeyNav from './components/GooeyNav';
import GlassIcons from './components/GlassIcons';
import PixelCard from './components/PixelCard';
import SpotlightCard from './components/SpotlightCard';
import Squares from './components/Squares';

const roots = new WeakMap();

const iconNode = (path, viewBox = '0 0 24 24') =>
  React.createElement(
    'svg',
    {
      viewBox,
      fill: 'none',
      xmlns: 'http://www.w3.org/2000/svg',
      'aria-hidden': 'true'
    },
    React.createElement('path', {
      d: path,
      stroke: 'currentColor',
      strokeWidth: '1.8',
      strokeLinecap: 'round',
      strokeLinejoin: 'round'
    })
  );

const ICONS = {
  menu: iconNode('M4 7h16M4 12h16M4 17h16'),
  cart: iconNode('M3 4h2l2.2 10.2a1 1 0 0 0 1 .8h8.6a1 1 0 0 0 1-.8L20 7H7M10 20a1 1 0 1 0 0 .01M17 20a1 1 0 1 0 0 .01'),
  desk: iconNode('M4 20V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12M4 14h16M9 10h.01M15 10h.01'),
  instagram: iconNode('M8 3h8a5 5 0 0 1 5 5v8a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5V8a5 5 0 0 1 5-5M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8M17.5 6.5h.01'),
  phone: iconNode('M5 4h3l1.5 4-2 1.5a15 15 0 0 0 6 6L15.5 13 19 14.5v3A2.5 2.5 0 0 1 16.5 20C9.6 20 4 14.4 4 7.5A2.5 2.5 0 0 1 6.5 5'),
  home: iconNode('M3 11 12 4l9 7M5 10v10h14V10')
};

function safeParseJSON(value, fallback) {
  if (!value) return fallback;
  try {
    return JSON.parse(value);
  } catch {
    return fallback;
  }
}

function safeParseInt(value, fallback = 0) {
  const parsed = parseInt(value, 10);
  return Number.isNaN(parsed) ? fallback : parsed;
}

function getRoot(node) {
  if (!roots.has(node)) {
    roots.set(node, createRoot(node));
  }
  return roots.get(node);
}

function renderIsland(root, element) {
  if (typeof flushSync === 'function') {
    flushSync(() => {
      root.render(element);
    });
    return;
  }

  root.render(element);
}

function mountSquares(node) {
  const root = getRoot(node);
  root.render(
    React.createElement(Squares, {
      direction: 'diagonal',
      speed: 0.4,
      borderColor: 'rgba(16, 3, 112, 0.35)',
      hoverFillColor: 'rgba(99, 2, 31, 0.2)',
      squareSize: 44,
      className: 'rb-squares-canvas'
    })
  );
}

function normalizeNavItems(rawItems) {
  const defaults = [
    { label: 'منو', href: '/cafe/menu/', icon: 'menu' },
    { label: 'سبد', href: '/cafe/cart/', icon: 'cart', badgeId: 'cart-badge-mobile' },
    { label: 'فضا', href: '/cowork/', icon: 'desk' }
  ];
  const source = Array.isArray(rawItems) && rawItems.length ? rawItems : defaults;
  return source.map(item => ({
    ...item,
    icon: ICONS[item.icon] || ICONS.home
  }));
}

function mountGooeyNav(node) {
  const rawItems = safeParseJSON(node.dataset.items, []);
  const cartCount = safeParseInt(node.dataset.cartCount, 0);
  const items = normalizeNavItems(rawItems).map(item =>
    item.badgeId
      ? {
          ...item,
          badgeValue: cartCount,
          badgeHidden: cartCount <= 0
        }
      : item
  );
  const activeIndex = safeParseInt(node.dataset.activeIndex, 0);
  const root = getRoot(node);
  root.render(React.createElement(GooeyNav, { items, activeIndex, className: 'rb-gooey-nav' }));
  node.classList.add('rb-mounted');
}

function normalizeGlassItems(rawItems) {
  const defaults = [
    { label: 'منو', href: '/cafe/menu/', color: 'blue', icon: 'menu' },
    { label: 'رزرو', href: '/cowork/', color: 'wine', icon: 'desk' },
    { label: 'اینستا', href: 'https://instagram.com/36.coworkingspace', color: 'blend', icon: 'instagram' },
    { label: 'تماس', href: 'tel:09001655040', color: 'blue', icon: 'phone' }
  ];
  const source = Array.isArray(rawItems) && rawItems.length ? rawItems : defaults;
  return source.map(item => ({
    ...item,
    icon: ICONS[item.icon] || ICONS.home,
    color: item.color || 'blend'
  }));
}

function mountGlassIcons(node) {
  const rawItems = safeParseJSON(node.dataset.items, []);
  const items = normalizeGlassItems(rawItems);
  const root = getRoot(node);
  root.render(React.createElement(GlassIcons, { items, className: 'rb-glass-icons' }));
}

function mountSpotlightCard(node) {
  if (!node.dataset.rbOriginalHtml) {
    node.dataset.rbOriginalHtml = node.innerHTML;
  }

  const originalHtml = node.dataset.rbOriginalHtml;
  const spotlightColor = node.dataset.spotlightColor || 'rgba(99, 2, 31, 0.32)';
  const root = getRoot(node);

  const element = (
    React.createElement(
      SpotlightCard,
      {
        className: 'rb-spotlight-shell',
        spotlightColor
      },
      React.createElement('div', {
        className: 'rb-island-content',
        dangerouslySetInnerHTML: { __html: originalHtml }
      })
    )
  );
  renderIsland(root, element);
}

function mountPixelCard(node) {
  if (!node.dataset.rbOriginalHtml) {
    node.dataset.rbOriginalHtml = node.innerHTML;
  }

  const originalHtml = node.dataset.rbOriginalHtml;
  const variant = node.dataset.variant || 'blue';
  const root = getRoot(node);

  const element = (
    React.createElement(
      PixelCard,
      {
        className: 'rb-pixel-shell',
        variant,
        noFocus: true
      },
      React.createElement('div', {
        className: 'rb-island-content',
        dangerouslySetInnerHTML: { __html: originalHtml }
      })
    )
  );
  renderIsland(root, element);
}

function parseGalleryItems(html) {
  if (!html) return [];
  const wrapper = document.createElement('div');
  wrapper.innerHTML = html;
  return Array.from(wrapper.querySelectorAll('img'))
    .map(img => ({
      src: img.getAttribute('src'),
      alt: img.getAttribute('alt') || ''
    }))
    .filter(item => item.src);
}

function mountPixelGallery(node) {
  if (!node.dataset.rbOriginalHtml) {
    node.dataset.rbOriginalHtml = node.innerHTML;
  }

  const items = parseGalleryItems(node.dataset.rbOriginalHtml);
  if (!items.length) return;

  const root = getRoot(node);
  root.render(
    React.createElement(
      'div',
      { className: 'rb-pixel-gallery' },
      items.map((item, index) =>
        React.createElement(
          PixelCard,
          {
            key: `${item.src}-${index}`,
            className: 'rb-pixel-shell rb-pixel-gallery__item',
            variant: index % 2 === 0 ? 'blue' : 'wine',
            noFocus: true
          },
          React.createElement('img', {
            src: item.src,
            alt: item.alt,
            className: 'rb-pixel-gallery__image',
            loading: 'lazy'
          })
        )
      )
    )
  );
}

const handlers = {
  'squares-bg': mountSquares,
  'gooey-nav': mountGooeyNav,
  'glass-icons': mountGlassIcons,
  'spotlight-card': mountSpotlightCard,
  'pixel-card': mountPixelCard,
  'pixel-gallery': mountPixelGallery
};

export function initReactBitsIslands(scope = document) {
  const nodes = scope.querySelectorAll('[data-rb-island]');
  nodes.forEach(node => {
    const key = node.dataset.rbIsland;
    const handler = handlers[key];
    if (!handler) return;
    try {
      handler(node);
    } catch (error) {
      console.error(`[ReactBits] Failed to mount ${key}`, error);
    }
  });
}
