from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class ValuationMethod(Enum):
    COST_BASED = "cost_based"
    MARKET_BASED = "market_based"
    INCOME_BASED = "income_based"
    SCORECARD = "scorecard"
    UNICORN_HUNTER = "unicorn_hunter"


@dataclass
class ValuationInputs:
    repo_data: Dict[str, Any]
    team_size: int = 1
    hourly_rate: float = 100.0
    development_months: int = 6
    market_multiplier: float = 10.0


class ValuationCalculator:
    """Multiple valuation methodologies"""
    
    def calculate_cost_based(self, inputs: ValuationInputs) -> float:
        """Calculate development cost replacement value"""
        dev_hours = inputs.team_size * 160 * inputs.development_months  # 160 hours/month
        return dev_hours * inputs.hourly_rate
    
    def calculate_market_based(self, inputs: ValuationInputs, comparable_data: List[Dict] = None) -> float:
        """Calculate value based on market comparables"""
        if not comparable_data:
            comparable_data = []
        
        if not comparable_data:
            # Default multiplier based on stars
            stars = inputs.repo_data.get("metrics", {}).get("stars", 0)
            return stars * 1000 * inputs.market_multiplier
        
        # Average stars per dollar from comparables
        total_value = sum(comp.get("value", 0) for comp in comparable_data)
        total_stars = sum(comp.get("stars", 1) for comp in comparable_data)
        
        if total_stars == 0:
            return 0.0
        
        stars_per_dollar = total_value / total_stars
        repo_stars = inputs.repo_data.get("metrics", {}).get("stars", 0)
        
        return repo_stars * stars_per_dollar * inputs.market_multiplier
    
    def calculate_scorecard(self, inputs: ValuationInputs) -> Dict[str, Any]:
        """Scorecard valuation method"""
        factors = {
            "technology_quality": 0.25,
            "market_opportunity": 0.20,
            "development_team": 0.15,
            "competitive_position": 0.15,
            "deployment_readiness": 0.15,
            "documentation": 0.10,
        }
        
        scores = {}
        
        # Sample scoring logic
        repo_metrics = inputs.repo_data.get("metrics", {})
        repo_scores = inputs.repo_data.get("scores", {})
        
        # Technology quality based on overall score
        overall_score = repo_scores.get("overall_score", 0.5)
        scores["technology_quality"] = min(overall_score, 1.0) * factors["technology_quality"]
        
        # Market opportunity based on stars and forks
        stars = repo_metrics.get("stars", 0)
        forks = repo_metrics.get("forks", 0)
        market_potential = min((stars + forks) / 1000, 1.0)
        scores["market_opportunity"] = market_potential * factors["market_opportunity"]
        
        # Development team based on contributors
        dev_info = inputs.repo_data.get("development", {})
        contributors = dev_info.get("contributors", 0)
        team_score = min(contributors / 50, 1.0)
        scores["development_team"] = team_score * factors["development_team"]
        
        # Competitive position based on activity
        activity_score = repo_scores.get("activity_score", 0.5)
        scores["competitive_position"] = activity_score * factors["competitive_position"]
        
        # Deployment readiness (assuming good deployment)
        scores["deployment_readiness"] = 0.8 * factors["deployment_readiness"]
        
        # Documentation based on health score
        health_score = repo_scores.get("health_score", 0.5)
        scores["documentation"] = health_score * factors["documentation"]
        
        total_score = sum(scores.values())
        
        # Base valuation range
        base_range = {
            "low": max(10000 * total_score, 5000),
            "medium": max(50000 * total_score, 25000),
            "high": max(250000 * total_score, 100000),
        }
        
        return {
            "total_score": round(total_score, 3),
            "factor_scores": {k: round(v, 3) for k, v in scores.items()},
            "valuation_range": {k: round(v, 2) for k, v in base_range.items()},
            "method": "scorecard"
        }
    
    def calculate_income_based(self, inputs: ValuationInputs, annual_revenue: float = 0) -> Dict[str, Any]:
        """Calculate value based on income approach"""
        if annual_revenue <= 0:
            # Estimate based on activity and community
            stars = inputs.repo_data.get("metrics", {}).get("stars", 0)
            estimated_revenue = stars * 100  # $100 per star as rough estimate
        else:
            estimated_revenue = annual_revenue
        
        # Apply discount rate and multiple
        discount_rate = 0.15  # 15% discount rate
        revenue_multiple = 3  # 3x revenue multiple
        
        valuation = estimated_revenue * revenue_multiple / (1 + discount_rate)
        
        return {
            "estimated_annual_revenue": round(estimated_revenue, 2),
            "revenue_multiple": revenue_multiple,
            "discount_rate": discount_rate,
            "valuation": round(valuation, 2),
            "method": "income_based"
        }
    
    def calculate_unicorn_hunter(self, inputs: ValuationInputs, codebase_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        🦄 Unicorn Hunter: Speculative valuation with $1B maximum
        Calculates a unicorn score (0-100) and speculative valuation ranges
        Now enhanced with codebase analysis when available
        """
        repo_metrics = inputs.repo_data.get("metrics", {})
        repo_scores = inputs.repo_data.get("scores", {})
        dev_info = inputs.repo_data.get("development", {})
        has_codebase_analysis = codebase_analysis is not None and codebase_analysis.get("status") == "success"
        
        # Calculate component scores (0-100 each)
        scores = {}
        
        # 1. Community Momentum (0-100)
        stars = repo_metrics.get("stars", 0)
        forks = repo_metrics.get("forks", 0)
        watchers = repo_metrics.get("watchers", 0)
        
        # Logarithmic scaling for community metrics
        # Stars: 100k+ = 100, 10k+ = 80, 1k+ = 60, 100+ = 40, 10+ = 20
        star_score = min(100, max(0, 20 * (1 + (stars / 1000) ** 0.3)))
        fork_score = min(100, max(0, 15 * (1 + (forks / 500) ** 0.3)))
        watcher_score = min(100, max(0, 10 * (1 + (watchers / 200) ** 0.3)))
        community_momentum = (star_score * 0.5 + fork_score * 0.3 + watcher_score * 0.2)
        scores["community_momentum"] = round(community_momentum, 1)
        
        # 2. Development Velocity (0-100)
        contributors = dev_info.get("contributors", 0)
        total_commits = dev_info.get("total_commits", 0)
        commit_frequency = dev_info.get("commit_frequency", 0)
        
        contributor_score = min(100, max(0, 30 * (1 + (contributors / 50) ** 0.4)))
        commit_score = min(100, max(0, 40 * (1 + (total_commits / 1000) ** 0.3)))
        frequency_score = min(100, max(0, 30 * (1 + (commit_frequency / 10) ** 0.5)))
        development_velocity = (contributor_score * 0.3 + commit_score * 0.4 + frequency_score * 0.3)
        scores["development_velocity"] = round(development_velocity, 1)
        
        # 3. Technology Quality (0-100) - ENHANCED with codebase analysis
        overall_score = repo_scores.get("overall_score", 0.5)
        health_score = repo_scores.get("health_score", 0.5)
        activity_score = repo_scores.get("activity_score", 0.5)
        base_tech_quality = (overall_score * 0.4 + health_score * 0.3 + activity_score * 0.3) * 100
        
        # Enhance with codebase analysis if available
        if has_codebase_analysis:
            quality_scores = codebase_analysis.get("quality_scores", {})
            architecture = codebase_analysis.get("architecture", {})
            dependencies = codebase_analysis.get("dependencies", {})
            
            # Code quality component (40% of tech quality)
            maintainability = quality_scores.get("maintainability_index", 50)
            code_quality_score = maintainability * 0.4
            
            # Architecture component (30% of tech quality)
            modularity = architecture.get("modularity_score", 5) * 10  # Convert 0-10 to 0-100
            coupling = architecture.get("coupling_score", 5)
            cohesion = architecture.get("cohesion_score", 5) * 10
            arch_score = (modularity * 0.4 + (10 - coupling) * 10 * 0.3 + cohesion * 0.3) * 0.3
            
            # Dependency health component (30% of tech quality)
            vulns = dependencies.get("security_vulnerabilities", 0)
            outdated_pct = dependencies.get("outdated_percentage", 0)
            dep_score = max(0, 100 - (vulns * 5) - (outdated_pct * 0.5)) * 0.3
            
            technology_quality = base_tech_quality * 0.3 + code_quality_score + arch_score + dep_score
        else:
            technology_quality = base_tech_quality
        
        scores["technology_quality"] = round(technology_quality, 1)
        
        # 4. Market Potential (0-100)
        # Based on stars growth potential and category
        market_potential = min(100, max(0, 25 * (1 + (stars / 5000) ** 0.4) + 
                                        20 * (1 + (forks / 1000) ** 0.4) +
                                        15 * (1 + (contributors / 100) ** 0.3)))
        scores["market_potential"] = round(market_potential, 1)
        
        # 5. Network Effects (0-100)
        # Based on forks (adoption) and watchers (interest)
        network_effects = min(100, max(0, 50 * (1 + (forks / 2000) ** 0.3) +
                                      50 * (1 + (watchers / 500) ** 0.3)))
        scores["network_effects"] = round(network_effects, 1)
        
        # NEW: Code Quality Score (0-100) - from codebase analysis
        if has_codebase_analysis:
            quality_scores = codebase_analysis.get("quality_scores", {})
            test_coverage = codebase_analysis.get("test_coverage", {})
            documentation = codebase_analysis.get("documentation", {})
            
            maintainability = quality_scores.get("maintainability_index", 50)
            test_cov = test_coverage.get("overall_coverage", 0)
            doc_quality = documentation.get("readme_quality_score", 0) * 10  # Convert 0-10 to 0-100
            
            code_quality = (maintainability * 0.4 + test_cov * 0.35 + doc_quality * 0.25)
            scores["code_quality"] = round(code_quality, 1)
            scores["maintainability"] = round(maintainability, 1)
            scores["test_reliability"] = round(test_cov, 1)
            
            # Security Posture (0-100)
            dependencies = codebase_analysis.get("dependencies", {})
            vulns = dependencies.get("security_vulnerabilities", 0)
            critical_vulns = dependencies.get("critical_vulnerabilities", 0)
            security_score = max(0, 100 - (critical_vulns * 20) - (vulns * 5))
            scores["security_posture"] = round(security_score, 1)
        else:
            # Default scores when no codebase analysis
            scores["code_quality"] = 0
            scores["maintainability"] = 0
            scores["test_reliability"] = 0
            scores["security_posture"] = 0
        
        # Calculate weighted unicorn score (0-100)
        # Updated weights to include codebase analysis
        if has_codebase_analysis:
            weights = {
                "community_momentum": 0.25,
                "development_velocity": 0.15,  # Reduced from 0.20
                "technology_quality": 0.20,
                "market_potential": 0.15,  # Reduced from 0.20
                "network_effects": 0.10,  # Reduced from 0.15
                "code_quality": 0.10,  # NEW
                "security_posture": 0.05  # NEW
            }
        else:
            weights = {
                "community_momentum": 0.25,
                "development_velocity": 0.20,
                "technology_quality": 0.20,
                "market_potential": 0.20,
                "network_effects": 0.15
            }
        
        # Only sum scores that are in weights (to avoid KeyError)
        unicorn_score = sum(scores[key] * weights[key] for key in weights.keys() if key in scores)
        unicorn_score = round(unicorn_score, 1)
        
        # Calculate speculative valuation ranges (capped at $1B)
        # Use exponential scaling: score^2.5 * 10M gives good distribution
        # Score of 100 = $1B, score of 50 = ~$88M, score of 25 = ~$9.8M
        max_valuation = 1_000_000_000  # $1B cap
        
        # Conservative estimate (lower bound)
        conservative = min(max_valuation, max(0, (unicorn_score / 100) ** 2.2 * 5_000_000))
        
        # Realistic estimate (midpoint)
        realistic = min(max_valuation, max(0, (unicorn_score / 100) ** 2.5 * 10_000_000))
        
        # Optimistic estimate (upper bound)
        optimistic = min(max_valuation, max(0, (unicorn_score / 100) ** 2.8 * 20_000_000))
        
        # Determine unicorn status
        if unicorn_score >= 90:
            status = "🦄 UNICORN ALERT! ($1B+ potential)"
            tier = "unicorn"
        elif unicorn_score >= 75:
            status = "🚀 Soaring! ($500M+ potential)"
            tier = "soaring"
        elif unicorn_score >= 60:
            status = "⭐ Rising Star ($100M+ potential)"
            tier = "rising_star"
        elif unicorn_score >= 45:
            status = "📈 Promising ($10M+ potential)"
            tier = "promising"
        elif unicorn_score >= 30:
            status = "🌱 Early Stage ($1M+ potential)"
            tier = "early_stage"
        else:
            status = "💡 Seed Stage ($100K+ potential)"
            tier = "seed_stage"
        
        result = {
            "method": "unicorn_hunter",
            "unicorn_score": unicorn_score,
            "status": status,
            "tier": tier,
            "component_scores": scores,
            "speculative_valuation_ranges": {
                "conservative": round(conservative, 2),
                "realistic": round(realistic, 2),
                "optimistic": round(optimistic, 2),
                "maximum_cap": max_valuation,
                "currency": "USD"
            },
            "interpretation": {
                "score_meaning": f"Score of {unicorn_score}/100 indicates {status.lower()}",
                "valuation_note": "These are speculative estimates based on GitHub metrics and should not be considered financial advice.",
                "factors_considered": list(scores.keys())
            }
        }
        
        # Add codebase analysis if available
        if has_codebase_analysis:
            result["codebase_analysis"] = codebase_analysis
            # Enhance interpretation with codebase insights
            code_quality = scores.get("code_quality", 0)
            test_cov = scores.get("test_reliability", 0)
            security = scores.get("security_posture", 0)
            vulns = codebase_analysis.get("dependencies", {}).get("security_vulnerabilities", 0)
            
            result["interpretation"]["valuation_note"] = (
                f"These are speculative estimates based on GitHub metrics and codebase analysis. "
                f"Code quality score: {code_quality}/100. Test coverage: {test_cov}%. "
                f"Security vulnerabilities: {vulns} critical."
            )
        
        return result
