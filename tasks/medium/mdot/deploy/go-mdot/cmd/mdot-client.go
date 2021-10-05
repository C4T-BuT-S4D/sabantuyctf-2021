package main

import (
	"fmt"
	"os"
	"time"

	"sabantuy.ctf/mdot/pkg/client"
	"sabantuy.ctf/mdot/pkg/protocol"
)

func main() {
	if len(os.Args) < 3 {
		fmt.Printf("Usage: %s ip:port domain\n")
		return
	}

	client := &client.Client{Domain: os.Args[2]}

	fmt.Printf("Connecting to %s\n", os.Args[1])
	err := client.Connect(os.Args[1])
	if err != nil {
		fmt.Println("Failed to connect:", err)
		return
	}

	response, _ := client.Read("/")
	fmt.Println(response.Content)
	fmt.Print("Syntax: \n\tread /path\n\twrite /path value\n")
	for {
		var (
			verb, path, value string
			response          *protocol.Response = nil
			err               error              = nil
		)
		time.Sleep(time.Second)
		fmt.Scan(&verb, &path)
		switch verb {
		case "read":
			response, err = client.Read(path)
		case "write":
			fmt.Scan(&value)
			response, err = client.Write(path, value)
		default:
			fmt.Println("Invalid action:", verb)
			continue
		}
		if err != nil {
			fmt.Println("Error:", err)
			break
		}
		fmt.Printf("Status: %d\nContent:\n%s\n", response.Status, response.Content)
	}
}
