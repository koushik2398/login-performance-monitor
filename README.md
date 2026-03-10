# Login Performance Monitoring System

## Project Overview
Built a high-concurrency login system to simulate and resolve real-world database performance issues.

## Problem
500+ concurrent users caused login response time to spike from 200ms to 9800ms due to missing database index on 1 million user records.

## Solution
- Identified missing SQL index using query analysis
- Added index on username column
- Implemented connection pooling
- Response time reduced from 9800ms to under 200ms

## Tech Stack
- Python (Flask) — Login web application
- MS SQL Server — Database with 1M user records
- Locust — Load testing (500 concurrent users)
- Prometheus — Metrics collection
- Grafana — Performance dashboard
- Docker — Container management
- Git/GitHub — Version control

## Results
| Metric | Before Fix | After Fix |
|--------|-----------|-----------|
| Median Response | 7100ms | ~150ms |
| Max Response | 9795ms | ~300ms |
| Failures | High | Zero |
