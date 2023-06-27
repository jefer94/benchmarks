package main

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"
)

type Request struct {
	Id     int64  `json:"id"`
	Worker int64  `json:"worker"`
	Nonce  string `json:"nonce"`
}

var requests = map[int64]map[int64]Request{}
var lastId int64 = 0
var secret, _ = os.ReadFile("../../../id_rsa")

func getDB() *redis.Client {
	host := os.Getenv("REDIS_HOST")
	if host == "" {
		host = "localhost"
	}
	return redis.NewClient(&redis.Options{
		Addr:     host + ":6379",
		Password: "", // no password set
		DB:       0,  // use default DB
	})
}

var db = getDB()
var ctx = context.Background()

func main() {
	router := gin.New()
	router.Use(
		gin.Recovery(),
	)

	router.POST("/", endpoint)
	router.GET("/shutdown", shutdown)

	port := os.Getenv("PORT")
	if port == "" {
		port = "4000"
	}

	router.Run("localhost:" + port)
}

func endpoint(c *gin.Context) {
	var request Request

	if err := c.BindJSON(&request); err != nil {
		return
	}

	postBody, _ := json.Marshal(request)
	token := strings.Replace(c.Request.Header.Get("Authorization"), "Bearer ", "", 1)
	user := c.Request.Header.Get("User")

	t, err := db.Get(ctx, "token:"+user).Result()

	if err != nil {
		c.IndentedJSON(401, gin.H{})
		return
	}

	if t != token {
		c.IndentedJSON(401, gin.H{})
		return
	}

	responseBody := bytes.NewBuffer(postBody)
	http.Post("http://localhost:5000/result", "application/json", responseBody)

	c.IndentedJSON(200, request)
}

func shutdown(c *gin.Context) {
	c.IndentedJSON(204, gin.H{})
	os.Exit(0)
}
