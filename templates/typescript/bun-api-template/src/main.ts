import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { healthRoutes } from './routes/health.js';
import { itemsRoutes } from './routes/items.js';

const app = new Hono();

app.use('*', logger());
app.use('*', cors());

app.route('/health', healthRoutes);
app.route('/api/v1/items', itemsRoutes);

const port = Number(process.env['PORT'] ?? 3000);

export default {
  port,
  fetch: app.fetch,
};

console.log(`__SERVICE__ listening on :${port}`);
