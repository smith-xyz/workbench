package cmd

import (
	"context"
	"fmt"
	"os/signal"
	"syscall"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var runCmd = &cobra.Command{
	Use:   "run",
	Short: "Run the main process",
	RunE: func(cmd *cobra.Command, args []string) error {
		ctx, cancel := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
		defer cancel()

		if viper.GetBool("verbose") {
			fmt.Println("starting in verbose mode...")
		}

		fmt.Println("running... (ctrl+c to stop)")
		<-ctx.Done()
		fmt.Println("\nshutting down")
		return nil
	},
}

func init() {
	rootCmd.AddCommand(runCmd)
}
