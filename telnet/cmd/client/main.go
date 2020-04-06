package main

import (
	"flag"
	"fmt"
	"io"
	"log"
	"net"
	"time"
)

var (
	flServer = flag.String("s", "127.0.0.1:8080", "Server address")
)

func main() {
	from1 := time.Now()
	conn, err := net.Dial("tcp", *flServer)
	if err != nil {
		log.Fatalln(err)
	}
	d1 := time.Since(from1)

	buf := make([]byte, 1024*1024)

	from2 := time.Now()
	conn.Write([]byte{0x00, 0x01, 0x02, 0x03})
	io.ReadFull(conn, buf[0:4])
	d2 := time.Since(from2)

	from3 := time.Now()
	io.ReadFull(conn, buf)
	d3 := time.Since(from3)

	fmt.Println(d1.Milliseconds(), d2.Milliseconds(), d3.Milliseconds())
}
