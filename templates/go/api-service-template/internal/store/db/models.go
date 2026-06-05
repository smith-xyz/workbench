package db

import "time"

type Item struct {
	ID        uint      `gorm:"primaryKey"`
	Name      string    `gorm:"not null"`
	Status    string    `gorm:"default:active"`
	CreatedAt time.Time
	UpdatedAt time.Time
}
