#!/usr/bin/env node
import { parseArgs } from "node:util";
import { loadConfig, resolveConfig } from "./config.js";
import { runCommand } from "./commands/run.js";
import pkg from "../package.json" with { type: "json" };

const { values } = parseArgs({
  args: process.argv.slice(2),
  options: {
    config: { type: "string", short: "c" },
    verbose: { type: "boolean", short: "v" },
    "log-level": { type: "string" },
    version: { type: "boolean", short: "V" },
    help: { type: "boolean", short: "h" },
  },
  strict: true,
  allowPositionals: true,
});

if (values.version) {
  console.log(`__SERVICE__ v${pkg.version}`);
  process.exit(0);
}

if (values.help) {
  console.log(`Usage: __SERVICE__ [options]

Options:
  -c, --config <path>    Config file (default: ~/.__SERVICE__.json)
  -v, --verbose          Enable verbose output
  --log-level <level>    Log level: debug, info, warn, error
  -V, --version          Show version
  -h, --help             Show this help`);
  process.exit(0);
}

const fileConfig = loadConfig(values.config);
const config = resolveConfig(fileConfig, {
  verbose: values.verbose,
  logLevel: values["log-level"],
});

await runCommand(config);
