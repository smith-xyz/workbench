package health

import (
	"encoding/json"
	"os"
	"path/filepath"
	"time"
)

type Writer struct {
	path string
}

type Status struct {
	Status    string  `json:"status"`
	Error     string  `json:"error,omitempty"`
	Timestamp float64 `json:"timestamp"`
}

func NewWriter(path string) *Writer {
	_ = os.MkdirAll(filepath.Dir(path), 0o755)
	return &Writer{path: path}
}

func (w *Writer) WriteOK() {
	w.write(Status{Status: "ok", Timestamp: nowUnix()})
}

func (w *Writer) WriteError(msg string) {
	w.write(Status{Status: "error", Error: msg, Timestamp: nowUnix()})
}

func (w *Writer) write(s Status) {
	data, _ := json.Marshal(s)
	tmp := w.path + ".tmp"
	if err := os.WriteFile(tmp, data, 0o644); err != nil {
		return
	}
	_ = os.Rename(tmp, w.path)
}

func nowUnix() float64 {
	return float64(time.Now().UnixMilli()) / 1000.0
}
