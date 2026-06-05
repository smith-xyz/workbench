package cmd

import (
	"fmt"

	"github.com/spf13/cobra"

	"github.com/__ORG__/__SERVICE__/internal/version"
)

var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "Print version information",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println(version.Info())
	},
}

func init() {
	rootCmd.AddCommand(versionCmd)
}
