import pkg from "../../package.json";

export function version(): void {
  console.log(`__SERVICE__ v${pkg.version}`);
}
