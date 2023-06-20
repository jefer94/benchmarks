package main

import (
	"bytes"
	"crypto/ed25519"
	"crypto/x509"
	"encoding/hex"
	"encoding/json"
	"encoding/pem"
	"log"
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

// func getSignature(message []byte) []byte {
// 	hash := hmac.New(sha256.New, secret)
// 	hash.Write(message)

// 	return hash.Sum(nil)
// }

func getSignature(object interface{}) string {
	message, _ := json.Marshal(object)
	file := secret

	block, _ := pem.Decode(file)
	if block == nil || block.Type != "PRIVATE KEY" {
		log.Fatal("failed to decode PEM block containing public key")
	}

	private, err := x509.ParsePKCS8PrivateKey(block.Bytes)
	if err != nil {
		log.Fatal(err)
	}

	PrivateKey := private.(ed25519.PrivateKey)
	signature := ed25519.Sign(PrivateKey, message)
	encodedString := hex.EncodeToString(signature)

	return encodedString
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
	req.Header.Set("Signature", signature)
	client.Do(req)

	c.IndentedJSON(200, request)
}

func shutdown(c *gin.Context) {
	c.IndentedJSON(204, gin.H{})
	os.Exit(0)
}
