import { http, HttpResponse } from 'msw'
import type { User } from '../components'

// Mock data
const mockUsers = [
  { id: 1, email: 'john.doe@example.com', name: 'John Doe', is_active: true },
  { id: 2, email: 'jane.smith@example.com', name: 'Jane Smith', is_active: true },
  { id: 3, email: 'bob.johnson@example.com', name: 'Bob Johnson', is_active: false },
]

export const handlers = [
  // Core status endpoint
  http.get('/api/core/status', () => {
    return HttpResponse.json({
      engine: {
        status: 'running',
        config: { version: '2.0.0', mode: 'development' },
        version: '1.2.3'
      },
      processor: {
        processor_type: 'async',
        config: { workers: 4, queue_size: 100 },
        status: 'ready'
      }
    })
  }),

  // Core process endpoint
  http.post('/api/core/process', async () => {
    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 500))
    
    return HttpResponse.json({
      status: 'completed',
      result: {
        processed_id: 1,
        timestamp: new Date().toISOString(),
        message: 'Processing completed successfully'
      }
    })
  }),

  // Users endpoints
  http.get('/api/users/', () => {
    return HttpResponse.json(mockUsers)
  }),

  http.post('/api/users/', async ({ request }) => {
    const newUser = await request.json() as User
    const user = {
      ...newUser,
    }
    mockUsers.push(user)
    
    return HttpResponse.json(user, { status: 201 })
  }),

  http.delete('/api/users/:id', ({ params }) => {
    const userId = parseInt(params.id as string)
    const userIndex = mockUsers.findIndex(user => user.id === userId)
    
    if (userIndex === -1) {
      return HttpResponse.json(
        { error: 'User not found' },
        { status: 404 }
      )
    }
    
    mockUsers.splice(userIndex, 1)
    return HttpResponse.json({ message: 'User deleted successfully' })
  }),

  // Catch-all for unhandled requests
  http.all('*', ({ request }) => {
    console.warn(`Unhandled ${request.method} request to ${request.url}`)
    return HttpResponse.json(
      { error: 'Endpoint not found' },
      { status: 404 }
    )
  })
]
