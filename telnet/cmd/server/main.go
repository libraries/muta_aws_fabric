package main

import (
	"crypto/rand"
	"flag"
	"io"
	"log"
	"net"
)

var (
	flListen = flag.String("l", "127.0.0.1:8080", "Listen address")
)

func main() {
	l, err := net.Listen("tcp", *flListen)
	if err != nil {
		log.Fatalln(err)
	}
	for {
		conn, err := l.Accept()
		if err != nil {
			continue
		}
		go func() {
			if err := func() error {
				defer conn.Close()
				log.Println("Accept conn")
				buf := make([]byte, 1024*1024)
				io.ReadFull(conn, buf[0:4])
				conn.Write(buf[0:4])
				rand.Read(buf)
				conn.Write(buf)
				return nil
			}(); err != nil {
				log.Panicln(err)
			}
		}()
	}
}
