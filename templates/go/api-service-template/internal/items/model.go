package items

type ItemResponse struct {
	ID     uint   `json:"id"`
	Name   string `json:"name"`
	Status string `json:"status"`
}

type CreateItemRequest struct {
	Name string `json:"name"`
}
