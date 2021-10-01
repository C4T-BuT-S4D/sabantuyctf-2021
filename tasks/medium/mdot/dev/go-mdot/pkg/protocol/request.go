package protocol

import (
	"encoding/gob"
	"io"
)

type Request struct {
	Version uint16
	Domain  string
	Method  bool
	Path    string
	Content string
}

func ReadRequest(conn io.Reader) (*Request, error) {
	decoder := gob.NewDecoder(conn)
	result := new(Request)
	if err := decoder.Decode(result); err != nil {
		return nil, err
	}
	return result, nil
}

func WriteRequest(conn io.Writer, req *Request) error {
	encoder := gob.NewEncoder(conn)
	return encoder.Encode(req)
}
