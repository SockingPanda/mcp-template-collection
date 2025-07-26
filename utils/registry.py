class Registry:
    """可复用的装饰器收集器 - 完全模拟 FastMCP 装饰器行为"""
    def __init__(self):
        self.tools     = {}
        self.resources = {}
        self.prompts   = {}

    def tool(self, name_or_fn=None, *, name=None, title=None, description=None, 
             tags=None, output_schema=None, annotations=None, exclude_args=None, enabled=None):
        """工具装饰器 - 完全模拟 @mcp.tool() 的行为和参数"""
        def decorator(f):
            # 确定工具名称
            if name is not None:
                tool_name = name
            elif isinstance(name_or_fn, str):
                tool_name = name_or_fn
            else:
                tool_name = f.__name__
            
            # 存储函数和所有元数据
            self.tools[tool_name] = {
                'function': f,
                'name': tool_name,
                'title': title,
                'description': description or f.__doc__,
                'tags': tags,
                'output_schema': output_schema,
                'annotations': annotations,
                'exclude_args': exclude_args,
                'enabled': enabled if enabled is not None else True
            }
            return f
        
        # 处理不同的调用模式
        if callable(name_or_fn):
            # @registry.tool 或 @registry.tool()
            return decorator(name_or_fn)
        else:
            # @registry.tool("name") 或 @registry.tool(name="name")
            return decorator

    def resource(self, name_or_fn=None, *, name=None, title=None, description=None,
                 tags=None, output_schema=None, annotations=None, exclude_args=None, enabled=None):
        """资源装饰器 - 完全模拟 @mcp.resource() 的行为和参数"""
        def decorator(f):
            # 确定资源名称
            if name is not None:
                resource_name = name
            elif isinstance(name_or_fn, str):
                resource_name = name_or_fn
            else:
                resource_name = f.__name__
            
            # 存储函数和所有元数据
            self.resources[resource_name] = {
                'function': f,
                'name': resource_name,
                'title': title,
                'description': description or f.__doc__,
                'tags': tags,
                'output_schema': output_schema,
                'annotations': annotations,
                'exclude_args': exclude_args,
                'enabled': enabled if enabled is not None else True
            }
            return f
        
        # 处理不同的调用模式
        if callable(name_or_fn):
            # @registry.resource 或 @registry.resource()
            return decorator(name_or_fn)
        else:
            # @registry.resource("name") 或 @registry.resource(name="name")
            return decorator

    def prompt(self, name_or_fn=None, *, name=None, title=None, description=None,
               tags=None, output_schema=None, annotations=None, exclude_args=None, enabled=None):
        """提示装饰器 - 完全模拟 @mcp.prompt() 的行为和参数"""
        def decorator(f):
            # 确定提示名称
            if name is not None:
                prompt_name = name
            elif isinstance(name_or_fn, str):
                prompt_name = name_or_fn
            else:
                prompt_name = f.__name__
            
            # 存储函数和所有元数据
            self.prompts[prompt_name] = {
                'function': f,
                'name': prompt_name,
                'title': title,
                'description': description or f.__doc__,
                'tags': tags,
                'output_schema': output_schema,
                'annotations': annotations,
                'exclude_args': exclude_args,
                'enabled': enabled if enabled is not None else True
            }
            return f
        
        # 处理不同的调用模式
        if callable(name_or_fn):
            # @registry.prompt 或 @registry.prompt()
            return decorator(name_or_fn)
        else:
            # @registry.prompt("name") 或 @registry.prompt(name="name")
            return decorator 