package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"int-db-token/model"
	"net/http"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type Request struct {
	Id     int64  `json:"id"`
	Worker int64  `json:"worker"`
	Nonce  string `json:"nonce"`
}

var requests = map[int64]map[int64]Request{}
var lastId int64 = 0
var secret, _ = os.ReadFile("../../../id_rsa")

func getConnection() *mongo.Client {
	uri := os.Getenv("MONGO_URI")
	if uri == "" {
		uri = "mongodb://root:example@localhost:27017"
	}

	client, err := mongo.Connect(context.TODO(), options.Client().ApplyURI(uri))
	if err != nil {
		fmt.Println(err)
	}
	return client
}

var connection = getConnection()
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

	opts := options.FindOne().SetSort(bson.M{"$natural": -1})
	t := connection.Database("benchmarks").Collection("tokens").FindOne(ctx, bson.M{"key": token}, opts)
	obj := model.Token{}
	err := t.Decode(&obj)

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
