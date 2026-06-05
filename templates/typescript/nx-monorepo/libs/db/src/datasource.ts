import { DataSource } from 'typeorm';
import { ItemEntity } from './entities/item.entity.js';

export function createDataSource(url: string): DataSource {
  return new DataSource({
    type: 'postgres',
    url,
    entities: [ItemEntity],
    synchronize: false,
    logging: process.env['NODE_ENV'] === 'development',
  });
}
