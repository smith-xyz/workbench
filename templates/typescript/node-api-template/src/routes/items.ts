import type { FastifyPluginAsync } from 'fastify';

interface Item {
  id: string;
  name: string;
  description: string | null;
}

const store = new Map<string, Item>();

export const itemsRoutes: FastifyPluginAsync = async (app) => {
  app.get('/', async () => {
    const items = [...store.values()];
    return { items, total: items.length };
  });

  app.get<{ Params: { id: string } }>('/:id', async (req, reply) => {
    const item = store.get(req.params.id);
    if (!item) return reply.status(404).send({ error: 'not found' });
    return item;
  });

  app.post<{ Body: { name?: string; description?: string } }>('/', async (req, reply) => {
    const { name, description } = req.body;
    if (!name) return reply.status(400).send({ error: 'name required' });

    const item: Item = {
      id: crypto.randomUUID(),
      name,
      description: description ?? null,
    };
    store.set(item.id, item);
    return reply.status(201).send(item);
  });

  app.delete<{ Params: { id: string } }>('/:id', async (req, reply) => {
    const deleted = store.delete(req.params.id);
    if (!deleted) return reply.status(404).send({ error: 'not found' });
    return reply.status(204).send();
  });
};
