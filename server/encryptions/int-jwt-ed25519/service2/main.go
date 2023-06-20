package main

import (
	"bytes"
	"crypto/ed25519"
	"crypto/x509"
	"encoding/json"
	"encoding/pem"
	"io/ioutil"
	"net/http"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)

type Request struct {
	Id     int64  `json:"id"`
	Worker int64  `json:"worker"`
	Nonce  string `json:"nonce"`
}

var requests = map[int64]map[int64]Request{}
var lastId int64 = 0
var secret, _ = os.ReadFile("../../../id_rsa")

func getPublicKey() ed25519.PublicKey {
	file, _ := ioutil.ReadFile("../../../id_rsa.pub")

	block, _ := pem.Decode(file)
	public, _ := x509.ParsePKIXPublicKey(block.Bytes)

	key := public.(ed25519.PublicKey)

	return key
}

var public = getPublicKey()

func verifyToken(token string) bool {
	claims := jwt.MapClaims{}
	_, err := jwt.ParseWithClaims(token, claims, func(token *jwt.Token) (interface{}, error) {
		return public, nil
	})

	if err != nil {
		return false
	}

	return true
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

	if verifyToken(token) == false {
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
