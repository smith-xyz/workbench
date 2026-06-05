import { Router } from 'express';

export const itemsRouter = Router();

itemsRouter.get('/', (_req, res) => {
  res.json({ items: [], total: 0 });
});

itemsRouter.post('/', (req, res) => {
  const { name, description } = req.body as { name: string; description?: string };
  if (!name) {
    res.status(400).json({ error: 'name required' });
    return;
  }
  res.status(201).json({ id: crypto.randomUUID(), name, description: description ?? null });
});
