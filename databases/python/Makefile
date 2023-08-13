.PHONY: all

# all: mongo cassandra scylla
# all: mongo scylla
# all: postgres
# all: scylla
# all: mongo scylla
all: mongo

setup:
	echo A


scylla:
	@echo ""
	@echo "# Scylla benchmark..."

	@echo ""
	@echo "Normalized:"
	@CQLENG_ALLOW_SCHEMA_MANAGEMENT=1 python -m benchmark.scylla.normalized

	@echo ""
	@echo "Denormalized:"
	@CQLENG_ALLOW_SCHEMA_MANAGEMENT=1 python -m benchmark.scylla.denormalized

	@echo ""
	@echo "Materialized view denormalized:"
	@CQLENG_ALLOW_SCHEMA_MANAGEMENT=1 python -m benchmark.scylla.denormalized-view


cassandra:
	@echo ""
	@echo "# Cassandra benchmark..."

	@echo ""
	@echo "Normalized:"
	@CQLENG_ALLOW_SCHEMA_MANAGEMENT=1 python -m benchmark.cassandra.normalized

	@echo ""
	@echo "Denormalized:"
	@CQLENG_ALLOW_SCHEMA_MANAGEMENT=1 python -m benchmark.cassandra.denormalized

	@echo ""
	@echo "Materialized view denormalized:"
	@CQLENG_ALLOW_SCHEMA_MANAGEMENT=1 python -m benchmark.cassandra.denormalized-view


mongo:
	@echo ""
	@echo "# Mongo benchmark..."

	@echo ""
	@echo "Normalized:"
	@python -m benchmark.mongo.normalized

	@echo ""
	@echo "Denormalized:"
	@python -m benchmark.mongo.denormalized


postgres:
	@echo ""
	@echo "# Postgres benchmark..."

	@echo ""
	@echo "Normalized:"
	@python -m benchmark.postgres.normalized

	@echo ""
	@echo "Denormalized:"
	@python -m benchmark.postgres.denormalized

