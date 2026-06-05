package v1

import (
	"net/http"

	"github.com/__ORG__/__SERVICE__/internal/apiutil"
	"github.com/__ORG__/__SERVICE__/internal/health"
)

type HealthResponse struct {
	Status string `json:"status"`
}

func Health(resp *apiutil.Helper) http.HandlerFunc {
	return func(w http.ResponseWriter, _ *http.Request) {
		resp.JSON(w, http.StatusOK, HealthResponse{Status: "ok"})
	}
}

type ReadyResponse struct {
	Status string            `json:"status"`
	Checks map[string]string `json:"checks,omitempty"`
}

func Ready(checks []health.Checker, resp *apiutil.Helper) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		result := ReadyResponse{Status: "ok", Checks: make(map[string]string)}
		status := http.StatusOK

		for i, c := range checks {
			name := "check"
			if n, ok := c.(interface{ Name() string }); ok {
				name = n.Name()
			} else {
				name = http.StatusText(i)
			}
			if err := c.Health(r.Context()); err != nil {
				result.Status = "degraded"
				result.Checks[name] = err.Error()
				status = http.StatusServiceUnavailable
			} else {
				result.Checks[name] = "ok"
			}
		}

		resp.JSON(w, status, result)
	}
}
