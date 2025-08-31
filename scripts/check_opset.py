#!/usr/bin/env python3
"""
Check ONNX Opset Information
Quick script to check opset version and other model attributes
"""

import onnx
import sys

def check_opset(model_path):
    """Check opset information for an ONNX model"""
    print(f"Checking opset for: {model_path}")
    print("=" * 50)

    try:
        model = onnx.load(model_path)
        print(f"✓ Successfully loaded ONNX model")

        # Check available attributes
        print("\nAvailable model attributes:")
        attrs = [attr for attr in dir(model) if not attr.startswith('_')]
        for attr in sorted(attrs):
            print(f"  {attr}")

        # Check opset information
        print("\nOpset Information:")
        if hasattr(model, 'opset_import') and model.opset_import:
            print(f"opset_import exists: {len(model.opset_import)} items")
            for i, opset in enumerate(model.opset_import):
                print(f"  Opset {i}: domain='{opset.domain}', version={opset.version}")
        else:
            print("No opset_import found or it's empty")

        # Check other relevant attributes
        print("\nOther model info:")
        print(f"  IR Version: {getattr(model, 'ir_version', 'N/A')}")
        print(f"  Producer: {getattr(model, 'producer_name', 'N/A')}")
        print(f"  Domain: {getattr(model, 'domain', 'N/A')}")

    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 check_opset.py <onnx_file_path>")
        sys.exit(1)

    check_opset(sys.argv[1])
