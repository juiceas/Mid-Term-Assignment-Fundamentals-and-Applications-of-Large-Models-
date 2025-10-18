"""
快速测试脚本 - 验证模型和数据加载器
"""
import sys
sys.path.insert(0, 'src')

import torch
from model import Transformer, create_padding_mask, create_target_mask
from data_loader import get_data_loaders

def test_model():
    print("="*60)
    print("测试Transformer模型")
    print("="*60)
    
    # 创建小型模型用于测试
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
    
    # 统计参数
    total_params = sum(p.numel() for p in model.parameters())
    print(f"模型参数数量: {total_params:,}")
    
    # 测试前向传播
    batch_size = 2
    src_len = 10
    tgt_len = 8
    
    src = torch.randint(0, 100, (batch_size, src_len))
    tgt = torch.randint(0, 100, (batch_size, tgt_len))
    
    src_mask = create_padding_mask(src)
    tgt_mask = create_target_mask(tgt)
    
    print(f"\n输入形状:")
    print(f"  src: {src.shape}")
    print(f"  tgt: {tgt.shape}")
    
    # 前向传播
    output = model(src, tgt, src_mask, tgt_mask)
    
    print(f"\n输出形状: {output.shape}")
    print(f"期望形状: [{batch_size}, {tgt_len}, 100]")
    
    assert output.shape == (batch_size, tgt_len, 100), "输出形状不正确！"
    print("\n✓ 模型测试通过！")
    return True

def test_data_loader():
    print("\n" + "="*60)
    print("测试数据加载器")
    print("="*60)
    
    try:
        train_loader, val_loader, src_vocab, tgt_vocab = get_data_loaders(
            task='copy',
            batch_size=4,
            num_samples=100,
            train_ratio=0.8
        )
        
        print(f"\n训练集批次数: {len(train_loader)}")
        print(f"验证集批次数: {len(val_loader)}")
        print(f"Source词汇表大小: {len(src_vocab)}")
        print(f"Target词汇表大小: {len(tgt_vocab)}")
        
        # 获取一个批次
        for src_batch, tgt_batch in train_loader:
            print(f"\nBatch形状:")
            print(f"  Source: {src_batch.shape}")
            print(f"  Target: {tgt_batch.shape}")
            
            assert src_batch.dim() == 2, "Source batch维度错误！"
            assert tgt_batch.dim() == 2, "Target batch维度错误！"
            break
        
        print("\n✓ 数据加载器测试通过！")
        return True
    except Exception as e:
        print(f"\n✗ 数据加载器测试失败: {e}")
        return False

def main():
    print("\n开始测试...\n")
    
    success = True
    
    # 测试模型
    try:
        if not test_model():
            success = False
    except Exception as e:
        print(f"\n✗ 模型测试失败: {e}")
        import traceback
        traceback.print_exc()
        success = False
    
    # 测试数据加载器
    try:
        if not test_data_loader():
            success = False
    except Exception as e:
        print(f"\n✗ 数据加载器测试失败: {e}")
        import traceback
        traceback.print_exc()
        success = False
    
    print("\n" + "="*60)
    if success:
        print("所有测试通过！✓")
        print("="*60)
        return 0
    else:
        print("部分测试失败！✗")
        print("="*60)
        return 1

if __name__ == "__main__":
    exit(main())

