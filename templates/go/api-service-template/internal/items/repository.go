package items

import (
	"context"
	"fmt"

	"gorm.io/gorm"

	storedb "github.com/__ORG__/__SERVICE__/internal/store/db"
)

type Repository struct {
	db *gorm.DB
}

func NewRepository(db *gorm.DB) *Repository {
	return &Repository{db: db}
}

func (r *Repository) List(ctx context.Context) ([]storedb.Item, error) {
	var items []storedb.Item
	if err := r.db.WithContext(ctx).Order("created_at DESC").Find(&items).Error; err != nil {
		return nil, fmt.Errorf("list items: %w", err)
	}
	return items, nil
}

func (r *Repository) GetByID(ctx context.Context, id uint) (*storedb.Item, error) {
	var item storedb.Item
	if err := r.db.WithContext(ctx).First(&item, id).Error; err != nil {
		return nil, fmt.Errorf("get item %d: %w", id, err)
	}
	return &item, nil
}

func (r *Repository) Create(ctx context.Context, item *storedb.Item) error {
	if err := r.db.WithContext(ctx).Create(item).Error; err != nil {
		return fmt.Errorf("create item: %w", err)
	}
	return nil
}
