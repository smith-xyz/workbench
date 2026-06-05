package apierr

import (
	"fmt"
	"net/http"
)

type Error struct {
	Status  int
	Code    string
	Message string
	Err     error
}

func (e *Error) Error() string {
	if e.Err != nil {
		return fmt.Sprintf("%s: %v", e.Message, e.Err)
	}
	return e.Message
}

func (e *Error) Unwrap() error { return e.Err }

func NotFound(resource, id string) *Error {
	return &Error{
		Status:  http.StatusNotFound,
		Code:    "not_found",
		Message: fmt.Sprintf("%s %q not found", resource, id),
	}
}

func Validation(msg string) *Error {
	return &Error{
		Status:  http.StatusUnprocessableEntity,
		Code:    "validation",
		Message: msg,
	}
}

func BadRequest(msg string) *Error {
	return &Error{
		Status:  http.StatusBadRequest,
		Code:    "bad_request",
		Message: msg,
	}
}

func Internal(err error) *Error {
	return &Error{
		Status:  http.StatusInternalServerError,
		Code:    "internal",
		Message: "internal server error",
		Err:     err,
	}
}
