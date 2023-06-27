package main

import (
	"bytes"
	"context"
	"crypto/ed25519"
	"crypto/x509"
	"encoding/json"
	"encoding/pem"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"

	"github.com/golang-jwt/jwt/v5"
	"github.com/redis/go-redis/v9"
)

type Request struct {
	Id     int64 `json:"id"`
	Worker int64 `json:"worker"`
}

var requests = map[int64]map[int64]Request{}
var lastId int64 = 0

func getDB() *redis.Client {
	return redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password set
		DB:       0,  // use default DB
	})
}

var db = getDB()
var ctx = context.Background()

func getPrivateKey() ed25519.PrivateKey {
	file, _ := os.ReadFile("../../../id_rsa")

	block, _ := pem.Decode(file)
	private, _ := x509.ParsePKCS8PrivateKey(block.Bytes)
	privateKey := private.(ed25519.PrivateKey)
	return privateKey
}

var secret = getPrivateKey()

func saveToken() string {
	g := jwt.NewWithClaims(jwt.SigningMethodEdDSA,
		jwt.MapClaims{
			"id":       2,
			"username": "john",
			"exp":      time.Now().Add(10 * time.Minute),
		})

	s, _ := g.SignedString(secret)

	db.Set(ctx, "token:1", s, 2*time.Minute)
	return s
}

func main() {
	saveToken()

	router := gin.New()
	router.Use(
		gin.Recovery(),
	)

	router.POST("/", endpoint)
	router.GET("/shutdown", shutdown)

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}

	router.Run("localhost:" + port)
}

func endpoint(c *gin.Context) {
	var request Request

	if err := c.BindJSON(&request); err != nil {
		return
	}

	token, err := db.Get(ctx, "token:1").Result()

	// renew token
	if err != nil {
		token = saveToken()
	}

	postBody, _ := json.Marshal(request)

	responseBody := bytes.NewBuffer(postBody)

	client := &http.Client{}
	req, _ := http.NewRequest("POST", "http://localhost:4000/", responseBody)
	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("User", "1")
	client.Do(req)

	c.IndentedJSON(200, request)
}

func shutdown(c *gin.Context) {
	c.IndentedJSON(204, gin.H{})
	os.Exit(0)
}
