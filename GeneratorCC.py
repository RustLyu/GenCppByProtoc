import textwrap
from string import Template

class GeneratorCC:
    # 定义实现文件模板
    IMPL_TEMPLATE = textwrap.dedent("""
        #include "${class_name}.h"

        class ${impl_class} {
        public:
        ${impl_members}
        };

        ${class_name}::${class_name}() : pImpl(new ${impl_class}()) {}

        ${class_name}::~${class_name}() {
            delete pImpl;
        }

        ${get_methods}
    """)

    # 定义getter方法模板
    GETTER_TEMPLATE = textwrap.dedent("""
        /**
         * @brief 获取
         * @return ${field_type} 返回
         */
        ${return_type} ${class_name}::Get${field_name}() {
            return pImpl->m_${field_name};
        }
    """)

    def generate_cpp(self, class_name, namespace, fields):
        """生成实现文件内容"""
        impl_class = f"{class_name}Impl"
        
        # 生成实现类成员变量
        impl_members = []
        for field_type, field_name in fields:
            member = f"{self.type_map(field_type)} m_{field_name};"
            impl_members.append(member)
        
        # 生成所有getter方法实现
        get_methods = []
        for field_type, field_name in fields:
            getter = Template(self.GETTER_TEMPLATE).substitute(
                field_type=field_type,
                return_type=self.type_map(field_type),
                class_name=class_name,
                field_name=field_name
            )
            get_methods.append(getter.strip())
        
        # 使用模板生成最终实现文件
        return Template(self.IMPL_TEMPLATE).substitute(
            class_name=class_name,
            impl_class=impl_class,
            impl_members=textwrap.indent('\n'.join(impl_members), '    '),
            get_methods='\n\n'.join(get_methods)
        ).strip()

    def type_map(self, proto_type):
        """类型映射"""
        return {
            "Int": "int32_t",
            "Double": "double",
            "String": "std::string"
        }.get(proto_type, proto_type)