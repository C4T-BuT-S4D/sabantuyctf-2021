package main

import (
	"fmt"
	"os"
	"strings"

	"sabantuy.ctf/mdot/pkg/client"
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
	client.Write("kek", "lol")
	resp, _ := client.Read("/")
	files := strings.Split(resp.Content, "\n")
	fmt.Println(files)
	for _, file := range files {
		fNameStart := len("- [")
		if len(file) < fNameStart {
			continue
		}
		fNameEnd := strings.Index(file[fNameStart:], "]") + fNameStart
		filename := file[fNameStart:fNameEnd]
		resp, _ := client.Read(filename)
		fmt.Println(resp)
	}
}
