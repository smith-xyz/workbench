package items

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/go-chi/chi/v5"

	"github.com/__ORG__/__SERVICE__/internal/apierr"
	"github.com/__ORG__/__SERVICE__/internal/apiutil"
)

type Handler struct {
	svc  *Service
	resp *apiutil.Helper
}

func NewHandler(svc *Service, resp *apiutil.Helper) *Handler {
	return &Handler{svc: svc, resp: resp}
}

func (h *Handler) Mount(r chi.Router) {
	r.Get("/", h.List)
	r.Get("/{id}", h.Get)
	r.Post("/", h.Create)
}

func (h *Handler) List(w http.ResponseWriter, r *http.Request) {
	items, err := h.svc.List(r.Context())
	if err != nil {
		h.resp.Err(w, apierr.Internal(err))
		return
	}
	h.resp.JSON(w, http.StatusOK, items)
}

func (h *Handler) Get(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.ParseUint(chi.URLParam(r, "id"), 10, 64)
	if err != nil {
		h.resp.Err(w, apierr.BadRequest("invalid id"))
		return
	}
	item, err := h.svc.Get(r.Context(), uint(id))
	if err != nil {
		h.resp.Err(w, apierr.NotFound("item", chi.URLParam(r, "id")))
		return
	}
	h.resp.JSON(w, http.StatusOK, item)
}

func (h *Handler) Create(w http.ResponseWriter, r *http.Request) {
	var req CreateItemRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		h.resp.Err(w, apierr.BadRequest("invalid request body"))
		return
	}
	if req.Name == "" {
		h.resp.Err(w, apierr.Validation("name is required"))
		return
	}
	item, err := h.svc.Create(r.Context(), req)
	if err != nil {
		h.resp.Err(w, apierr.Internal(err))
		return
	}
	h.resp.JSON(w, http.StatusCreated, item)
}
