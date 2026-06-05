package items

import (
	"context"

	storedb "github.com/__ORG__/__SERVICE__/internal/store/db"
)

type Service struct {
	repo *Repository
}

func NewService(repo *Repository) *Service {
	return &Service{repo: repo}
}

func (s *Service) List(ctx context.Context) ([]ItemResponse, error) {
	items, err := s.repo.List(ctx)
	if err != nil {
		return nil, err
	}
	resp := make([]ItemResponse, len(items))
	for i, item := range items {
		resp[i] = toResponse(item)
	}
	return resp, nil
}

func (s *Service) Get(ctx context.Context, id uint) (*ItemResponse, error) {
	item, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}
	r := toResponse(*item)
	return &r, nil
}

func (s *Service) Create(ctx context.Context, req CreateItemRequest) (*ItemResponse, error) {
	item := &storedb.Item{
		Name:   req.Name,
		Status: "active",
	}
	if err := s.repo.Create(ctx, item); err != nil {
		return nil, err
	}
	r := toResponse(*item)
	return &r, nil
}

func toResponse(item storedb.Item) ItemResponse {
	return ItemResponse{
		ID:     item.ID,
		Name:   item.Name,
		Status: item.Status,
	}
}
