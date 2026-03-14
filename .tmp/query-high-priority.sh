#!/bin/bash
# 临时查询脚本：通过 memory_list 工具查询高优先级记忆
openclaw agent -a main -m "使用 memory_list 工具查询所有 importance ≥ 0.9 的记忆，limit 50，输出 JSON 格式到 ~/.openclaw/workspace/.tmp/high-priority-memories.json"
