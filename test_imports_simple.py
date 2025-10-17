#!/usr/bin/env python3
"""
Simple test to verify imports work with modernized pybatfish API.
"""

if __name__ == "__main__":
    try:
        print("Testing pybatfish imports...")

        from pybatfish.client.session import Session
        print("✓ Session import successful")

        from pybatfish.question import bfq
        print("✓ bfq import successful")

        from pybatfish.question import load_questions, list_questions
        print("✓ Question functions import successful")

        from pybatfish.datamodel import HeaderConstraints, Interface
        print("✓ Data model imports successful")

        print("\n✓ All pybatfish imports working!")

        # Test our components
        from components.batfish import Batfish
        print("✓ Batfish class import successful")

        print("\n🎉 All imports successful! Ready to test with live Batfish.")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()