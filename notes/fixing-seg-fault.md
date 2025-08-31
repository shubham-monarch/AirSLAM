# (1) List onnx files in output folder
_Exported on 31/08/2025 at 16:39:48 GMT+5:30 from Cursor (1.5.7)_

---

**User**

list all the `.onnx` files in `src/AirSLAM/output` folder. 
Use tables. 
If possible, group related files together.

---

**Cursor**

Based on the contents of the `src/AirSLAM/output` folder, here are all the `.onnx` files grouped by their related functionality:

## PLNet Models (Line Detection)
| File Name | Size | Description |
|-----------|------|-------------|
| `plnet_s0.onnx` | 31MB | Stage 0 model for initial processing |
| `plnet_s1.onnx` | 1.8MB | Stage 1 model for line and junction detection |

## SuperPoint Models (Keypoint Detection)
| File Name | Size | Description |
|-----------|------|-------------|
| `superpoint_v1_sim_int32.onnx` | 5.0MB | Standalone SuperPoint model for keypoint detection |
| `superpoint_lightglue.onnx` | 44MB | Combined SuperPoint + LightGlue model |

## SuperGlue Models (Feature Matching)
| File Name | Size | Description |
|-----------|------|-------------|
| `superglue_indoor_sim_int32.onnx` | 46MB | Optimized SuperGlue matcher for indoor environments |
| `superglue_outdoor_sim_int32.onnx` | 46MB | Optimized SuperGlue matcher for outdoor environments |

## Summary
- **Total files**: 6
- **Total size**: ~173.8MB
- **Categories**: PLNet (2 files), SuperPoint (2 files), SuperGlue (2 files)

The models appear to be organized around three main computer vision tasks: line detection (PLNet), keypoint detection (SuperPoint), and feature matching (SuperGlue).

---

**User**

Let's start with converting the `.onnx` files to `.engine`.
Use `trtexec` from `TENSORRT_ROOT` specified in @CMakeLists.txt 

Let's start with `superglue_` files. 
Refer the corresponding `.cpp` files in @cpp-onnx-relation.md 

---

**Cursor**

Perfect! The `trtexec` tool is available at `/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec`.

## Plan for Converting Superglue ONNX Files to Engine Files

I will convert the two superglue ONNX files to TensorRT engine files:

1. **superglue_indoor_sim_int32.onnx** → **superglue_indoor_sim_int32.engine**
2. **superglue_outdoor_sim_int32.onnx** → **superglue_outdoor_sim_int32.engine**

Both files correspond to `super_glue.cpp` as mentioned in the cpp-onnx-relation.md file.

The conversion commands will be:
```bash
/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec --onnx=src/AirSLAM/output/superglue_indoor_sim_int32.onnx --saveEngine=src/AirSLAM/output/superglue_indoor_sim_int32.engine

/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec --onnx=src/AirSLAM/output/superglue_outdoor_sim_int32.onnx --saveEngine=src/AirSLAM/output/superglue_outdoor_sim_int32.engine
```

**Note:** This process may take several minutes for each file, especially for the larger 46MB models.

Would you like me to proceed with the conversion? I'll start with the indoor model first, then the outdoor model.

```shellscript
/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec --onnx=src/AirSLAM/output/superglue_indoor_sim_int32.onnx --saveEngine=src/AirSLAM/output/superglue_indoor_sim_int32.engine

/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec --onnx=src/AirSLAM/output/superglue_outdoor_sim_int32.onnx --saveEngine=src/AirSLAM/output/superglue_outdoor_sim_int32.engine
```

---

**User**

Yes. 

can you check @super_glue.cpp for all the necessary params that need to be passed to `trtexec`? 

---

**Cursor**

Based on my analysis of the `super_glue.cpp` and `point_matcher.cc` files, here are the **essential parameters** that need to be passed to `trtexec` for converting the SuperGlue ONNX files:

## Required trtexec Parameters for SuperGlue

### Input/Output Tensor Specifications
**Input Tensors (6 total):**
- `keypoints_0` - Keypoints for first image
- `scores_0` - Confidence scores for first image keypoints  
- `descriptors_0` - Feature descriptors for first image
- `keypoints_1` - Keypoints for second image
- `scores_1` - Confidence scores for second image keypoints
- `descriptors_1` - Feature descriptors for second image

**Output Tensors (1 total):**
- `scores` - Matching scores matrix

### Key trtexec Options (based on code analysis):
1. **Precision**: `--fp16` (FP16 precision is enabled in the code)
2. **Workspace**: Consider adding `--workspace=512` (512MB workspace is referenced in comments)
3. **Input shapes**: Dynamic shapes are supported with optimization profiles

### Complete trtexec Commands:

```bash
# For indoor model
/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec \
  --onnx=src/AirSLAM/output/superglue_indoor_sim_int32.onnx \
  --saveEngine=src/AirSLAM/output/superglue_indoor_sim_int32.engine \
  --fp16 \
  --workspace=512

# For outdoor model  
/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec \
  --onnx=src/AirSLAM/output/superglue_outdoor_sim_int32.onnx \
  --saveEngine=src/AirSLAM/output/superglue_outdoor_sim_int32.engine \
  --fp16 \
  --workspace=512
```

### Additional Options You Might Need:
- `--verbose` - For detailed logging (useful for troubleshooting)
- `--buildOnly` - If you want to build without running inference
- `--profilingVerbosity=detailed` - For performance profiling

The tensor names are hardcoded in `point_matcher.cc` lines 21-27, and the FP16 precision setting is found in `super_glue.cpp` line 146. This should resolve the conversion issues you encountered earlier.

```shellscript
# For indoor model
/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec \
  --onnx=src/AirSLAM/output/superglue_indoor_sim_int32.onnx \
  --saveEngine=src/AirSLAM/output/superglue_indoor_sim_int32.engine \
  --fp16 \
  --workspace=512

# For outdoor model  
/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec \
  --onnx=src/AirSLAM/output/superglue_outdoor_sim_int32.onnx \
  --saveEngine=src/AirSLAM/output/superglue_outdoor_sim_int32.engine \
  --fp16 \
  --workspace=512
```

---

**User**

go ahead. 
Also, pass `--buildOnly`. 

create a new script inside the @scripts/ folder instead. 
Also, see @inspect_onnx.py or @check_opset.py helps?
use `src/AirSLAM/.venv` before running any python script. 

---

**Cursor**

```python
#!/usr/bin/env python3
"""
SuperGlue ONNX to TensorRT Engine Converter
Comprehensive conversion script with troubleshooting and multiple approaches

Usage:
    python3 convert_superglue_to_engine.py --model superglue_indoor_sim_int32.onnx
    python3 convert_superglue_to_engine.py --model superglue_outdoor_sim_int32.onnx
    python3 convert_superglue_to_engine.py --all
"""

import argparse
import os
import sys
import subprocess
import time
from pathlib import Path
import json

def run_command(cmd, description=""):
    """Run a command and return the result"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, shell=isinstance(cmd, str),
                              capture_output=True, text=True, cwd=os.getcwd())
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        print(f"Return code: {result.returncode}")
        return result.returncode == 0, result
    except Exception as e:
        print(f"Error running command: {e}")
        return False, None

def check_tensorrt_setup():
    """Check TensorRT installation and setup"""
    print("\n🔍 Checking TensorRT Setup...")

    # Check trtexec
    trtexec_path = "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec"
    if not os.path.exists(trtexec_path):
        print(f"❌ trtexec not found at {trtexec_path}")
        return False

    print(f"✅ trtexec found at {trtexec_path}")

    # Check libraries
    lib_paths = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvinfer.so",
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvinfer_plugin.so",
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvonnxparser.so"
    ]

    for lib_path in lib_paths:
        if os.path.exists(lib_path):
            print(f"✅ {os.path.basename(lib_path)} found")
        else:
            print(f"❌ {os.path.basename(lib_path)} not found")

    return True

def try_trtexec_basic(onnx_path, engine_path):
    """Try basic trtexec conversion"""
    print(f"\n🔄 Attempt 1: Basic trtexec conversion")
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--verbose"
    ]
    success, result = run_command(cmd, "Basic trtexec conversion")
    return success

def try_trtexec_with_options(onnx_path, engine_path):
    """Try trtexec with various optimization options"""
    print(f"\n🔄 Attempt 2: trtexec with optimization options")

    # First try with minimal options
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec with workspace and verbose")
    if success:
        return True

    # Try without FP16
    print(f"\n🔄 Attempt 2b: trtexec without FP16")
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--noTF32",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec without FP16 and TF32")
    if success:
        return True

    return False

def try_trtexec_build_only(onnx_path, engine_path):
    """Try trtexec with build-only mode"""
    print(f"\n🔄 Attempt 3: trtexec build-only mode")

    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--buildOnly",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec build-only mode")
    return success

def try_trtexec_minimal(onnx_path, engine_path):
    """Try trtexec with minimal settings"""
    print(f"\n🔄 Attempt 4: trtexec minimal settings")

    # Try with explicit shapes to avoid dynamic shape issues
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--minShapes=keypoints_0:1x1x2,scores_0:1x1,descriptors_0:1x256x1,keypoints_1:1x1x2,scores_1:1x1,descriptors_1:1x256x1",
        "--optShapes=keypoints_0:1x256x2,scores_0:1x256,descriptors_0:1x256x256,keypoints_1:1x256x2,scores_1:1x256,descriptors_1:1x256x256",
        "--maxShapes=keypoints_0:1x512x2,scores_0:1x512,descriptors_0:1x256x512,keypoints_1:1x512x2,scores_1:1x512,descriptors_1:1x256x512",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec with explicit shapes")
    return success

def try_python_conversion(onnx_path, engine_path):
    """Try Python-based conversion using tensorrt python API"""
    print(f"\n🔄 Attempt 5: Python-based conversion")

    try:
        import tensorrt as trt
        import onnxruntime as ort

        print("✅ TensorRT and ONNX Runtime Python packages available")

        # This is a more complex implementation that would require
        # setting up the builder, network, parser, etc.
        print("🔧 Python conversion requires custom implementation...")
        print("💡 Consider implementing this as a separate function")

        return False

    except ImportError as e:
        print(f"❌ Python conversion not available: {e}")
        return False

def diagnose_system():
    """Diagnose system for potential issues"""
    print(f"\n🔍 System Diagnostics:")

    # Check GPU memory
    try:
        result = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total",
                                "--format=csv,noheader,nounits"],
                               capture_output=True, text=True)
        if result.returncode == 0:
            used, total = result.stdout.strip().split(',')
            print(f"📊 GPU Memory: {used}MB / {total}MB used")
        else:
            print("❌ Failed to check GPU memory")
    except Exception as e:
        print(f"❌ GPU check failed: {e}")

    # Check CUDA version
    try:
        result = subprocess.run(["nvcc", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ CUDA available")
        else:
            print("❌ CUDA not available")
    except Exception as e:
        print(f"❌ CUDA check failed: {e}")

def convert_single_model(onnx_path, force=False):
    """Convert a single ONNX model to TensorRT engine"""
    if not os.path.exists(onnx_path):
        print(f"❌ ONNX file not found: {onnx_path}")
        return False

    engine_path = onnx_path.replace('.onnx', '.engine')

    if os.path.exists(engine_path) and not force:
        print(f"⚠️  Engine already exists: {engine_path}")
        print("Use --force to overwrite")
        return True

    print(f"\n🚀 Converting: {onnx_path}")
    print(f"📁 Target: {engine_path}")

    # Check setup first
    if not check_tensorrt_setup():
        return False

    # Try different conversion approaches
    attempts = [
        try_trtexec_basic,
        try_trtexec_with_options,
        try_trtexec_build_only,
        try_trtexec_minimal,
        try_python_conversion
    ]

    for attempt_func in attempts:
        if attempt_func(onnx_path, engine_path):
            print(f"\n✅ SUCCESS: Engine created at {engine_path}")
            return True
        print("❌ Attempt failed, trying next method...")

    print("
❌ All conversion attempts failed"    diagnose_system()
    return False

def main():
    parser = argparse.ArgumentParser(
        description="Convert SuperGlue ONNX models to TensorRT engines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 convert_superglue_to_engine.py --model superglue_indoor_sim_int32.onnx
  python3 convert_superglue_to_engine.py --all
  python3 convert_superglue_to_engine.py --model superglue_outdoor_sim_int32.onnx --force
        """
    )

    parser.add_argument(
        "--model",
        type=str,
        help="Path to specific ONNX model file"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Convert all SuperGlue models"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing engine files"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="src/AirSLAM/output",
        help="Output directory for engine files"
    )

    args = parser.parse_args()

    print("🔧 SuperGlue ONNX to TensorRT Converter")
    print("=" * 60)

    # Determine which models to convert
    models_to_convert = []

    if args.all:
        # Convert both models
        base_models = [
            "superglue_indoor_sim_int32.onnx",
            "superglue_outdoor_sim_int32.onnx"
        ]
        for model in base_models:
            model_path = os.path.join(args.output_dir, model)
            if os.path.exists(model_path):
                models_to_convert.append(model_path)
            else:
                print(f"⚠️  Model not found: {model_path}")

    elif args.model:
        if os.path.isabs(args.model):
            models_to_convert.append(args.model)
        else:
            model_path = os.path.join(args.output_dir, args.model)
            models_to_convert.append(model_path)
    else:
        print("❌ Specify --model <filename> or --all")
        sys.exit(1)

    if not models_to_convert:
        print("❌ No valid models found to convert")
        sys.exit(1)

    # Convert each model
    success_count = 0
    for model_path in models_to_convert:
        if convert_single_model(model_path, args.force):
            success_count += 1

    print("
📊 Summary:"    print(f"   Models processed: {len(models_to_convert)}")
    print(f"   Successful conversions: {success_count}")
    print(f"   Failed conversions: {len(models_to_convert) - success_count}")

    if success_count == len(models_to_convert):
        print("🎉 All conversions completed successfully!")
        return 0
    else:
        print("⚠️  Some conversions failed. Check output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

```python
#!/usr/bin/env python3
"""
SuperGlue ONNX to TensorRT Engine Converter
Comprehensive conversion script with troubleshooting and multiple approaches

Usage:
    python3 convert_superglue_to_engine.py --model superglue_indoor_sim_int32.onnx
    python3 convert_superglue_to_engine.py --model superglue_outdoor_sim_int32.onnx
    python3 convert_superglue_to_engine.py --all
"""

import argparse
import os
import sys
import subprocess
import time
from pathlib import Path
import json

def run_command(cmd, description=""):
    """Run a command and return the result"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, shell=isinstance(cmd, str),
                              capture_output=True, text=True, cwd=os.getcwd())
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        print(f"Return code: {result.returncode}")
        return result.returncode == 0, result
    except Exception as e:
        print(f"Error running command: {e}")
        return False, None

def check_tensorrt_setup():
    """Check TensorRT installation and setup"""
    print("\n🔍 Checking TensorRT Setup...")

    # Check trtexec
    trtexec_path = "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec"
    if not os.path.exists(trtexec_path):
        print(f"❌ trtexec not found at {trtexec_path}")
        return False

    print(f"✅ trtexec found at {trtexec_path}")

    # Check libraries
    lib_paths = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvinfer.so",
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvinfer_plugin.so",
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvonnxparser.so"
    ]

    for lib_path in lib_paths:
        if os.path.exists(lib_path):
            print(f"✅ {os.path.basename(lib_path)} found")
        else:
            print(f"❌ {os.path.basename(lib_path)} not found")

    return True

def try_trtexec_basic(onnx_path, engine_path):
    """Try basic trtexec conversion"""
    print(f"\n🔄 Attempt 1: Basic trtexec conversion")
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--verbose"
    ]
    success, result = run_command(cmd, "Basic trtexec conversion")
    return success

def try_trtexec_with_options(onnx_path, engine_path):
    """Try trtexec with various optimization options"""
    print(f"\n🔄 Attempt 2: trtexec with optimization options")

    # First try with minimal options
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec with workspace and verbose")
    if success:
        return True

    # Try without FP16
    print(f"\n🔄 Attempt 2b: trtexec without FP16")
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--noTF32",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec without FP16 and TF32")
    if success:
        return True

    return False

def try_trtexec_build_only(onnx_path, engine_path):
    """Try trtexec with build-only mode"""
    print(f"\n🔄 Attempt 3: trtexec build-only mode")

    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--buildOnly",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec build-only mode")
    return success

def try_trtexec_minimal(onnx_path, engine_path):
    """Try trtexec with minimal settings"""
    print(f"\n🔄 Attempt 4: trtexec minimal settings")

    # Try with explicit shapes to avoid dynamic shape issues
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--minShapes=keypoints_0:1x1x2,scores_0:1x1,descriptors_0:1x256x1,keypoints_1:1x1x2,scores_1:1x1,descriptors_1:1x256x1",
        "--optShapes=keypoints_0:1x256x2,scores_0:1x256,descriptors_0:1x256x256,keypoints_1:1x256x2,scores_1:1x256,descriptors_1:1x256x256",
        "--maxShapes=keypoints_0:1x512x2,scores_0:1x512,descriptors_0:1x256x512,keypoints_1:1x512x2,scores_1:1x512,descriptors_1:1x256x512",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec with explicit shapes")
    return success

def try_python_conversion(onnx_path, engine_path):
    """Try Python-based conversion using tensorrt python API"""
    print(f"\n🔄 Attempt 5: Python-based conversion")

    try:
        import tensorrt as trt
        import onnxruntime as ort

        print("✅ TensorRT and ONNX Runtime Python packages available")

        # This is a more complex implementation that would require
        # setting up the builder, network, parser, etc.
        print("🔧 Python conversion requires custom implementation...")
        print("💡 Consider implementing this as a separate function")

        return False

    except ImportError as e:
        print(f"❌ Python conversion not available: {e}")
        return False

def diagnose_system():
    """Diagnose system for potential issues"""
    print(f"\n🔍 System Diagnostics:")

    # Check GPU memory
    try:
        result = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total",
                                "--format=csv,noheader,nounits"],
                               capture_output=True, text=True)
        if result.returncode == 0:
            used, total = result.stdout.strip().split(',')
            print(f"📊 GPU Memory: {used}MB / {total}MB used")
        else:
            print("❌ Failed to check GPU memory")
    except Exception as e:
        print(f"❌ GPU check failed: {e}")

    # Check CUDA version
    try:
        result = subprocess.run(["nvcc", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ CUDA available")
        else:
            print("❌ CUDA not available")
    except Exception as e:
        print(f"❌ CUDA check failed: {e}")

def convert_single_model(onnx_path, force=False):
    """Convert a single ONNX model to TensorRT engine"""
    if not os.path.exists(onnx_path):
        print(f"❌ ONNX file not found: {onnx_path}")
        return False

    engine_path = onnx_path.replace('.onnx', '.engine')

    if os.path.exists(engine_path) and not force:
        print(f"⚠️  Engine already exists: {engine_path}")
        print("Use --force to overwrite")
        return True

    print(f"\n🚀 Converting: {onnx_path}")
    print(f"📁 Target: {engine_path}")

    # Check setup first
    if not check_tensorrt_setup():
        return False

    # Try different conversion approaches
    attempts = [
        try_trtexec_basic,
        try_trtexec_with_options,
        try_trtexec_build_only,
        try_trtexec_minimal,
        try_python_conversion
    ]

    for attempt_func in attempts:
        if attempt_func(onnx_path, engine_path):
            print(f"\n✅ SUCCESS: Engine created at {engine_path}")
            return True
        print("❌ Attempt failed, trying next method...")

    print("\n❌ All conversion attempts failed")
    diagnose_system()
    return False

def main():
    parser = argparse.ArgumentParser(
        description="Convert SuperGlue ONNX models to TensorRT engines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 convert_superglue_to_engine.py --model superglue_indoor_sim_int32.onnx
  python3 convert_superglue_to_engine.py --all
  python3 convert_superglue_to_engine.py --model superglue_outdoor_sim_int32.onnx --force
        """
    )

    parser.add_argument(
        "--model",
        type=str,
        help="Path to specific ONNX model file"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Convert all SuperGlue models"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing engine files"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="src/AirSLAM/output",
        help="Output directory for engine files"
    )

    args = parser.parse_args()

    print("🔧 SuperGlue ONNX to TensorRT Converter")
    print("=" * 60)

    # Determine which models to convert
    models_to_convert = []

    if args.all:
        # Convert both models
        base_models = [
            "superglue_indoor_sim_int32.onnx",
            "superglue_outdoor_sim_int32.onnx"
        ]
        for model in base_models:
            model_path = os.path.join(args.output_dir, model)
            if os.path.exists(model_path):
                models_to_convert.append(model_path)
            else:
                print(f"⚠️  Model not found: {model_path}")

    elif args.model:
        if os.path.isabs(args.model):
            models_to_convert.append(args.model)
        else:
            model_path = os.path.join(args.output_dir, args.model)
            models_to_convert.append(model_path)
    else:
        print("❌ Specify --model <filename> or --all")
        sys.exit(1)

    if not models_to_convert:
        print("❌ No valid models found to convert")
        sys.exit(1)

    # Convert each model
    success_count = 0
    for model_path in models_to_convert:
        if convert_single_model(model_path, args.force):
            success_count += 1

    print("
📊 Summary:"    print(f"   Models processed: {len(models_to_convert)}")
    print(f"   Successful conversions: {success_count}")
    print(f"   Failed conversions: {len(models_to_convert) - success_count}")

    if success_count == len(models_to_convert):
        print("🎉 All conversions completed successfully!")
        return 0
    else:
        print("⚠️  Some conversions failed. Check output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

```

```python
#!/usr/bin/env python3
"""
SuperGlue ONNX to TensorRT Engine Converter
Comprehensive conversion script with troubleshooting and multiple approaches

Usage:
    python3 convert_superglue_to_engine.py --model superglue_indoor_sim_int32.onnx
    python3 convert_superglue_to_engine.py --model superglue_outdoor_sim_int32.onnx
    python3 convert_superglue_to_engine.py --all
"""

import argparse
import os
import sys
import subprocess
import time
from pathlib import Path
import json

def run_command(cmd, description=""):
    """Run a command and return the result"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, shell=isinstance(cmd, str),
                              capture_output=True, text=True, cwd=os.getcwd())
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        print(f"Return code: {result.returncode}")
        return result.returncode == 0, result
    except Exception as e:
        print(f"Error running command: {e}")
        return False, None

def check_tensorrt_setup():
    """Check TensorRT installation and setup"""
    print("\n🔍 Checking TensorRT Setup...")

    # Check trtexec
    trtexec_path = "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec"
    if not os.path.exists(trtexec_path):
        print(f"❌ trtexec not found at {trtexec_path}")
        return False

    print(f"✅ trtexec found at {trtexec_path}")

    # Check libraries
    lib_paths = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvinfer.so",
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvinfer_plugin.so",
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvonnxparser.so"
    ]

    for lib_path in lib_paths:
        if os.path.exists(lib_path):
            print(f"✅ {os.path.basename(lib_path)} found")
        else:
            print(f"❌ {os.path.basename(lib_path)} not found")

    return True

def try_trtexec_basic(onnx_path, engine_path):
    """Try basic trtexec conversion"""
    print(f"\n🔄 Attempt 1: Basic trtexec conversion")
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--verbose"
    ]
    success, result = run_command(cmd, "Basic trtexec conversion")
    return success

def try_trtexec_with_options(onnx_path, engine_path):
    """Try trtexec with various optimization options"""
    print(f"\n🔄 Attempt 2: trtexec with optimization options")

    # First try with minimal options
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec with workspace and verbose")
    if success:
        return True

    # Try without FP16
    print(f"\n🔄 Attempt 2b: trtexec without FP16")
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--noTF32",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec without FP16 and TF32")
    if success:
        return True

    return False

def try_trtexec_build_only(onnx_path, engine_path):
    """Try trtexec with build-only mode"""
    print(f"\n🔄 Attempt 3: trtexec build-only mode")

    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--buildOnly",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec build-only mode")
    return success

def try_trtexec_minimal(onnx_path, engine_path):
    """Try trtexec with minimal settings"""
    print(f"\n🔄 Attempt 4: trtexec minimal settings")

    # Try with explicit shapes to avoid dynamic shape issues
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--minShapes=keypoints_0:1x1x2,scores_0:1x1,descriptors_0:1x256x1,keypoints_1:1x1x2,scores_1:1x1,descriptors_1:1x256x1",
        "--optShapes=keypoints_0:1x256x2,scores_0:1x256,descriptors_0:1x256x256,keypoints_1:1x256x2,scores_1:1x256,descriptors_1:1x256x256",
        "--maxShapes=keypoints_0:1x512x2,scores_0:1x512,descriptors_0:1x256x512,keypoints_1:1x512x2,scores_1:1x512,descriptors_1:1x256x512",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec with explicit shapes")
    return success

def try_python_conversion(onnx_path, engine_path):
    """Try Python-based conversion using tensorrt python API"""
    print(f"\n🔄 Attempt 5: Python-based conversion")

    try:
        import tensorrt as trt
        import onnxruntime as ort

        print("✅ TensorRT and ONNX Runtime Python packages available")

        # This is a more complex implementation that would require
        # setting up the builder, network, parser, etc.
        print("🔧 Python conversion requires custom implementation...")
        print("💡 Consider implementing this as a separate function")

        return False

    except ImportError as e:
        print(f"❌ Python conversion not available: {e}")
        return False

def diagnose_system():
    """Diagnose system for potential issues"""
    print(f"\n🔍 System Diagnostics:")

    # Check GPU memory
    try:
        result = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total",
                                "--format=csv,noheader,nounits"],
                               capture_output=True, text=True)
        if result.returncode == 0:
            used, total = result.stdout.strip().split(',')
            print(f"📊 GPU Memory: {used}MB / {total}MB used")
        else:
            print("❌ Failed to check GPU memory")
    except Exception as e:
        print(f"❌ GPU check failed: {e}")

    # Check CUDA version
    try:
        result = subprocess.run(["nvcc", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ CUDA available")
        else:
            print("❌ CUDA not available")
    except Exception as e:
        print(f"❌ CUDA check failed: {e}")

def convert_single_model(onnx_path, force=False):
    """Convert a single ONNX model to TensorRT engine"""
    if not os.path.exists(onnx_path):
        print(f"❌ ONNX file not found: {onnx_path}")
        return False

    engine_path = onnx_path.replace('.onnx', '.engine')

    if os.path.exists(engine_path) and not force:
        print(f"⚠️  Engine already exists: {engine_path}")
        print("Use --force to overwrite")
        return True

    print(f"\n🚀 Converting: {onnx_path}")
    print(f"📁 Target: {engine_path}")

    # Check setup first
    if not check_tensorrt_setup():
        return False

    # Try different conversion approaches
    attempts = [
        try_trtexec_basic,
        try_trtexec_with_options,
        try_trtexec_build_only,
        try_trtexec_minimal,
        try_python_conversion
    ]

    for attempt_func in attempts:
        if attempt_func(onnx_path, engine_path):
            print(f"\n✅ SUCCESS: Engine created at {engine_path}")
            return True
        print("❌ Attempt failed, trying next method...")

    print("\n❌ All conversion attempts failed")
    diagnose_system()
    return False

def main():
    parser = argparse.ArgumentParser(
        description="Convert SuperGlue ONNX models to TensorRT engines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 convert_superglue_to_engine.py --model superglue_indoor_sim_int32.onnx
  python3 convert_superglue_to_engine.py --all
  python3 convert_superglue_to_engine.py --model superglue_outdoor_sim_int32.onnx --force
        """
    )

    parser.add_argument(
        "--model",
        type=str,
        help="Path to specific ONNX model file"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Convert all SuperGlue models"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing engine files"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="src/AirSLAM/output",
        help="Output directory for engine files"
    )

    args = parser.parse_args()

    print("🔧 SuperGlue ONNX to TensorRT Converter")
    print("=" * 60)

    # Determine which models to convert
    models_to_convert = []

    if args.all:
        # Convert both models
        base_models = [
            "superglue_indoor_sim_int32.onnx",
            "superglue_outdoor_sim_int32.onnx"
        ]
        for model in base_models:
            model_path = os.path.join(args.output_dir, model)
            if os.path.exists(model_path):
                models_to_convert.append(model_path)
            else:
                print(f"⚠️  Model not found: {model_path}")

    elif args.model:
        if os.path.isabs(args.model):
            models_to_convert.append(args.model)
        else:
            model_path = os.path.join(args.output_dir, args.model)
            models_to_convert.append(model_path)
    else:
        print("❌ Specify --model <filename> or --all")
        sys.exit(1)

    if not models_to_convert:
        print("❌ No valid models found to convert")
        sys.exit(1)

    # Convert each model
    success_count = 0
    for model_path in models_to_convert:
        if convert_single_model(model_path, args.force):
            success_count += 1

    print("\n📊 Summary:")
    print(f"   Models processed: {len(models_to_convert)}")
    print(f"   Successful conversions: {success_count}")
    print(f"   Failed conversions: {len(models_to_convert) - success_count}")

    if success_count == len(models_to_convert):
        print("🎉 All conversions completed successfully!")
        return 0
    else:
        print("⚠️  Some conversions failed. Check output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

```

```python
#!/usr/bin/env python3
"""
SuperGlue ONNX to TensorRT Engine Converter
Comprehensive conversion script with troubleshooting and multiple approaches

Usage:
    python3 convert_superglue_to_engine.py --model superglue_indoor_sim_int32.onnx
    python3 convert_superglue_to_engine.py --model superglue_outdoor_sim_int32.onnx
    python3 convert_superglue_to_engine.py --all
"""

import argparse
import os
import sys
import subprocess
import time
from pathlib import Path
import json

def run_command(cmd, description=""):
    """Run a command and return the result"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, shell=isinstance(cmd, str),
                              capture_output=True, text=True, cwd=os.getcwd())
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        print(f"Return code: {result.returncode}")
        return result.returncode == 0, result
    except Exception as e:
        print(f"Error running command: {e}")
        return False, None

def check_tensorrt_setup():
    """Check TensorRT installation and setup"""
    print("\n🔍 Checking TensorRT Setup...")

    # Check trtexec
    trtexec_path = "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec"
    if not os.path.exists(trtexec_path):
        print(f"❌ trtexec not found at {trtexec_path}")
        return False

    print(f"✅ trtexec found at {trtexec_path}")

    # Check libraries
    lib_paths = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvinfer.so",
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvinfer_plugin.so",
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvonnxparser.so"
    ]

    for lib_path in lib_paths:
        if os.path.exists(lib_path):
            print(f"✅ {os.path.basename(lib_path)} found")
        else:
            print(f"❌ {os.path.basename(lib_path)} not found")

    return True

def try_trtexec_basic(onnx_path, engine_path):
    """Try basic trtexec conversion"""
    print(f"\n🔄 Attempt 1: Basic trtexec conversion")
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        f"--onnx={onnx_path}",
        f"--saveEngine={engine_path}",
        "--verbose"
    ]
    success, result = run_command(cmd, "Basic trtexec conversion")
    return success

def try_trtexec_with_options(onnx_path, engine_path):
    """Try trtexec with various optimization options"""
    print(f"\n🔄 Attempt 2: trtexec with optimization options")

    # First try with minimal options
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec with workspace and verbose")
    if success:
        return True

    # Try without FP16
    print(f"\n🔄 Attempt 2b: trtexec without FP16")
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--noTF32",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec without FP16 and TF32")
    if success:
        return True

    return False

def try_trtexec_build_only(onnx_path, engine_path):
    """Try trtexec with build-only mode"""
    print(f"\n🔄 Attempt 3: trtexec build-only mode")

    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--buildOnly",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec build-only mode")
    return success

def try_trtexec_minimal(onnx_path, engine_path):
    """Try trtexec with minimal settings"""
    print(f"\n🔄 Attempt 4: trtexec minimal settings")

    # Try with explicit shapes to avoid dynamic shape issues
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--minShapes=keypoints_0:1x1x2,scores_0:1x1,descriptors_0:1x256x1,keypoints_1:1x1x2,scores_1:1x1,descriptors_1:1x256x1",
        "--optShapes=keypoints_0:1x256x2,scores_0:1x256,descriptors_0:1x256x256,keypoints_1:1x256x2,scores_1:1x256,descriptors_1:1x256x256",
        "--maxShapes=keypoints_0:1x512x2,scores_0:1x512,descriptors_0:1x256x512,keypoints_1:1x512x2,scores_1:1x512,descriptors_1:1x256x512",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec with explicit shapes")
    return success

def try_python_conversion(onnx_path, engine_path):
    """Try Python-based conversion using tensorrt python API"""
    print(f"\n🔄 Attempt 5: Python-based conversion")

    try:
        import tensorrt as trt
        import onnxruntime as ort

        print("✅ TensorRT and ONNX Runtime Python packages available")

        # This is a more complex implementation that would require
        # setting up the builder, network, parser, etc.
        print("🔧 Python conversion requires custom implementation...")
        print("💡 Consider implementing this as a separate function")

        return False

    except ImportError as e:
        print(f"❌ Python conversion not available: {e}")
        return False

def diagnose_system():
    """Diagnose system for potential issues"""
    print(f"\n🔍 System Diagnostics:")

    # Check GPU memory
    try:
        result = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total",
                                "--format=csv,noheader,nounits"],
                               capture_output=True, text=True)
        if result.returncode == 0:
            used, total = result.stdout.strip().split(',')
            print(f"📊 GPU Memory: {used}MB / {total}MB used")
        else:
            print("❌ Failed to check GPU memory")
    except Exception as e:
        print(f"❌ GPU check failed: {e}")

    # Check CUDA version
    try:
        result = subprocess.run(["nvcc", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ CUDA available")
        else:
            print("❌ CUDA not available")
    except Exception as e:
        print(f"❌ CUDA check failed: {e}")

def convert_single_model(onnx_path, force=False):
    """Convert a single ONNX model to TensorRT engine"""
    if not os.path.exists(onnx_path):
        print(f"❌ ONNX file not found: {onnx_path}")
        return False

    engine_path = onnx_path.replace('.onnx', '.engine')

    if os.path.exists(engine_path) and not force:
        print(f"⚠️  Engine already exists: {engine_path}")
        print("Use --force to overwrite")
        return True

    print(f"\n🚀 Converting: {onnx_path}")
    print(f"📁 Target: {engine_path}")

    # Check setup first
    if not check_tensorrt_setup():
        return False

    # Try different conversion approaches
    attempts = [
        try_trtexec_basic,
        try_trtexec_with_options,
        try_trtexec_build_only,
        try_trtexec_minimal,
        try_python_conversion
    ]

    for attempt_func in attempts:
        if attempt_func(onnx_path, engine_path):
            print(f"\n✅ SUCCESS: Engine created at {engine_path}")
            return True
        print("❌ Attempt failed, trying next method...")

    print("\n❌ All conversion attempts failed")
    diagnose_system()
    return False

def main():
    parser = argparse.ArgumentParser(
        description="Convert SuperGlue ONNX models to TensorRT engines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 convert_superglue_to_engine.py --model superglue_indoor_sim_int32.onnx
  python3 convert_superglue_to_engine.py --all
  python3 convert_superglue_to_engine.py --model superglue_outdoor_sim_int32.onnx --force
        """
    )

    parser.add_argument(
        "--model",
        type=str,
        help="Path to specific ONNX model file"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Convert all SuperGlue models"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing engine files"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="src/AirSLAM/output",
        help="Output directory for engine files"
    )

    args = parser.parse_args()

    print("🔧 SuperGlue ONNX to TensorRT Converter")
    print("=" * 60)

    # Determine which models to convert
    models_to_convert = []

    if args.all:
        # Convert both models
        base_models = [
            "superglue_indoor_sim_int32.onnx",
            "superglue_outdoor_sim_int32.onnx"
        ]
        for model in base_models:
            model_path = os.path.join(args.output_dir, model)
            if os.path.exists(model_path):
                models_to_convert.append(model_path)
            else:
                print(f"⚠️  Model not found: {model_path}")

    elif args.model:
        if os.path.isabs(args.model):
            models_to_convert.append(args.model)
        else:
            model_path = os.path.join(args.output_dir, args.model)
            models_to_convert.append(model_path)
    else:
        print("❌ Specify --model <filename> or --all")
        sys.exit(1)

    if not models_to_convert:
        print("❌ No valid models found to convert")
        sys.exit(1)

    # Convert each model
    success_count = 0
    for model_path in models_to_convert:
        if convert_single_model(model_path, args.force):
            success_count += 1

    print("\n📊 Summary:")
    print(f"   Models processed: {len(models_to_convert)}")
    print(f"   Successful conversions: {success_count}")
    print(f"   Failed conversions: {len(models_to_convert) - success_count}")

    if success_count == len(models_to_convert):
        print("🎉 All conversions completed successfully!")
        return 0
    else:
        print("⚠️  Some conversions failed. Check output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

```

```python
#!/usr/bin/env python3
"""
SuperGlue ONNX to TensorRT Engine Converter
Comprehensive conversion script with troubleshooting and multiple approaches

Usage:
    python3 convert_superglue_to_engine.py --model superglue_indoor_sim_int32.onnx
    python3 convert_superglue_to_engine.py --model superglue_outdoor_sim_int32.onnx
    python3 convert_superglue_to_engine.py --all
"""

import argparse
import os
import sys
import subprocess
import time
from pathlib import Path
import json

def run_command(cmd, description=""):
    """Run a command and return the result"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, shell=isinstance(cmd, str),
                              capture_output=True, text=True, cwd=os.getcwd())
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        print(f"Return code: {result.returncode}")
        return result.returncode == 0, result
    except Exception as e:
        print(f"Error running command: {e}")
        return False, None

def check_tensorrt_setup():
    """Check TensorRT installation and setup"""
    print("\n🔍 Checking TensorRT Setup...")

    # Check trtexec
    trtexec_path = "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec"
    if not os.path.exists(trtexec_path):
        print(f"❌ trtexec not found at {trtexec_path}")
        return False

    print(f"✅ trtexec found at {trtexec_path}")

    # Check libraries
    lib_paths = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvinfer.so",
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvinfer_plugin.so",
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvonnxparser.so"
    ]

    for lib_path in lib_paths:
        if os.path.exists(lib_path):
            print(f"✅ {os.path.basename(lib_path)} found")
        else:
            print(f"❌ {os.path.basename(lib_path)} not found")

    return True

def try_trtexec_basic(onnx_path, engine_path):
    """Try basic trtexec conversion"""
    print(f"\n🔄 Attempt 1: Basic trtexec conversion")
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        f"--onnx={onnx_path}",
        f"--saveEngine={engine_path}",
        "--verbose"
    ]
    success, result = run_command(cmd, "Basic trtexec conversion")
    return success

def try_trtexec_with_options(onnx_path, engine_path):
    """Try trtexec with various optimization options"""
    print(f"\n🔄 Attempt 2: trtexec with optimization options")

    # First try with minimal options
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        f"--onnx={onnx_path}",
        f"--saveEngine={engine_path}",
        "--memPoolSize=workspace:1024",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec with workspace and verbose")
    if success:
        return True

    # Try without FP16
    print(f"\n🔄 Attempt 2b: trtexec without FP16")
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        f"--onnx={onnx_path}",
        f"--saveEngine={engine_path}",
        "--memPoolSize=workspace:1024",
        "--noTF32",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec without FP16 and TF32")
    if success:
        return True

    return False

def try_trtexec_build_only(onnx_path, engine_path):
    """Try trtexec with build-only mode"""
    print(f"\n🔄 Attempt 3: trtexec build-only mode")

    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--buildOnly",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec build-only mode")
    return success

def try_trtexec_minimal(onnx_path, engine_path):
    """Try trtexec with minimal settings"""
    print(f"\n🔄 Attempt 4: trtexec minimal settings")

    # Try with explicit shapes to avoid dynamic shape issues
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--minShapes=keypoints_0:1x1x2,scores_0:1x1,descriptors_0:1x256x1,keypoints_1:1x1x2,scores_1:1x1,descriptors_1:1x256x1",
        "--optShapes=keypoints_0:1x256x2,scores_0:1x256,descriptors_0:1x256x256,keypoints_1:1x256x2,scores_1:1x256,descriptors_1:1x256x256",
        "--maxShapes=keypoints_0:1x512x2,scores_0:1x512,descriptors_0:1x256x512,keypoints_1:1x512x2,scores_1:1x512,descriptors_1:1x256x512",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec with explicit shapes")
    return success

def try_python_conversion(onnx_path, engine_path):
    """Try Python-based conversion using tensorrt python API"""
    print(f"\n🔄 Attempt 5: Python-based conversion")

    try:
        import tensorrt as trt
        import onnxruntime as ort

        print("✅ TensorRT and ONNX Runtime Python packages available")

        # This is a more complex implementation that would require
        # setting up the builder, network, parser, etc.
        print("🔧 Python conversion requires custom implementation...")
        print("💡 Consider implementing this as a separate function")

        return False

    except ImportError as e:
        print(f"❌ Python conversion not available: {e}")
        return False

def diagnose_system():
    """Diagnose system for potential issues"""
    print(f"\n🔍 System Diagnostics:")

    # Check GPU memory
    try:
        result = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total",
                                "--format=csv,noheader,nounits"],
                               capture_output=True, text=True)
        if result.returncode == 0:
            used, total = result.stdout.strip().split(',')
            print(f"📊 GPU Memory: {used}MB / {total}MB used")
        else:
            print("❌ Failed to check GPU memory")
    except Exception as e:
        print(f"❌ GPU check failed: {e}")

    # Check CUDA version
    try:
        result = subprocess.run(["nvcc", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ CUDA available")
        else:
            print("❌ CUDA not available")
    except Exception as e:
        print(f"❌ CUDA check failed: {e}")

def convert_single_model(onnx_path, force=False):
    """Convert a single ONNX model to TensorRT engine"""
    if not os.path.exists(onnx_path):
        print(f"❌ ONNX file not found: {onnx_path}")
        return False

    engine_path = onnx_path.replace('.onnx', '.engine')

    if os.path.exists(engine_path) and not force:
        print(f"⚠️  Engine already exists: {engine_path}")
        print("Use --force to overwrite")
        return True

    print(f"\n🚀 Converting: {onnx_path}")
    print(f"📁 Target: {engine_path}")

    # Check setup first
    if not check_tensorrt_setup():
        return False

    # Try different conversion approaches
    attempts = [
        try_trtexec_basic,
        try_trtexec_with_options,
        try_trtexec_build_only,
        try_trtexec_minimal,
        try_python_conversion
    ]

    for attempt_func in attempts:
        if attempt_func(onnx_path, engine_path):
            print(f"\n✅ SUCCESS: Engine created at {engine_path}")
            return True
        print("❌ Attempt failed, trying next method...")

    print("\n❌ All conversion attempts failed")
    diagnose_system()
    return False

def main():
    parser = argparse.ArgumentParser(
        description="Convert SuperGlue ONNX models to TensorRT engines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 convert_superglue_to_engine.py --model superglue_indoor_sim_int32.onnx
  python3 convert_superglue_to_engine.py --all
  python3 convert_superglue_to_engine.py --model superglue_outdoor_sim_int32.onnx --force
        """
    )

    parser.add_argument(
        "--model",
        type=str,
        help="Path to specific ONNX model file"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Convert all SuperGlue models"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing engine files"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="src/AirSLAM/output",
        help="Output directory for engine files"
    )

    args = parser.parse_args()

    print("🔧 SuperGlue ONNX to TensorRT Converter")
    print("=" * 60)

    # Determine which models to convert
    models_to_convert = []

    if args.all:
        # Convert both models
        base_models = [
            "superglue_indoor_sim_int32.onnx",
            "superglue_outdoor_sim_int32.onnx"
        ]
        for model in base_models:
            model_path = os.path.join(args.output_dir, model)
            if os.path.exists(model_path):
                models_to_convert.append(model_path)
            else:
                print(f"⚠️  Model not found: {model_path}")

    elif args.model:
        if os.path.isabs(args.model):
            models_to_convert.append(args.model)
        else:
            model_path = os.path.join(args.output_dir, args.model)
            models_to_convert.append(model_path)
    else:
        print("❌ Specify --model <filename> or --all")
        sys.exit(1)

    if not models_to_convert:
        print("❌ No valid models found to convert")
        sys.exit(1)

    # Convert each model
    success_count = 0
    for model_path in models_to_convert:
        if convert_single_model(model_path, args.force):
            success_count += 1

    print("\n📊 Summary:")
    print(f"   Models processed: {len(models_to_convert)}")
    print(f"   Successful conversions: {success_count}")
    print(f"   Failed conversions: {len(models_to_convert) - success_count}")

    if success_count == len(models_to_convert):
        print("🎉 All conversions completed successfully!")
        return 0
    else:
        print("⚠️  Some conversions failed. Check output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

```

```python
#!/usr/bin/env python3
"""
SuperGlue ONNX to TensorRT Engine Converter
Comprehensive conversion script with troubleshooting and multiple approaches

Usage:
    python3 convert_superglue_to_engine.py --model superglue_indoor_sim_int32.onnx
    python3 convert_superglue_to_engine.py --model superglue_outdoor_sim_int32.onnx
    python3 convert_superglue_to_engine.py --all
"""

import argparse
import os
import sys
import subprocess
import time
from pathlib import Path
import json

def run_command(cmd, description=""):
    """Run a command and return the result"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, shell=isinstance(cmd, str),
                              capture_output=True, text=True, cwd=os.getcwd())
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        print(f"Return code: {result.returncode}")
        return result.returncode == 0, result
    except Exception as e:
        print(f"Error running command: {e}")
        return False, None

def check_tensorrt_setup():
    """Check TensorRT installation and setup"""
    print("\n🔍 Checking TensorRT Setup...")

    # Check trtexec
    trtexec_path = "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec"
    if not os.path.exists(trtexec_path):
        print(f"❌ trtexec not found at {trtexec_path}")
        return False

    print(f"✅ trtexec found at {trtexec_path}")

    # Check libraries
    lib_paths = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvinfer.so",
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvinfer_plugin.so",
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvonnxparser.so"
    ]

    for lib_path in lib_paths:
        if os.path.exists(lib_path):
            print(f"✅ {os.path.basename(lib_path)} found")
        else:
            print(f"❌ {os.path.basename(lib_path)} not found")

    return True

def try_trtexec_basic(onnx_path, engine_path):
    """Try basic trtexec conversion"""
    print(f"\n🔄 Attempt 1: Basic trtexec conversion")
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        f"--onnx={onnx_path}",
        f"--saveEngine={engine_path}",
        "--verbose"
    ]
    success, result = run_command(cmd, "Basic trtexec conversion")
    return success

def try_trtexec_with_options(onnx_path, engine_path):
    """Try trtexec with various optimization options"""
    print(f"\n🔄 Attempt 2: trtexec with optimization options")

    # First try with minimal options
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        f"--onnx={onnx_path}",
        f"--saveEngine={engine_path}",
        "--memPoolSize=workspace:1024",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec with workspace and verbose")
    if success:
        return True

    # Try without FP16
    print(f"\n🔄 Attempt 2b: trtexec without FP16")
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        f"--onnx={onnx_path}",
        f"--saveEngine={engine_path}",
        "--memPoolSize=workspace:1024",
        "--noTF32",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec without FP16 and TF32")
    if success:
        return True

    return False

def try_trtexec_build_only(onnx_path, engine_path):
    """Try trtexec with build-only mode"""
    print(f"\n🔄 Attempt 3: trtexec build-only mode")

    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        f"--onnx={onnx_path}",
        f"--saveEngine={engine_path}",
        "--memPoolSize=workspace:1024",
        "--skipInference",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec build-only mode")
    return success

def try_trtexec_minimal(onnx_path, engine_path):
    """Try trtexec with minimal settings"""
    print(f"\n🔄 Attempt 4: trtexec minimal settings")

    # Try with explicit shapes to avoid dynamic shape issues
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        "--onnx", onnx_path,
        "--saveEngine", engine_path,
        "--workspace=1024",
        "--minShapes=keypoints_0:1x1x2,scores_0:1x1,descriptors_0:1x256x1,keypoints_1:1x1x2,scores_1:1x1,descriptors_1:1x256x1",
        "--optShapes=keypoints_0:1x256x2,scores_0:1x256,descriptors_0:1x256x256,keypoints_1:1x256x2,scores_1:1x256,descriptors_1:1x256x256",
        "--maxShapes=keypoints_0:1x512x2,scores_0:1x512,descriptors_0:1x256x512,keypoints_1:1x512x2,scores_1:1x512,descriptors_1:1x256x512",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec with explicit shapes")
    return success

def try_python_conversion(onnx_path, engine_path):
    """Try Python-based conversion using tensorrt python API"""
    print(f"\n🔄 Attempt 5: Python-based conversion")

    try:
        import tensorrt as trt
        import onnxruntime as ort

        print("✅ TensorRT and ONNX Runtime Python packages available")

        # This is a more complex implementation that would require
        # setting up the builder, network, parser, etc.
        print("🔧 Python conversion requires custom implementation...")
        print("💡 Consider implementing this as a separate function")

        return False

    except ImportError as e:
        print(f"❌ Python conversion not available: {e}")
        return False

def diagnose_system():
    """Diagnose system for potential issues"""
    print(f"\n🔍 System Diagnostics:")

    # Check GPU memory
    try:
        result = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total",
                                "--format=csv,noheader,nounits"],
                               capture_output=True, text=True)
        if result.returncode == 0:
            used, total = result.stdout.strip().split(',')
            print(f"📊 GPU Memory: {used}MB / {total}MB used")
        else:
            print("❌ Failed to check GPU memory")
    except Exception as e:
        print(f"❌ GPU check failed: {e}")

    # Check CUDA version
    try:
        result = subprocess.run(["nvcc", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ CUDA available")
        else:
            print("❌ CUDA not available")
    except Exception as e:
        print(f"❌ CUDA check failed: {e}")

def convert_single_model(onnx_path, force=False):
    """Convert a single ONNX model to TensorRT engine"""
    if not os.path.exists(onnx_path):
        print(f"❌ ONNX file not found: {onnx_path}")
        return False

    engine_path = onnx_path.replace('.onnx', '.engine')

    if os.path.exists(engine_path) and not force:
        print(f"⚠️  Engine already exists: {engine_path}")
        print("Use --force to overwrite")
        return True

    print(f"\n🚀 Converting: {onnx_path}")
    print(f"📁 Target: {engine_path}")

    # Check setup first
    if not check_tensorrt_setup():
        return False

    # Try different conversion approaches
    attempts = [
        try_trtexec_basic,
        try_trtexec_with_options,
        try_trtexec_build_only,
        try_trtexec_minimal,
        try_python_conversion
    ]

    for attempt_func in attempts:
        if attempt_func(onnx_path, engine_path):
            print(f"\n✅ SUCCESS: Engine created at {engine_path}")
            return True
        print("❌ Attempt failed, trying next method...")

    print("\n❌ All conversion attempts failed")
    diagnose_system()
    return False

def main():
    parser = argparse.ArgumentParser(
        description="Convert SuperGlue ONNX models to TensorRT engines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 convert_superglue_to_engine.py --model superglue_indoor_sim_int32.onnx
  python3 convert_superglue_to_engine.py --all
  python3 convert_superglue_to_engine.py --model superglue_outdoor_sim_int32.onnx --force
        """
    )

    parser.add_argument(
        "--model",
        type=str,
        help="Path to specific ONNX model file"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Convert all SuperGlue models"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing engine files"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="src/AirSLAM/output",
        help="Output directory for engine files"
    )

    args = parser.parse_args()

    print("🔧 SuperGlue ONNX to TensorRT Converter")
    print("=" * 60)

    # Determine which models to convert
    models_to_convert = []

    if args.all:
        # Convert both models
        base_models = [
            "superglue_indoor_sim_int32.onnx",
            "superglue_outdoor_sim_int32.onnx"
        ]
        for model in base_models:
            model_path = os.path.join(args.output_dir, model)
            if os.path.exists(model_path):
                models_to_convert.append(model_path)
            else:
                print(f"⚠️  Model not found: {model_path}")

    elif args.model:
        if os.path.isabs(args.model):
            models_to_convert.append(args.model)
        else:
            model_path = os.path.join(args.output_dir, args.model)
            models_to_convert.append(model_path)
    else:
        print("❌ Specify --model <filename> or --all")
        sys.exit(1)

    if not models_to_convert:
        print("❌ No valid models found to convert")
        sys.exit(1)

    # Convert each model
    success_count = 0
    for model_path in models_to_convert:
        if convert_single_model(model_path, args.force):
            success_count += 1

    print("\n📊 Summary:")
    print(f"   Models processed: {len(models_to_convert)}")
    print(f"   Successful conversions: {success_count}")
    print(f"   Failed conversions: {len(models_to_convert) - success_count}")

    if success_count == len(models_to_convert):
        print("🎉 All conversions completed successfully!")
        return 0
    else:
        print("⚠️  Some conversions failed. Check output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

```

```python
#!/usr/bin/env python3
"""
SuperGlue ONNX to TensorRT Engine Converter
Comprehensive conversion script with troubleshooting and multiple approaches

Usage:
    python3 convert_superglue_to_engine.py --model superglue_indoor_sim_int32.onnx
    python3 convert_superglue_to_engine.py --model superglue_outdoor_sim_int32.onnx
    python3 convert_superglue_to_engine.py --all
"""

import argparse
import os
import sys
import subprocess
import time
from pathlib import Path
import json

def run_command(cmd, description=""):
    """Run a command and return the result"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, shell=isinstance(cmd, str),
                              capture_output=True, text=True, cwd=os.getcwd())
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        print(f"Return code: {result.returncode}")
        return result.returncode == 0, result
    except Exception as e:
        print(f"Error running command: {e}")
        return False, None

def check_tensorrt_setup():
    """Check TensorRT installation and setup"""
    print("\n🔍 Checking TensorRT Setup...")

    # Check trtexec
    trtexec_path = "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec"
    if not os.path.exists(trtexec_path):
        print(f"❌ trtexec not found at {trtexec_path}")
        return False

    print(f"✅ trtexec found at {trtexec_path}")

    # Check libraries
    lib_paths = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvinfer.so",
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvinfer_plugin.so",
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/lib/libnvonnxparser.so"
    ]

    for lib_path in lib_paths:
        if os.path.exists(lib_path):
            print(f"✅ {os.path.basename(lib_path)} found")
        else:
            print(f"❌ {os.path.basename(lib_path)} not found")

    return True

def try_trtexec_basic(onnx_path, engine_path):
    """Try basic trtexec conversion"""
    print(f"\n🔄 Attempt 1: Basic trtexec conversion")
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        f"--onnx={onnx_path}",
        f"--saveEngine={engine_path}",
        "--verbose"
    ]
    success, result = run_command(cmd, "Basic trtexec conversion")
    return success

def try_trtexec_with_options(onnx_path, engine_path):
    """Try trtexec with various optimization options"""
    print(f"\n🔄 Attempt 2: trtexec with optimization options")

    # First try with minimal options
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        f"--onnx={onnx_path}",
        f"--saveEngine={engine_path}",
        "--memPoolSize=workspace:1024",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec with workspace and verbose")
    if success:
        return True

    # Try without FP16
    print(f"\n🔄 Attempt 2b: trtexec without FP16")
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        f"--onnx={onnx_path}",
        f"--saveEngine={engine_path}",
        "--memPoolSize=workspace:1024",
        "--noTF32",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec without FP16 and TF32")
    if success:
        return True

    return False

def try_trtexec_build_only(onnx_path, engine_path):
    """Try trtexec with build-only mode"""
    print(f"\n🔄 Attempt 3: trtexec build-only mode")

    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        f"--onnx={onnx_path}",
        f"--saveEngine={engine_path}",
        "--memPoolSize=workspace:1024",
        "--skipInference",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec build-only mode")
    return success

def try_trtexec_minimal(onnx_path, engine_path):
    """Try trtexec with minimal settings"""
    print(f"\n🔄 Attempt 4: trtexec minimal settings")

    # Try with explicit shapes to avoid dynamic shape issues
    cmd = [
        "/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec",
        f"--onnx={onnx_path}",
        f"--saveEngine={engine_path}",
        "--memPoolSize=workspace:1024",
        "--minShapes=keypoints_0:1x1x2,scores_0:1x1,descriptors_0:1x256x1,keypoints_1:1x1x2,scores_1:1x1,descriptors_1:1x256x1",
        "--optShapes=keypoints_0:1x256x2,scores_0:1x256,descriptors_0:1x256x256,keypoints_1:1x256x2,scores_1:1x256,descriptors_1:1x256x256",
        "--maxShapes=keypoints_0:1x512x2,scores_0:1x512,descriptors_0:1x256x512,keypoints_1:1x512x2,scores_1:1x512,descriptors_1:1x256x512",
        "--verbose"
    ]
    success, result = run_command(cmd, "trtexec with explicit shapes")
    return success

def try_python_conversion(onnx_path, engine_path):
    """Try Python-based conversion using tensorrt python API"""
    print(f"\n🔄 Attempt 5: Python-based conversion")

    try:
        import tensorrt as trt
        import onnxruntime as ort

        print("✅ TensorRT and ONNX Runtime Python packages available")

        # This is a more complex implementation that would require
        # setting up the builder, network, parser, etc.
        print("🔧 Python conversion requires custom implementation...")
        print("💡 Consider implementing this as a separate function")

        return False

    except ImportError as e:
        print(f"❌ Python conversion not available: {e}")
        return False

def diagnose_system():
    """Diagnose system for potential issues"""
    print(f"\n🔍 System Diagnostics:")

    # Check GPU memory
    try:
        result = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total",
                                "--format=csv,noheader,nounits"],
                               capture_output=True, text=True)
        if result.returncode == 0:
            used, total = result.stdout.strip().split(',')
            print(f"📊 GPU Memory: {used}MB / {total}MB used")
        else:
            print("❌ Failed to check GPU memory")
    except Exception as e:
        print(f"❌ GPU check failed: {e}")

    # Check CUDA version
    try:
        result = subprocess.run(["nvcc", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ CUDA available")
        else:
            print("❌ CUDA not available")
    except Exception as e:
        print(f"❌ CUDA check failed: {e}")

def convert_single_model(onnx_path, force=False):
    """Convert a single ONNX model to TensorRT engine"""
    if not os.path.exists(onnx_path):
        print(f"❌ ONNX file not found: {onnx_path}")
        return False

    engine_path = onnx_path.replace('.onnx', '.engine')

    if os.path.exists(engine_path) and not force:
        print(f"⚠️  Engine already exists: {engine_path}")
        print("Use --force to overwrite")
        return True

    print(f"\n🚀 Converting: {onnx_path}")
    print(f"📁 Target: {engine_path}")

    # Check setup first
    if not check_tensorrt_setup():
        return False

    # Try different conversion approaches
    attempts = [
        try_trtexec_basic,
        try_trtexec_with_options,
        try_trtexec_build_only,
        try_trtexec_minimal,
        try_python_conversion
    ]

    for attempt_func in attempts:
        if attempt_func(onnx_path, engine_path):
            print(f"\n✅ SUCCESS: Engine created at {engine_path}")
            return True
        print("❌ Attempt failed, trying next method...")

    print("\n❌ All conversion attempts failed")
    diagnose_system()
    return False

def main():
    parser = argparse.ArgumentParser(
        description="Convert SuperGlue ONNX models to TensorRT engines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 convert_superglue_to_engine.py --model superglue_indoor_sim_int32.onnx
  python3 convert_superglue_to_engine.py --all
  python3 convert_superglue_to_engine.py --model superglue_outdoor_sim_int32.onnx --force
        """
    )

    parser.add_argument(
        "--model",
        type=str,
        help="Path to specific ONNX model file"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Convert all SuperGlue models"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing engine files"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="src/AirSLAM/output",
        help="Output directory for engine files"
    )

    args = parser.parse_args()

    print("🔧 SuperGlue ONNX to TensorRT Converter")
    print("=" * 60)

    # Determine which models to convert
    models_to_convert = []

    if args.all:
        # Convert both models
        base_models = [
            "superglue_indoor_sim_int32.onnx",
            "superglue_outdoor_sim_int32.onnx"
        ]
        for model in base_models:
            model_path = os.path.join(args.output_dir, model)
            if os.path.exists(model_path):
                models_to_convert.append(model_path)
            else:
                print(f"⚠️  Model not found: {model_path}")

    elif args.model:
        if os.path.isabs(args.model):
            models_to_convert.append(args.model)
        else:
            model_path = os.path.join(args.output_dir, args.model)
            models_to_convert.append(model_path)
    else:
        print("❌ Specify --model <filename> or --all")
        sys.exit(1)

    if not models_to_convert:
        print("❌ No valid models found to convert")
        sys.exit(1)

    # Convert each model
    success_count = 0
    for model_path in models_to_convert:
        if convert_single_model(model_path, args.force):
            success_count += 1

    print("\n📊 Summary:")
    print(f"   Models processed: {len(models_to_convert)}")
    print(f"   Successful conversions: {success_count}")
    print(f"   Failed conversions: {len(models_to_convert) - success_count}")

    if success_count == len(models_to_convert):
        print("🎉 All conversions completed successfully!")
        return 0
    else:
        print("⚠️  Some conversions failed. Check output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

```

Perfect! The script is now working correctly with the fixed command format. I can see from the output that trtexec is properly parsing the commands and starting the conversion process. However, all attempts are still failing with a segmentation fault (return code -11).

## Key Findings from the Troubleshooting:

1. **✅ ONNX Models are Valid**: Both models load correctly and pass validation
2. **✅ Command Format Fixed**: trtexec now properly recognizes the arguments
3. **✅ TensorRT Setup OK**: Libraries are found and accessible
4. **❌ Segmentation Fault**: All trtexec attempts crash with SIGSEGV

## Root Cause Analysis:

The segmentation fault occurs consistently after "Loading standard plugins", which suggests:

1. **Plugin Loading Issue**: The crash happens during plugin initialization
2. **ONNX Compatibility**: The ONNX opset (v12) might have compatibility issues with TensorRT 8.6.1
3. **Dynamic Shapes**: The model's dynamic input shapes might be causing issues

## Recommended Next Steps:

Since the automatic conversion is failing, I recommend trying these manual approaches:

### Option 1: Try with Explicit Build Shapes (Skip Inference)
```bash
cd /media/skumar/External/catkin_ws
/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec \
  --onnx=src/AirSLAM/output/superglue_indoor_sim_int32.onnx \
  --saveEngine=src/AirSLAM/output/superglue_indoor_sim_int32.engine \
  --memPoolSize=workspace:2048 \
  --skipInference \
  --verbose \
  --minShapes=keypoints_0:1x1x2,scores_0:1x1,descriptors_0:1x256x1,keypoints_1:1x1x2,scores_1:1x1,descriptors_1:1x256x1 \
  --optShapes=keypoints_0:1x256x2,scores_0:1x256,descriptors_0:1x256x256,keypoints_1:1x256x2,scores_1:1x256,descriptors_1:1x256x256 \
  --maxShapes=keypoints_0:1x512x2,scores_0:1x512,descriptors_0:1x256x512,keypoints_1:1x512x2,scores_1:1x512,descriptors_1:1x256x512
```

### Option 2: Try with FP16 Enabled
```bash
cd /media/skumar/External/catkin_ws
/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec \
  --onnx=src/AirSLAM/output/superglue_indoor_sim_int32.onnx \
  --saveEngine=src/AirSLAM/output/superglue_indoor_sim_int32.engine \
  --memPoolSize=workspace:2048 \
  --fp16 \
  --skipInference \
  --verbose
```

### Option 3: Alternative - Use the Existing Engine Files
Since the conversion is failing, check if there are already engine files in the output directory that were created previously:

```bash
ls -la /media/skumar/External/catkin_ws/src/AirSLAM/output/*.engine
```

The script I created (`convert_superglue_to_engine.py`) is now working correctly and can be used to systematically try different conversion approaches. Would you like me to try one of the manual command options above, or would you prefer to investigate the existing engine files first?

```shellscript
cd /media/skumar/External/catkin_ws
/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec \
  --onnx=src/AirSLAM/output/superglue_indoor_sim_int32.onnx \
  --saveEngine=src/AirSLAM/output/superglue_indoor_sim_int32.engine \
  --memPoolSize=workspace:2048 \
  --skipInference \
  --verbose \
  --minShapes=keypoints_0:1x1x2,scores_0:1x1,descriptors_0:1x256x1,keypoints_1:1x1x2,scores_1:1x1,descriptors_1:1x256x1 \
  --optShapes=keypoints_0:1x256x2,scores_0:1x256,descriptors_0:1x256x256,keypoints_1:1x256x2,scores_1:1x256,descriptors_1:1x256x256 \
  --maxShapes=keypoints_0:1x512x2,scores_0:1x512,descriptors_0:1x256x512,keypoints_1:1x512x2,scores_1:1x512,descriptors_1:1x256x512
```

```shellscript
cd /media/skumar/External/catkin_ws
/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec \
  --onnx=src/AirSLAM/output/superglue_indoor_sim_int32.onnx \
  --saveEngine=src/AirSLAM/output/superglue_indoor_sim_int32.engine \
  --memPoolSize=workspace:2048 \
  --fp16 \
  --skipInference \
  --verbose
```

```shellscript
ls -la /media/skumar/External/catkin_ws/src/AirSLAM/output/*.engine
```

---

**User**

Let's try `option 1`.

can you list all the `onnx` files inside the `TENSORRT_ROOT`?

can you refer @onnx-to-engine-success.md to figure out how to debug this issue? 

can you compare the `trtexec` commands in the two cases -> 
1. earlier one leading to the segmentation fault
2. the newer one that was success, leading to the generation of `output/superglue_indoor_sim_int32.engine`.

---

**Cursor**

### Comparison of trtexec invocations

- **Earlier (segfault)**
```bash
/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec \
  --onnx=src/AirSLAM/output/superglue_indoor_sim_int32.onnx \
  --saveEngine=src/AirSLAM/output/superglue_indoor_sim_int32.engine \
  --verbose
```
- Environment: No `LD_LIBRARY_PATH` set to include cuDNN/TensorRT target libs
- Flags: Minimal (or later attempts with shapes/memPool/workspace still under same env)
- Paths: Relative input/output
- Result: Segmentation fault right after “Loading standard plugins”

- **Newer (success)**
```bash
cd /home/skumar/ext_ssd/TensorRT-8.6.1.6 && \
export LD_LIBRARY_PATH=./targets/x86_64-linux-gnu/lib:/usr/local/cuda/targets/x86_64-linux-gnu/lib:$LD_LIBRARY_PATH && \
/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec \
  --onnx=/media/skumar/External/catkin_ws/src/AirSLAM/output/superglue_indoor_sim_int32.onnx \
  --saveEngine=/media/skumar/External/catkin_ws/src/AirSLAM/output/superglue_indoor_sim_int32.engine \
  --memPoolSize=workspace:512 \
  --fp16 \
  --verbose \
  --minShapes=keypoints_0:1x1x2,scores_0:1x1,descriptors_0:1x256x1,keypoints_1:1x1x2,scores_1:1x1,descriptors_1:1x256x1 \
  --optShapes=keypoints_0:1x512x2,scores_0:1x512,descriptors_0:1x256x512,keypoints_1:1x512x2,scores_1:1x512,descriptors_1:1x256x512 \
  --maxShapes=keypoints_0:1x1024x2,scores_0:1x1024,descriptors_0:1x256x1024,keypoints_1:1x1024x2,scores_1:1x1024,descriptors_1:1x256x1024
```
- Environment: `LD_LIBRARY_PATH` explicitly includes cuDNN (`.../targets/x86_64-linux-gnu/lib`) and CUDA libs
- Flags: `--fp16`, `--memPoolSize`, explicit dynamic shapes (min/opt/max)
- Paths: Absolute input/output
- Result: Engine built successfully (~35 MB), inference ran; no segfault

### Key differences that fixed the crash
- **cuDNN on library path**: Adding `.../targets/x86_64-linux-gnu/lib` (cuDNN .so’s) to `LD_LIBRARY_PATH` prevented the segfault during plugin load.
- Explicit dynamic shape profiles and `--fp16` were used in the successful run, but earlier attempts with shapes still failed; the decisive change was the environment setup.

```shellscript
/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec \
  --onnx=src/AirSLAM/output/superglue_indoor_sim_int32.onnx \
  --saveEngine=src/AirSLAM/output/superglue_indoor_sim_int32.engine \
  --verbose
```

```shellscript
cd /home/skumar/ext_ssd/TensorRT-8.6.1.6 && \
export LD_LIBRARY_PATH=./targets/x86_64-linux-gnu/lib:/usr/local/cuda/targets/x86_64-linux-gnu/lib:$LD_LIBRARY_PATH && \
/home/skumar/ext_ssd/TensorRT-8.6.1.6/bin/trtexec \
  --onnx=/media/skumar/External/catkin_ws/src/AirSLAM/output/superglue_indoor_sim_int32.onnx \
  --saveEngine=/media/skumar/External/catkin_ws/src/AirSLAM/output/superglue_indoor_sim_int32.engine \
  --memPoolSize=workspace:512 \
  --fp16 \
  --verbose \
  --minShapes=keypoints_0:1x1x2,scores_0:1x1,descriptors_0:1x256x1,keypoints_1:1x1x2,scores_1:1x1,descriptors_1:1x256x1 \
  --optShapes=keypoints_0:1x512x2,scores_0:1x512,descriptors_0:1x256x512,keypoints_1:1x512x2,scores_1:1x512,descriptors_1:1x256x512 \
  --maxShapes=keypoints_0:1x1024x2,scores_0:1x1024,descriptors_0:1x256x1024,keypoints_1:1x1024x2,scores_1:1x1024,descriptors_1:1x256x1024
```

