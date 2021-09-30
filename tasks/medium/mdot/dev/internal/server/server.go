package server

import (
	"errors"
	"fmt"
	"log"
	"net"
	"os"
	"time"

	"sabantuy.ctf/mdot/pkg/protocol"
)

type Server struct {
	logger  *log.Logger
	Timeout time.Duration
	Domain  string
	Flag    string
	Files   []string
}

func generateListing(files map[string]string) string {
	result := ""
	for filepath := range files {
		result += fmt.Sprintf("- [%s](%s)", filepath, filepath)
	}
	return result
}

func (s *Server) readRequest(conn *net.TCPConn) (*protocol.Request, error) {
	request, err := protocol.ReadRequest(conn)
	if err != nil {
		return nil, err
	}
	s.logger.Printf("[%v] Request: %v", conn.RemoteAddr().String(), request)
	return request, nil
}

func (s *Server) sendResponse(conn *net.TCPConn, resp *protocol.Response) error {
	s.logger.Printf("[%v] Response: %v", conn.RemoteAddr().String(), resp)
	return protocol.WriteResponse(conn, resp)
}

func (s *Server) handleConnection(conn *net.TCPConn) {
	defer func() {
		if err := recover(); err != nil {
			s.logger.Printf("[%v] Recovered from panic: %v", conn.RemoteAddr().String(), err)
		}
	}()
	s.logger.Printf("[%v] Connected", conn.RemoteAddr().String())

	// Handle requests, respect the timeout
	session := InitializeSession(s)
	conn.SetDeadline(time.Now().Add(s.Timeout))
	for {
		var response *protocol.Response
		request, err := s.readRequest(conn)
		if err != nil {
			s.logger.Printf("[%v] Error during request reading: %v", conn.RemoteAddr().String(), err)
			response = &protocol.Response{
				Status:  protocol.StatusBadRequest,
				Content: "# Error  \n**Invalid request**",
			}
		} else {
			response = session.handleRequest(request)
		}
		if err = s.sendResponse(conn, response); err != nil {
			s.logger.Printf("[%v] Error during response writing: %v", conn.RemoteAddr().String(), err)
			break
		}
	}
}

func (s *Server) ListenAndServe(address string) error {
	// Check that we have been properly initialized
	if s.Flag == "" {
		return errors.New("Unable to start server without flag")
	}
	if s.Domain == "" {
		return errors.New("Domain name must be set up for server")
	}
	if s.Files == nil {
		return errors.New("Unable to start server without files")
	}

	// Launch listener
	listen_address, err := net.ResolveTCPAddr("tcp", address)
	if err != nil {
		return err
	}
	listener, err := net.ListenTCP("tcp", listen_address)
	if err != nil {
		return err
	}

	// Poll for connections, handle them, recover from panics
	s.logger = log.New(os.Stdout, "MDOT", log.LstdFlags)
	for {
		conn, err := listener.AcceptTCP()
		if err != nil {
			s.logger.Println("Error during accepting connection: ", err)
			continue
		}
		go s.handleConnection(conn)
	}
}
