package v1

import (
	"github.com/go-chi/chi/v5"

	"github.com/__ORG__/__SERVICE__/internal/apiutil"
	"github.com/__ORG__/__SERVICE__/internal/health"
	"github.com/__ORG__/__SERVICE__/internal/items"
)

const Prefix = "/api/v1"

func MountHealth(r chi.Router, resp *apiutil.Helper) {
	r.Get("/health", Health(resp))
}

func MountReady(r chi.Router, checks []health.Checker, resp *apiutil.Helper) {
	r.Get("/ready", Ready(checks, resp))
}

func MountItems(r chi.Router, h *items.Handler) {
	r.Route("/items", h.Mount)
}
