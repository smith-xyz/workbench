import type { Config } from "../config.js";

export async function runCommand(config: Config): Promise<void> {
  if (config.verbose) {
    console.log("Config:", JSON.stringify(config, null, 2));
  }
  console.log("Running...");

  const ac = new AbortController();
  process.on("SIGINT", () => ac.abort());
  process.on("SIGTERM", () => ac.abort());

  try {
    await new Promise((_, reject) => {
      ac.signal.addEventListener("abort", () => reject(new Error("aborted")));
    });
  } catch {
    console.log("Shutting down");
  }
}
