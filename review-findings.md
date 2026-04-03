# Code Review Findings: TransportabilityCalc

**Reviewer**: Claude Opus 4.6 (1M context)
**Date**: 2026-04-03
**Files reviewed**: `transportability-calc.html` (1,856 lines), `index.html` (44 lines)

## P0 (Critical) -- 0 found

No critical issues. The app already has:
- `csvSafe()` function with proper formula injection protection (line 872-882): checks for `=`, `+`, `@`, `\t`, `\r` prefixes
- `escapeHtml()` function (line 865-869)
- Skip-nav link (line 434)
- Proper ARIA tabs with keyboard navigation (ArrowLeft/Right, Home, End)
- Proper `</html>` closing tag
- `URL.revokeObjectURL()` after blob download

## P1 (Important) -- 2 found

### P1-1: Temporal penalty allows negative gap to produce penalty > 1
- **File**: `transportability-calc.html`, line 924
- **Issue**: `temporalGap = inputs.targetYear - inputs.yearMedian` -- if target year is BEFORE the median trial year, `temporalGap` is negative, `Math.max(0, temporalGap)` becomes 0, so `temporalPenalty = 1.0`. This is correct behavior (applying evidence to the past is not penalized).
- **Status**: Correct.

### P1-2: Effect adjustment uses simple multiplicative scaling
- **File**: `transportability-calc.html`, lines 1122-1124
- **Issue**: `adjEffect = inputs.effect * penalty.overall` applies the penalty directly to the effect estimate. This is a simplification -- real transportability adjustment would use IOSW or target trial emulation. The paper acknowledges this as a demonstration.
- **Status**: Acceptable for the tool's purpose.

## P2 (Minor) -- 1 found

### P2-1: localStorage key is unique (`transport-calc-data`)

## Summary
- P0: 0 | P1: 2 | P2: 1
- Best-practice app: skip-nav, csvSafe, escapeHtml, ARIA, keyboard nav all present.
