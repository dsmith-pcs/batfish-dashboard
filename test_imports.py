#!/usr/bin/env python3
"""
Test script to verify all imports work correctly after modernization.
"""

try:
    print("Testing imports...")

    # Test core app imports
    from app import app
    print("✓ app.py imports successfully")

    # Test layouts imports
    from layouts import main_page_layout
    print("✓ layouts.py imports successfully")

    # Test components imports
    from components.batfish import Batfish
    from components.functions import save_file, get_layer3_graph
    print("✓ components imports successfully")

    # Test callbacks imports
    import callbacks
    print("✓ callbacks.py imports successfully")

    print("\n🎉 All imports successful! The modernization appears to be working.")
    print("Ready to test with live Batfish instance.")

except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    exit(1)