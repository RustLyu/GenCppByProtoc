import textwrap
from string import Template

class GeneratorH:
    # 定义头文件模板
    HEADER_TEMPLATE = textwrap.dedent("""
        #ifndef ${include_guard}
        #define ${include_guard}

        class ${impl_class};

        class ${class_name} {
        public:
            ${class_name}();
            ~${class_name}();
        ${get_methods}

        private:
            ${impl_class}* pImpl;
        };

        #endif // ${include_guard}
    """)

    # 定义getter方法模板
    GETTER_TEMPLATE = textwrap.dedent("""
        /**
         * @brief 获取
         * @return ${field_type} 返回
         */
        ${return_type} Get${field_name}();
    """)

    def generate_header(self, class_name, namespace, fields):
        """生成头文件内容"""
        # 准备模板变量
        include_guard = f"{class_name.upper()}_H"
        impl_class = f"{class_name}Impl"
        
        # 生成所有getter方法
        get_methods = []
        for field_type, field_name in fields:
            getter = Template(self.GETTER_TEMPLATE).substitute(
                field_type=field_type,
                return_type=self.type_map(field_type),
                field_name=field_name
            )
            get_methods.append(textwrap.indent(getter.strip(), '    '))
        
        # 使用模板生成最终头文件
        return Template(self.HEADER_TEMPLATE).substitute(
            include_guard=include_guard,
            impl_class=impl_class,
            class_name=class_name,
            get_methods='\n'.join(get_methods)
        ).strip()

    def type_map(self, proto_type):
        """类型映射"""
        return {
            "Int": "int32_t",
            "Double": "double",
            "String": "std::string"
        }.get(proto_type, proto_type)