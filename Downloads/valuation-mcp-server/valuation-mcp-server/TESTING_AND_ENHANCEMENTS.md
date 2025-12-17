# Testing & Enhancement Guide

## Quick Start Testing

### Run the Test Suite

**Bash/Git Bash:**
```bash
./test_server.sh
```

**Windows PowerShell:**
```powershell
bash test_server.sh
```

The script will:
- ✅ Test health and manifest endpoints
- ✅ Test basic repository analysis
- ✅ Test deep codebase analysis
- ✅ Test error handling
- ✅ Save all responses to JSON files for review

### Manual Testing Commands

**Full Analysis (Recommended):**
```bash
curl -X POST "https://valuation-mcp-server-554655392699.us-central1.run.app/mcp/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "agent_executor",
    "arguments": {
      "input": "analyze mcpmessenger/slashmcp with deep codebase analysis and calculate the unicorn score"
    }
  }' > full_analysis.json
```

**Quick Health Check:**
```bash
curl https://valuation-mcp-server-554655392699.us-central1.run.app/health
```

## Enhancement Implementation Status

### ✅ Completed
- Test script (`test_server.sh`)
- Enhancement roadmap (`ENHANCEMENT_ROADMAP.md`)
- Package stats tool foundation (`src/tools/package_stats.py`)

### ⏳ Ready to Integrate

**Package Stats Integration** (`src/tools/package_stats.py`)
- ✅ npm download statistics
- ✅ PyPI download statistics  
- ✅ Cargo download statistics
- ✅ Adoption score calculation (0-100)

**Next Steps:**
1. Add `package_stats` tool to MCP manifest in `src/main.py`
2. Integrate into `agent_executor` workflow
3. Add `ecosystem_adoption` component to `unicorn_hunter` scoring
4. Test with real repositories (e.g., `react`, `fastapi`, `serde`)

### 📋 Planned Enhancements

See `ENHANCEMENT_ROADMAP.md` for detailed plans:
1. **Phase 1:** Package Registry Integration (npm/PyPI/Cargo) - **READY**
2. **Phase 2:** Crunchbase API Integration
3. **Phase 3:** Developer Community Engagement (Stack Overflow, Reddit)
4. **Phase 4:** Social Media Tracking & Team Background

## Integration Example

To integrate package stats into the existing workflow:

```python
# In src/main.py, add to agent_executor:
from tools.package_stats import PackageStatsTool

package_stats_tool = PackageStatsTool()

# After analyzing repository:
package_stats = package_stats_tool.get_package_stats(owner, repo)
if package_stats.get("status") == "success":
    result["package_stats"] = package_stats
    adoption_score = package_stats_tool.calculate_adoption_score(package_stats)
    # Add to unicorn score calculation
```

## Validation Checklist

When testing, verify:

- [ ] **Accuracy:** Scores for well-known projects (React, Next.js) are directionally correct
- [ ] **Error Handling:** Invalid repositories return clear error messages
- [ ] **Performance:** Response time < 10 seconds for full analysis
- [ ] **Completeness:** All expected data fields are present in responses
- [ ] **Codebase Analysis:** Deep analysis includes quality, complexity, tests, dependencies
- [ ] **Unicorn Score:** Scores are between 0-100 with meaningful breakdowns

## Current Server Status

**URL:** `https://valuation-mcp-server-554655392699.us-central1.run.app`  
**Version:** 1.2.0  
**Status:** ✅ Operational

**Available Tools:**
1. `analyze_github_repository`
2. `calculate_valuation`
3. `compare_with_market`
4. `agent_executor` (natural language)
5. `analyze_codebase` (NEW)
6. `unicorn_hunter` (enhanced)

## Next Actions

1. **Run test suite** to validate current functionality
2. **Review test results** in generated JSON files
3. **Integrate package stats** (Phase 1 enhancement)
4. **Test enhanced scoring** with package adoption data
5. **Deploy updated version** with package stats integration

## Support

For issues or questions:
- Check `ENHANCEMENT_ROADMAP.md` for implementation details
- Review `QUICK_START.md` for API usage examples
- Test with `test_server.sh` to diagnose problems
