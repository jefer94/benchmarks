package model

import (
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

type Token struct {
	ID        primitive.ObjectID `json:"id" bson:"_id"`
	TokenType string             `json:"tokenType" bson:"tokenType"`
	ExpiresAt time.Time          `json:"expiresAt" bson:"expiresAt"`
	Key       string             `json:"key" bson:"key"`
	UserID    primitive.ObjectID `json:"userID" bson:"userID"`
}
