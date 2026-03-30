# v3

V3 represents a fundamental architectural shift: **channel-specific APIs → unified cross-channel API**.

In v2, each advertising channel had its own path prefix (`/amazon/v2/...`, `/walmart/v2/...`, `/dsp/v2/...`). In v3, all channels share a single set of endpoints under `/advertising/` that return results across Amazon, Google, Meta, Walmart, and others from a single call — filtered optionally by `?channel=`.

Additional changes:
- **Read-only**: All write operations (PUT, DELETE, PATCH, /batch) have been removed from the public API. Data mutation is handled by internal systems.
- **Async reports**: Report generation is now job-based — `POST /reports` enqueues a job; poll `GET /jobs/{id}` for status and result URL.
- **New domains**: Catalog (listings, quality scores) and Fulfillment (inventory, eligibility) are new in v3.
- **`/advertising/` prefix**: v2 had `/amazon/v2/`, `/walmart/v2/` etc. v3 groups advertising routes under `/advertising/` (`/advertising/accounts`, `/advertising/campaigns`, etc.).

---

**Legend**

- **Changed**: The endpoint behavior or contract has changed.
- **Endpoint**: The path has changed.
- **Json(In/Out)**: The input/output contract has changed.
- **~**: Not available in v2. New in v3.
- **✗**: Not available in v3. Removed from v2.

---

## **Auth API**

Authentication moved from `/auth/v2/` to `/auth/v3/`. The flow is the same (Azure B2C web-credential), but v3 adds full PKCE support (`code_challenge` / `code_verifier`) and a `state` parameter, making the login flow more secure and compatible with stricter B2C policies.

The token response shape is unchanged — clients that store and forward the `id_token` as `Authorization: Bearer` continue to work without modification.

Path: `/auth/{version}`

| Method | v2              | v3         | Changed          | Endpoint         | Json(In/Out)     |
|--------|-----------------|------------|:----------------:|:----------------:|:----------------:|
| `POST` | /v2/login       | /v3/login    | :material-check: | :material-check: | :material-close: |
| `POST` | /v2/refresh     | /v3/refresh  | :material-check: | :material-check: | :material-close: |
| `POST` | /v2/validate    | /v3/validate | :material-check: | :material-check: | :material-close: |

---

## **Advertising API (Cross-Channel)**

In v2, advertising data was siloed per channel under `/amazon/v2/pipe/`, `/walmart/v2/`, `/dsp/v2/`, etc. In v3, a single set of endpoints returns data across **all channels** (Amazon, Google, Meta, Walmart…), optionally filtered by `?channel=`.

All endpoints are **read-only** (GET). Write operations are not exposed in v3.

### **Accounts**

Path: `/advertising/accounts`

| Method | v2                            | v3                            | Changed          | Endpoint         | Json(In/Out)     |
|--------|-------------------------------|-------------------------------|:----------------:|:----------------:|:----------------:|
| `GET`  | /amazon/v2/accounts           | /advertising/accounts         | :material-check: | :material-check: | :material-check: |
| `GET`  | ~                             | /advertising/accounts/{id}    | :material-close: | :material-close: | :material-close: |

**What changed:** Single cross-channel endpoint replaces the Amazon-only `/amazon/v2/accounts`. Response now includes `channel`, `is_connected`, `linked_channel_id`, pagination cursor. Optional filters: `?channel`, `?is_connected`.

---

### **Campaigns**

Path: `/advertising/campaigns`

| Method | v2                            | v3                              | Changed          | Endpoint         | Json(In/Out)     |
|--------|-------------------------------|---------------------------------|:----------------:|:----------------:|:----------------:|
| `GET`  | /amazon/v2/pipe/campaigns     | /advertising/campaigns          | :material-check: | :material-check: | :material-check: |
| `GET`  | ~                             | /advertising/campaigns/{id}     | :material-close: | :material-close: | :material-close: |

**What changed:** Cross-channel. Response enriched with latest metrics (ROAS, ACOS, spend, impressions, clicks, conversions). Optional filters: `?channel`, `?status`, `?account_id`, `?campaign_type`. The `/adgroup` level from v2 is not exposed in v3.

---

### **Keywords**

Path: `/advertising/keywords`

| Method | v2                            | v3                              | Changed          | Endpoint         | Json(In/Out)     |
|--------|-------------------------------|---------------------------------|:----------------:|:----------------:|:----------------:|
| `GET`  | /amazon/v2/pipe/keyword       | /advertising/keywords           | :material-check: | :material-check: | :material-check: |
| `GET`  | ~                             | /advertising/keywords/{id}      | :material-close: | :material-close: | :material-close: |

**What changed:** Cross-channel. Response includes `match_type`, `bid`, `state`, `campaign_id`, `ad_group_id`. Optional filters: `?channel`, `?status`, `?campaign_id`, `?ad_group_id`.

---

### **Product Targets (removed)**

| Method | v2                            | v3              | Changed | Endpoint | Json(In/Out) |
|--------|-------------------------------|-----------------|:-------:|:--------:|:------------:|
| `GET`  | /amazon/v2/pipe/target        | ✗ (not in v3)   | —       | —        | —            |

**Removed in v3:** Product target data is no longer exposed as a standalone endpoint. Target management is handled by internal systems.

---

### **Removed write operations (v2 → not in v3)**

The following v2 endpoints **do not exist in v3**. All write operations on advertising resources are handled internally.

| Method   | v2 path (examples)                              |
|----------|-------------------------------------------------|
| `PUT`    | /amazon/v2/process/masterlist/{id}              |
| `DELETE` | /amazon/v2/process/masterlist/{id}              |
| `PATCH`  | /amazon/v2/process/masterlist/batch             |
| `PUT`    | /amazon/v2/parameters/products/acos/{id}        |
| `DELETE` | /amazon/v2/parameters/products/acos/{id}        |
| `PUT`    | /amazon/v2/parameters/campaigns/acos/{id}       |
| `DELETE` | /amazon/v2/parameters/campaigns/acos/{id}       |
| `PUT`    | /amazon/v2/products/tags/{id}                   |
| `PUT`    | /amazon/v2/products/info/{id}                   |
| `DELETE` | /amazon/v2/products/info/{id}                   |
| `PUT`    | /amazon/v2/products/inbound-inventory/{id}      |
| `DELETE` | /amazon/v2/products/inbound-inventory/{id}      |
| `PUT`    | /amazon/v2/unmanaged/asins/{id}                 |
| `DELETE` | /amazon/v2/unmanaged/asins/{id}                 |
| `PATCH`  | /amazon/v2/unmanaged/asins/batch                |
| `PUT`    | /amazon/v2/unmanaged/campaigns/{id}             |
| `DELETE` | /amazon/v2/unmanaged/campaigns/{id}             |
| `PATCH`  | /amazon/v2/unmanaged/campaigns/batch            |

---

## **Reports API**

V2 had synchronous, channel-specific report endpoints that returned data inline. V3 introduces an **async job pattern**: submit a report request, receive a `job_id`, and poll until complete.

Path: `/advertising/reports`, `/advertising/jobs`

| Method | v2                                           | v3                               | Changed          | Endpoint         | Json(In/Out)     |
|--------|----------------------------------------------|----------------------------------|:----------------:|:----------------:|:----------------:|
| `POST` | /amazon/v2/pipe/reports                      | /advertising/reports             | :material-check: | :material-check: | :material-check: |
| `GET`  | /amazon/v2/pipe/reports/{reportId}           | /advertising/jobs/{jobId}        | :material-check: | :material-check: | :material-check: |
| `POST` | ~                                            | /advertising/jobs/{jobId}/cancel | :material-close: | :material-close: | :material-close: |
| `POST` | /amazon/v2/report/keyword_branded_competitor | ✗ (not in v3)                    | —                | —                | —                |
| `GET`  | /amazon/v2/report/download/{id}              | ✗ (not in v3)                    | —                | —                | —                |
| `POST` | /amazon/v2/report/product_metrics            | ✗ (not in v3)                    | —                | —                | —                |
| `GET`  | /amazon/v2/report/product_metrics/{id}       | ✗ (not in v3)                    | —                | —                | —                |
| `POST` | /walmart/v2/report/adgroup                   | ✗ (not in v3)                    | —                | —                | —                |
| `POST` | /walmart/v2/report/aditem                    | ✗ (not in v3)                    | —                | —                | —                |
| `POST` | /dsp/v2/report/geo                           | ✗ (not in v3)                    | —                | —                | —                |
| `POST` | /dsp/v2/report/inventory                     | ✗ (not in v3)                    | —                | —                | —                |
| `POST` | /dsp/v2/report/advertiser_metrics            | ✗ (not in v3)                    | —                | —                | —                |

**Job status flow:**
```
POST /advertising/reports  →  202 Accepted  →  { id, status: "pending", poll_url: "/advertising/jobs/{id}" }
GET  /advertising/jobs/{id} →  { status: "pending" | "running" | "completed" | "failed", result_url }
POST /advertising/jobs/{id}/cancel  →  { status: "cancelled" }
```

---

## **Catalog API (new in v3)**

The catalog domain is entirely new in v3. It exposes product listing data and quality scores from Databricks Unity Catalog, unified across channels.

Path: `/catalog`

| Method | v2  | v3                                    | Changed          | Endpoint         | Json(In/Out)     |
|--------|-----|---------------------------------------|:----------------:|:----------------:|:----------------:|
| `GET`  | ~   | /catalog/listings                     | :material-close: | :material-close: | :material-close: |
| `GET`  | ~   | /catalog/listings/{listingId}         | :material-close: | :material-close: | :material-close: |
| `GET`  | ~   | /catalog/listings/{listingId}/quality | :material-close: | :material-close: | :material-close: |

**`/catalog/listings`** returns product listings with status, pricing, inventory level, FBA flag, and parent/child ASIN relationship. Optional filters: `?channel`, `?status`, `?is_parent`, `?account_id`.

**`/catalog/listings/{id}/quality`** returns a quality score (0–100) with individual signal breakdowns: title completeness, description completeness, image count, brand signal. Useful for optimization prioritization.

---

## **Fulfillment API (new in v3)**

Fulfillment endpoints are entirely new in v3. They expose inventory and eligibility data for Quartile's fulfillment optimization features.

Path: `/fulfillment`

| Method | v2  | v3                         | Changed          | Endpoint         | Json(In/Out)     |
|--------|-----|----------------------------|:----------------:|:----------------:|:----------------:|
| `GET`  | ~   | /fulfillment/inventory     | :material-close: | :material-close: | :material-close: |
| `POST` | ~   | /fulfillment/eligibility   | :material-close: | :material-close: | :material-close: |

**`/fulfillment/inventory`** returns FBA and merchant inventory levels per product and channel. Optional filters: `?channel`, `?account_id`, pagination cursor.

**`/fulfillment/eligibility`** accepts a batch of `product_ids` (POST body) and returns per-product eligibility flags (`is_eligible_for_optimization`, `has_fba`). Batch size: up to 100 IDs per request.

---

## **Core API (new in v3)**

| Method | v2  | v3            | Changed          | Endpoint         | Json(In/Out)     |
|--------|-----|---------------|:----------------:|:----------------:|:----------------:|
| `GET`  | ~   | /rate-limits  | :material-close: | :material-close: | :material-close: |

**`/rate-limits`** returns the rate limit tiers (starter / growth / scale / enterprise), operation costs per request type, and the response header reference for `RateLimit-*` headers. Requires `Subscription-Key` and `Authorization` headers.

---

## **Removed channel-specific paths**

The following v2 path families have **no equivalent in v3** because the functionality is either handled by unified cross-channel endpoints or by internal systems:

| v2 path prefix                        | Reason removed in v3                                    |
|---------------------------------------|---------------------------------------------------------|
| `/amazon/v2/process/*`                | Write operations not exposed publicly in v3             |
| `/amazon/v2/parameters/*`             | ACOS parameter management moved to internal systems     |
| `/amazon/v2/products/*`               | Catalog data unified under `/catalog/listings`          |
| `/amazon/v2/unmanaged/*`              | Unmanaged campaign management moved to internal systems |
| `/walmart/v2/report/*`                | Unified under `/reports` async job pattern              |
| `/dsp/v2/report/*`                    | Unified under `/reports` async job pattern              |

---

## **Summary of changes**

| Category          | v2                             | v3                                                          |
|-------------------|--------------------------------|-------------------------------------------------------------|
| Architecture      | Channel-specific paths         | Unified cross-channel under `/advertising/`                 |
| Auth              | `/auth/v2/`                    | `/auth/v3/` + PKCE                                          |
| Advertising reads | `/amazon/v2/pipe/*`            | `/advertising/campaigns`, `/advertising/keywords`           |
| Accounts          | `/amazon/v2/accounts`          | `/advertising/accounts`                                     |
| Reports           | Synchronous, inline data       | Async jobs — `POST /advertising/reports` + poll             |
| Catalog           | Not available                  | `/catalog/listings`, `/catalog/listings/{id}/quality`       |
| Fulfillment       | Not available                  | `/fulfillment/inventory`, `/fulfillment/eligibility`        |
| Product Targets   | `/amazon/v2/pipe/target`       | Removed — handled by internal systems                       |
| Write operations  | Full CRUD on all resources     | Read-only (GET + async POST)                                |
| Route prefix      | `/amazon/v2/`, `/walmart/v2/`  | `/advertising/` for ad data, `/catalog/`, `/fulfillment/`   |
