import pytest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tools.github_analysis import GitHubAnalysisTool
from tools.valuation_models import ValuationCalculator, ValuationInputs


class TestGitHubAnalysisTool:
    """Tests for GitHub analysis tool"""
    
    @pytest.fixture
    def github_tool(self):
        return GitHubAnalysisTool()
    
    def test_github_tool_initialization(self, github_tool):
        """Test that GitHub tool initializes correctly"""
        assert github_tool.base_url == "https://api.github.com"
        assert github_tool.headers is not None
    
    @patch('tools.github_analysis.requests.get')
    def test_fetch_repo_data(self, mock_get, github_tool):
        """Test fetching repository data"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "full_name": "test/repo",
            "description": "Test repository",
            "stargazers_count": 100
        }
        mock_get.return_value = mock_response
        
        result = github_tool._fetch_repo_data("test", "repo")
        assert result["full_name"] == "test/repo"
        assert result["stargazers_count"] == 100
    
    def test_calculate_health_score(self, github_tool):
        """Test health score calculation"""
        repo_data = {
            "description": "Test repo",
            "has_wiki": True,
            "open_issues_count": 10,
            "license": {"name": "MIT"}
        }
        commit_activity = {"weekly_avg": 5}
        
        score = github_tool._calculate_health_score(repo_data, commit_activity)
        assert 0 <= score <= 1.0
    
    def test_calculate_activity_score(self, github_tool):
        """Test activity score calculation"""
        # High activity
        score_high = github_tool._calculate_activity_score({"weekly_avg": 15})
        assert score_high == 1.0
        
        # Medium activity
        score_medium = github_tool._calculate_activity_score({"weekly_avg": 5})
        assert 0.5 < score_medium < 1.0
        
        # Low activity
        score_low = github_tool._calculate_activity_score({"weekly_avg": 0})
        assert score_low == 0.0
    
    def test_calculate_community_score(self, github_tool):
        """Test community score calculation"""
        repo_data = {
            "stargazers_count": 500,
            "forks_count": 50
        }
        contributors = [{"login": f"user{i}"} for i in range(20)]
        
        score = github_tool._calculate_community_score(repo_data, contributors)
        assert 0 <= score <= 1.0


class TestValuationCalculator:
    """Tests for valuation calculator"""
    
    @pytest.fixture
    def calculator(self):
        return ValuationCalculator()
    
    @pytest.fixture
    def sample_repo_data(self):
        return {
            "metrics": {
                "stars": 100,
                "forks": 20,
                "watchers": 10,
                "open_issues": 5
            },
            "scores": {
                "health_score": 0.8,
                "activity_score": 0.7,
                "community_score": 0.6,
                "overall_score": 0.7
            },
            "development": {
                "total_commits": 200,
                "contributors": 5,
                "last_commit_date": "2024-12-16",
                "commit_frequency": 3.5
            }
        }
    
    def test_cost_based_valuation(self, calculator, sample_repo_data):
        """Test cost-based valuation calculation"""
        inputs = ValuationInputs(
            repo_data=sample_repo_data,
            team_size=2,
            hourly_rate=100.0,
            development_months=6
        )
        
        valuation = calculator.calculate_cost_based(inputs)
        # 2 team members * 160 hours/month * 6 months * $100/hour = $192,000
        assert valuation == 192000.0
    
    def test_market_based_valuation(self, calculator, sample_repo_data):
        """Test market-based valuation calculation"""
        inputs = ValuationInputs(
            repo_data=sample_repo_data,
            market_multiplier=10.0
        )
        
        valuation = calculator.calculate_market_based(inputs)
        # Should be based on stars * multiplier
        assert isinstance(valuation, (int, float))
        assert valuation > 0
    
    def test_scorecard_valuation(self, calculator, sample_repo_data):
        """Test scorecard valuation calculation"""
        inputs = ValuationInputs(repo_data=sample_repo_data)
        
        result = calculator.calculate_scorecard(inputs)
        assert "total_score" in result
        assert "factor_scores" in result
        assert "valuation_range" in result
        assert result["method"] == "scorecard"
        
        # Check valuation range
        valuation_range = result["valuation_range"]
        assert valuation_range["low"] <= valuation_range["medium"]
        assert valuation_range["medium"] <= valuation_range["high"]
    
    def test_income_based_valuation(self, calculator, sample_repo_data):
        """Test income-based valuation calculation"""
        inputs = ValuationInputs(repo_data=sample_repo_data)
        
        result = calculator.calculate_income_based(inputs)
        assert "estimated_annual_revenue" in result
        assert "valuation" in result
        assert result["method"] == "income_based"
        assert result["valuation"] > 0
    
    def test_valuation_inputs_dataclass(self, sample_repo_data):
        """Test ValuationInputs dataclass"""
        inputs = ValuationInputs(
            repo_data=sample_repo_data,
            team_size=3,
            hourly_rate=150.0,
            development_months=12,
            market_multiplier=15.0
        )
        
        assert inputs.team_size == 3
        assert inputs.hourly_rate == 150.0
        assert inputs.development_months == 12
        assert inputs.market_multiplier == 15.0


class TestIntegration:
    """Integration tests"""
    
    def test_full_analysis_workflow(self):
        """Test complete analysis workflow"""
        github_tool = GitHubAnalysisTool()
        calculator = ValuationCalculator()
        
        # Create sample repo data
        repo_data = {
            "metrics": {
                "stars": 250,
                "forks": 50,
                "watchers": 30,
                "open_issues": 8
            },
            "scores": {
                "health_score": 0.85,
                "activity_score": 0.8,
                "community_score": 0.75,
                "overall_score": 0.8
            },
            "development": {
                "total_commits": 500,
                "contributors": 15,
                "last_commit_date": "2024-12-16",
                "commit_frequency": 8.5
            }
        }
        
        # Test all valuation methods
        inputs = ValuationInputs(repo_data=repo_data)
        
        cost_valuation = calculator.calculate_cost_based(inputs)
        assert cost_valuation > 0
        
        market_valuation = calculator.calculate_market_based(inputs)
        assert market_valuation > 0
        
        scorecard_result = calculator.calculate_scorecard(inputs)
        assert scorecard_result["total_score"] > 0
        
        income_result = calculator.calculate_income_based(inputs)
        assert income_result["valuation"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
