package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"

	"github.com/__ORG__/__SERVICE__/internal/config"
)

var cfgFile string

var rootCmd = &cobra.Command{
	Use:   "__SERVICE__",
	Short: "A brief description of your CLI",
	PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
		return config.Load(cfgFile)
	},
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func init() {
	rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default $HOME/.__SERVICE__.yaml)")
	rootCmd.PersistentFlags().BoolP("verbose", "v", false, "verbose output")
	_ = viper.BindPFlag("verbose", rootCmd.PersistentFlags().Lookup("verbose"))
}
