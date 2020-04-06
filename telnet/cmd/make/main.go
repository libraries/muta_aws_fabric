package main

import (
	"log"
	"os"
	"os/exec"
	"strings"
)

func call(name string, arg ...string) {
	log.Println("$", name, strings.Join(arg, " "))
	cmd := exec.Command(name, arg...)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	if err := cmd.Run(); err != nil {
		log.Panicln(err)
	}
}

func main() {
	os.MkdirAll("./bin", 0755)
	call("bash", "-c", "go build -o bin github.com/libraries/muta_aws_fabric/telnet/cmd/server")
	call("bash", "-c", "go build -o bin github.com/libraries/muta_aws_fabric/telnet/cmd/client")
}
