# Bounty PR Template - iota-rust-sdk #496

Use this template when opening PR for:
- Issue: https://github.com/iotaledger/iota-rust-sdk/issues/496
- Goal: Add Android support to Kotlin bindings

---

## Linked Issue
Fixes https://github.com/iotaledger/iota-rust-sdk/issues/496

## Scope
- [ ] Update Kotlin bindings project settings for Android usage
- [ ] Update release/build process for Android-compatible artifacts
- [ ] Add Android section in Kotlin README
- [ ] Add minimal Android demo app with one IOTA API call

## What Changed
### 1) Build & Packaging
- Describe gradle/cargo/uniffi/CI changes
- List exact files touched

### 2) Android Support
- Describe Android compatibility settings (minSdk/abi/aar/jni, etc.)
- Explain how SDK is consumed by Android app

### 3) Documentation
- Added/updated docs:
  - Setup steps
  - Known limitations
  - Troubleshooting

### 4) Demo App
- Demo location:
- API call used:
- Expected output:

## Test Plan
### Local checks
- [ ] Build bindings locally
- [ ] Build Android demo app
- [ ] Run demo and verify successful API response

### CI checks
- [ ] Relevant CI jobs are green
- [ ] No lint/test regressions

### Manual validation
- Device/Emulator:
- Android version:
- Result:

## Evidence
Attach concrete proof:
- [ ] Build logs (bindings + Android)
- [ ] Screenshot or video of demo app call result
- [ ] Output snippet showing successful SDK/API call

## Risk & Rollback
- Main risks:
- Rollback approach:

## Review Notes (for maintainers)
- Design decisions and tradeoffs:
- Areas needing special attention:

## Follow-up (optional)
- Future improvements not included in this PR:
