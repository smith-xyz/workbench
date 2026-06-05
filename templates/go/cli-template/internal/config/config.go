package config

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/spf13/viper"
)

type Config struct {
	Verbose bool   `mapstructure:"verbose"`
	LogFile string `mapstructure:"log_file"`
}

func Load(cfgFile string) error {
	if cfgFile != "" {
		viper.SetConfigFile(cfgFile)
	} else {
		home, err := os.UserHomeDir()
		if err != nil {
			return fmt.Errorf("find home dir: %w", err)
		}
		viper.AddConfigPath(home)
		viper.AddConfigPath(".")
		viper.SetConfigName(".__SERVICE__")
		viper.SetConfigType("yaml")
	}

	viper.SetEnvPrefix("__SERVICE_UPPER__")
	viper.AutomaticEnv()

	if err := viper.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); !ok {
			return fmt.Errorf("read config: %w", err)
		}
	}

	return nil
}

func Get() Config {
	var cfg Config
	_ = viper.Unmarshal(&cfg)
	return cfg
}

func Dir() string {
	home, _ := os.UserHomeDir()
	dir := filepath.Join(home, ".__SERVICE__")
	_ = os.MkdirAll(dir, 0o755)
	return dir
}
