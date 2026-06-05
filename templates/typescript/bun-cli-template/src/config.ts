import { existsSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

export interface Config {
  verbose: boolean;
  logLevel: string;
}

const defaults: Config = {
  verbose: false,
  logLevel: "info",
};

export function loadConfig(path?: string): Partial<Config> {
  const file = path ?? join(homedir(), ".__SERVICE__.json");
  if (!existsSync(file)) return {};
  return JSON.parse(Bun.file(file).textSync()) as Partial<Config>;
}

export interface CliOverrides {
  verbose?: boolean;
  logLevel?: string;
}

export function resolveConfig(fileConfig: Partial<Config>, cli: CliOverrides): Config {
  return {
    ...defaults,
    ...fileConfig,
    ...(cli.verbose !== undefined && { verbose: cli.verbose }),
    ...(cli.logLevel !== undefined && { logLevel: cli.logLevel }),
  };
}
