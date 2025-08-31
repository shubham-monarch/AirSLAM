# List trxtexec options and descriptions
_Exported on 31/08/2025 at 20:44:53 GMT+5:30 from Cursor (1.5.7)_

---

**User**

use the `trxtexec` cli in `TENSORRT_ROOT` (See @CMakeLists.txt ) and run with the `--help` flag.
List all the options available in a tabular form along with a brief description. 

---

**Cursor**

Below is a comprehensive list of all options available in the `trtexec` CLI tool, organized in a tabular format with brief descriptions. I've grouped them by category based on the help output structure.

| Option | Description | Category |
|--------|-------------|----------|
| `--uff=<file>` | UFF model | Model Options |
| `--onnx=<file>` | ONNX model | Model Options |
| `--model=<file>` | Caffe model (default = no model, random weights used) | Model Options |
| `--deploy=<file>` | Caffe prototxt file | Model Options |
| `--output=<name>[,<name>]*` | Output names (it can be specified multiple times); at least one output is required for UFF and Caffe | Model Options |
| `--uffInput=<name>,X,Y,Z` | Input blob name and its dimensions (X,Y,Z=C,H,W), it can be specified multiple times; at least one is required for UFF models | Model Options |
| `--uffNHWC` | Set if inputs are in the NHWC layout instead of NCHW (use X,Y,Z=H,W,C order in --uffInput) | Model Options |
| `--maxBatch` | Set max batch size and build an implicit batch engine (default = same size as --batch). This option should not be used when the input model is ONNX or when dynamic shapes are provided. | Build Options |
| `--minShapes=spec` | Build with dynamic shapes using a profile with the min shapes provided | Build Options |
| `--optShapes=spec` | Build with dynamic shapes using a profile with the opt shapes provided | Build Options |
| `--maxShapes=spec` | Build with dynamic shapes using a profile with the max shapes provided | Build Options |
| `--minShapesCalib=spec` | Calibrate with dynamic shapes using a profile with the min shapes provided | Build Options |
| `--optShapesCalib=spec` | Calibrate with dynamic shapes using a profile with the opt shapes provided | Build Options |
| `--maxShapesCalib=spec` | Calibrate with dynamic shapes using a profile with the max shapes provided | Build Options |
| `--inputIOFormats=spec` | Type and format of each of the input tensors (default = all inputs in fp32:chw) | Build Options |
| `--outputIOFormats=spec` | Type and format of each of the output tensors (default = all outputs in fp32:chw) | Build Options |
| `--workspace=N` | Set workspace size in MiB | Build Options |
| `--memPoolSize=poolspec` | Specify the size constraints of the designated memory pool(s) in MiB | Build Options |
| `--profilingVerbosity=mode` | Specify profiling verbosity. mode ::= layer_names_only\|detailed\|none (default = layer_names_only) | Build Options |
| `--minTiming=M` | Set the minimum number of iterations used in kernel selection (default = 1) | Build Options |
| `--avgTiming=M` | Set the number of times averaged in each iteration for kernel selection (default = 8) | Build Options |
| `--refit` | Mark the engine as refittable. This will allow the inspection of refittable layers and weights within the engine. | Build Options |
| `--versionCompatible, --vc` | Mark the engine as version compatible. This allows the engine to be used with newer versions of TensorRT on the same host OS, as well as TensorRT's dispatch and lean runtimes. Only supported with explicit batch. | Build Options |
| `--useRuntime=runtime` | TensorRT runtime to execute engine. "lean" and "dispatch" require loading VC engine and do not support building an engine. runtime::= "full"\|"lean"\|"dispatch" | Build Options |
| `--leanDLLPath=<file>` | External lean runtime DLL to use in version compatible mode. | Build Options |
| `--excludeLeanRuntime` | When --versionCompatible is enabled, this flag indicates that the generated engine should not include an embedded lean runtime. If this is set, the user must explicitly specify a valid lean runtime to use when loading the engine. Only supported with explicit batch and weights within the engine. | Build Options |
| `--sparsity=spec` | Control sparsity (default = disabled). Sparsity: spec ::= "disable", "enable", "force" | Build Options |
| `--noTF32` | Disable tf32 precision (default is to enable tf32, in addition to fp32) | Build Options |
| `--fp16` | Enable fp16 precision, in addition to fp32 (default = disabled) | Build Options |
| `--int8` | Enable int8 precision, in addition to fp32 (default = disabled) | Build Options |
| `--fp8` | Enable fp8 precision, in addition to fp32 (default = disabled) | Build Options |
| `--best` | Enable all precisions to achieve the best performance (default = disabled) | Build Options |
| `--directIO` | Avoid reformatting at network boundaries. (default = disabled) | Build Options |
| `--precisionConstraints=spec` | Control precision constraint setting. (default = none) | Build Options |
| `--layerPrecisions=spec` | Control per-layer precision constraints. Effective only when precisionConstraints is set to "obey" or "prefer". (default = none) | Build Options |
| `--layerOutputTypes=spec` | Control per-layer output type constraints. Effective only when precisionConstraints is set to "obey" or "prefer". (default = none | Build Options |
| `--layerDeviceTypes=spec` | Specify layer-specific device type. | Build Options |
| `--calib=<file>` | Read INT8 calibration cache file | Build Options |
| `--safe` | Enable build safety certified engine, if DLA is enable, --buildDLAStandalone will be specified automatically (default = disabled) | Build Options |
| `--buildDLAStandalone` | Enable build DLA standalone loadable which can be loaded by cuDLA, when this option is enabled, --allowGPUFallback is disallowed and --skipInference is enabled by default. Additionally, specifying --inputIOFormats and --outputIOFormats restricts I/O data type and memory layout (default = disabled) | Build Options |
| `--allowGPUFallback` | When DLA is enabled, allow GPU fallback for unsupported layers (default = disabled) | Build Options |
| `--consistency` | Perform consistency checking on safety certified engine | Build Options |
| `--restricted` | Enable safety scope checking with kSAFETY_SCOPE build flag | Build Options |
| `--saveEngine=<file>` | Save the serialized engine | Build Options |
| `--loadEngine=<file>` | Load a serialized engine | Build Options |
| `--tacticSources=tactics` | Specify the tactics to be used by adding (+) or removing (-) tactics from the default tactic sources (default = all available tactics). | Build Options |
| `--noBuilderCache` | Disable timing cache in builder (default is to enable timing cache) | Build Options |
| `--heuristic` | Enable tactic selection heuristic in builder (default is to disable the heuristic) | Build Options |
| `--timingCacheFile=<file>` | Save/load the serialized global timing cache | Build Options |
| `--preview=features` | Specify preview feature to be used by adding (+) or removing (-) preview features from the default | Build Options |
| `--builderOptimizationLevel` | Set the builder optimization level. (default is 3) | Build Options |
| `--hardwareCompatibilityLevel=mode` | Make the engine file compatible with other GPU architectures. (default = none) | Build Options |
| `--tempdir=<dir>` | Overrides the default temporary directory TensorRT will use when creating temporary files. | Build Options |
| `--tempfileControls=controls` | Controls what TensorRT is allowed to use when creating temporary executable files. | Build Options |
| `--maxAuxStreams=N` | Set maximum number of auxiliary streams per inference stream that TRT is allowed to use to run kernels in parallel if the network contains ops that can run in parallel, with the cost of more memory usage. Set this to 0 for optimal memory usage. (default = using heuristics) | Build Options |
| `--batch=N` | Set batch size for implicit batch engines (default = 1) | Inference Options |
| `--shapes=spec` | Set input shapes for dynamic shapes inference inputs. | Inference Options |
| `--loadInputs=spec` | Load input values from files (default = generate random inputs). Input names can be wrapped with single quotes (ex: 'Input:0') | Inference Options |
| `--iterations=N` | Run at least N inference iterations (default = 10) | Inference Options |
| `--warmUp=N` | Run for N milliseconds to warmup before measuring performance (default = 200) | Inference Options |
| `--duration=N` | Run performance measurements for at least N seconds wallclock time (default = 3) | Inference Options |
| `--sleepTime=N` | Delay inference start with a gap of N milliseconds between launch and compute (default = 0) | Inference Options |
| `--idleTime=N` | Sleep N milliseconds between two continuous iterations(default = 0) | Inference Options |
| `--infStreams=N` | Instantiate N engines to run inference concurrently (default = 1) | Inference Options |
| `--exposeDMA` | Serialize DMA transfers to and from device (default = disabled). | Inference Options |
| `--noDataTransfers` | Disable DMA transfers to and from device (default = enabled). | Inference Options |
| `--useManagedMemory` | Use managed memory instead of separate host and device allocations (default = disabled). | Inference Options |
| `--useSpinWait` | Actively synchronize on GPU events. This option may decrease synchronization time but increase CPU usage and power (default = disabled) | Inference Options |
| `--threads` | Enable multithreading to drive engines with independent threads or speed up refitting (default = disabled) | Inference Options |
| `--useCudaGraph` | Use CUDA graph to capture engine execution and then launch inference (default = disabled). | Inference Options |
| `--timeDeserialize` | Time the amount of time it takes to deserialize the network and exit. | Inference Options |
| `--timeRefit` | Time the amount of time it takes to refit the engine before inference. | Inference Options |
| `--separateProfileRun` | Do not attach the profiler in the benchmark run; if profiling is enabled, a second profile run will be executed (default = disabled) | Inference Options |
| `--skipInference` | Exit after the engine has been built and skip inference perf measurement (default = disabled) | Inference Options |
| `--persistentCacheRatio` | Set the persistentCacheLimit in ratio, 0.5 represent half of max persistent L2 size (default = 0) | Inference Options |
| `--verbose` | Use verbose logging (default = false) | Reporting Options |
| `--avgRuns=N` | Report performance measurements averaged over N consecutive iterations (default = 10) | Reporting Options |
| `--percentile=P1,P2,P3,...` | Report performance for the P1,P2,P3,... percentages (0<=P_i<=100, 0 representing max perf, and 100 representing min perf; (default = 90,95,99%) | Reporting Options |
| `--dumpRefit` | Print the refittable layers and weights from a refittable engine | Reporting Options |
| `--dumpOutput` | Print the output tensor(s) of the last inference iteration (default = disabled) | Reporting Options |
| `--dumpRawBindingsToFile` | Print the input/output tensor(s) of the last inference iteration to file(default = disabled) | Reporting Options |
| `--dumpProfile` | Print profile information per layer (default = disabled) | Reporting Options |
| `--dumpLayerInfo` | Print layer information of the engine to console (default = disabled) | Reporting Options |
| `--exportTimes=<file>` | Write the timing results in a json file (default = disabled) | Reporting Options |
| `--exportOutput=<file>` | Write the output tensors to a json file (default = disabled) | Reporting Options |
| `--exportProfile=<file>` | Write the profile information per layer in a json file (default = disabled) | Reporting Options |
| `--exportLayerInfo=<file>` | Write the layer information of the engine in a json file (default = disabled) | Reporting Options |
| `--device=N` | Select cuda device N (default = 0) | System Options |
| `--useDLACore=N` | Select DLA core N for layers that support DLA (default = none) | System Options |
| `--staticPlugins` | Plugin library (.so) to load statically (can be specified multiple times) | System Options |
| `--dynamicPlugins` | Plugin library (.so) to load dynamically and may be serialized with the engine if they are included in --setPluginsToSerialize (can be specified multiple times) | System Options |
| `--setPluginsToSerialize` | Plugin library (.so) to be serialized with the engine (can be specified multiple times) | System Options |
| `--ignoreParsedPluginLibs` | By default, when building a version-compatible engine, plugin libraries specified by the ONNX parser are implicitly serialized with the engine (unless --excludeLeanRuntime is specified) and loaded dynamically. Enable this flag to ignore these plugin libraries instead. | System Options |
| `--help, -h` | Print this message | Help |

**Notes:**
- The tool supports various model formats (UFF, ONNX, Caffe)
- Extensive build options for optimization, precision, and hardware targeting
- Comprehensive inference options for performance measurement and profiling
- Multiple reporting options for analyzing engine performance and characteristics
- System-level options for device selection and plugin management

This covers all the options available in TensorRT's trtexec tool version 8.6.1.6.

