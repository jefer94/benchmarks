package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
)

type Request struct {
	Id     int64 `json:"id"`
	Worker int64 `json:"worker"`
	Start  int64 `json:"start"`
	End    int64 `json:"end"`
}

var requests = map[string]*Request{}
var requestsMutex = sync.RWMutex{}
var lastId int64 = 0

func main() {
	x := api{requests: &requests}
	router := gin.New()
	router.Use(
		gin.Recovery(),
	)

	router.POST("/result", x.report)

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}

	env := os.Getenv("WORKERS")
	if env == "" {
		env = "10"
	}

	workers, _ := strconv.ParseInt(env, 10, 64)
	var n int64 = 0
	for n = 0; n < workers; n++ {
		go worker(n)
	}
	go result()
	router.Run("localhost:" + port)
}

func result() {
	time.Sleep(time.Second * 12)

	http.Get("http://localhost:3000/shutdown")
	http.Get("http://localhost:4000/shutdown")

	requestsMutex.Lock()
	howMany := len(requests)
	requestsMutex.Unlock()

	results := make([]int64, howMany)

	var n int64 = 0
	requestsMutex.Lock()
	for _, request := range requests {
		results[n] = request.End - request.Start
		n++
	}
	requestsMutex.Unlock()

	sort.Slice(results, func(i, j int) bool {
		return results[i] < results[j]
	})

	medianIndex := int(float64(howMany) / 2)
	median := results[medianIndex]
	min := results[0]
	max := results[howMany-1]

	var average int64 = 0

	for _, result := range results {
		average += result
	}

	average = average / int64(howMany)

	result := ""

	lines := []string{
		"",
		"Summary",
		"",
		"- Median was " + strconv.FormatInt(median, 10),
		"- Average was " + strconv.FormatInt(average, 10),
		"- Min was " + strconv.FormatInt(min, 10),
		"- Max was " + strconv.FormatInt(max, 10),
		"- About " + strconv.FormatInt(int64(howMany)/10, 10) + " requests per second",
		"",
		"",
	}

	result += strings.Join(lines, "\n")

	fmt.Println(result)

	f, _ := os.OpenFile("../../../results.md", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)

	defer f.Close()

	f.WriteString("## Encryption, internal HMAC-SHA256, external nothing\n" + result)

	os.Exit(0)
}

func worker(number int64) {
	requestsMutex.Lock()
	if requests == nil {
		requests = map[string]*Request{}
	}
	requestsMutex.Unlock()

	limit := time.Now().Add(time.Second * 10)
	for {
		lastId++
		now := time.Now()
		if now.After(limit) {
			break
		}

		x := map[string]int64{
			"id":     lastId,
			"worker": number,
		}
		postBody, _ := json.Marshal(x)
		responseBody := bytes.NewBuffer(postBody)
		start := time.Now().UnixMilli()
		http.Post("http://localhost:3000/", "application/json", responseBody)
		end := time.Now().UnixMilli()
		requestsMutex.Lock()
		key := strconv.FormatInt(number, 10) + "-" + strconv.FormatInt(lastId, 10)

		requests[key] = &Request{
			Id:     lastId,
			Worker: number,
			Start:  start,
			End:    end,
		}
		requestsMutex.Unlock()
	}
}

type api struct {
	requests *map[string]*Request
}

func (x *api) report(c *gin.Context) {
	var request Request

	if err := c.BindJSON(&request); err != nil {
		return
	}

	return
}
