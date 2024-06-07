import os


def init_one_api():
    one_api_installation_path = r"C:\Program Files (x86)\Intel\oneAPI"
    os.environ["APM"] = rf"{one_api_installation_path}\advisor\2024.1\perfmodels"
    os.environ["CLASSPATH"] = (
        rf"{one_api_installation_path}\dal\latest\share\java\onedal.jar"
    )
    os.environ["CMAKE_PREFIX_PATH"] = os.pathsep.join(
        [
            rf"{one_api_installation_path}\compiler\latest",
            rf"{one_api_installation_path}\dal\latest",
            rf"{one_api_installation_path}\dnnl\latest\lib\cmake",
            rf"{one_api_installation_path}\dpl\latest\lib\cmake\oneDPL",
            rf"{one_api_installation_path}\ipp\latest\lib\cmake\ipp",
            rf"{one_api_installation_path}\tbb\latest",
        ]
    )
    os.environ["CMPLR_ROOT"] = rf"{one_api_installation_path}\compiler\latest"
    os.environ["CONDA_BAT"] = (
        r"C:\Users\particleg\scoop\apps\miniconda\current\condabin\conda.bat"
    )
    os.environ["CONDA_EXE"] = (
        r"C:\Users\particleg\scoop\apps\miniconda\current\Scripts\conda.exe"
    )
    os.environ["CONDA_PREFIX_1"] = r"C:\Users\particleg\scoop\apps\miniconda\current"
    os.environ["CONDA_PYTHON_EXE"] = (
        r"C:\Users\particleg\scoop\apps\miniconda\current\python.exe"
    )
    os.environ["CONDA_SHLVL"] = r"1"
    os.environ["CPATH"] = os.pathsep.join(
        [
            rf"{one_api_installation_path}\compiler\latest\opt\oclfpga\include",
            rf"{one_api_installation_path}\compiler\latest\include",
            rf"{one_api_installation_path}\dal\latest\include\dal",
            rf"{one_api_installation_path}\dev-utilities\latest\include",
            rf"{one_api_installation_path}\dpcpp-ct\latest\include",
            rf"{one_api_installation_path}\dpl\latest\include",
            rf"{one_api_installation_path}\ipp\latest\include",
            rf"{one_api_installation_path}\ippcp\latest\include",
            rf"{one_api_installation_path}\mkl\latest\include",
            rf"{one_api_installation_path}\ocloc\latest\include",
            rf"{one_api_installation_path}\tbb\latest\include",
        ]
    )
    os.environ["DAL_MAJOR_BINARY"] = r"2"
    os.environ["DAL_MINOR_BINARY"] = r"0"
    os.environ["DALROOT"] = rf"{one_api_installation_path}\dal\latest"
    os.environ["DNNLROOT"] = rf"{one_api_installation_path}\dnnl\latest"
    os.environ["DPL_ROOT"] = rf"{one_api_installation_path}\dpl\latest"
    os.environ["ERRORSTATE"] = r"0"
    os.environ["INCLUDE"] = os.pathsep.join(
        [
            rf"{one_api_installation_path}\compiler\latest\include",
            rf"{one_api_installation_path}\dal\latest\include\dal",
            rf"{one_api_installation_path}\dev-utilities\latest\include",
            rf"{one_api_installation_path}\dnnl\latest\include",
            rf"{one_api_installation_path}\dpcpp-ct\latest\env\..\include",
            rf"{one_api_installation_path}\ipp\latest\include",
            rf"{one_api_installation_path}\ippcp\latest\include",
            rf"{one_api_installation_path}\mkl\latest\include",
            rf"{one_api_installation_path}\ocloc\latest\include",
            rf"{one_api_installation_path}\tbb\latest\include",
        ]
    )
    os.environ["INTEL_PYTHONPATH"] = (
        rf"{one_api_installation_path}\advisor\2024.1\pythonapi"
    )
    os.environ["INTELFPGAOCLSDKROOT"] = (
        rf"{one_api_installation_path}\compiler\latest\opt\oclfpga"
    )
    os.environ["INTELGTDEBUGGERROOT"] = rf"{one_api_installation_path}\debugger\latest"
    os.environ["IPP_TARGET_ARCH"] = r"intel64"
    os.environ["IPPCP_TARGET_ARCH"] = r"intel64"
    os.environ["IPPCP_TARGET_BIN_ARCH"] = r"bin"
    os.environ["IPPCP_TARGET_LIB_ARCH"] = r"lib"
    os.environ["IPPCRYPTOROOT"] = rf"{one_api_installation_path}\ippcp\latest"
    os.environ["IPPROOT"] = rf"{one_api_installation_path}\ipp\latest"
    os.environ["LIB"] = os.pathsep.join(
        [
            rf"{one_api_installation_path}\tbb\latest\lib",
            rf"{one_api_installation_path}\mkl\latest\lib",
            rf"{one_api_installation_path}\ippcp\latest\lib",
            rf"{one_api_installation_path}\ipp\latest\lib",
            rf"{one_api_installation_path}\dnnl\latest\lib",
            rf"{one_api_installation_path}\dal\latest\lib",
            rf"{one_api_installation_path}\compiler\latest\lib\clang\18\lib\windows",
            rf"{one_api_installation_path}\compiler\latest\opt\compiler\lib",
            rf"{one_api_installation_path}\compiler\latest\lib",
        ]
    )
    os.environ["LIBRARY_PATH"] = os.pathsep.join(
        [
            rf"{one_api_installation_path}\ippcp\latest\lib",
            rf"{one_api_installation_path}\ipp\latest\lib",
        ]
    )
    os.environ["MKLROOT"] = rf"{one_api_installation_path}\mkl\latest"
    os.environ["NLSPATH"] = rf"{one_api_installation_path}\mkl\latest\share\locale\1033"
    os.environ["OCL_ICD_FILENAMES"] = os.pathsep.join(
        [
            rf"{one_api_installation_path}\compiler\latest\opt\oclfpga\host\windows64\bin\alteracl.dll",
            rf"{one_api_installation_path}\compiler\latest\bin\intelocl64_emu.dll",
            rf"{one_api_installation_path}\compiler\latest\bin\intelocl64.dll",
        ]
    )
    os.environ["OCLOC_ROOT"] = rf"{one_api_installation_path}\ocloc\latest"
    os.environ["ONEAPI_ROOT"] = rf"{one_api_installation_path}"
    os.environ["Path"] += os.pathsep + os.pathsep.join(
        [
            rf"{one_api_installation_path}\advisor\2024.1\bin64",
            rf"{one_api_installation_path}\compiler\latest\bin",
            rf"{one_api_installation_path}\compiler\latest\lib\ocloc",
            rf"{one_api_installation_path}\compiler\latest\opt\oclfpga\bin",
            rf"{one_api_installation_path}\compiler\latest\opt\oclfpga\host\windows64\bin",
            rf"{one_api_installation_path}\dal\latest\bin",
            rf"{one_api_installation_path}\debugger\latest\opt\debugger\bin",
            rf"{one_api_installation_path}\dev-utilities\latest\bin",
            rf"{one_api_installation_path}\dnnl\latest\bin",
            rf"{one_api_installation_path}\dpcpp-ct\latest\bin",
            rf"{one_api_installation_path}\ipp\latest\bin",
            rf"{one_api_installation_path}\ippcp\latest\bin",
            rf"{one_api_installation_path}\mkl\latest\bin",
            rf"{one_api_installation_path}\ocloc\latest\bin",
            rf"{one_api_installation_path}\tbb\latest\bin",
            rf"{one_api_installation_path}\vtune\2024.1\bin64",
        ]
    )
    os.environ["PKG_CONFIG_PATH"] = os.pathsep.join(
        [
            rf"{one_api_installation_path}\tbb\latest\lib\pkgconfig",
            rf"{one_api_installation_path}\mkl\latest\lib\pkgconfig",
            rf"{one_api_installation_path}\ippcp\latest\lib\pkgconfig",
            rf"{one_api_installation_path}\dpl\latest\lib\pkgconfig",
            rf"{one_api_installation_path}\dnnl\latest\lib\pkgconfig",
            rf"{one_api_installation_path}\dal\latest\lib\pkgconfig",
            rf"{one_api_installation_path}\compiler\latest\lib\pkgconfig",
        ]
    )
    os.environ["PYTHONPATH"] = rf"{one_api_installation_path}\advisor\2024.1\pythonapi"
    os.environ["SETVARS_COMPLETED"] = r"1"
    os.environ["TBB_BIN_DIR"] = rf"{one_api_installation_path}\tbb\latest\bin"
    os.environ["TBB_DLL_PATH"] = rf"{one_api_installation_path}\tbb\latest\bin"
    os.environ["TBB_SCRIPT_DIR"] = rf"{one_api_installation_path}\tbb\latest\env"
    os.environ["TBB_TARGET_ARCH"] = r"intel64"
    os.environ["TBBROOT"] = rf"{one_api_installation_path}\tbb\latest"
    os.environ["USE_INTEL_LLVM"] = r"0"
    os.environ["VARSDIR"] = rf"{one_api_installation_path}\ocloc\latest\env"
    os.environ["VTUNE_PROFILER_DIR"] = rf"{one_api_installation_path}\vtune\2024.1"

    with open("oneAPI_env.txt", "w") as f:
        for key, value in os.environ.items():
            f.write(f"{key}={value}\n")
