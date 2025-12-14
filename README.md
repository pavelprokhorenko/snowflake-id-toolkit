# Snowflake ID Toolkit

A high-performance Python library for generating distributed, time-ordered unique identifiers using Snowflake-like algorithms. This toolkit provides production-ready implementations of Twitter Snowflake, Instagram Snowflake, and Sony Sonyflake ID generation schemes.

[![PyPI](https://img.shields.io/pypi/v/snowflake-id-toolkit.svg)](https://pypi.org/project/snowflake-id-toolkit/)
[![Python Versions](https://img.shields.io/pypi/pyversions/snowflake-id-toolkit.svg)](https://pypi.org/project/snowflake-id-toolkit/)
[![License](https://img.shields.io/github/license/pavelprokhorenko/snowflake-id-toolkit.svg)](https://github.com/pavelprokhorenko/snowflake-id-toolkit/blob/main/LICENSE)
[![codecov](https://codecov.io/gh/pavelprokhorenko/snowflake-id-toolkit/branch/main/graph/badge.svg)](https://codecov.io/gh/pavelprokhorenko/snowflake-id-toolkit)

## What are Snowflake IDs?

Snowflake IDs are 64-bit integers designed for distributed systems that need to generate unique identifiers without coordination between nodes. Originally developed by Twitter in 2010, they solve the fundamental challenge of ID generation in distributed architectures where traditional auto-increment integers fail.

Each Snowflake ID encodes three key components into a single 64-bit integer:
- **Timestamp** - Millisecond precision time since a custom epoch
- **Node ID** - Unique identifier for the generating machine/process
- **Sequence** - Counter for IDs generated within the same millisecond

**Why time-ordered IDs matter:**
- **Database performance**: Time-ordered inserts keep B-tree indexes balanced, avoiding page splits and fragmentation
- **Range queries**: Efficiently query recent records without secondary indexes
- **Caching**: Hot data naturally clusters together, improving cache hit rates
- **Debugging**: IDs encode creation time, making troubleshooting easier
- **Sharding**: Time-based sharding strategies work naturally with sorted IDs

Learn more: [Snowflake ID on Wikipedia](https://en.wikipedia.org/wiki/Snowflake_ID)

## Installation

```bash
pip install snowflake-id-toolkit
```

## Quick Start

```python
from snowflake_id_toolkit import TwitterSnowflakeIDGenerator

# Initialize generator with node ID and epoch
generator = TwitterSnowflakeIDGenerator(
    node_id=0,
    epoch=1288834974657  # Twitter's default: 2010-11-04T01:42:54.657Z
)

# Generate IDs
id1 = generator.generate_next_id()
id2 = generator.generate_next_id()

print(f"Generated ID: {id1}")
# Extract components
print(f"Timestamp: {id1.timestamp_ms(epoch=1288834974657)} ms")
print(f"Node ID: {id1.node_id()}")
print(f"Sequence: {id1.sequence()}")

# Encode for transmission/storage
print(f"Base64: {id1.as_base64()}")
print(f"Hex: {id1.as_base16()}")
```

## Supported Implementations

### Twitter Snowflake
The original implementation from Twitter, optimized for distributed tweet ID generation.

**Bit Layout (64 bits):**
```
[1 unused][41 timestamp][10 node_id][12 sequence]
```

**Specifications:**
- **Lifespan**: ~69 years from epoch (2^41 milliseconds)
- **Nodes**: 1,024 (2^10)
- **Throughput**: 4,096 IDs/ms per node (~4.1M IDs/sec)
- **Time Resolution**: 1 millisecond

**Usage:**
```python
from snowflake_id_toolkit import TwitterSnowflakeIDGenerator

generator = TwitterSnowflakeIDGenerator(
    node_id=42,
    epoch=1288834974657  # 2010-11-04T01:42:54.657Z
)
```

**Use Cases:**
- Social media platforms
- High-frequency distributed systems
- Systems needing 1ms time precision
- Deployments with up to 1,024 nodes

---

### Instagram Snowflake
Instagram's variant optimized for their sharding architecture with more node capacity.

**Bit Layout (64 bits):**
```
[41 timestamp][13 node_id][10 sequence]
```

**Specifications:**
- **Lifespan**: ~69 years from epoch (2^41 milliseconds)
- **Nodes**: 8,192 (2^13)
- **Throughput**: 1,024 IDs/ms per node (1M IDs/sec)
- **Time Resolution**: 1 millisecond

**Usage:**
```python
from snowflake_id_toolkit import InstagramSnowflakeIDGenerator

generator = InstagramSnowflakeIDGenerator(
    node_id=100,
    epoch=1314220021721  # 2011-08-24T21:07:01.721Z
)
```

**Use Cases:**
- Systems requiring many shards (8,192+)
- Multi-region deployments with shard-per-region
- Moderate throughput per node
- Full 64-bit utilization (no sign bit waste)

---

### Sony Sonyflake
Sony's implementation with extended lifespan and higher per-node throughput using 10ms precision.

**Bit Layout (64 bits):**
```
[1 unused][39 timestamp][8 node_id][16 sequence]
```

**Specifications:**
- **Lifespan**: ~174 years from epoch (2^39 × 10ms intervals)
- **Nodes**: 256 (2^8)
- **Throughput**: 65,536 IDs per 10ms per node (6.5M IDs/sec)
- **Time Resolution**: 10 milliseconds

**Usage:**
```python
from snowflake_id_toolkit import SonyflakeIDGenerator

generator = SonyflakeIDGenerator(
    node_id=5,
    epoch=173568960000  # 2025-01-01T00:00:00.00Z
)
```

**Why 10ms resolution is often better:**
1. **Extended lifespan**: 174 years vs 69 years (2.5x longer)
2. **Higher burst capacity**: 65K IDs per 10ms window vs 4K per 1ms
3. **Clock skew tolerance**: More resilient to NTP adjustments
4. **Sufficient precision**: Most applications don't need sub-10ms ordering

**Use Cases:**
- Long-lived infrastructure (no epoch resets for 174 years)
- Ultra-high throughput per node requirements
- Smaller deployments (≤256 nodes)
- Systems tolerant of 10ms timestamp granularity

## SnowflakeID Type Features

All generated IDs inherit from `SnowflakeID`, providing rich functionality beyond simple integers:

### Component Extraction
```python
# Get timestamp in milliseconds since Unix epoch
timestamp = snowflake_id.timestamp_ms(epoch=1288834974657)

# Extract node identifier
node = snowflake_id.node_id()

# Get sequence number
seq = snowflake_id.sequence()
```

### Encoding & Serialization
```python
from snowflake_id_toolkit import TwitterSnowflakeID

# Binary representation (8 bytes)
binary = snowflake_id.as_bytes()
restored = TwitterSnowflakeID.parse_bytes(binary)

# Base16 (hexadecimal)
hex_str = snowflake_id.as_base16()
restored = TwitterSnowflakeID.parse_base16(hex_str)

# Base32
b32 = snowflake_id.as_base32()
restored = TwitterSnowflakeID.parse_base32(b32)

# Base64
b64 = snowflake_id.as_base64()
restored = TwitterSnowflakeID.parse_base64(b64)

# URL-safe Base64
urlsafe = snowflake_id.as_base64_urlsafe()
restored = TwitterSnowflakeID.parse_base64_urlsafe(urlsafe)

# Base85
b85 = snowflake_id.as_base85()
restored = TwitterSnowflakeID.parse_base85(b85)
```

### Integer Operations
Since `SnowflakeID` inherits from `int`, it supports all integer operations:
```python
# Arithmetic
result = snowflake_id + 100
doubled = snowflake_id * 2

# Comparisons
is_greater = snowflake_id1 > snowflake_id2  # Time-ordered comparison

# Database storage (as bigint)
cursor.execute("INSERT INTO events (id) VALUES (?)", (int(snowflake_id),))
```

## Advanced Usage

### Custom Epochs

**IMPORTANT:** Always set a custom epoch close to your project's start date. Using epoch=0 (Unix epoch, 1970) wastes timestamp bits and significantly reduces your ID lifespan.

```python
from snowflake_id_toolkit import TwitterSnowflakeIDGenerator, SonyflakeIDGenerator

# RECOMMENDED: Use get_current_timestamp() for correct time resolution
# For Twitter/Instagram (1ms resolution)
current_epoch = TwitterSnowflakeIDGenerator.get_current_timestamp()
generator = TwitterSnowflakeIDGenerator(node_id=0, epoch=current_epoch)

# For Sonyflake (10ms resolution)
current_epoch = SonyflakeIDGenerator.get_current_timestamp()
generator = SonyflakeIDGenerator(node_id=0, epoch=current_epoch)
```

**Why custom epochs matter:**
- Twitter Snowflake has ~69 years from epoch (2^41 milliseconds)
- Starting from 1970 means you've already used 55+ years of that range
- Setting epoch to current time gives you the full 69-year lifespan

**Common epochs (for reference):**
- Twitter: `1288834974657` (2010-11-04)
- Instagram: `1314220021721` (2011-08-24)
- Discord: `1420070400000` (2015-01-01)
- **Your project:** Use `get_current_timestamp()` when initializing

### Error Handling

```python
from snowflake_id_toolkit import (
    TwitterSnowflakeIDGenerator,
    MaxTimestampHasReachedError,
    LastGenerationTimestampIsGreaterError,
)

generator = TwitterSnowflakeIDGenerator(node_id=0, epoch=1288834974657)

try:
    snowflake_id = generator.generate_next_id()
except MaxTimestampHasReachedError:
    # Epoch exhausted (won't happen for ~69 years with Twitter Snowflake)
    print("Timestamp overflow - need new epoch")
except LastGenerationTimestampIsGreaterError:
    # System clock moved backward
    print("Clock skew detected - sync NTP")
```

### Thread Safety

All generators are thread-safe:
```python
from concurrent.futures import ThreadPoolExecutor
from snowflake_id_toolkit import TwitterSnowflakeIDGenerator

generator = TwitterSnowflakeIDGenerator(node_id=0, epoch=1288834974657)

def generate_batch(count):
    return [generator.generate_next_id() for _ in range(count)]

with ThreadPoolExecutor(max_workers=10) as executor:
    # Generate IDs from multiple threads safely
    futures = [executor.submit(generate_batch, 1000) for _ in range(10)]
    results = [f.result() for f in futures]
```

### Multi-Node Deployment

Assign unique node IDs to each instance:
```python
import os
from snowflake_id_toolkit import TwitterSnowflakeIDGenerator

# Option 1: Environment variable
node_id = int(os.environ.get("NODE_ID", 0))

# Option 2: Container orchestrator (K8s pod ID, ECS task ID, etc.)
# Option 3: Hash hostname/IP
# Option 4: Central registry service

generator = TwitterSnowflakeIDGenerator(
    node_id=node_id,
    epoch=1288834974657
)
```

**Node ID assignment strategies:**
- **Static configuration**: Environment variables, config files
- **Service discovery**: Consul, etcd, ZooKeeper
- **Container orchestration**: Kubernetes StatefulSet ordinals
- **Hash-based**: Hash(hostname) % max_nodes

## Comparison with Other ID Strategies

### UUIDv4
- **Sortable by time:** ❌ No - completely random
- **Distributed generation:** ✅ Yes - zero coordination
- **DB index-friendly:** ❌ Poor - random inserts cause 50-70% fragmentation
- **Size:** 128-bit (16 bytes) - 2x larger than Snowflake
- **Throughput:** Unlimited (no sequence coordination)

**Database impact:** Random distribution causes severe index fragmentation, 10-100x write amplification. 2x larger storage (128-bit vs 64-bit), but real-world indexes can be 2-2.5x larger due to fragmentation overhead.

**When to use:** Security tokens, API keys, session IDs where unpredictability is required and database performance isn't critical.

---

### UUIDv7
- **Sortable by time:** ✅ Yes - millisecond precision (48-bit timestamp)
- **Distributed generation:** ✅ Yes - no coordination needed
- **DB index-friendly:** ⚠️ Moderate - better than v4, worse than Snowflake
- **Size:** 128-bit (16 bytes) - 2x larger than Snowflake
- **Throughput:** Unlimited (74 random bits for uniqueness)

**Database impact:** Time-ordered prefix helps, but random suffix still causes 15-25% fragmentation and 2x slower inserts than Snowflake IDs.

**When to use:** New projects requiring UUID standard compliance with time-ordering. Modern default when 128-bit size is acceptable.

---

### ULID
- **Sortable by time:** ✅ Yes - millisecond precision (48-bit timestamp)
- **Distributed generation:** ✅ Yes - no coordination needed
- **DB index-friendly:** ⚠️ Moderate - similar to UUIDv7
- **Size:** 128-bit (16 bytes) - 2x larger than Snowflake
- **Throughput:** Unlimited (80 random bits)

**String format:** 26-character Crockford Base32 (`01ARZ3NDEKTSV4RRFFQ69G5FAV`) - lexicographically sortable, more human-friendly than hex UUIDs.

**Database impact:** 15-20% fragmentation, comparable to UUIDv7. Better than UUIDv4 but still 2x slower than Snowflake IDs.

**When to use:** Need human-readable, string-sortable IDs for APIs/URLs. NoSQL databases preferring string keys (MongoDB, DynamoDB).

---

### KSUID
- **Sortable by time:** ✅ Yes - **second precision only** (32-bit timestamp)
- **Distributed generation:** ✅ Yes - no coordination needed
- **DB index-friendly:** ❌ Poor - 128 random bits cause significant fragmentation
- **Size:** 160-bit (20 bytes) - 2.5x larger than Snowflake
- **Throughput:** Unlimited (large random space)

**Limitations:** Only second-level precision means IDs within the same second are randomly ordered. Much larger than alternatives with worse database performance.

**Database impact:** 40-60% fragmentation, 3-5x write amplification, 2.5x larger indexes than Snowflake IDs.

**When to use:** Second-precision ordering sufficient, extremely low collision probability needed. Limited adoption compared to UUID/ULID.

---

### Auto-increment
- **Sortable by time:** ✅ Yes - monotonically increasing
- **Distributed generation:** ❌ No - database coordination required
- **DB index-friendly:** ✅ Excellent - perfectly sequential
- **Size:** 32-bit (4 bytes) or 64-bit (8 bytes) - most compact
- **Throughput:** DB-limited - bottlenecked by database writes

**Distributed challenges:** Cannot scale horizontally, single point of failure, impossible offline generation. All ID generation funnels through database.

**Security concerns:** Trivial enumeration (`/users/1`, `/users/2`), leaks entity counts, predictable next ID.

**When to use:** Single-database monolithic applications where simplicity matters. Internal-only identifiers not exposed in APIs.

---

### Snowflake IDs (This Toolkit)
- **Sortable by time:** ✅ Yes - 1ms (Twitter/Instagram) or 10ms (Sonyflake) precision
- **Distributed generation:** ✅ Yes - only requires unique node IDs
- **DB index-friendly:** ✅ Excellent - time-ordered, minimal fragmentation
- **Size:** 64-bit (8 bytes) - half the size of UUIDs
- **Throughput:** 4.1-6.5M IDs/sec per node (deterministic limits)

**Database impact:** <5% fragmentation, sequential inserts, 50% smaller indexes than UUIDs, 2-4x faster inserts.

**Coordination:** Node IDs must be unique. Clocks should be synchronized (NTP). No runtime coordination needed.

**When to use:** High-throughput distributed systems, database performance critical, time-range queries common, cost-sensitive deployments.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## References

- [Twitter Snowflake Announcement](https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake)
- [Instagram Engineering Blog](https://instagram-engineering.com/sharding-ids-at-instagram-1cf5a71e5a5c)
- [Sonyflake GitHub](https://github.com/sony/sonyflake)
- [Snowflake ID - Wikipedia](https://en.wikipedia.org/wiki/Snowflake_ID)
