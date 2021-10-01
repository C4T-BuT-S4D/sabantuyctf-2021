package main

import (
	"fmt"
	"math/rand"
	"os"
	"time"

	"sabantuy.ctf/mdot/internal/server"
)

func main() {
	uniqueFiles := []string{
		"Could you please sign this petition?  \n- [ ] Yes  \n- [ ] No",
		"## M-m-markdown over tcp! - a short guide  \n**WIP**",
		"# My hopefully private note  \nJust kidding!",
		"## An opinion (idk if popular or unpopular)  \n**Coke** > *Pepsi*",
		"# Monday   \n Hi to everyone who reads this... Today I woke up in a strange cell with only a computer in it, instead of my house. I'm afraid. The PC had this mdot this open, so I hope someone will see this and help..",
		"# Thursday  \nHow did I end up in this forgotten place? I don't remember where I came from... I hope someone will read these notes and help me...",
		"## Awesome sauce recipe  \nIngredients:\n- Awesome mood\n- Cool friends\n- Fun times",
		"Markdown is a lightweight markup language for creating formatted text using a plain-text editor.",
		"### Ducks  \nDuckeroos are quite cute. Love me some good duckies.",
		"## Cheapo Shack  \nHenlo fren, this is da cheap shaq. If you see somn cheap, you can buy it for cheep.  \nItems:\n- Amogus\n- Sussy baka\n- Kola\n- Pitza",
	}

	files := []string{}
	for i := 0; i < 200; i++ {
		files = append(files, uniqueFiles[rand.Intn(len(uniqueFiles))])
		files = append(files, fmt.Sprintf("Test message #%d", rand.Int()))
	}

	server := &server.Server{
		Flag:    os.Getenv("FLAG"),
		Domain:  "sabantuy.ctf/mdot",
		Timeout: time.Second * 30,
		Files:   files,
	}
	port, ok := os.LookupEnv("PORT")
	if !ok {
		port = "4020"
	}
	if err := server.ListenAndServe(":" + port); err != nil {
		fmt.Println("Failed to serve mdot: ", err)
	}
}
