package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"

	flag "github.com/spf13/pflag"
)

var (
	server string
	query  string
	label  string
)

type Result struct {
	Status    string                 `json:"status"`
	Data      map[string]interface{} `json:"data,omitempty"`
	ErrorType string                 `json:"errorType,omitempty"`
	Error     string                 `json:"error,omitempty"`
}

func init() {
	flag.StringVar(
		&server, "server", "status-mlab-oti.measurementlab.net:9090",
		"Run query against this Prometheus server.")
	flag.StringVar(&query, "query", "", "Value to encode.")
	flag.StringVar(&label, "label", "", "Label to extract from result.")
}

func main() {
	flag.Parse()
	v := url.Values{}
	v.Set("query", query)

	url := fmt.Sprintf("http://%s/api/v1/query?%s", server, v.Encode())
	fmt.Printf("Getting: %s\n", url)

	resp, err := http.Get(url)
	if err != nil {
		log.Fatal("Failed to download results: %v", err)
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal("Failed to download results: %v", err)
	}

	result := &Result{}
	err = json.Unmarshal(body, result)
	if err != nil {
		log.Fatal("Failed to parse result: %v", err)
	}

	// fmt.Printf("Body: %s\n", body)
	for _, metric := range result.Data["result"].([]interface{}) {
		// fmt.Printf("%d: %v\n", i, pretty.Sprint(metric))
		metric := metric.(map[string]interface{})
		values := metric["metric"].(map[string]interface{})
		for k, val := range values {
			if label == k {
				fmt.Println(val)
			}
		}
	}
}
