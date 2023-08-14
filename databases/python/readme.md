# Benchmarks

## MongoDB

Normalized:
- Insert took 0.579488 seconds
- Select took 0.276584 seconds
- Update took 0.280585 seconds
- Delete took 0.289465 seconds
- Total took 1.426121 seconds

Denormalized:
- Insert took 0.306990 seconds
- Select took 0.254290 seconds
- Update took 0.333762 seconds
- Delete took 0.217955 seconds
- Total took 1.112997 seconds

## Apache Cassandra

Normalized:
- Insert took 1.008930 seconds
- Select took 0.598822 seconds
- Update took 1.149858 seconds
- Delete took 1.118393 seconds
- Total took 3.876004 seconds

Denormalized:
- Insert took 0.500405 seconds
- Select took 0.559505 seconds
- Update took 1.263691 seconds
- Delete took 1.076699 seconds
- Total took 3.400300 seconds

Materialized view denormalized:
- Insert took 0.580328 seconds
- Select took 0.590688 seconds
- Update took 1.268679 seconds
- Delete took 1.093381 seconds
- Total took 3.533075 seconds

## Scylla

Normalized:
- Insert took 0.937415 seconds
- Select took 0.538156 seconds
- Update took 1.034339 seconds
- Delete took 1.025356 seconds
- Total took 3.535266 seconds

Denormalized:
- Insert took 0.471891 seconds
- Select took 0.499975 seconds
- Update took 1.128829 seconds
- Delete took 0.959208 seconds
- Total took 3.059903 seconds

Materialized view denormalized:
- Insert took 0.525855 seconds
- Select took 0.513409 seconds
- Update took 1.186302 seconds
- Delete took 1.067590 seconds
- Total took 3.293156 seconds

## PostgreSQL

Normalized:
- Insert took 3.568992 seconds
- Select took 0.323311 seconds
- Update took 1.502764 seconds
- Delete took 1.462736 seconds
- Total took 6.857803 seconds

Denormalized:
- Insert took 0.192011 seconds
- Select took 0.540501 seconds
- Update took 1.043179 seconds
- Delete took 0.853332 seconds
- Total took 2.629022 seconds
