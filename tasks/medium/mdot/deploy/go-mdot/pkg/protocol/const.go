package protocol

const (
	MethodRead  = false
	MethodWrite = true
)

const (
	StatusOK = iota
	StatusBadRequest
	StatusNotFound
	StatusUnauthorized
	StatusInternalError
)

const Version = 69
