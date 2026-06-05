import { describe, expect, test } from "bun:test";
import { resolveConfig } from "../src/config.js";

describe("resolveConfig", () => {
  test("applies defaults when no overrides", () => {
    const cfg = resolveConfig({}, {});
    expect(cfg.verbose).toBe(false);
    expect(cfg.logLevel).toBe("info");
  });

  test("CLI overrides take precedence", () => {
    const cfg = resolveConfig({ logLevel: "warn" }, { logLevel: "debug", verbose: true });
    expect(cfg.logLevel).toBe("debug");
    expect(cfg.verbose).toBe(true);
  });

  test("file config overrides defaults", () => {
    const cfg = resolveConfig({ verbose: true }, {});
    expect(cfg.verbose).toBe(true);
  });
});
