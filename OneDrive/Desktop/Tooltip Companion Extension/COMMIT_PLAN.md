# Operation Juicebox - Commit Plan

## 🎯 Strategy: Separate Safe Changes from Experimental

**Goal:** Commit Phase 1 & 2 (proven) separately from workflow analysis (experimental)

## ✅ Safe to Commit (Phase 1 & 2 + Template System)

These changes are tested and ready:

### Files to Commit:
1. **`tooltip-template.js`** (NEW) - Unified template system ✅
2. **`docs/PURPOSE_AND_VISION.md`** (NEW) - Vision document ✅
3. **`docs/OPERATION_JUICEBOX_STATUS.md`** (NEW) - Status summary ✅
4. **`docs/OPERATION_JUICEBOX.md`** (UPDATED) - Updated with latest status ✅
5. **`content.js`** (MODIFIED) - Template integration, chat improvements ✅
6. **`manifest.json`** (MODIFIED) - Added template script ✅

### Backend Files (Phase 1 & 2 only):
7. **`playwright_service/server.js`** (MODIFIED) - BUT need to revert workflow analysis parts
8. **`playwright_service/mcp-server.js`** (MODIFIED) - Context passing improvements ✅

## ⚠️ Hold Back (Experimental - Needs Testing)

### Workflow Analysis (Not Ready):
- ❌ `playwright_service/server.js` - Workflow detection functions (lines ~442-574)
- ❌ `playwright_service/server.js` - Enhanced system prompt (workflow-focused)
- ❌ Workflow step extraction logic

**Why:** These are new features that haven't been tested on real sites yet.

## 📋 Recommended Commit Steps

### Option A: Two-Stage Commit (Recommended)

**Stage 1: Commit Safe Changes**
```bash
# Add safe files
git add tooltip-template.js
git add docs/PURPOSE_AND_VISION.md
git add docs/OPERATION_JUICEBOX_STATUS.md
git add docs/OPERATION_JUICEBOX.md
git add content.js
git add manifest.json
git add playwright_service/mcp-server.js

# Commit with message
git commit -m "🧃 Operation Juicebox: Phase 1 & 2 complete + template system

- ✅ Unified template system (tooltip-template.js)
- ✅ Enhanced chat intelligence (context-aware)
- ✅ Phase 1: Backend stabilization (logging, retry, circuit breaker)
- ✅ Phase 2: CSP-aware fallback (data URIs, buffer normalization)
- 📝 Added status documentation and vision doc

Ready for production deployment"
```

**Stage 2: Revert Workflow Analysis (or keep separate branch)**
```bash
# Option 1: Revert workflow changes from server.js
git checkout HEAD -- playwright_service/server.js
# Then manually re-add only Phase 1 & 2 changes

# Option 2: Create separate branch for workflow analysis
git checkout -b feature/workflow-analysis
# Keep workflow changes here for testing
```

### Option B: Commit Everything (Risky)

If you want to commit everything including experimental workflow analysis:
```bash
git add .
git commit -m "🧃 Operation Juicebox: Phase 1 & 2 + experimental workflow analysis

- ✅ Phase 1 & 2 complete (tested, ready for deployment)
- 🧪 Experimental: Workflow detection and step extraction
- ⚠️ Workflow analysis needs testing before production deployment"
```

## 🚀 After Committing

1. **Push to GitHub:**
   ```bash
   git push origin operation-juicebox-v1.5
   ```

2. **Deploy Phase 1 & 2:**
   - Deploy backend with resilience + CSP fixes
   - Test in production
   - Monitor CloudWatch alarms

3. **Test Workflow Analysis (if committed):**
   - Test locally on real sites
   - Validate workflow detection accuracy
   - Refine before production

## 📝 Commit Message Template

```
🧃 Operation Juicebox: [Phase/Feature Name]

- ✅ [What's complete and tested]
- 🧪 [What's experimental]
- 📝 [Documentation updates]

Status: [Ready for deployment / Needs testing]
```

