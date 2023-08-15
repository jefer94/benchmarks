# Benchmarks

## Relational databases

### PostgreSQL

Normalized:
- Insert took 1.351837 seconds
- Select took 0.121539 seconds
- Update took 0.566995 seconds
- Delete took 0.544552 seconds
- Total took 2.584923 seconds

Denormalized:
- Insert took 0.091469 seconds
- Select took 0.255610 seconds
- Update took 0.476220 seconds
- Delete took 0.308292 seconds
- Total took 1.131592 seconds

### MySQL

Normalized:
- Insert took 2.595673 seconds
- Select took 0.163980 seconds
- Update took 1.190948 seconds
- Delete took 1.123263 seconds
- Total took 5.073863 seconds

Denormalized:
- Insert took 0.179059 seconds
- Select took 0.671804 seconds
- Update took 0.670808 seconds
- Delete took 0.650200 seconds
- Total took 2.171870 seconds

### MariaDB

Normalized:
- Insert took 1.426637 seconds
- Select took 0.163204 seconds
- Update took 0.620263 seconds
- Delete took 0.553941 seconds
- Total took 2.764045 seconds

Denormalized:
- Insert took 0.102323 seconds
- Select took 0.571364 seconds
- Update took 0.828115 seconds
- Delete took 0.528161 seconds
- Total took 2.029963 seconds

## Document databases

### MongoDB

Normalized:
- Insert took 0.151863 seconds
- Select took 0.065632 seconds
- Update took 0.080190 seconds
- Delete took 0.057956 seconds
- Total took 0.355642 seconds

Denormalized:
- Insert took 0.080627 seconds
- Select took 0.065755 seconds
- Update took 0.140136 seconds
- Delete took 0.047680 seconds
- Total took 0.334199 seconds

## Wide-column store databases

### Apache Cassandra

Normalized:
- Insert took 0.408187 seconds
- Select took 0.256049 seconds
- Update took 0.476884 seconds
- Delete took 0.472108 seconds
- Total took 1.613228 seconds

Denormalized:
- Insert took 0.208915 seconds
- Select took 0.239401 seconds
- Update took 0.550962 seconds
- Delete took 0.427869 seconds
- Total took 1.427146 seconds

Materialized view denormalized:
- Insert took 0.228418 seconds
- Select took 0.248262 seconds
- Update took 0.592511 seconds
- Delete took 0.468324 seconds
- Total took 1.537515 seconds

### Scylla

Normalized:
- Insert took 0.354200 seconds
- Select took 0.214282 seconds
- Update took 0.372551 seconds
- Delete took 0.386429 seconds
- Total took 1.327462 seconds

Denormalized:
- Insert took 0.191769 seconds
- Select took 0.225223 seconds
- Update took 0.546197 seconds
- Delete took 0.378927 seconds
- Total took 1.342116 seconds

Materialized view denormalized:
- Insert took 0.226647 seconds
- Select took 0.208908 seconds
- Update took 0.564151 seconds
- Delete took 0.393889 seconds
- Total took 1.393594 seconds

### HBase

Normalized:
- Insert took 0.169461 seconds
- Select took 0.045451 seconds
- Update took 0.094352 seconds
- Delete took 0.146155 seconds
- Total took 0.455419 seconds

Denormalized:
- Insert took 0.099150 seconds
- Select took 0.038581 seconds
- Update took 0.156718 seconds
- Delete took 0.140258 seconds
- Total took 0.434707 seconds
