# List all onnx files in directory
_Exported on 31/08/2025 at 4:21:43 GMT+5:30 from Cursor (1.5.7)_

---

**User**

list all the `.onnx` files in `/home/skumar/ext_ssd/TensorRT-8.6.1.6`.

---

**Cursor**

Here are the `.onnx` files found in `/home/skumar/ext_ssd/TensorRT-8.6.1.6`:

- `data/resnet50/ResNet50.onnx`
- `data/mnist/mnist.onnx`

There are 2 `.onnx` files in total in that directory.

---

**User**

can you use the `trtexec` from the same folder to convert these to `.engine`? 

check the `bin` folder. 

---

**Cursor**

The issue is that **cuDNN runtime libraries are missing** from your system. TensorRT 8.6.1 requires cuDNN to be installed as system libraries, but only a stub library is present in your TensorRT installation.

## Summary of the problem:
- **TensorRT version**: 8.6.1 ✓
- **CUDA version**: 12.1 (nvcc) / 12.8 (driver) ✓  
- **GPU**: RTX 3070 ✓
- **cuDNN**: Missing ❌

## To fix this issue, you need to:

1. **Download cuDNN 8.6.x** from NVIDIA's website (compatible with TensorRT 8.6.1)
2. **Install cuDNN** system-wide or add it to LD_LIBRARY_PATH
3. **Ensure version compatibility**:
   - TensorRT 8.6.1 works with CUDA 11.8, 12.0, 12.1
   - cuDNN should be version 8.6.x

## Alternative approaches:
- **Use a different TensorRT version** that's compatible with your current CUDA/cuDNN setup
- **Install via NVIDIA's package manager** (if available for your system)
- **Use Docker containers** with pre-configured TensorRT environments

The segmentation fault occurs because TensorRT tries to load cuDNN plugins during initialization but fails to find the required shared libraries. Once you install the proper cuDNN libraries, the `trtexec` commands should work correctly to convert your `.onnx` models to `.engine` files.

---

**User**

I have downloaded `cudnn-linux-x86_64-8.9.0.131_cuda12-archive.tar.xz` at `/home/skumar/ext_ssd`.

---

**Cursor**

## ✅ Conversion Complete!

Both ONNX models have been successfully converted to TensorRT engine files! Here's a summary of what was accomplished:

### 📁 **Files Created:**
- **`data/mnist/mnist.engine`** - 297 KB (converted from MNIST ONNX model)
- **`data/resnet50/ResNet50.engine`** - 105 MB (converted from ResNet50 ONNX model)

### 📊 **Performance Results:**

**MNIST Model:**
- **Throughput:** 40,105 qps (queries per second)
- **Latency:** ~0.025 ms mean
- **GPU Compute Time:** ~0.017 ms

**ResNet50 Model:**
- **Throughput:** 547 qps (queries per second)
- **Latency:** ~1.86 ms mean
- **GPU Compute Time:** ~1.83 ms

### 🔧 **What Was Fixed:**
The original issue was **missing cuDNN libraries**. I resolved this by:
1. **Installing cuDNN 8.9.0** from the downloaded archive
2. **Copying cuDNN libraries** to the TensorRT installation directory
3. **Setting proper LD_LIBRARY_PATH** to include both TensorRT and cuDNN libraries
4. **Successfully converting** both models using `trtexec`

### 🎯 **Next Steps:**
You can now use these `.engine` files for:
- **Inference** with TensorRT runtime
- **Deployment** on NVIDIA GPUs
- **Integration** with your AirSLAM project

The engines are optimized for your RTX 3070 GPU and should provide significantly faster inference compared to the original ONNX models! 🚀

