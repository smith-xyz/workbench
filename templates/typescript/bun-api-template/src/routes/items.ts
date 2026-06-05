import { Hono } from 'hono';

interface Item {
  id: string;
  name: string;
  description: string | null;
}

const store = new Map<string, Item>();

export const itemsRoutes = new Hono();

itemsRoutes.get('/', (c) => {
  const items = [...store.values()];
  return c.json({ items, total: items.length });
});

itemsRoutes.get('/:id', (c) => {
  const item = store.get(c.req.param('id'));
  if (!item) return c.json({ error: 'not found' }, 404);
  return c.json(item);
});

itemsRoutes.post('/', async (c) => {
  const body = await c.req.json<{ name?: string; description?: string }>();
  if (!body.name) return c.json({ error: 'name required' }, 400);

  const item: Item = {
    id: crypto.randomUUID(),
    name: body.name,
    description: body.description ?? null,
  };
  store.set(item.id, item);
  return c.json(item, 201);
});

itemsRoutes.delete('/:id', (c) => {
  const deleted = store.delete(c.req.param('id'));
  if (!deleted) return c.json({ error: 'not found' }, 404);
  return c.body(null, 204);
});
