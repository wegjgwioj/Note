from typing import TYPE_CHECKING # 用于类型检查时的条件导入

from ...utils import _LazyModule # 用于实现延迟导入机制
from ...utils.import_utils import define_import_structure # 定义模块的导入结构


# 在类型检查场景下直接导入，便于静态分析工具获取符号
if TYPE_CHECKING:
    from .configuration_llama import *  # 配置相关的符号
    from .modeling_llama import *  # 模型相关的符号
    from .tokenization_llama import * # 分词器相关的符号
else:
    import sys # 导入 sys 模块以便操作模块字典

    # 运行时使用 LazyModule 延迟导入，减少初始加载开销
    _file = globals()["__file__"]
    sys.modules[__name__] = _LazyModule(__name__, _file, define_import_structure(_file), module_spec=__spec__)
