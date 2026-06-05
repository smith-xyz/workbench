import { describe, expect, test } from 'bun:test';
import app from '../src/main.js';

const baseUrl = `http://localhost:${app.port}`;

describe('items API', () => {
  test('GET /api/v1/items returns empty', async () => {
    const res = await fetch(`${baseUrl}/api/v1/items`);
    const data = await res.json();
    expect(res.status).toBe(200);
    expect(data.items).toBeInstanceOf(Array);
  });

  test('POST /api/v1/items creates item', async () => {
    const res = await fetch(`${baseUrl}/api/v1/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'test', description: 'hello' }),
    });
    const data = await res.json();
    expect(res.status).toBe(201);
    expect(data.name).toBe('test');
    expect(data.id).toBeDefined();
  });

  test('POST /api/v1/items rejects missing name', async () => {
    const res = await fetch(`${baseUrl}/api/v1/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({}),
    });
    expect(res.status).toBe(400);
  });
});
