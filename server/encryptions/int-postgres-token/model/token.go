package model

import (
	"time"

	"gorm.io/gorm"
)

type Token struct {
	gorm.Model
	TokenType string    `json:"tokenType"`
	ExpiresAt time.Time `json:"expiresAt"`
	Key       string    `json:"key"`
	User      User
	UserID    uint64 `json:"userID"`
}
