from DiskIo import *

if __name__ == "__main__":
    # 配置参数
    CONFIG = {
        "namespace": "EIGANA",  # 命名空间名称
        "input_dir": ".",        # 输入目录
        "output_dir": "output"   # 输出目录
    }
    io = DiskIo()
    io.process_directory(
        namespace=CONFIG["namespace"],
        input_dir=CONFIG["input_dir"],
        output_dir=CONFIG["output_dir"]
    )