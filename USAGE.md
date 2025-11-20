# Alien Invasion - 使用指南 / Usage Guide

## 快速开始 / Quick Start

### 1. 安装依赖 / Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. 运行游戏 / Run the Game
```bash
python alien_invasion.py
```

### 3. 测试游戏组件 / Test Game Components
```bash
python test_game.py
```

## 游戏功能详解 / Game Features Explained

### 战机控制 / Spaceship Control
- **左箭头键 (←)**: 向左移动战机 / Move ship left
- **右箭头键 (→)**: 向右移动战机 / Move ship right
- **空格键 (Space)**: 发射导弹 / Fire bullets
- 战机可以同时发射最多5枚导弹 / Maximum 5 bullets on screen at once

### 外星人系统 / Alien System
- 外星人成群结队地向地球移动 / Aliens move in formation towards Earth
- 外星人会左右移动并逐渐下降 / Aliens move side to side and descend
- 外星人会随机发射导弹反击 / Aliens randomly fire bullets back
- 当一波外星人被消灭后，新一波会出现 / New wave appears after all aliens destroyed
- 每一波难度会增加（速度更快）/ Each wave increases in difficulty

### 护盾系统 / Shield System
- 屏幕底部有4个护盾保护战机 / 4 shields protect the ship
- 护盾可以阻挡外星人和战机的导弹 / Shields block both player and alien bullets
- 护盾被击中3次后会消失 / Shields disappear after 3 hits
- 护盾颜色会随着损伤程度变化 / Shield color changes with damage level
  - 绿色 (Green): 完好 / Full health
  - 黄绿色 (Yellow-green): 中度损伤 / Medium damage
  - 橙色 (Orange): 严重损伤 / Heavy damage

### 得分系统 / Scoring System
- 每击毁一个外星人获得50分 / 50 points per alien destroyed
- 完成一关后得分倍率增加 / Score multiplier increases with each level
- 高分会被保存 / High score is saved during session
- 分数显示在屏幕右上角 / Score displayed in top-right corner
- 最高分显示在屏幕顶部中央 / High score displayed at top-center
- 当前关卡显示在分数下方 / Current level displayed below score

### 生命系统 / Lives System
- 初始有3条生命 / Start with 3 lives
- 战机图标显示在左上角 / Ship icons shown in top-left
- 被外星人或其导弹击中会失去一条生命 / Lose a life when hit by alien or bullet
- 外星人到达屏幕底部也会失去一条生命 / Lose a life if aliens reach bottom
- 生命耗尽游戏结束 / Game over when all lives lost

### 音效系统 / Sound Effects
- 射击音效：发射导弹时播放 / Shooting sound when firing
- 爆炸音效：击毁外星人时播放 / Explosion sound when alien destroyed
- 受击音效：战机被击中时播放 / Hit sound when ship is hit
- 音效会在无音频设备环境下自动禁用 / Sounds auto-disabled in headless environments

### 游戏控制 / Game Control
- **P键**: 开始新游戏 / Start new game
- **Q键**: 退出游戏 / Quit game
- **鼠标点击Play按钮**: 开始游戏 / Click Play button to start
- 游戏暂停时鼠标可见 / Mouse visible when game paused
- 游戏进行时鼠标隐藏 / Mouse hidden during gameplay

## 游戏策略 / Game Strategy

1. **使用护盾**: 护盾是你最好的防御，尽量让外星人的导弹打在护盾上
   Use shields: They are your best defense against alien bullets

2. **移动射击**: 不要站在原地，边移动边射击更安全
   Move and shoot: Don't stay in one place, keep moving

3. **优先击毁底部外星人**: 它们更接近你，威胁更大
   Target bottom aliens: They're closer and more dangerous

4. **注意外星人导弹**: 外星人会反击，注意躲避红色导弹
   Watch for alien bullets: Red bullets come from aliens, dodge them

5. **保存护盾**: 早期关卡保持护盾完整，后期会更需要它们
   Preserve shields: Keep them intact early, you'll need them later

## 技术信息 / Technical Information

- **引擎**: Pygame 2.5.0+
- **Python版本**: Python 3.6+
- **分辨率**: 1200x800 pixels
- **帧率**: 60 FPS
- **架构**: 面向对象设计 / Object-oriented design

## 疑难解答 / Troubleshooting

### 游戏无法启动 / Game Won't Start
```bash
# 确保安装了pygame / Make sure pygame is installed
pip install pygame

# 检查Python版本 / Check Python version
python --version  # Should be 3.6+
```

### 没有声音 / No Sound
- 这是正常的，如果系统没有音频设备，音效会自动禁用
  This is normal if your system has no audio device, sounds auto-disable

### 测试失败 / Tests Fail
```bash
# 重新安装依赖 / Reinstall dependencies
pip install --upgrade -r requirements.txt

# 运行测试 / Run tests
python test_game.py
```

## 项目结构 / Project Structure

```
Alien-Invasion-/
├── alien_invasion.py    # 主游戏文件 / Main game file
├── settings.py          # 游戏设置 / Game settings
├── ship.py             # 战机类 / Ship class
├── bullet.py           # 导弹类 / Bullet classes
├── alien.py            # 外星人类 / Alien class
├── shield.py           # 护盾类 / Shield class
├── game_stats.py       # 游戏统计 / Game statistics
├── scoreboard.py       # 记分牌 / Scoreboard
├── button.py           # 按钮类 / Button class
├── sound_manager.py    # 音效管理 / Sound manager
├── test_game.py        # 测试脚本 / Test script
├── requirements.txt    # 依赖列表 / Dependencies
├── README.md           # 说明文档 / Documentation
├── USAGE.md           # 使用指南 / Usage guide
└── .gitignore         # Git忽略文件 / Git ignore
```

## 贡献 / Contributing

欢迎提交问题和改进建议！
Welcome to submit issues and improvement suggestions!

## 许可证 / License

请查看 LICENSE 文件
See LICENSE file for details
