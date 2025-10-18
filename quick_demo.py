"""
快速演示脚本 - 用小参数快速训练一个模型
这个脚本使用非常小的参数，可以在几分钟内完成训练
"""
import sys
sys.path.insert(0, 'src')

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR
import matplotlib.pyplot as plt
import numpy as np
import os
from tqdm import tqdm

from model import Transformer, create_padding_mask, create_target_mask
from data_loader import get_data_loaders


def quick_train():
    """快速训练演示"""
    print("="*70)
    print("Transformer快速演示训练")
    print("="*70)
    print("\n使用非常小的参数，快速展示训练过程")
    print("这不是完整训练，只是演示！\n")
    
    # 设置随机种子
    torch.manual_seed(42)
    np.random.seed(42)
    
    # 超小配置（几分钟就能完成）
    config = {
        'd_model': 64,
        'n_heads': 4,
        'd_ff': 256,
        'n_layers': 2,
        'max_len': 50,
        'dropout': 0.1,
        'batch_size': 8,
        'epochs': 10,
        'lr': 5e-4,
        'num_samples': 200,
    }
    
    # 设备
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"使用设备: {device}\n")
    
    # 加载数据
    print("加载数据...")
    train_loader, val_loader, src_vocab, tgt_vocab = get_data_loaders(
        task='copy',
        batch_size=config['batch_size'],
        num_samples=config['num_samples'],
        train_ratio=0.8
    )
    
    print(f"  训练批次: {len(train_loader)}")
    print(f"  验证批次: {len(val_loader)}")
    print(f"  词汇表大小: {len(src_vocab)}\n")
    
    # 创建模型
    print("创建模型...")
    model = Transformer(
        src_vocab_size=len(src_vocab),
        tgt_vocab_size=len(tgt_vocab),
        d_model=config['d_model'],
        n_heads=config['n_heads'],
        d_ff=config['d_ff'],
        n_layers=config['n_layers'],
        max_len=config['max_len'],
        dropout=config['dropout']
    ).to(device)
    
    total_params = sum(p.numel() for p in model.parameters())
    print(f"  参数数量: {total_params:,}\n")
    
    # 优化器和损失函数
    optimizer = optim.AdamW(model.parameters(), lr=config['lr'], weight_decay=0.01)
    scheduler = CosineAnnealingLR(optimizer, T_max=config['epochs'])
    criterion = nn.CrossEntropyLoss(ignore_index=0)
    
    # 训练历史
    history = {
        'train_loss': [],
        'val_loss': [],
        'train_ppl': [],
        'val_ppl': []
    }
    
    print("开始训练...\n")
    
    # 训练循环
    for epoch in range(config['epochs']):
        # 训练
        model.train()
        train_loss = 0
        pbar = tqdm(train_loader, desc=f'Epoch {epoch+1}/{config["epochs"]} [Train]')
        
        for src, tgt in pbar:
            src, tgt = src.to(device), tgt.to(device)
            tgt_input = tgt[:, :-1]
            tgt_output = tgt[:, 1:]
            
            src_mask = create_padding_mask(src).to(device)
            tgt_mask = create_target_mask(tgt_input).to(device)
            
            optimizer.zero_grad()
            output = model(src, tgt_input, src_mask, tgt_mask)
            
            loss = criterion(output.contiguous().view(-1, output.size(-1)),
                           tgt_output.contiguous().view(-1))
            loss.backward()
            
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            
            train_loss += loss.item()
            pbar.set_postfix({'loss': f'{loss.item():.4f}'})
        
        train_loss /= len(train_loader)
        train_ppl = np.exp(train_loss)
        
        # 验证
        model.eval()
        val_loss = 0
        
        with torch.no_grad():
            for src, tgt in val_loader:
                src, tgt = src.to(device), tgt.to(device)
                tgt_input = tgt[:, :-1]
                tgt_output = tgt[:, 1:]
                
                src_mask = create_padding_mask(src).to(device)
                tgt_mask = create_target_mask(tgt_input).to(device)
                
                output = model(src, tgt_input, src_mask, tgt_mask)
                loss = criterion(output.contiguous().view(-1, output.size(-1)),
                               tgt_output.contiguous().view(-1))
                val_loss += loss.item()
        
        val_loss /= len(val_loader)
        val_ppl = np.exp(val_loss)
        
        # 更新学习率
        scheduler.step()
        
        # 记录历史
        history['train_loss'].append(train_loss)
        history['val_loss'].append(val_loss)
        history['train_ppl'].append(train_ppl)
        history['val_ppl'].append(val_ppl)
        
        # 打印统计
        print(f"Epoch {epoch+1}: Train Loss={train_loss:.4f} (PPL={train_ppl:.2f}), "
              f"Val Loss={val_loss:.4f} (PPL={val_ppl:.2f})")
    
    print("\n训练完成！\n")
    
    # 绘制结果
    print("绘制训练曲线...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    epochs = range(1, len(history['train_loss']) + 1)
    
    # 损失曲线
    axes[0].plot(epochs, history['train_loss'], 'b-o', label='训练损失', linewidth=2)
    axes[0].plot(epochs, history['val_loss'], 'r-s', label='验证损失', linewidth=2)
    axes[0].set_xlabel('Epoch', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Loss', fontsize=12, fontweight='bold')
    axes[0].set_title('训练和验证损失', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # 困惑度曲线
    axes[1].plot(epochs, history['train_ppl'], 'b-o', label='训练困惑度', linewidth=2)
    axes[1].plot(epochs, history['val_ppl'], 'r-s', label='验证困惑度', linewidth=2)
    axes[1].set_xlabel('Epoch', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Perplexity', fontsize=12, fontweight='bold')
    axes[1].set_title('训练和验证困惑度', fontsize=14, fontweight='bold')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # 保存图表
    os.makedirs('demo_results', exist_ok=True)
    save_path = 'demo_results/quick_demo_curves.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"训练曲线已保存到: {save_path}")
    
    plt.show()
    
    # 保存模型
    model_path = 'demo_results/quick_demo_model.pth'
    torch.save({
        'model_state_dict': model.state_dict(),
        'config': config,
        'history': history,
        'vocab_sizes': (len(src_vocab), len(tgt_vocab))
    }, model_path)
    print(f"模型已保存到: {model_path}")
    
    # 打印总结
    print("\n" + "="*70)
    print("演示完成！")
    print("="*70)
    print(f"最终训练损失: {history['train_loss'][-1]:.4f}")
    print(f"最终验证损失: {history['val_loss'][-1]:.4f}")
    print(f"最终验证困惑度: {history['val_ppl'][-1]:.2f}")
    print("\n注意：这只是快速演示，使用了非常小的参数。")
    print("要进行完整训练，请运行: python src/train.py")
    print("="*70)


if __name__ == "__main__":
    quick_train()

