package main

import (
	"bytes"
	"encoding/json"
	"int-db-token/database"
	"int-db-token/query"
	"net/http"
	"os"
	"strings"
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

var db = database.Init()

func main() {
	query.SetDefault(db)

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

	u := query.Token
	_, err := query.Token.Where(u.Key.Eq(token), u.ExpiresAt.Gte(time.Now())).First()

	if err != nil {
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
