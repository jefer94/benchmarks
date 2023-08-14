# Benchmarks

## MongoDB

Normalized:
- Insert took 0.146911 seconds
- Select took 0.060957 seconds
- Update took 0.070731 seconds
- Delete took 0.057704 seconds
- Total took 0.336303 seconds

Denormalized:
- Insert took 0.079255 seconds
- Select took 0.054621 seconds
- Update took 0.127965 seconds
- Delete took 0.047566 seconds
- Total took 0.309407 seconds

## Apache Cassandra

Normalized:
- Insert took 0.537338 seconds
- Select took 0.287378 seconds
- Update took 0.567351 seconds
- Delete took 0.513734 seconds
- Total took 1.905801 seconds

Denormalized:
- Insert took 0.206198 seconds
- Select took 0.258155 seconds
- Update took 0.528348 seconds
- Delete took 0.451063 seconds
- Total took 1.443764 seconds

Materialized view denormalized:
- Insert took 0.266798 seconds
- Select took 0.261471 seconds
- Update took 0.620968 seconds
- Delete took 0.526993 seconds
- Total took 1.676231 seconds

## Scylla

Normalized:
- Insert took 0.342124 seconds
- Select took 0.238698 seconds
- Update took 0.386585 seconds
- Delete took 0.378146 seconds
- Total took 1.345553 seconds

Denormalized:
- Insert took 0.206530 seconds
- Select took 0.250133 seconds
- Update took 0.527851 seconds
- Delete took 0.353975 seconds
- Total took 1.338490 seconds

Materialized view denormalized:
- Insert took 0.222082 seconds
- Select took 0.229672 seconds
- Update took 0.570394 seconds
- Delete took 0.434926 seconds
- Total took 1.457073 seconds

## PostgreSQL

Normalized:
- Insert took 1.311502 seconds
- Select took 0.110442 seconds
- Update took 0.547565 seconds
- Delete took 0.531207 seconds
- Total took 2.500716 seconds

Denormalized:
- Insert took 0.083305 seconds
- Select took 0.254135 seconds
- Update took 0.454685 seconds
- Delete took 0.293414 seconds
- Total took 1.085538 seconds
