# Animated Component Boundary

- Only files under `src/components/animated/` may import ReactBits packages directly.
- Pages and non-adapter components must consume animated components from this folder.
- Keep public adapter props vendor-agnostic.
- Prefer Framer Motion for baseline transitions; use vendor adapters for advanced effects.
