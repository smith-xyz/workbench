package db

import (
	"bytes"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"
	"text/template"
	"time"
	"unicode"
)

var validMigrationName = regexp.MustCompile(`^[a-z][a-z0-9_]*$`)

const migrationTemplate = `package migrations

import (
	"gorm.io/gorm"

	"github.com/__ORG__/__SERVICE__/internal/store/db"
)

func init() { db.Register(&{{.Struct}}{}) }

type {{.Struct}} struct{}

func ({{.Struct}}) Version() db.MigrationVersion {
	return db.NewVersion({{.Year}}, {{.Month}}, {{.Day}}, {{.Seq}}, "{{.Name}}")
}

func ({{.Struct}}) Up(tx *gorm.DB) error {
	// TODO: implement migration
	return nil
}

func ({{.Struct}}) Down(tx *gorm.DB) error {
	// TODO: implement rollback
	return nil
}
`

var migrationTmpl = template.Must(template.New("migration").Parse(migrationTemplate))

type migrationData struct {
	Struct string
	Year   int
	Month  int
	Day    int
	Seq    int
	Name   string
}

func CreateMigration(name string) error {
	name = strings.ToLower(strings.TrimSpace(name))
	if !validMigrationName.MatchString(name) {
		return fmt.Errorf("migration name must be lowercase alphanumeric with underscores (got %q)", name)
	}

	now := time.Now()
	datePrefix := fmt.Sprintf("%04d%02d%02d", now.Year(), now.Month(), now.Day())
	seq := 1

	migrationsDir := migrationsPath()
	entries, _ := os.ReadDir(migrationsDir)
	for _, e := range entries {
		if strings.HasPrefix(e.Name(), datePrefix+"_") {
			seq++
		}
	}

	filename := fmt.Sprintf("%s_%03d_%s.go", datePrefix, seq, name)
	path := filepath.Join(migrationsDir, filename)

	var buf bytes.Buffer
	if err := migrationTmpl.Execute(&buf, migrationData{
		Struct: snakeToPascal(name),
		Year:   now.Year(),
		Month:  int(now.Month()),
		Day:    now.Day(),
		Seq:    seq,
		Name:   name,
	}); err != nil {
		return fmt.Errorf("render template: %w", err)
	}

	if err := os.WriteFile(path, buf.Bytes(), 0o644); err != nil {
		return fmt.Errorf("write migration file: %w", err)
	}

	fmt.Printf("created %s\n", path)
	return nil
}

func migrationsPath() string {
	_, thisFile, _, ok := runtime.Caller(0)
	if !ok {
		return filepath.Join("internal", "store", "db", "migrations")
	}
	return filepath.Join(filepath.Dir(thisFile), "migrations")
}

func snakeToPascal(s string) string {
	var b strings.Builder
	upper := true
	for _, c := range s {
		if c == '_' {
			upper = true
			continue
		}
		if upper {
			b.WriteRune(unicode.ToUpper(c))
			upper = false
		} else {
			b.WriteRune(c)
		}
	}
	return b.String()
}
