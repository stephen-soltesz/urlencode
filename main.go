package main

import (
	"fmt"
	"net/url"

	flag "github.com/spf13/pflag"
)

var (
	prefix string
	value  string
)

func init() {
	flag.StringVar(&prefix, "prefix", "", "Prefix to append to value.")
	flag.StringVar(&value, "value", "", "Value to encode.")
}

func main() {
	flag.Parse()
	v := url.Values{}
	v.Set("", value)
	fmt.Printf("%s%s\n", prefix, v.Encode())
}
