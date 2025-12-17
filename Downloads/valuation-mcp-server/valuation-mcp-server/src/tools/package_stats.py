"""
Package Registry Statistics Tool
Fetches download statistics from npm, PyPI, and Cargo registries
"""
import os
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class PackageStatsTool:
    """Tool for fetching package download statistics from various registries"""
    
    def __init__(self):
        self.npm_base = "https://api.npmjs.org"
        self.pypi_base = "https://pypistats.org/api"
        self.crates_base = "https://crates.io/api/v1"
    
    def get_package_stats(self, owner: str, repo: str, package_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get package statistics for a repository.
        Attempts to detect package manager and fetch stats.
        
        Args:
            owner: GitHub repository owner
            repo: GitHub repository name
            package_name: Optional explicit package name (if different from repo name)
        
        Returns:
            Dictionary with package stats and registry information
        """
        result = {
            "repository": f"{owner}/{repo}",
            "package_manager": None,
            "package_name": None,
            "stats": {},
            "status": "not_found"
        }
        
        # Try npm first (most common for JS/TS projects)
        npm_stats = self._get_npm_stats(repo, package_name)
        if npm_stats:
            result["package_manager"] = "npm"
            result["package_name"] = npm_stats.get("package_name")
            result["stats"] = npm_stats
            result["status"] = "success"
            return result
        
        # Try PyPI (Python projects)
        pypi_stats = self._get_pypi_stats(repo, package_name)
        if pypi_stats:
            result["package_manager"] = "pypi"
            result["package_name"] = pypi_stats.get("package_name")
            result["stats"] = pypi_stats
            result["status"] = "success"
            return result
        
        # Try Cargo (Rust projects)
        cargo_stats = self._get_cargo_stats(repo, package_name)
        if cargo_stats:
            result["package_manager"] = "cargo"
            result["package_name"] = cargo_stats.get("package_name")
            result["stats"] = cargo_stats
            result["status"] = "success"
            return result
        
        return result
    
    def _get_npm_stats(self, repo_name: str, package_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Fetch npm package download statistics"""
        package = package_name or repo_name
        
        try:
            # Try to get package info first
            info_url = f"https://registry.npmjs.org/{package}"
            info_response = requests.get(info_url, timeout=5)
            
            if info_response.status_code == 404:
                return None
            
            if info_response.status_code != 200:
                return None
            
            package_info = info_response.json()
            
            # Get download stats for last week
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            downloads_url = f"{self.npm_base}/downloads/range/{start_date.strftime('%Y-%m-%d')}:{end_date.strftime('%Y-%m-%d')}/{package}"
            downloads_response = requests.get(downloads_url, timeout=5)
            
            weekly_downloads = 0
            if downloads_response.status_code == 200:
                downloads_data = downloads_response.json()
                downloads = downloads_data.get("downloads", [])
                weekly_downloads = sum(d.get("downloads", 0) for d in downloads)
            
            # Get package metadata
            latest_version = package_info.get("dist-tags", {}).get("latest", "unknown")
            versions = list(package_info.get("versions", {}).keys())
            
            return {
                "package_name": package,
                "latest_version": latest_version,
                "total_versions": len(versions),
                "weekly_downloads": weekly_downloads,
                "registry": "npm",
                "package_url": f"https://www.npmjs.com/package/{package}"
            }
        except Exception as e:
            return None
    
    def _get_pypi_stats(self, repo_name: str, package_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Fetch PyPI package download statistics"""
        package = package_name or repo_name
        
        try:
            # PyPI Stats API
            stats_url = f"{self.pypi_base}/packages/{package}/overall"
            response = requests.get(stats_url, timeout=5)
            
            if response.status_code == 404:
                return None
            
            if response.status_code != 200:
                return None
            
            stats_data = response.json()
            
            # Calculate monthly downloads from recent data
            monthly_downloads = 0
            if "data" in stats_data:
                recent_data = stats_data["data"].get("last_month", 0)
                monthly_downloads = recent_data
            
            return {
                "package_name": package,
                "monthly_downloads": monthly_downloads,
                "registry": "pypi",
                "package_url": f"https://pypi.org/project/{package}/"
            }
        except Exception as e:
            return None
    
    def _get_cargo_stats(self, repo_name: str, package_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Fetch Cargo (Rust) package download statistics"""
        package = package_name or repo_name
        
        try:
            # Cargo API
            crate_url = f"{self.crates_base}/crates/{package}"
            response = requests.get(crate_url, timeout=5)
            
            if response.status_code == 404:
                return None
            
            if response.status_code != 200:
                return None
            
            crate_data = response.json()
            crate_info = crate_data.get("crate", {})
            
            # Get download stats
            downloads = crate_info.get("downloads", 0)
            recent_downloads = crate_info.get("recent_downloads", 0)
            
            return {
                "package_name": package,
                "total_downloads": downloads,
                "recent_downloads": recent_downloads,
                "latest_version": crate_info.get("max_version", "unknown"),
                "registry": "cargo",
                "package_url": f"https://crates.io/crates/{package}"
            }
        except Exception as e:
            return None
    
    def calculate_adoption_score(self, stats: Dict[str, Any]) -> float:
        """
        Calculate an adoption score (0-100) based on package statistics.
        
        Scoring:
        - npm: Based on weekly downloads
        - PyPI: Based on monthly downloads
        - Cargo: Based on total and recent downloads
        """
        if not stats or stats.get("status") != "success":
            return 0.0
        
        package_manager = stats.get("package_manager")
        package_stats = stats.get("stats", {})
        
        if package_manager == "npm":
            weekly_downloads = package_stats.get("weekly_downloads", 0)
            # Score: 0-100 based on weekly downloads
            # 100k+ downloads/week = 100, 10k = 50, 1k = 25, 100 = 10, 0 = 0
            if weekly_downloads >= 100000:
                return 100.0
            elif weekly_downloads >= 10000:
                return 50.0 + (weekly_downloads / 10000) * 50.0
            elif weekly_downloads >= 1000:
                return 25.0 + ((weekly_downloads - 1000) / 9000) * 25.0
            elif weekly_downloads >= 100:
                return 10.0 + ((weekly_downloads - 100) / 900) * 15.0
            else:
                return min(10.0, weekly_downloads / 10.0)
        
        elif package_manager == "pypi":
            monthly_downloads = package_stats.get("monthly_downloads", 0)
            # Similar scoring for PyPI
            if monthly_downloads >= 500000:
                return 100.0
            elif monthly_downloads >= 50000:
                return 50.0 + (monthly_downloads / 50000) * 50.0
            elif monthly_downloads >= 5000:
                return 25.0 + ((monthly_downloads - 5000) / 45000) * 25.0
            elif monthly_downloads >= 500:
                return 10.0 + ((monthly_downloads - 500) / 4500) * 15.0
            else:
                return min(10.0, monthly_downloads / 50.0)
        
        elif package_manager == "cargo":
            total_downloads = package_stats.get("total_downloads", 0)
            recent_downloads = package_stats.get("recent_downloads", 0)
            # Combine total and recent for score
            if total_downloads >= 1000000:
                base_score = 100.0
            elif total_downloads >= 100000:
                base_score = 50.0 + ((total_downloads - 100000) / 900000) * 50.0
            elif total_downloads >= 10000:
                base_score = 25.0 + ((total_downloads - 10000) / 90000) * 25.0
            else:
                base_score = min(25.0, total_downloads / 400.0)
            
            # Boost for recent activity
            recent_boost = min(20.0, recent_downloads / 1000.0)
            return min(100.0, base_score + recent_boost)
        
        return 0.0
