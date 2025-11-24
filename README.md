# snowflake-id-toolkit

A Python toolkit for generating snowflake-like unique IDs.

## Supported Implementations

- **Twitter Snowflake** - 64-bit IDs with ~69 years of timestamps, 1024 nodes, 4096 IDs per millisecond per node
- **Instagram Snowflake** - 64-bit IDs with ~69 years of timestamps, 8192 shards, 1024 IDs per millisecond per shard
- **Sony Sonyflake** - 64-bit IDs with ~174 years of timestamps, 256 nodes, 65,536 IDs per 10ms per node

## Installation

```bash
pip install snowflake-id-toolkit
```

## Usage

```python
from snowflake_id_toolkit.twitter import TwitterSnowflakeIDGenerator

generator = TwitterSnowflakeIDGenerator(
    node_id=0,
    epoch=1288834974657  # Twitter's default epoch
)
snowflake_id = generator.generate_next_id()
```

## Comparison with Other ID Strategies

| Feature                | Snowflake                                        | UUIDv4    | UUIDv7        | Auto-increment |
|------------------------|--------------------------------------------------|-----------|---------------|----------------|
| Size                   | 64 bits                                          | 128 bits  | 128 bits      | 32-64 bits     |
| Sortable by time       | ✅                                                | ❌         | ✅             | ✅              |
| Distributed generation | ✅                                                | ✅         | ✅             | ❌              |
| No coordination needed | ⚠️                                               | ✅         | ✅             | ❌              |
| DB Index-friendly      | ✅                                                | ❌         | ⚠️            | ✅              |
| Predictability         | Medium                                           | None      | Low           | High           |
| Throughput             | 4,096,000/sec/node<br/>(6,553,600 for Sonyflake) | Unlimited | Unlimited     | DB-limited     |
| Relative speed         | ~5.2x                                            | ~1.1x     | 1x (baseline) | N/A (DB-bound) |

### When to Use

- **Snowflake**: High-throughput distributed systems needing compact, sortable IDs
- **UUIDv4**: When unpredictability matters, size doesn't, and no sorting needed
- **UUIDv7**: Modern default choice when simplicity is key factor and 128 bits is acceptable
- **Auto-increment**: Single-database apps where simplicity wins

## License

The **snowflake-id-toolkit** is licensed under the MIT License. See the LICENSE file for more information.
