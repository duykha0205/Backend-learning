package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
)

type CDN struct {
	cache map[string][]byte
}

func NewCDN() *CDN {
	return &CDN{
		cache: make(map[string][]byte),
	}
}

func (c *CDN) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	url := r.URL.Path[1:]
	if content, ok := c.cache[url]; ok {
		// Serve from cache
		w.Write(content)
		fmt.Println("Served from cache:", url)
	} else {
		// Fetch from origin
		resp, err := http.Get(url)
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadGateway)
			return
		}
		defer resp.Body.Close()
		content, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		// Cache content
		c.cache[url] = content
		// Serve
		w.Write(content)
		fmt.Println("Served from origin:", url)
	}
}

func main() {
	cdn := NewCDN()
	http.ListenAndServe(":8080", cdn)
}
