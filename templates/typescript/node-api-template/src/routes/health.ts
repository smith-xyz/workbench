import type { FastifyPluginAsync } from 'fastify';

export const healthRoutes: FastifyPluginAsync = async (app) => {
  app.get('/', async () => ({ status: 'ok' }));
  app.get('/ready', async () => ({ status: 'ready' }));
};
