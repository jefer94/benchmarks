package main

import (
	"bytes"
	"crypto/ed25519"
	"crypto/x509"
	"encoding/json"
	"encoding/pem"
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"

	"github.com/golang-jwt/jwt/v5"

	"int-db-token/database"
	"int-db-token/model"
	"int-db-token/query"
)

type Request struct {
	Id     int64 `json:"id"`
	Worker int64 `json:"worker"`
}

var requests = map[int64]map[int64]Request{}
var lastId int64 = 0

var db = database.Init()

func getPrivateKey() ed25519.PrivateKey {
	file, _ := os.ReadFile("../../../id_rsa")

	block, _ := pem.Decode(file)
	private, _ := x509.ParsePKCS8PrivateKey(block.Bytes)
	privateKey := private.(ed25519.PrivateKey)
	return privateKey
}

var secret = getPrivateKey()

func seedToken() {
	g := jwt.NewWithClaims(jwt.SigningMethodEdDSA,
		jwt.MapClaims{
			"id":       2,
			"username": "john",
			"exp":      time.Now().Add(10 * time.Minute),
		})

	s, _ := g.SignedString(secret)

	u := query.User
	_, err := query.User.Unscoped().Where(u.Username.Eq("username")).Delete()
	if err != nil {
		fmt.Println("Error deleting users", err)
	}

	user := model.User{
		Username:  "username",
		Password:  "password",
		FirstName: "John",
		LastName:  "Doe",
		Email:     "jjj@jjj.jjj",
		Active:    true,
	}
	err = query.User.Create(&user)
	if err != nil {
		fmt.Println("Error creating user", err)
	}

	t := query.Token
	_, err = query.Token.Unscoped().Where(t.CreatedAt.Lte(time.Now())).Delete()
	if err != nil {
		fmt.Println("Error deleting tokens", err)
	}

	token := model.Token{
		User:      user,
		Key:       s,
		ExpiresAt: time.Now().Add(10 * time.Minute),
		TokenType: "login",
	}

	err = query.Token.Create(&token)
	if err != nil {
		fmt.Println("Error creating token", err)
	}
}

func main() {
	query.SetDefault(db)
	seedToken()

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

	u := query.Token
	token, _ := query.Token.Where(u.ExpiresAt.Gte(time.Now())).First()

	postBody, _ := json.Marshal(request)

	responseBody := bytes.NewBuffer(postBody)

	client := &http.Client{}
	req, _ := http.NewRequest("POST", "http://localhost:4000/", responseBody)
	req.Header.Set("Authorization", "Bearer "+token.Key)
	client.Do(req)

	c.IndentedJSON(200, request)
}

func shutdown(c *gin.Context) {
	c.IndentedJSON(204, gin.H{})
	os.Exit(0)
}
