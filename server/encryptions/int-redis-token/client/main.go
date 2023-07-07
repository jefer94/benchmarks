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
	"github.com/mackerelio/go-osstat/cpu"
	"github.com/mackerelio/go-osstat/memory"
)

type Request struct {
	Id       int64  `json:"id"`
	Worker   int64  `json:"worker"`
	Start    int64  `json:"start"`
	End      int64  `json:"end"`
	CpuStart uint64 `json:"cpuStart"`
	CpuEnd   uint64 `json:"cpuEnd"`
	Memory   uint64 `json:"memory"`
	Swap     uint64 `json:"swap"`
}

var requests = map[string]*Request{}
var requestsMutex = sync.RWMutex{}
var lastId int64 = 0

func main() {
	time.Sleep(time.Second * 5)
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

	durations := make([]int64, howMany)
	memory := make([]int64, howMany)
	swap := make([]int64, howMany)
	cpu := make([]uint64, howMany)

	var n int64 = 0
	requestsMutex.Lock()
	for _, request := range requests {
		durations[n] = request.End - request.Start
		memory[n] = int64(request.Memory)
		swap[n] = int64(request.Swap)
		cpu[n] = request.CpuEnd - request.CpuStart
		n++
	}
	requestsMutex.Unlock()

	sort.Slice(durations, func(i, j int) bool {
		return durations[i] < durations[j]
	})

	sort.Slice(memory, func(i, j int) bool {
		return memory[i] < memory[j]
	})

	sort.Slice(swap, func(i, j int) bool {
		return swap[i] < swap[j]
	})

	sort.Slice(cpu, func(i, j int) bool {
		return cpu[i] < cpu[j]
	})

	medianIndex := int(float64(howMany) / 2)

	msMedian := durations[medianIndex]
	msMin := durations[0]
	msMax := durations[howMany-1]

	memoryMedian := memory[medianIndex]
	memoryMin := memory[0]
	memoryMax := memory[howMany-1]

	swapMedian := swap[medianIndex]
	swapMin := swap[0]
	swapMax := swap[howMany-1]

	cpuMedian := cpu[medianIndex]
	cpuMin := cpu[0]
	cpuMax := cpu[howMany-1]

	var msAverage int64 = 0

	for _, result := range durations {
		msAverage += result
	}

	msAverage = msAverage / int64(howMany)

	var memoryAverage int64 = 0

	for _, result := range memory {
		memoryAverage += result
	}

	memoryAverage = memoryAverage / int64(howMany)

	var swapAverage int64 = 0

	for _, result := range swap {
		swapAverage += result
	}

	swapAverage = swapAverage / int64(howMany)

	var cpuAverage uint64 = 0

	for _, result := range cpu {
		cpuAverage += result
	}

	cpuAverage = cpuAverage / uint64(howMany)

	result := ""

	memoryDelta := memoryMax - memoryMin
	lines := []string{
		"",
		"Responses",
		"",
		"- Median was " + strconv.FormatInt(msMedian, 10) + "ms",
		"- Average was " + strconv.FormatInt(msAverage, 10) + "ms",
		"- Min was " + strconv.FormatInt(msMin, 10) + "ms",
		"- Max was " + strconv.FormatInt(msMax, 10) + "ms",
		"- About " + strconv.FormatInt(int64(howMany)/10, 10) + " requests per second",
		"",
		"CPU (based in amount of cycles waited)",
		"",
		"- Median was " + strconv.FormatInt(int64(cpuMedian), 10) + "Hz",
		"- Average was " + strconv.FormatInt(int64(cpuAverage), 10) + "Hz",
		"- Min was " + strconv.FormatInt(int64(cpuMin), 10) + "Hz",
		"- Max was " + strconv.FormatInt(int64(cpuMax), 10) + "Hz",
		"",
		"RAM",
		"",
		"- Median was " + strconv.FormatInt(memoryMedian/1024/1024, 10) + "MB",
		"- Average was " + strconv.FormatInt(memoryAverage/1024/1024, 10) + "MB",
		"- Min was " + strconv.FormatInt(memoryMin/1024/1024, 10) + "MB",
		"- Max was " + strconv.FormatInt(memoryMax/1024/1024, 10) + "MB",
		"- Delta was " + strconv.FormatInt(memoryDelta/1024/1024, 10) + "MB",
		"- About " + strconv.FormatFloat(float64((float64(memoryDelta)/1024/1024)/(float64(howMany)/10)), 'f', 3, 64) + "MB per request",
		"",
		"SWAP",
		"",
		"- Median was " + strconv.FormatInt(swapMedian/1024/1024, 10) + "MB",
		"- Average was " + strconv.FormatInt(swapAverage/1024/1024, 10) + "MB",
		"- Min was " + strconv.FormatInt(swapMin/1024/1024, 10) + "MB",
		"- Max was " + strconv.FormatInt(swapMax/1024/1024, 10) + "MB",
		"",
		"",
	}

	result += strings.Join(lines, "\n")

	fmt.Println(result)

	f, _ := os.OpenFile("../../../results.md", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)

	defer f.Close()

	extra := ""
	if os.Getenv("REDIS_HOST") != "localhost" {
		extra = "(external)"
	}

	f.WriteString("## Encryption, JWT ED25519 saved in Redis Database " + extra + "\n" + result)

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
		before, _ := cpu.Get()

		start := time.Now().UnixMilli()
		response, err := http.Post("http://localhost:3000/", "application/json", responseBody)
		end := time.Now().UnixMilli()
		after, _ := cpu.Get()
		memory, _ := memory.Get()

		requestsMutex.Lock()
		key := strconv.FormatInt(number, 10) + "-" + strconv.FormatInt(lastId, 10)

		if err == nil && response.StatusCode == 200 {
			requests[key] = &Request{
				Id:       lastId,
				Worker:   number,
				Start:    start,
				End:      end,
				Memory:   memory.Used,
				Swap:     memory.SwapUsed,
				CpuStart: before.User,
				CpuEnd:   after.User,
			}
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
