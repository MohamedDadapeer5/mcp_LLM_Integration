#!/usr/bin/env python3
"""
Verify MCP Q&A Bot Setup
This script checks that all files are in place and the server can start
"""

import os
import sys
from pathlib import Path

def check_file(path, description):
    """Check if a file exists"""
    if Path(path).exists():
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description} NOT FOUND: {path}")
        return False

def main():
    print("\n" + "="*70)
    print("  MCP Q&A Bot - Setup Verification")
    print("="*70 + "\n")
    
    # Get script directory
    script_dir = Path(__file__).parent
    print(f"📂 Working directory: {script_dir}\n")
    
    all_ok = True
    
    # Check core files
    print("Checking Core Files:")
    print("-" * 70)
    all_ok &= check_file(script_dir / "src" / "fastmcp_server.py", "FastMCP Server")
    all_ok &= check_file(script_dir / "requirements.txt", "Requirements")
    print()
    
    # Check optional Docker files (Challenge 2)
    print("Checking Docker Files (Optional - Challenge 2):")
    print("-" * 70)
    check_file(script_dir / "Dockerfile", "Dockerfile")
    check_file(script_dir / "docker-compose.yml", "Docker Compose")
    print()
    
    # Check configs
    print("Checking Configuration Files:")
    print("-" * 70)
    configs = ["banking", "healthcare", "saas", "government", "telecom"]
    for config in configs:
        all_ok &= check_file(script_dir / "configs" / f"{config}.yaml", f"{config.capitalize()} config")
    print()
    
    # Check knowledge bases
    print("Checking Knowledge Base Files:")
    print("-" * 70)
    for config in configs:
        kb_file = script_dir / "knowledge" / f"{config}-kb.yaml"
        # Check for common typo: healthcare.kb.yaml instead of healthcare-kb.yaml
        if config == "healthcare" and not kb_file.exists():
            wrong_name = script_dir / "knowledge" / "healthcare.kb.yaml"
            if wrong_name.exists():
                print(f"⚠️  Found 'healthcare.kb.yaml' but expected 'healthcare-kb.yaml'")
                print(f"   Run: mv knowledge/healthcare.kb.yaml knowledge/healthcare-kb.yaml")
                all_ok = False
                continue
        all_ok &= check_file(kb_file, f"{config.capitalize()} KB")
    print()
    
    # Check Python version
    print("Checking Python Environment:")
    print("-" * 70)
    print(f"✅ Python version: {sys.version.split()[0]}")
    
    # Check imports
    try:
        import yaml
        print(f"✅ PyYAML installed")
    except ImportError:
        print(f"❌ PyYAML NOT installed - run: pip install -r requirements.txt")
        all_ok = False
    
    try:
        import mcp
        print(f"✅ MCP library installed")
    except ImportError:
        print(f"❌ MCP library NOT installed - run: pip install -r requirements.txt")
        all_ok = False
    
    print()
    
    # Summary
    print("="*70)
    if all_ok:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("Run the FastMCP server:")
        print("  python src/fastmcp_server.py")
        print()
        print("Or use Docker:")
        print("  docker-compose up")
        print()
        print("Test endpoints:")
        print("  curl http://localhost:8000/health/banking")
        print("  curl http://localhost:8000/industries")
        print()
    else:
        print("❌ SOME CHECKS FAILED")
        print()
        print("Please fix the issues above before running the server.")
        print()
    print("="*70 + "\n")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
