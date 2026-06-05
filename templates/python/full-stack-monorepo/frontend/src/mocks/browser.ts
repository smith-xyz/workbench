import { setupWorker } from 'msw/browser'
import { handlers } from './handlers'

// Setup the service worker with our handlers
export const worker = setupWorker(...handlers)
