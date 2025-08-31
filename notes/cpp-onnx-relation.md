# Map src files to onnx files
_Exported on 31/08/2025 at 16:09:44 GMT+5:30 from Cursor (1.5.7)_

---

**User**

Look at the `onnx` files in `src/AirSLAM/output` folder. 
Look at the files in @src/ folder. 

Can you now build a table that shows which file(s) from the `src` folder corresponds to which `onnx` files in the `src/AirSLAM/otuput` folder?

---

**Cursor**

Based on my analysis of the ONNX files in the `src/AirSLAM/output` folder and the source files in `src/AirSLAM/src`, here is the mapping table:

| Source File | ONNX Model(s) | Description |
|-------------|---------------|-------------|
| `plnet.cpp` | `plnet_s0.onnx`<br>`plnet_s1.onnx` | PLNet uses a two-stage architecture with separate models for line detection and feature extraction |
| `super_point.cpp` | `superpoint_v1_sim_int32.onnx`<br>`superpoint_lightglue.onnx` | SuperPoint for keypoint detection (standalone and combined with LightGlue) |
| `super_glue.cpp` | `superglue_indoor_sim_int32.onnx`<br>`superglue_outdoor_sim_int32.onnx` | SuperGlue matcher for indoor and outdoor environments |
| `light_glue.cpp` | `superpoint_lightglue.onnx` | LightGlue matcher combined with SuperPoint |

## Key Findings:

1. **PLNet** (`plnet.cpp`) uses a two-stage ONNX model system:
   - `plnet_s0.onnx` - Stage 0 model for initial processing
   - `plnet_s1.onnx` - Stage 1 model for line and junction detection

2. **SuperPoint** (`super_point.cpp`) has both standalone and combined models:
   - `superpoint_v1_sim_int32.onnx` - Standalone SuperPoint model
   - `superpoint_lightglue.onnx` - Combined SuperPoint + LightGlue model

3. **SuperGlue** (`super_glue.cpp`) has environment-specific models:
   - `superglue_indoor_sim_int32.onnx` - Optimized for indoor environments
   - `superglue_outdoor_sim_int32.onnx` - Optimized for outdoor environments

4. **LightGlue** (`light_glue.cpp`) primarily uses the combined model:
   - `superpoint_lightglue.onnx` - Integrated SuperPoint and LightGlue matching

The configuration files primarily use `superpoint_lightglue.onnx` as the default point matcher, which combines SuperPoint feature detection with LightGlue matching in a single optimized model. The individual models exist for flexibility and specialized use cases.

