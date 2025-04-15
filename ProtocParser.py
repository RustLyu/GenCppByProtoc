import re

class ProtocParser:
    def parse_fields(self, input_file):
        """解析协议文件获取字段列表"""
        pattern = re.compile(r'require\s+(\w+)\s+(\w+);')
        fields = []
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                if match := pattern.match(line.strip()):
                    fields.append((match.group(1), match.group(2)))
        return fields