import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { itemsRouter } from './routes/items.js';
import { healthRouter } from './routes/health.js';

const app = express();
const port = Number(process.env['PORT'] ?? 4000);

app.use(helmet());
app.use(cors());
app.use(express.json());

app.use('/health', healthRouter);
app.use('/api/v1/items', itemsRouter);

const server = app.listen(port, () => {
  console.log(`api listening on :${port}`);
});

process.on('SIGTERM', () => {
  server.close(() => process.exit(0));
});
