package migrations

import (
	"gorm.io/gorm"

	"github.com/__ORG__/__SERVICE__/internal/store/db"
)

func init() { db.Register(&InitialSchema{}) }

type InitialSchema struct{}

func (InitialSchema) Version() db.MigrationVersion {
	return db.NewVersion(2025, 1, 1, 1, "initial_schema")
}

func (InitialSchema) Up(tx *gorm.DB) error {
	return tx.AutoMigrate(&db.Item{})
}

func (InitialSchema) Down(tx *gorm.DB) error {
	return tx.Migrator().DropTable("items")
}
