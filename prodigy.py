#!/usr/bin/env python3
"""Prodigy Companion - entry point"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from src.cli.main import cli

if __name__ == "__main__":
    cli()
