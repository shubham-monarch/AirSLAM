#!/usr/bin/env python3
"""
ONNX Model Inspector
Inspects ONNX model files and displays their properties

Usage:
    python3 inspect_onnx.py <onnx_file_path>
    python3 inspect_onnx.py /path/to/model.onnx
"""

import onnx
import sys
import os
import argparse
from pathlib import Path

def inspect_onnx_model(model_path, skip_validation=False, quiet=False):
    """Inspect a single ONNX model and print its properties"""
    if not quiet:
        print(f"\n{'='*60}")
        print(f"Inspecting: {model_path}")
        print(f"{'='*60}")

    try:
        # Load the model
        model = onnx.load(model_path)
        if not quiet:
            print(f"✓ Successfully loaded ONNX model")

        # Basic model information
        if not quiet:
            print(f"Model IR Version: {model.ir_version}")
            print(f"Model Producer: {model.producer_name}")
            print(f"Model Producer Version: {model.producer_version}")
            print(f"Model Domain: {model.domain}")
            print(f"Model Version: {model.model_version}")

        # Opset information
        if hasattr(model, 'opset_import') and len(model.opset_import) > 0:
            if not quiet:
                print(f"Opset Imports:")
            for opset in model.opset_import:
                domain = opset.domain if opset.domain else 'ai.onnx'
                if not quiet:
                    print(f"  {domain}: v{opset.version}")
        else:
            if not quiet:
                print(f"Opset Imports: None")

        # Graph information
        graph = model.graph
        if not quiet:
            print(f"\nGraph Name: {graph.name}")

        # Input information
        print(f"\nInputs ({len(graph.input)}):")
        for i, input_tensor in enumerate(graph.input):
            print(f"  {i+1}. Name: {input_tensor.name}")
            if input_tensor.type.tensor_type:
                shape = []
                for dim in input_tensor.type.tensor_type.shape.dim:
                    if dim.dim_value:
                        shape.append(str(dim.dim_value))
                    elif dim.dim_param:
                        shape.append(dim.dim_param)
                    else:
                        shape.append("?")
                print(f"      Shape: [{', '.join(shape)}]")
                if not quiet:
                    print(f"      Data Type: {input_tensor.type.tensor_type.elem_type}")

        # Output information
        print(f"\nOutputs ({len(graph.output)}):")
        for i, output_tensor in enumerate(graph.output):
            print(f"  {i+1}. Name: {output_tensor.name}")
            if output_tensor.type.tensor_type:
                shape = []
                for dim in output_tensor.type.tensor_type.shape.dim:
                    if dim.dim_value:
                        shape.append(str(dim.dim_value))
                    elif dim.dim_param:
                        shape.append(dim.dim_param)
                    else:
                        shape.append("?")
                print(f"      Shape: [{', '.join(shape)}]")
                if not quiet:
                    print(f"      Data Type: {output_tensor.type.tensor_type.elem_type}")

        # Node information
        if not quiet:
            print(f"\nNodes ({len(graph.node)}):")
            op_types = {}
            for node in graph.node:
                op_type = node.op_type
                op_types[op_type] = op_types.get(op_type, 0) + 1

            for op_type, count in sorted(op_types.items()):
                print(f"  {op_type}: {count}")

        # Model size
        file_size = os.path.getsize(model_path)
        if not quiet:
            print(f"\nFile Size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")

        # Validate model
        if not skip_validation:
            if not quiet:
                print(f"\nValidation:")
            try:
                onnx.checker.check_model(model)
                if not quiet:
                    print("  ✓ Model validation passed")
            except onnx.checker.ValidationError as e:
                print(f"  ✗ Model validation failed: {e}")

    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return False

    return True

def main():
    parser = argparse.ArgumentParser(
        description="Inspect ONNX model files and display their properties",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 inspect_onnx.py --model /path/to/model.onnx
    python3 inspect_onnx.py -m /path/to/model.onnx
    python3 inspect_onnx.py --help
        """
    )

    parser.add_argument(
        "-m", "--model",
        type=str,
        required=True,
        help="Path to the ONNX model file to inspect"
    )

    parser.add_argument(
        "--no-validation",
        action="store_true",
        help="Skip model validation (faster for large models)"
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce output verbosity"
    )

    args = parser.parse_args()

    if not args.quiet:
        print("ONNX Model Inspection Tool")
        print("=" * 60)

    model_path = args.model

    # Check if file exists
    if not os.path.exists(model_path):
        print(f"✗ Model file not found: {model_path}")
        sys.exit(1)

    # Check if it's actually a file
    if not os.path.isfile(model_path):
        print(f"✗ Path is not a file: {model_path}")
        sys.exit(1)

    # Check file extension
    if not model_path.lower().endswith('.onnx'):
        print(f"⚠ Warning: File does not have .onnx extension: {model_path}")

    inspect_onnx_model(model_path, args.no_validation, args.quiet)

if __name__ == "__main__":
    main()
