import { describe, expect, test } from 'bun:test';
import { parseArgs } from '../src/args.js';

describe('parseArgs', () => {
  test('parses command', () => {
    const result = parseArgs(['run']);
    expect(result.command).toBe('run');
  });

  test('parses flags', () => {
    const result = parseArgs(['run', '--verbose', '--config=/tmp/cfg.json']);
    expect(result.flags['verbose']).toBe(true);
    expect(result.flags['config']).toBe('/tmp/cfg.json');
  });

  test('parses positional args', () => {
    const result = parseArgs(['run', 'file.txt', 'other.txt']);
    expect(result.positional).toEqual(['file.txt', 'other.txt']);
  });
});
