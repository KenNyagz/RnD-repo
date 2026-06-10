package main

import (
	"fmt"
	"sync"
	"time"
	"net/http"
	"io"
	"strings"
)

const allLetters = "abcdefghijklmnopqrstuvwxyz"

func CountLetters (url string, frequency []int, mutex *sync.Mutex) {
    resp, _ := http.Get(url)
    defer resp.Body.Close()
    if resp.StatusCode != 200 {
        panic("Error....")
    }
    body, _ := io.ReadAll(resp.Body)
    mutex.Lock()
    for _, b := range body {
        c := strings.ToLower(string (b))
        cIndex := strings.IndexByte(allLetters, c[0])
        if cIndex >= 0 {
             frequency[cIndex] += 1
        }
    }
    mutex.Unlock()
}

func main() {
     mutex := sync.Mutex{}
     var frequency = make([]int, 26)
     for i := 1000; i <= 1030; i++ {
         url := fmt.Sprintf("https://rfc-editor.org/rfc/rfc%d.txt", i)
         go CountLetters(url, frequency, &mutex)
     }
     time.Sleep(60 * time.Second)
     mutex.Lock()
     for i, c := range allLetters {
          fmt.Printf("%c-%d, ", c, frequency[i])
     }
     mutex.Unlock()
}
