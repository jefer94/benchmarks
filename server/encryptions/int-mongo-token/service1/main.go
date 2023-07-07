package main

import (
	"bytes"
	"context"
	"crypto/ed25519"
	"crypto/x509"
	"encoding/json"
	"encoding/pem"
	"fmt"
	"int-db-token/model"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"

	"github.com/golang-jwt/jwt/v5"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type Request struct {
	Id     int64 `json:"id"`
	Worker int64 `json:"worker"`
}

var requests = map[int64]map[int64]Request{}
var lastId int64 = 0

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

func getPrivateKey() ed25519.PrivateKey {
	file, _ := os.ReadFile("../../../id_rsa")

	block, _ := pem.Decode(file)
	private, _ := x509.ParsePKCS8PrivateKey(block.Bytes)
	privateKey := private.(ed25519.PrivateKey)
	return privateKey
}

var secret = getPrivateKey()

func saveToken() {
	g := jwt.NewWithClaims(jwt.SigningMethodEdDSA,
		jwt.MapClaims{
			"id":       2,
			"username": "john",
			"exp":      time.Now().Add(10 * time.Minute),
		})

	s, _ := g.SignedString(secret)

	users := connection.Database("benchmarks").Collection("users")
	tokens := connection.Database("benchmarks").Collection("tokens")

	u := model.User{

		Username:  "username",
		Password:  "password",
		FirstName: "John",
		LastName:  "Doe",
		Email:     "jjj@jjj.jjj",
		Active:    true,
	}

	users.DeleteMany(context.TODO(), bson.D{{}})
	xu, err := users.InsertOne(context.TODO(), &u)

	if err != nil {
		fmt.Println(err)
	}

	t := model.Token{
		UserID:    xu.InsertedID.(primitive.ObjectID),
		Key:       s,
		ExpiresAt: time.Now().Add(10 * time.Minute),
		TokenType: "login",
	}

	tokens.DeleteMany(context.TODO(), bson.D{{}})
	_, err = tokens.InsertOne(context.TODO(), &t)

	if err != nil {
		fmt.Println(err)
	}

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

	opts := options.FindOne().SetSort(bson.M{"$natural": -1})
	t := connection.Database("benchmarks").Collection("tokens").FindOne(ctx, bson.M{}, opts)
	token := model.Token{}
	t.Decode(&token)

	postBody, _ := json.Marshal(request)

	responseBody := bytes.NewBuffer(postBody)

	client := &http.Client{}
	req, _ := http.NewRequest("POST", "http://localhost:4000/", responseBody)
	req.Header.Set("Authorization", "Bearer "+token.Key)
	response, _ := client.Do(req)

	if response.StatusCode != 200 {
		fmt.Println("Client - Status code ", response.StatusCode)
	}

	c.IndentedJSON(200, request)
}

func shutdown(c *gin.Context) {
	c.IndentedJSON(204, gin.H{})
	os.Exit(0)
}
