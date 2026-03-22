---
name: react-native-patterns
description: Best practices and patterns for React Native / Expo development including navigation, state management, performance, and native modules
---

# React Native & Expo Patterns

## Component Structure

Always use functional components with typed props:

```tsx
interface Props {
  title: string;
  onPress: () => void;
  disabled?: boolean;
}

const MyButton: React.FC<Props> = ({ title, onPress, disabled = false }) => {
  return (
    <TouchableOpacity onPress={onPress} disabled={disabled}>
      <Text>{title}</Text>
    </TouchableOpacity>
  );
};
```

## State Management (Zustand)

```ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface State {
  value: string;
  setValue: (v: string) => void;
}

export const useMyStore = create<State>()(
  persist(
    (set) => ({
      value: '',
      setValue: (v) => set({ value: v }),
    }),
    { name: 'my-store', storage: createJSONStorage(() => AsyncStorage) }
  )
);
```

## Navigation (Expo Router)

- Use file-based routing in `app/` directory
- Use `(tabs)` grouping for tab navigation
- Never use string-based navigation: always type route params
- Use `useLocalSearchParams()` to read params

## Performance Rules

- `FlatList` over `ScrollView` for lists > 20 items
- Always provide `keyExtractor` returning a stable unique string
- Memoize expensive components with `React.memo()`
- Use `useCallback` for handlers passed to child components
- Use `useMemo` for expensive computed values
- Never create objects/arrays inline in JSX props (causes re-renders)

## API Calls

```ts
// Always use try/catch and handle network errors explicitly
try {
  const response = await fetch(url, { signal: AbortSignal.timeout(10000) });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data = await response.json();
  return data;
} catch (err) {
  if (err instanceof Error && err.name === 'TimeoutError') {
    // Handle timeout separately
  }
  throw err;
}
```

## Notifications (Notifee)

- Always request permissions before scheduling
- Use `AndroidImportance.HIGH` for prayer/reminder alerts
- Store notification IDs in AsyncStorage to cancel later

## Common Pitfalls to Avoid

- ❌ `useEffect` with missing dependencies
- ❌ Calling hooks conditionally
- ❌ `console.log` in production (use a logger wrapper)
- ❌ Direct mutation of state objects
- ❌ Storing sensitive data in AsyncStorage (use SecureStore)
