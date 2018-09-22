#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/8/6'
Info:

    绝大部分时候让__init__.py空着就好。但是有些情况下可能包含代码。 举个例子，__init__.py能够用来自动加载子模块:
	from . import a1
	from . import a2
	
	import pk1.pk11 能够快速高效导入pk11 包下所有模块
	
"""

from . import a1
from . import a2
