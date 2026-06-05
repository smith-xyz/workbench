package db

import (
	"errors"
	"fmt"
	"log/slog"
	"os"
	"sort"
	"time"

	"gorm.io/gorm"
)

type MigrationVersion struct {
	year  int
	month int
	day   int
	seq   int
	name  string
	str   string
}

func NewVersion(year, month, day, seq int, name string) MigrationVersion {
	if name == "" {
		panic("migration version: name is required")
	}
	return MigrationVersion{
		year: year, month: month, day: day, seq: seq, name: name,
		str: fmt.Sprintf("%04d%02d%02d_%03d_%s", year, month, day, seq, name),
	}
}

func (v MigrationVersion) String() string { return v.str }

type Migration interface {
	Version() MigrationVersion
	Up(tx *gorm.DB) error
	Down(tx *gorm.DB) error
}

type SchemaMigration struct {
	Version   string    `gorm:"column:version;primaryKey"`
	AppliedAt time.Time `gorm:"column:applied_at;autoCreateTime"`
}

type MigrationLock struct {
	ID       int       `gorm:"column:id;primaryKey"`
	LockedBy string    `gorm:"column:locked_by;not null"`
	LockedAt time.Time `gorm:"column:locked_at;not null"`
}

type MigrationStatus struct {
	Version   string
	Name      string
	Applied   bool
	AppliedAt time.Time
}

var (
	ErrMigrationLocked = errors.New("migration is already running (locked by another process)")
	lockStaleDuration  = 10 * time.Minute
)

func (db *DB) Migrate() error {
	if err := db.ensureTables(); err != nil {
		return err
	}
	if err := db.acquireLock(); err != nil {
		return err
	}
	defer db.releaseLock()

	applied, err := db.appliedVersions()
	if err != nil {
		return err
	}

	for _, m := range sortedMigrations() {
		v := m.Version().String()
		if applied[v] {
			continue
		}
		slog.Info("applying migration", "version", v)
		if err := db.conn.Transaction(func(tx *gorm.DB) error {
			if err := m.Up(tx); err != nil {
				return err
			}
			return tx.Create(&SchemaMigration{Version: v}).Error
		}); err != nil {
			return fmt.Errorf("migration %s: %w", v, err)
		}
		slog.Info("applied migration", "version", v)
	}

	return nil
}

func (db *DB) Rollback() error {
	if err := db.ensureTables(); err != nil {
		return err
	}
	if err := db.acquireLock(); err != nil {
		return err
	}
	defer db.releaseLock()

	var last SchemaMigration
	if err := db.conn.Order("version DESC").First(&last).Error; err != nil {
		return fmt.Errorf("no migrations to rollback: %w", err)
	}

	for _, m := range sortedMigrations() {
		v := m.Version().String()
		if v != last.Version {
			continue
		}
		slog.Info("rolling back migration", "version", v)
		if err := db.conn.Transaction(func(tx *gorm.DB) error {
			if err := m.Down(tx); err != nil {
				return err
			}
			return tx.Where("version = ?", v).Delete(&SchemaMigration{}).Error
		}); err != nil {
			return fmt.Errorf("rollback %s: %w", v, err)
		}
		slog.Info("rolled back migration", "version", v)
		return nil
	}

	return fmt.Errorf("migration %s not found in registry", last.Version)
}

func (db *DB) MigrationStatus() ([]MigrationStatus, error) {
	if err := db.ensureTables(); err != nil {
		return nil, err
	}

	var rows []SchemaMigration
	if err := db.conn.Order("version").Find(&rows).Error; err != nil {
		return nil, fmt.Errorf("read applied migrations: %w", err)
	}
	appliedMap := make(map[string]time.Time, len(rows))
	for _, r := range rows {
		appliedMap[r.Version] = r.AppliedAt
	}

	sorted := sortedMigrations()
	statuses := make([]MigrationStatus, 0, len(sorted))
	for _, m := range sorted {
		v := m.Version().String()
		s := MigrationStatus{Version: v, Name: m.Version().name}
		if at, ok := appliedMap[v]; ok {
			s.Applied = true
			s.AppliedAt = at
		}
		statuses = append(statuses, s)
	}

	return statuses, nil
}

func (db *DB) ensureTables() error {
	if err := db.conn.AutoMigrate(&SchemaMigration{}, &MigrationLock{}); err != nil {
		return fmt.Errorf("ensure migration tables: %w", err)
	}
	return nil
}

func (db *DB) acquireLock() error {
	hostname, _ := os.Hostname()
	if hostname == "" {
		hostname = "unknown"
	}
	lockedBy := fmt.Sprintf("%s (pid %d)", hostname, os.Getpid())
	now := time.Now()

	if err := db.conn.Where("locked_at < ?", now.Add(-lockStaleDuration)).Delete(&MigrationLock{}).Error; err != nil {
		return fmt.Errorf("clear stale migration locks: %w", err)
	}

	lock := MigrationLock{ID: 1, LockedBy: lockedBy, LockedAt: now}
	result := db.conn.Create(&lock)
	if result.Error != nil {
		var existing MigrationLock
		db.conn.First(&existing, 1)
		return fmt.Errorf("%w: held by %q since %s",
			ErrMigrationLocked, existing.LockedBy, existing.LockedAt.Format(time.RFC3339))
	}
	return nil
}

func (db *DB) releaseLock() {
	db.conn.Delete(&MigrationLock{}, 1)
}

func (db *DB) appliedVersions() (map[string]bool, error) {
	var rows []SchemaMigration
	if err := db.conn.Order("version").Find(&rows).Error; err != nil {
		return nil, fmt.Errorf("read applied migrations: %w", err)
	}
	applied := make(map[string]bool, len(rows))
	for _, r := range rows {
		applied[r.Version] = true
	}
	return applied, nil
}

var registry []Migration

func Register(m Migration) {
	v := m.Version().String()
	for _, existing := range registry {
		if existing.Version().String() == v {
			panic(fmt.Sprintf("duplicate migration version: %s", v))
		}
	}
	registry = append(registry, m)
}

func sortedMigrations() []Migration {
	sorted := make([]Migration, len(registry))
	copy(sorted, registry)
	sort.Slice(sorted, func(i, j int) bool {
		return sorted[i].Version().String() < sorted[j].Version().String()
	})
	return sorted
}
