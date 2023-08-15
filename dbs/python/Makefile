.PHONY: all

sql: setup relational document wide-column-store

setup:
	@echo "# Benchmarks"
	@. .venv/bin/activate

relational:
	@echo ""
	@echo "## Relational databases"
	@$(MAKE) --no-print-directory postgres
	@$(MAKE) --no-print-directory mysql
	@$(MAKE) --no-print-directory mariadb

document:
	@echo ""
	@echo "## Document databases"
	@$(MAKE) --no-print-directory mongo

wide-column-store:
	@echo ""
	@echo "## Wide-column store databases"
	@$(MAKE) --no-print-directory cassandra
	@$(MAKE) --no-print-directory scylla
	@$(MAKE) --no-print-directory hbase

mysql:
	@echo ""
	@echo "### MySQL"

	@echo ""
	@echo "Normalized:"
	@python -m benchmark.mysql.normalized

	@echo ""
	@echo "Denormalized:"
	@python -m benchmark.mysql.denormalized

mariadb:
	@echo ""
	@echo "### MariaDB"

	@echo ""
	@echo "Normalized:"
	@python -m benchmark.mariadb.normalized

	@echo ""
	@echo "Denormalized:"
	@python -m benchmark.mariadb.denormalized


scylla:
	@echo ""
	@echo "### Scylla"
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
	@echo "### Apache Cassandra"

	@echo ""
	@echo "Normalized:"
	@CQLENG_ALLOW_SCHEMA_MANAGEMENT=1 python -m benchmark.cassandra.normalized

	@echo ""
	@echo "Denormalized:"
	@CQLENG_ALLOW_SCHEMA_MANAGEMENT=1 python -m benchmark.cassandra.denormalized

	@echo ""
	@echo "Materialized view denormalized:"
	@CQLENG_ALLOW_SCHEMA_MANAGEMENT=1 python -m benchmark.cassandra.denormalized-view


hbase:
	@echo ""
	@echo "### HBase"

	@echo ""
	@echo "Normalized:"
	@CQLENG_ALLOW_SCHEMA_MANAGEMENT=1 python -m benchmark.hbase.normalized

	@echo ""
	@echo "Denormalized:"
	@CQLENG_ALLOW_SCHEMA_MANAGEMENT=1 python -m benchmark.hbase.denormalized



mongo:
	@echo ""
	@echo "### MongoDB"

	@echo ""
	@echo "Normalized:"
	@python -m benchmark.mongo.normalized

	@echo ""
	@echo "Denormalized:"
	@python -m benchmark.mongo.denormalized


postgres:
	@echo ""
	@echo "### PostgreSQL"

	@echo ""
	@echo "Normalized:"
	@python -m benchmark.postgres.normalized

	@echo ""
	@echo "Denormalized:"
	@python -m benchmark.postgres.denormalized
