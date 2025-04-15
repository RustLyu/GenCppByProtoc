import os
import glob
from ProtocParser import *
from GeneratorH import *
from GeneratorCC import *

class DiskIo:
    def __init__(self):
        pass
    def save_file(self, filename, content):
        """保存文件带BOM头"""
        with open(filename, 'w', encoding='utf-8-sig') as f:
            f.write(content)

    def process_directory(self, namespace, input_dir=".", output_dir="."):
        """批量处理目录下所有协议文件
        Args:
            namespace: 命名空间名称
            input_dir: 输入目录路径
            output_dir: 输出目录路径
        """
        p = ProtocParser()
        gen_h = GeneratorH()
        gen_cc = GeneratorCC()
        io = DiskIo()
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

        # 处理输入目录中的所有txt文件
        for txt_file in glob.glob(os.path.join(input_dir, "*.txt")):
            class_name = os.path.splitext(os.path.basename(txt_file))[0]
            fields = p.parse_fields(txt_file)

            # 生成输出文件路径
            h_file = os.path.join(output_dir, f"{class_name}.h")
            cpp_file = os.path.join(output_dir, f"{class_name}.cpp")

            # 生成并保存文件
            io.save_file(h_file, gen_h.generate_header(class_name, namespace, fields))
            io.save_file(cpp_file, gen_cc.generate_cpp(class_name, namespace, fields))