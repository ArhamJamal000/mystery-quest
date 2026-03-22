---
description: Best practices for React Native / Expo development including navigation, state management, and performance
---

# /react-native-patterns — React Native/Expo Guide

## Component Structure
Use functional components and typed props.

## State Management (Zustand)
Use `zustand` with `AsyncStorage` persistence for global state.

## Navigation (Expo Router)
Use file-based routing in `app/`. Avoid string-based navigation; use typed params.

## Performance
- `FlatList` for long lists
- Stable `keyExtractor`
- `React.memo`, `useCallback`, `useMemo` for optimization
- Avoid inline objects/arrays in JSX props

## Security
- Use `Expo SecureStore` for sensitive data
- Handle network errors and timeouts explicitly

## Pitfalls to Avoid
- [ ] `useEffect` missing dependencies
- [ ] Conditional hooks
- [ ] `console.log` in production
