# ONNX to TensorRT Engine Conversion Index

## Successfully Converted Models

| ONNX File | Engine File | Size | Performance | Command Used |
|-----------|-------------|------|-------------|--------------|
| `superglue_indoor_sim_int32.onnx` | `superglue_indoor_sim_int32.engine` | 36MB | 173.191 qps | `trtexec --onnx=superglue_indoor_sim_int32.onnx --saveEngine=superglue_indoor_sim_int32.engine --memPoolSize=workspace:512 --fp16 --verbose --minShapes=keypoints_0:1x1x2,scores_0:1x1,descriptors_0:1x256x1,keypoints_1:1x1x2,scores_1:1x1,descriptors_1:1x256x1 --optShapes=keypoints_0:1x512x2,scores_0:1x512,descriptors_0:1x256x512,keypoints_1:1x512x2,scores_1:1x512,descriptors_1:1x256x512 --maxShapes=keypoints_0:1x1024x2,scores_0:1x1024,descriptors_0:1x256x1024,keypoints_1:1x1024x2,scores_1:1x1024,descriptors_1:1x256x1024` |
| `superglue_outdoor_sim_int32.onnx` | `superglue_outdoor_sim_int32.engine` | 36MB | 177.811 qps | `trtexec --onnx=superglue_outdoor_sim_int32.onnx --saveEngine=superglue_outdoor_sim_int32.engine --memPoolSize=workspace:512 --fp16 --verbose --minShapes=keypoints_0:1x1x2,scores_0:1x1,descriptors_0:1x256x1,keypoints_1:1x1x2,scores_1:1x1,descriptors_1:1x256x1 --optShapes=keypoints_0:1x512x2,scores_0:1x512,descriptors_0:1x256x512,keypoints_1:1x512x2,scores_1:1x512,descriptors_1:1x256x512 --maxShapes=keypoints_0:1x1024x2,scores_0:1x1024,descriptors_0:1x256x1024,keypoints_1:1x1024x2,scores_1:1x1024,descriptors_1:1x256x1024` |
| `superpoint_v1_sim_int32.onnx` | `superpoint_v1_sim_int32.engine` | 3.5MB | 519.793 qps | `trtexec --onnx=superpoint_v1_sim_int32.onnx --saveEngine=superpoint_v1_sim_int32.engine --memPoolSize=workspace:512 --fp16 --verbose --minShapes=input:1x1x100x100 --optShapes=input:1x1x500x500 --maxShapes=input:1x1x1500x1500` |
| `superpoint_lightglue.onnx` | `superpoint_lightglue.engine` | 28MB | 468.421 qps | `trtexec --onnx=superpoint_lightglue.onnx --saveEngine=superpoint_lightglue.engine --memPoolSize=workspace:512 --fp16 --verbose --minShapes=keypoints_0:1x1x2,keypoints_1:1x1x2,descriptors_0:1x1x256,descriptors_1:1x1x256 --optShapes=keypoints_0:1x512x2,keypoints_1:1x512x2,descriptors_0:1x512x256,descriptors_1:1x512x256 --maxShapes=keypoints_0:1x1024x2,keypoints_1:1x1024x2,descriptors_0:1x1024x256,descriptors_1:1x1024x256` |
| `plnet_s1.onnx` | `plnet_s1.engine` | 517KB | 298.447 qps | `trtexec --onnx=plnet_s1.onnx --saveEngine=plnet_s1.engine --memPoolSize=workspace:512 --fp16 --verbose --minShapes=juncs_pred:1x2,lines_pred:1x4,idx_lines_for_junctions:1x2,inverse:1x1,iskeep_index:1x1,loi_features:1x16x16x16,loi_features_thin:1x4x16x16,loi_features_aux:1x4x16x16 --optShapes=juncs_pred:250x2,lines_pred:20000x4,idx_lines_for_junctions:20000x2,inverse:20000x1,iskeep_index:20000x1,loi_features:1x128x128x128,loi_features_thin:1x4x128x128,loi_features_aux:1x4x128x128 --maxShapes=juncs_pred:500x2,lines_pred:50000x4,idx_lines_for_junctions:50000x2,inverse:50000x1,iskeep_index:50000x1,loi_features:1x512x512x512,loi_features_thin:1x4x512x512,loi_features_aux:1x4x512x512` |

## Conversion Environment

All conversions used:
- **TensorRT Version**: 8.6.1.6
- **LD_LIBRARY_PATH**: `./targets/x86_64-linux-gnu/lib:/usr/local/cuda/targets/x86_64-linux/lib:$LD_LIBRARY_PATH`
- **Working Directory**: `/home/skumar/ext_ssd/TensorRT-8.6.1.6`

## Failed Conversions

| ONNX File | Attempt | Command Used | Status | Details |
|-----------|---------|--------------|--------|---------|
| `plnet_s0.onnx` | Dynamic Shapes | `trtexec --onnx=plnet_s0.onnx --saveEngine=plnet_s0.engine --memPoolSize=workspace:512 --tf32 --verbose --minShapes=input:1x1x100x100 --optShapes=input:1x1x512x512 --maxShapes=input:1x1x1500x1500` | ❌ Failed | Segmentation fault during engine serialization |
| `plnet_s0.onnx` | Fixed Input Shape | `trtexec --onnx=plnet_s0.onnx --saveEngine=plnet_s0_fixed.engine --memPoolSize=workspace:4096 --verbose --shapes=input:1x1x512x512` | ✅ Success | Successfully converted using fixed input shape |

