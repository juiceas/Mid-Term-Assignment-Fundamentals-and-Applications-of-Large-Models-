"""验证修复的简单脚本"""
import sys
sys.path.insert(0, 'src')

import torch
from model import Transformer, create_padding_mask, create_target_mask

print("测试Transformer修复...")

# 创建模型
model = Transformer(
    src_vocab_size=100,
    tgt_vocab_size=100,
    d_model=64,
    n_heads=4,
    d_ff=256,
    n_layers=2,
    max_len=50,
    dropout=0.1
)

# 测试数据
batch_size = 2
src_len = 10
tgt_len = 8

src = torch.randint(0, 100, (batch_size, src_len))
tgt = torch.randint(0, 100, (batch_size, tgt_len))

# 创建mask
src_mask = create_padding_mask(src)
tgt_mask = create_target_mask(tgt)

print(f"输入形状:")
print(f"  src: {src.shape}")
print(f"  tgt: {tgt.shape}")
print(f"  src_mask: {src_mask.shape}")
print(f"  tgt_mask: {tgt_mask.shape}")

try:
    # 前向传播
    output = model(src, tgt, src_mask, tgt_mask)
    
    print(f"\n输出形状: {output.shape}")
    print(f"期望形状: [{batch_size}, {tgt_len}, 100]")
    
    if output.shape == (batch_size, tgt_len, 100):
        print("\n✓ 测试通过！修复成功！")
    else:
        print("\n✗ 输出形状不正确")
except Exception as e:
    print(f"\n✗ 测试失败: {e}")
    import traceback
    traceback.print_exc()

