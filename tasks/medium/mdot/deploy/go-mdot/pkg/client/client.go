package client

import (
	"net"
	"time"

	"sabantuy.ctf/mdot/pkg/protocol"
)

type Client struct {
	conn   net.Conn
	Domain string
}

func (c *Client) Connect(address string) error {
	var err error
	tcpaddr, err := net.ResolveTCPAddr("tcp", address)
	if err != nil {
		return err
	}
	c.conn, err = net.DialTCP("tcp", nil, tcpaddr)
	return err
}

func (c *Client) requestResponse(req *protocol.Request) (*protocol.Response, error) {
	if err := protocol.WriteRequest(c.conn, req); err != nil {
		return nil, err
	}
	c.conn.SetReadDeadline(time.Now().Add(time.Second * 5))
	resp, err := protocol.ReadResponse(c.conn)
	c.conn.SetReadDeadline(time.Time{})
	if err != nil {
		return nil, err
	}
	return resp, err
}

func (c *Client) Read(path string) (*protocol.Response, error) {
	req := &protocol.Request{
		Version: protocol.Version,
		Domain:  c.Domain,
		Method:  protocol.MethodRead,
		Path:    path,
		Content: "",
	}
	return c.requestResponse(req)
}

func (c *Client) Write(path, value string) (*protocol.Response, error) {
	req := &protocol.Request{
		Version: protocol.Version,
		Domain:  c.Domain,
		Method:  protocol.MethodWrite,
		Path:    path,
		Content: value,
	}
	return c.requestResponse(req)
}
