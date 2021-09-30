package server

import (
	"fmt"

	"sabantuy.ctf/mdot/internal/util"
	"sabantuy.ctf/mdot/pkg/protocol"
)

type Session struct {
	server   *Server
	verified bool
	// Randomly place files for each session
	files   map[string]string
	listing string
}

func InitializeSession(s *Server) *Session {
	session := &Session{verified: false, server: s, files: make(map[string]string)}
	for _, file := range s.Files {
		session.files[util.GenerateID()] = file
	}
	session.files[util.GenerateID()] = s.Flag
	session.listing = generateListing(session.files)
	return session
}

func (sess *Session) handleRequest(req *protocol.Request) *protocol.Response {
	if req.Domain != sess.server.Domain {
		return &protocol.Response{
			Status: protocol.StatusBadRequest,
			Content: fmt.Sprintf("# Error  \n**Unable to handle requested domain %v on domain %v**",
				req.Domain,
				sess.server.Domain),
		}
	}
	if req.Version != protocol.Version {
		return &protocol.Response{
			Status:  protocol.StatusBadRequest,
			Content: "# Error  \n**Unsupported protocol version**",
		}
	}

	// Amazing anti-bot heuristic - user must post at least one file to get verified (access to other files)
	switch req.Method {
	case protocol.MethodWrite:
		// Meh, don't really write anything doe...
		if sess.verified {
			return &protocol.Response{
				Status:  protocol.StatusOK,
				Content: "# Success  \nThank you for sharing!",
			}
		} else {
			sess.verified = true
			return &protocol.Response{
				Status:  protocol.StatusOK,
				Content: "# Success  \nThank you for sharing! You are now verified and authorized to read files.",
			}
		}
	case protocol.MethodRead:
		if req.Path == "/" {
			return &protocol.Response{
				Status:  protocol.StatusOK,
				Content: sess.listing,
			}
		} else if !sess.verified {
			return &protocol.Response{
				Status:  protocol.StatusUnauthorized,
				Content: "# Error  \n**Session unverified, please verify**",
			}
		} else if file, ok := sess.files[req.Path]; ok {
			return &protocol.Response{
				Status:  protocol.StatusOK,
				Content: file,
			}
		} else {
			return &protocol.Response{
				Status:  protocol.StatusNotFound,
				Content: "# Error  \n**File not found**",
			}
		}
	default:
		return &protocol.Response{
			Status:  protocol.StatusInternalError,
			Content: "# Error  \n**Unrecognized method**",
		}
	}
}
