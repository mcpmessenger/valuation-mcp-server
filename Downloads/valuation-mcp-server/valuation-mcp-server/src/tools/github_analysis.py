import os
import requests
from typing import Dict, Any
from datetime import datetime, timedelta


class GitHubAnalysisTool:
    """Tool for analyzing GitHub repositories"""
    
    def __init__(self, github_token: str = None):
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.headers = {"Authorization": f"token {self.github_token}"} if self.github_token else {}
    
    def analyze_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """Comprehensive repository analysis"""
        try:
            # Fetch repo data
            repo_data = self._fetch_repo_data(owner, repo)
            if not repo_data:
                return {"error": "Repository not found", "status": "failed"}
            
            commit_activity = self._fetch_commit_activity(owner, repo)
            contributor_stats = self._fetch_contributor_stats(owner, repo)
            
            # Calculate metrics
            health_score = self._calculate_health_score(repo_data, commit_activity)
            activity_score = self._calculate_activity_score(commit_activity)
            community_score = self._calculate_community_score(repo_data, contributor_stats)
            
            return {
                "basic_info": {
                    "name": repo_data.get("full_name"),
                    "description": repo_data.get("description"),
                    "primary_language": repo_data.get("language"),
                    "created_at": repo_data.get("created_at"),
                    "updated_at": repo_data.get("updated_at"),
                },
                "metrics": {
                    "stars": repo_data.get("stargazers_count", 0),
                    "forks": repo_data.get("forks_count", 0),
                    "watchers": repo_data.get("watchers_count", 0),
                    "open_issues": repo_data.get("open_issues_count", 0),
                },
                "scores": {
                    "health_score": health_score,
                    "activity_score": activity_score,
                    "community_score": community_score,
                    "overall_score": (health_score + activity_score + community_score) / 3,
                },
                "development": {
                    "total_commits": commit_activity.get("total", 0),
                    "contributors": len(contributor_stats) if contributor_stats else 0,
                    "last_commit_date": commit_activity.get("last_commit"),
                    "commit_frequency": commit_activity.get("weekly_avg", 0),
                }
            }
            
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    def _fetch_repo_data(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch basic repository information"""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{owner}/{repo}",
                headers=self.headers,
                timeout=10
            )
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            print(f"Error fetching repo data: {e}")
            return {}
    
    def _fetch_commit_activity(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch commit activity statistics"""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{owner}/{repo}/stats/commit_activity",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if data:
                    total = sum(week.get("total", 0) for week in data[-8:])  # Last 8 weeks
                    weekly_avg = total / 8 if data else 0
                    last_week = data[-1].get("week") if data else None
                    return {
                        "total": total,
                        "weekly_avg": weekly_avg,
                        "last_commit": last_week
                    }
            return {"total": 0, "weekly_avg": 0, "last_commit": None}
        except Exception as e:
            print(f"Error fetching commit activity: {e}")
            return {"total": 0, "weekly_avg": 0, "last_commit": None}
    
    def _fetch_contributor_stats(self, owner: str, repo: str) -> list:
        """Fetch contributor statistics"""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{owner}/{repo}/contributors",
                headers=self.headers,
                timeout=10
            )
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error fetching contributor stats: {e}")
            return []
    
    def _calculate_health_score(self, repo_data: Dict[str, Any], commit_activity: Dict[str, Any]) -> float:
        """Calculate repository health score (0-1)"""
        score = 0.0
        
        # Has documentation
        if repo_data.get("description"):
            score += 0.2
        
        # Has README
        if repo_data.get("has_wiki") or repo_data.get("description"):
            score += 0.2
        
        # Active maintenance
        if commit_activity.get("weekly_avg", 0) > 0:
            score += 0.2
        
        # Low issue count relative to activity
        open_issues = repo_data.get("open_issues_count", 0)
        if open_issues < 50:
            score += 0.2
        
        # Has license
        if repo_data.get("license"):
            score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_activity_score(self, commit_activity: Dict[str, Any]) -> float:
        """Calculate activity score (0-1)"""
        weekly_avg = commit_activity.get("weekly_avg", 0)
        
        if weekly_avg >= 10:
            return 1.0
        elif weekly_avg >= 5:
            return 0.8
        elif weekly_avg >= 1:
            return 0.6
        elif weekly_avg > 0:
            return 0.4
        else:
            return 0.0
    
    def _calculate_community_score(self, repo_data: Dict[str, Any], contributor_stats: list) -> float:
        """Calculate community score (0-1)"""
        score = 0.0
        
        # Stars
        stars = repo_data.get("stargazers_count", 0)
        if stars >= 1000:
            score += 0.3
        elif stars >= 100:
            score += 0.2
        elif stars >= 10:
            score += 0.1
        
        # Forks
        forks = repo_data.get("forks_count", 0)
        if forks >= 100:
            score += 0.3
        elif forks >= 10:
            score += 0.2
        elif forks >= 1:
            score += 0.1
        
        # Contributors
        contributors = len(contributor_stats) if contributor_stats else 0
        if contributors >= 50:
            score += 0.4
        elif contributors >= 10:
            score += 0.3
        elif contributors >= 1:
            score += 0.2
        
        return min(score, 1.0)
