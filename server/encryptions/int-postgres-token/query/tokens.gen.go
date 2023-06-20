// Code generated by gorm.io/gen. DO NOT EDIT.
// Code generated by gorm.io/gen. DO NOT EDIT.
// Code generated by gorm.io/gen. DO NOT EDIT.

package query

import (
	"context"
	"strings"

	"gorm.io/gorm"
	"gorm.io/gorm/clause"
	"gorm.io/gorm/schema"

	"gorm.io/gen"
	"gorm.io/gen/field"

	"gorm.io/plugin/dbresolver"

	"int-db-token/model"
)

func newToken(db *gorm.DB, opts ...gen.DOOption) token {
	_token := token{}

	_token.tokenDo.UseDB(db, opts...)
	_token.tokenDo.UseModel(&model.Token{})

	tableName := _token.tokenDo.TableName()
	_token.ALL = field.NewAsterisk(tableName)
	_token.ID = field.NewUint(tableName, "id")
	_token.CreatedAt = field.NewTime(tableName, "created_at")
	_token.UpdatedAt = field.NewTime(tableName, "updated_at")
	_token.DeletedAt = field.NewField(tableName, "deleted_at")
	_token.TokenType = field.NewString(tableName, "token_type")
	_token.ExpiresAt = field.NewTime(tableName, "expires_at")
	_token.Key = field.NewString(tableName, "key")
	_token.UserID = field.NewUint64(tableName, "user_id")
	_token.User = tokenBelongsToUser{
		db: db.Session(&gorm.Session{}),

		RelationField: field.NewRelation("User", "model.User"),
		Tokens: struct {
			field.RelationField
			User struct {
				field.RelationField
			}
		}{
			RelationField: field.NewRelation("User.Tokens", "model.Token"),
			User: struct {
				field.RelationField
			}{
				RelationField: field.NewRelation("User.Tokens.User", "model.User"),
			},
		},
	}

	_token.fillFieldMap()

	return _token
}

type token struct {
	tokenDo

	ALL       field.Asterisk
	ID        field.Uint
	CreatedAt field.Time
	UpdatedAt field.Time
	DeletedAt field.Field
	TokenType field.String
	ExpiresAt field.Time
	Key       field.String
	UserID    field.Uint64
	User      tokenBelongsToUser

	fieldMap map[string]field.Expr
}

func (t token) Table(newTableName string) *token {
	t.tokenDo.UseTable(newTableName)
	return t.updateTableName(newTableName)
}

func (t token) As(alias string) *token {
	t.tokenDo.DO = *(t.tokenDo.As(alias).(*gen.DO))
	return t.updateTableName(alias)
}

func (t *token) updateTableName(table string) *token {
	t.ALL = field.NewAsterisk(table)
	t.ID = field.NewUint(table, "id")
	t.CreatedAt = field.NewTime(table, "created_at")
	t.UpdatedAt = field.NewTime(table, "updated_at")
	t.DeletedAt = field.NewField(table, "deleted_at")
	t.TokenType = field.NewString(table, "token_type")
	t.ExpiresAt = field.NewTime(table, "expires_at")
	t.Key = field.NewString(table, "key")
	t.UserID = field.NewUint64(table, "user_id")

	t.fillFieldMap()

	return t
}

func (t *token) GetFieldByName(fieldName string) (field.OrderExpr, bool) {
	_f, ok := t.fieldMap[fieldName]
	if !ok || _f == nil {
		return nil, false
	}
	_oe, ok := _f.(field.OrderExpr)
	return _oe, ok
}

func (t *token) fillFieldMap() {
	t.fieldMap = make(map[string]field.Expr, 9)
	t.fieldMap["id"] = t.ID
	t.fieldMap["created_at"] = t.CreatedAt
	t.fieldMap["updated_at"] = t.UpdatedAt
	t.fieldMap["deleted_at"] = t.DeletedAt
	t.fieldMap["token_type"] = t.TokenType
	t.fieldMap["expires_at"] = t.ExpiresAt
	t.fieldMap["key"] = t.Key
	t.fieldMap["user_id"] = t.UserID

}

func (t token) clone(db *gorm.DB) token {
	t.tokenDo.ReplaceConnPool(db.Statement.ConnPool)
	return t
}

func (t token) replaceDB(db *gorm.DB) token {
	t.tokenDo.ReplaceDB(db)
	return t
}

type tokenBelongsToUser struct {
	db *gorm.DB

	field.RelationField

	Tokens struct {
		field.RelationField
		User struct {
			field.RelationField
		}
	}
}

func (a tokenBelongsToUser) Where(conds ...field.Expr) *tokenBelongsToUser {
	if len(conds) == 0 {
		return &a
	}

	exprs := make([]clause.Expression, 0, len(conds))
	for _, cond := range conds {
		exprs = append(exprs, cond.BeCond().(clause.Expression))
	}
	a.db = a.db.Clauses(clause.Where{Exprs: exprs})
	return &a
}

func (a tokenBelongsToUser) WithContext(ctx context.Context) *tokenBelongsToUser {
	a.db = a.db.WithContext(ctx)
	return &a
}

func (a tokenBelongsToUser) Session(session *gorm.Session) *tokenBelongsToUser {
	a.db = a.db.Session(session)
	return &a
}

func (a tokenBelongsToUser) Model(m *model.Token) *tokenBelongsToUserTx {
	return &tokenBelongsToUserTx{a.db.Model(m).Association(a.Name())}
}

type tokenBelongsToUserTx struct{ tx *gorm.Association }

func (a tokenBelongsToUserTx) Find() (result *model.User, err error) {
	return result, a.tx.Find(&result)
}

func (a tokenBelongsToUserTx) Append(values ...*model.User) (err error) {
	targetValues := make([]interface{}, len(values))
	for i, v := range values {
		targetValues[i] = v
	}
	return a.tx.Append(targetValues...)
}

func (a tokenBelongsToUserTx) Replace(values ...*model.User) (err error) {
	targetValues := make([]interface{}, len(values))
	for i, v := range values {
		targetValues[i] = v
	}
	return a.tx.Replace(targetValues...)
}

func (a tokenBelongsToUserTx) Delete(values ...*model.User) (err error) {
	targetValues := make([]interface{}, len(values))
	for i, v := range values {
		targetValues[i] = v
	}
	return a.tx.Delete(targetValues...)
}

func (a tokenBelongsToUserTx) Clear() error {
	return a.tx.Clear()
}

func (a tokenBelongsToUserTx) Count() int64 {
	return a.tx.Count()
}

type tokenDo struct{ gen.DO }

type ITokenDo interface {
	gen.SubQuery
	Debug() ITokenDo
	WithContext(ctx context.Context) ITokenDo
	WithResult(fc func(tx gen.Dao)) gen.ResultInfo
	ReplaceDB(db *gorm.DB)
	ReadDB() ITokenDo
	WriteDB() ITokenDo
	As(alias string) gen.Dao
	Session(config *gorm.Session) ITokenDo
	Columns(cols ...field.Expr) gen.Columns
	Clauses(conds ...clause.Expression) ITokenDo
	Not(conds ...gen.Condition) ITokenDo
	Or(conds ...gen.Condition) ITokenDo
	Select(conds ...field.Expr) ITokenDo
	Where(conds ...gen.Condition) ITokenDo
	Order(conds ...field.Expr) ITokenDo
	Distinct(cols ...field.Expr) ITokenDo
	Omit(cols ...field.Expr) ITokenDo
	Join(table schema.Tabler, on ...field.Expr) ITokenDo
	LeftJoin(table schema.Tabler, on ...field.Expr) ITokenDo
	RightJoin(table schema.Tabler, on ...field.Expr) ITokenDo
	Group(cols ...field.Expr) ITokenDo
	Having(conds ...gen.Condition) ITokenDo
	Limit(limit int) ITokenDo
	Offset(offset int) ITokenDo
	Count() (count int64, err error)
	Scopes(funcs ...func(gen.Dao) gen.Dao) ITokenDo
	Unscoped() ITokenDo
	Create(values ...*model.Token) error
	CreateInBatches(values []*model.Token, batchSize int) error
	Save(values ...*model.Token) error
	First() (*model.Token, error)
	Take() (*model.Token, error)
	Last() (*model.Token, error)
	Find() ([]*model.Token, error)
	FindInBatch(batchSize int, fc func(tx gen.Dao, batch int) error) (results []*model.Token, err error)
	FindInBatches(result *[]*model.Token, batchSize int, fc func(tx gen.Dao, batch int) error) error
	Pluck(column field.Expr, dest interface{}) error
	Delete(...*model.Token) (info gen.ResultInfo, err error)
	Update(column field.Expr, value interface{}) (info gen.ResultInfo, err error)
	UpdateSimple(columns ...field.AssignExpr) (info gen.ResultInfo, err error)
	Updates(value interface{}) (info gen.ResultInfo, err error)
	UpdateColumn(column field.Expr, value interface{}) (info gen.ResultInfo, err error)
	UpdateColumnSimple(columns ...field.AssignExpr) (info gen.ResultInfo, err error)
	UpdateColumns(value interface{}) (info gen.ResultInfo, err error)
	UpdateFrom(q gen.SubQuery) gen.Dao
	Attrs(attrs ...field.AssignExpr) ITokenDo
	Assign(attrs ...field.AssignExpr) ITokenDo
	Joins(fields ...field.RelationField) ITokenDo
	Preload(fields ...field.RelationField) ITokenDo
	FirstOrInit() (*model.Token, error)
	FirstOrCreate() (*model.Token, error)
	FindByPage(offset int, limit int) (result []*model.Token, count int64, err error)
	ScanByPage(result interface{}, offset int, limit int) (count int64, err error)
	Scan(result interface{}) (err error)
	Returning(value interface{}, columns ...string) ITokenDo
	UnderlyingDB() *gorm.DB
	schema.Tabler

	FilterWithNameAndRole(name string, role string) (result []model.Token, err error)
}

// SELECT * FROM @@table WHERE name = @name{{if role !=""}} AND role = @role{{end}}
func (t tokenDo) FilterWithNameAndRole(name string, role string) (result []model.Token, err error) {
	var params []interface{}

	var generateSQL strings.Builder
	params = append(params, name)
	generateSQL.WriteString("SELECT * FROM tokens WHERE name = ? ")
	if role != "" {
		params = append(params, role)
		generateSQL.WriteString("AND role = ? ")
	}

	var executeSQL *gorm.DB
	executeSQL = t.UnderlyingDB().Raw(generateSQL.String(), params...).Find(&result) // ignore_security_alert
	err = executeSQL.Error

	return
}

func (t tokenDo) Debug() ITokenDo {
	return t.withDO(t.DO.Debug())
}

func (t tokenDo) WithContext(ctx context.Context) ITokenDo {
	return t.withDO(t.DO.WithContext(ctx))
}

func (t tokenDo) ReadDB() ITokenDo {
	return t.Clauses(dbresolver.Read)
}

func (t tokenDo) WriteDB() ITokenDo {
	return t.Clauses(dbresolver.Write)
}

func (t tokenDo) Session(config *gorm.Session) ITokenDo {
	return t.withDO(t.DO.Session(config))
}

func (t tokenDo) Clauses(conds ...clause.Expression) ITokenDo {
	return t.withDO(t.DO.Clauses(conds...))
}

func (t tokenDo) Returning(value interface{}, columns ...string) ITokenDo {
	return t.withDO(t.DO.Returning(value, columns...))
}

func (t tokenDo) Not(conds ...gen.Condition) ITokenDo {
	return t.withDO(t.DO.Not(conds...))
}

func (t tokenDo) Or(conds ...gen.Condition) ITokenDo {
	return t.withDO(t.DO.Or(conds...))
}

func (t tokenDo) Select(conds ...field.Expr) ITokenDo {
	return t.withDO(t.DO.Select(conds...))
}

func (t tokenDo) Where(conds ...gen.Condition) ITokenDo {
	return t.withDO(t.DO.Where(conds...))
}

func (t tokenDo) Exists(subquery interface{ UnderlyingDB() *gorm.DB }) ITokenDo {
	return t.Where(field.CompareSubQuery(field.ExistsOp, nil, subquery.UnderlyingDB()))
}

func (t tokenDo) Order(conds ...field.Expr) ITokenDo {
	return t.withDO(t.DO.Order(conds...))
}

func (t tokenDo) Distinct(cols ...field.Expr) ITokenDo {
	return t.withDO(t.DO.Distinct(cols...))
}

func (t tokenDo) Omit(cols ...field.Expr) ITokenDo {
	return t.withDO(t.DO.Omit(cols...))
}

func (t tokenDo) Join(table schema.Tabler, on ...field.Expr) ITokenDo {
	return t.withDO(t.DO.Join(table, on...))
}

func (t tokenDo) LeftJoin(table schema.Tabler, on ...field.Expr) ITokenDo {
	return t.withDO(t.DO.LeftJoin(table, on...))
}

func (t tokenDo) RightJoin(table schema.Tabler, on ...field.Expr) ITokenDo {
	return t.withDO(t.DO.RightJoin(table, on...))
}

func (t tokenDo) Group(cols ...field.Expr) ITokenDo {
	return t.withDO(t.DO.Group(cols...))
}

func (t tokenDo) Having(conds ...gen.Condition) ITokenDo {
	return t.withDO(t.DO.Having(conds...))
}

func (t tokenDo) Limit(limit int) ITokenDo {
	return t.withDO(t.DO.Limit(limit))
}

func (t tokenDo) Offset(offset int) ITokenDo {
	return t.withDO(t.DO.Offset(offset))
}

func (t tokenDo) Scopes(funcs ...func(gen.Dao) gen.Dao) ITokenDo {
	return t.withDO(t.DO.Scopes(funcs...))
}

func (t tokenDo) Unscoped() ITokenDo {
	return t.withDO(t.DO.Unscoped())
}

func (t tokenDo) Create(values ...*model.Token) error {
	if len(values) == 0 {
		return nil
	}
	return t.DO.Create(values)
}

func (t tokenDo) CreateInBatches(values []*model.Token, batchSize int) error {
	return t.DO.CreateInBatches(values, batchSize)
}

// Save : !!! underlying implementation is different with GORM
// The method is equivalent to executing the statement: db.Clauses(clause.OnConflict{UpdateAll: true}).Create(values)
func (t tokenDo) Save(values ...*model.Token) error {
	if len(values) == 0 {
		return nil
	}
	return t.DO.Save(values)
}

func (t tokenDo) First() (*model.Token, error) {
	if result, err := t.DO.First(); err != nil {
		return nil, err
	} else {
		return result.(*model.Token), nil
	}
}

func (t tokenDo) Take() (*model.Token, error) {
	if result, err := t.DO.Take(); err != nil {
		return nil, err
	} else {
		return result.(*model.Token), nil
	}
}

func (t tokenDo) Last() (*model.Token, error) {
	if result, err := t.DO.Last(); err != nil {
		return nil, err
	} else {
		return result.(*model.Token), nil
	}
}

func (t tokenDo) Find() ([]*model.Token, error) {
	result, err := t.DO.Find()
	return result.([]*model.Token), err
}

func (t tokenDo) FindInBatch(batchSize int, fc func(tx gen.Dao, batch int) error) (results []*model.Token, err error) {
	buf := make([]*model.Token, 0, batchSize)
	err = t.DO.FindInBatches(&buf, batchSize, func(tx gen.Dao, batch int) error {
		defer func() { results = append(results, buf...) }()
		return fc(tx, batch)
	})
	return results, err
}

func (t tokenDo) FindInBatches(result *[]*model.Token, batchSize int, fc func(tx gen.Dao, batch int) error) error {
	return t.DO.FindInBatches(result, batchSize, fc)
}

func (t tokenDo) Attrs(attrs ...field.AssignExpr) ITokenDo {
	return t.withDO(t.DO.Attrs(attrs...))
}

func (t tokenDo) Assign(attrs ...field.AssignExpr) ITokenDo {
	return t.withDO(t.DO.Assign(attrs...))
}

func (t tokenDo) Joins(fields ...field.RelationField) ITokenDo {
	for _, _f := range fields {
		t = *t.withDO(t.DO.Joins(_f))
	}
	return &t
}

func (t tokenDo) Preload(fields ...field.RelationField) ITokenDo {
	for _, _f := range fields {
		t = *t.withDO(t.DO.Preload(_f))
	}
	return &t
}

func (t tokenDo) FirstOrInit() (*model.Token, error) {
	if result, err := t.DO.FirstOrInit(); err != nil {
		return nil, err
	} else {
		return result.(*model.Token), nil
	}
}

func (t tokenDo) FirstOrCreate() (*model.Token, error) {
	if result, err := t.DO.FirstOrCreate(); err != nil {
		return nil, err
	} else {
		return result.(*model.Token), nil
	}
}

func (t tokenDo) FindByPage(offset int, limit int) (result []*model.Token, count int64, err error) {
	result, err = t.Offset(offset).Limit(limit).Find()
	if err != nil {
		return
	}

	if size := len(result); 0 < limit && 0 < size && size < limit {
		count = int64(size + offset)
		return
	}

	count, err = t.Offset(-1).Limit(-1).Count()
	return
}

func (t tokenDo) ScanByPage(result interface{}, offset int, limit int) (count int64, err error) {
	count, err = t.Count()
	if err != nil {
		return
	}

	err = t.Offset(offset).Limit(limit).Scan(result)
	return
}

func (t tokenDo) Scan(result interface{}) (err error) {
	return t.DO.Scan(result)
}

func (t tokenDo) Delete(models ...*model.Token) (result gen.ResultInfo, err error) {
	return t.DO.Delete(models)
}

func (t *tokenDo) withDO(do gen.Dao) *tokenDo {
	t.DO = *do.(*gen.DO)
	return t
}
