package db

import (
	"gorm.io/driver/postgres"
	"gorm.io/driver/sqlite"
)

func OpenPostgres(dsn string, pool PoolConfig) (*DB, error) {
	return newBuilder(postgres.Open, dsn).WithPoolConfig(pool).Build()
}

func OpenSQLite(dsn string) (*DB, error) {
	return newBuilder(sqlite.Open, dsn).Build()
}
