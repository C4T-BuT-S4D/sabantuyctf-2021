package protocol

import (
	"encoding/gob"
	"io"
)

type Response struct {
	Status  uint
	Content string
}

func ReadResponse(conn io.Reader) (*Response, error) {
	decoder := gob.NewDecoder(conn)
	result := new(Response)
	if err := decoder.Decode(result); err != nil {
		return nil, err
	}
	return result, nil
}

func WriteResponse(conn io.Writer, resp *Response) error {
	encoder := gob.NewEncoder(conn)
	return encoder.Encode(resp)
}
