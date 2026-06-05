# Go CLI Template

Production-ready CLI scaffold using Cobra and Viper.

## Architecture

```
main.go                → Entry point (just calls cmd.Execute)
cmd/
  root.go              → Root command, global flags, config init
  run.go               → Example long-running subcommand with signal handling
  version.go           → Version subcommand (ldflags-injected)
internal/
  config/              → Viper config loading (file + env + flags)
  version/             → Build-time version info
```

## Features

- Cobra subcommand structure — add commands by adding files in `cmd/`
- Viper config — YAML file (`~/.yourcli.yaml`), env vars (`YOURCLI_*`), flags all merged
- Version injection via ldflags at build time
- Signal handling pattern in the `run` subcommand
- Config precedence: flags > env > config file > defaults

## Quick Start

```bash
# Build with version info
make build

# Run directly
go run . run --verbose

# Print version
go run . version

# Install globally
make install
```

## Adding a Subcommand

Create `cmd/yourcommand.go`:

```go
package cmd

import "github.com/spf13/cobra"

var yourCmd = &cobra.Command{
    Use:   "yourcommand",
    Short: "Does something useful",
    RunE: func(cmd *cobra.Command, args []string) error {
        // your logic here
        return nil
    },
}

func init() {
    rootCmd.AddCommand(yourCmd)
}
```

## Config

Create `~/.yourcli.yaml` or pass `--config path/to/config.yaml`:

```yaml
verbose: true
log_file: /tmp/yourcli.log
```

Environment variables override config file values with `YOURCLI_` prefix:

```bash
YOURCLI_VERBOSE=true yourcli run
```
