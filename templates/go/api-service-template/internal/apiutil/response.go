package apiutil

import (
	"encoding/json"
	"errors"
	"log/slog"
	"net/http"

	"github.com/__ORG__/__SERVICE__/internal/apierr"
)

type Helper struct {
	Debug bool
}

type ErrorBody struct {
	Error string `json:"error"`
	Code  string `json:"code,omitempty"`
}

func (h *Helper) JSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	if v != nil {
		_ = json.NewEncoder(w).Encode(v)
	}
}

func (h *Helper) Error(w http.ResponseWriter, status int, err error) {
	if err != nil {
		slog.Error("handler error", "err", err)
	}
	msg := http.StatusText(status)
	if h.Debug && err != nil {
		msg = err.Error()
	}
	h.JSON(w, status, ErrorBody{Error: msg})
}

func (h *Helper) Err(w http.ResponseWriter, err error) {
	var apiErr *apierr.Error
	if errors.As(err, &apiErr) {
		msg := apiErr.Message
		if h.Debug && apiErr.Err != nil {
			msg = apiErr.Error()
		}
		slog.Error("handler error", "code", apiErr.Code, "err", err)
		h.JSON(w, apiErr.Status, ErrorBody{Error: msg, Code: apiErr.Code})
		return
	}
	h.Error(w, http.StatusInternalServerError, err)
}
