package middleware

import (
	"log/slog"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/go-chi/chi/v5/middleware"
)

var Global = []func(http.Handler) http.Handler{
	middleware.RequestID,
	middleware.RealIP,
	CORS,
	RequestLogger,
	middleware.Recoverer,
}

func CORS(next http.Handler) http.Handler {
	origin := os.Getenv("CORS_ALLOW_ORIGIN")
	if origin == "" {
		return next
	}
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", origin)
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Accept, Content-Type, Authorization")
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}
		next.ServeHTTP(w, r)
	})
}

func RequestLogger(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ww := middleware.NewWrapResponseWriter(w, r.ProtoMajor)
		start := time.Now()

		next.ServeHTTP(ww, r)

		slog.Info("request",
			"method", sanitize(r.Method),
			"path", sanitize(r.URL.Path),
			"status", ww.Status(),
			"bytes", ww.BytesWritten(),
			"latency", time.Since(start).Round(time.Microsecond),
			"request_id", sanitize(middleware.GetReqID(r.Context())),
		)
	})
}

func sanitize(s string) string {
	return strings.Map(func(r rune) rune {
		if r == '\n' || r == '\r' {
			return ' '
		}
		return r
	}, s)
}
