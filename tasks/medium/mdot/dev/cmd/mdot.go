package main

import (
	"os"
	"time"

	"sabantuy.ctf/mdot/internal/server"
)

func main() {
	server := &server.Server{
		Flag:    os.Getenv("FLAG"),
		Domain:  "sabantuy.ctf/mdot",
		Timeout: time.Second * 30,
		Files:   []string{},
	}
}
