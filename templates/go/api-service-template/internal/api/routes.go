package api

import (
	"net/http"

	"github.com/go-chi/chi/v5"

	"github.com/__ORG__/__SERVICE__/internal/api/middleware"
	v1 "github.com/__ORG__/__SERVICE__/internal/api/v1"
	"github.com/__ORG__/__SERVICE__/internal/apiutil"
	"github.com/__ORG__/__SERVICE__/internal/health"
	"github.com/__ORG__/__SERVICE__/internal/items"
)

type APIDeps struct {
	Items  *items.Handler
	Resp   *apiutil.Helper
	Checks []health.Checker
}

func Routes(d *APIDeps) http.Handler {
	r := chi.NewRouter()
	r.Use(middleware.Global...)
	r.Route(v1.Prefix, func(r chi.Router) {
		v1.MountHealth(r, d.Resp)
		v1.MountReady(r, d.Checks, d.Resp)
		if d.Items != nil {
			v1.MountItems(r, d.Items)
		}
	})
	return r
}
