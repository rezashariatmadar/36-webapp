import React from 'react';
import { createRoot } from 'react-dom/client';

import './islands.css';

import { initReactBitsIslands } from './islands';

if (typeof window !== 'undefined') {
  window.React = window.React || React;
  window.ReactDOM = window.ReactDOM || { createRoot };
}

const HTMX_SELECTOR = '[hx-get], [hx-post], [hx-put], [hx-patch], [hx-delete]';

const processHtmx = (scope = document.body) => {
  if (!window.htmx || typeof window.htmx.process !== 'function') {
    return false;
  }
  window.htmx.process(scope);
  return true;
};

const countUnprocessedHtmxElements = (scope = document) => {
  const nodes = scope.querySelectorAll(HTMX_SELECTOR);
  let unprocessed = 0;
  nodes.forEach(node => {
    if (!node['htmx-internal-data']) {
      unprocessed += 1;
    }
  });
  return unprocessed;
};

const ensureHtmxProcessed = ({ scope = document.body, retries = 12, delayMs = 50 } = {}) => {
  let attempt = 0;

  const tick = () => {
    const didProcess = processHtmx(scope);
    if (!didProcess) {
      if (attempt < retries) {
        attempt += 1;
        window.setTimeout(tick, delayMs);
      }
      return;
    }

    if (countUnprocessedHtmxElements(document) > 0 && attempt < retries) {
      attempt += 1;
      window.setTimeout(tick, delayMs);
    }
  };

  tick();
};

const mount = () => {
  initReactBitsIslands(document);
  ensureHtmxProcessed();
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', mount, { once: true });
} else {
  mount();
}

window.setTimeout(mount, 0);
window.addEventListener('load', () => {
  mount();
  window.setTimeout(mount, 0);
}, { once: true });

document.addEventListener('htmx:afterSwap', event => {
  const target = event?.detail?.target || document;
  initReactBitsIslands(target);
  ensureHtmxProcessed();
});

window.ReactBitsIslands = {
  mount: initReactBitsIslands
};
