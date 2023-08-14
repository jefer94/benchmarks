.PHONY: all

all: setup mongo cassandra scylla postgre

setup:
	@echo "# Benchmarks"
	@. .venv/bin/activate


scylla:
	@echo ""
	@echo "## Scylla"

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
	@echo "## Apache Cassandra"

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
	@echo "## MongoDB"

	@echo ""
	@echo "Normalized:"
	@python -m benchmark.mongo.normalized

	@echo ""
	@echo "Denormalized:"
	@python -m benchmark.mongo.denormalized


postgre:
	@echo ""
	@echo "## PostgreSQL"

	@echo ""
	@echo "Normalized:"
	@python -m benchmark.postgres.normalized

	@echo ""
	@echo "Denormalized:"
	@python -m benchmark.postgres.denormalized

