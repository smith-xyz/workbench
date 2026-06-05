import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

// Start MSW in development
async function enableMocking() {
  const shouldMock = import.meta.env.VITE_ENABLE_MOCKING === 'true' || import.meta.env.DEV
  
  if (shouldMock) {
    const { worker } = await import('./mocks/browser')
    
    // Start the worker with quiet mode to reduce console noise
    return worker.start({
      onUnhandledRequest: 'warn'
    })
  }
  
  return Promise.resolve()
}

enableMocking().then(() => {
  createRoot(document.getElementById('root')!).render(
    <StrictMode>
      <App />
    </StrictMode>,
  )
})
