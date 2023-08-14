.PHONY: all

all: big-query big-table datastore firestore spanner


big-query:
	@echo ""
	@echo "# Big Query benchmark..."

	@echo ""
	@echo "Normalized:"
	@python -m benchmark.big-query.normalized

	@echo ""
	@echo "Denormalized:"
	@python -m benchmark.big-query.denormalized


big-table:
	@echo ""
	@echo "# Big Table benchmark..."

	@echo ""
	@echo "Normalized:"
	@python -m benchmark.big-table.normalized

	@echo ""
	@echo "Denormalized:"
	@python -m benchmark.big-table.denormalized


datastore:
	@echo ""
	@echo "# Datastore benchmark..."

	@echo ""
	@echo "Normalized:"
	@python -m benchmark.datastore.normalized

	@echo ""
	@echo "Denormalized:"
	@python -m benchmark.datastore.denormalized


firestore:
	@echo ""
	@echo "# Firestore benchmark..."

	@echo ""
	@echo "Normalized:"
	@python -m benchmark.firestore.normalized

	@echo ""
	@echo "Denormalized:"
	@python -m benchmark.firestore.denormalized


spanner:
	@echo ""
	@echo "# Spanner benchmark..."

	@echo ""
	@echo "Normalized:"
	@python -m benchmark.spanner.normalized

	@echo ""
	@echo "Denormalized:"
	@python -m benchmark.spanner.denormalized
