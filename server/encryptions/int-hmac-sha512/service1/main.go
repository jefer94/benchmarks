package main

import (
	"bytes"
	"crypto/hmac"
	"crypto/sha512"
	"encoding/hex"
	"encoding/json"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
)

type Request struct {
	Id     int64  `json:"id"`
	Worker int64  `json:"worker"`
	Nonce  string `json:"nonce"`
}

var requests = map[int64]map[int64]Request{}
var lastId int64 = 0

var secret, _ = os.ReadFile("../../../id_rsa")

func getSignature(message []byte) []byte {
	hash := hmac.New(sha512.New, secret)
	hash.Write(message)

	return hash.Sum(nil)
}

func main() {
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

	request.Nonce = time.Now().Format(time.RFC3339)

	postBody, _ := json.Marshal(request)
	signature := getSignature(postBody)

	responseBody := bytes.NewBuffer(postBody)

	client := &http.Client{}
	req, _ := http.NewRequest("POST", "http://localhost:4000/", responseBody)
	req.Header.Set("Signature", hex.EncodeToString(signature))
	client.Do(req)

	c.IndentedJSON(200, request)
}

func shutdown(c *gin.Context) {
	c.IndentedJSON(204, gin.H{})
	os.Exit(0)
}
