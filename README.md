# Alien-Invasion-
外星人要入侵地球了！扣1和我一起保卫学院，保卫深大，保卫长江，保卫中国，保卫地球！

![Python](https://img.shields.io/badge/Python-3.13.1-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green)
![SDL](https://img.shields.io/badge/SDL-2.28.4-orange)
![License](https://img.shields.io/badge/license-MIT-grey)

##  项目摘要 (Abstract)

本项目是基于经典 Python 教学案例《Alien Invasion》进行的重构与扩展。作为Python程序设计课程实验项目的一部分，本项目旨在通过引入**面向对象设计模式 (OOP)**、**有限状态机 (FSM)** 以及**模块化架构**，提升原版游戏的可维护性与交互深度。
经过测试，本项目可以在 **Python 3.13.1** 环境下稳定运行。

> **注意**：本项目包含完整的资源回退机制（Fallback Mechanism）。如果检测不到图像或音频资源，系统将自动生成几何图形替代，确保代码在任何环境下均可直接运行。

---

## 核心特性 (Key Features)

1.  **双重生存系统 (Health & Shield System)**
    * 引入护盾优先的伤害计算模型。
    * UI 层实现动态血条/护盾条渲染（颜色随血量百分比动态变化：绿 -> 黄 -> 红）。

2.  **增强型敌对 AI (Enhanced Enemy AI)**
     **主动反击**：外星人不再是静态靶子，会基于蒙特卡洛概率模型随机向下方发射子弹。
     **行级独立机动**：外星人舰队采用行级（Row-based）独立控制逻辑，触壁时仅特定行下沉并反转，而非整体移动，增加了游戏的不可预测性。

3.  **完整的游戏状态流 (Game State Management)**
     基于 FSM 实现多状态管理：`Menu` (菜单) -> `Playing` (游戏) -> `Paused` (暂停) -> `Win/Lose` (结算)。
     支持通过 `ESC` 键唤起暂停遮罩层。

---

## 项目结构（Project Structure）

项目核心代码全部为 Python 模块，项目目录为：

.
├─ alien_invasion.py   #   主程序入口 + 游戏主循环 + 状态机控制

├─ settings.py         #   全局静态/动态参数配置（屏幕、速度、难度等）

├─ game_stats.py       #   游戏过程统计与状态数据（生命、护盾、得分、关卡等）

├─ scoreboard.py       #   HUD / 记分板渲染（分数、生命图标、血条/盾条）

├─ ship.py             #   玩家飞船实体（移动、渲染、重置）

├─ alien.py            #   外星人实体（阵列移动、边界检测）
 
├─ bullet.py           #   玩家子弹 & 敌方子弹（弹道与渲染）

├─ button.py           #   通用 UI 按钮组件（菜单、重新开始、返回）

├─ images/

│   ├─ background.png      #   菜单/默认背景

│   ├─ background2.png     #   游戏中背景（若缺失会降级为 background.png）

│   ├─ ship.png            #   飞船贴图

│   └─ alien.png           #   外星人贴图

└─ sounds/

    ├─ background.flac         # 背景音乐

    
    ├─ laser.flac          #   玩家射击音效

     
    ├─ explosion.flac      #   外星人爆炸音效
    
    
    ├─ hit.flac            #   受击音效

    
    ├─ die.flac            #   飞船损毁音效

    
    ├─ win.flac            #   通关音效

    
    └─ gameover.flac       #   游戏失败音效
     

获取代码确保包含以下核心文件：

alien_invasion.py,

settings.py

ship.py

alien.py

bullet.py

game_stats.py

scoreboard.py

button.py

若要获得完整体验：确保根目录下存在 images/ 和 sounds/ 文件夹以获取音频和图片。

如果缺少资源文件，代码将自动触发 Fallback Mode，使用色块代替贴图，不影响逻辑复现。


## 环境依赖与复现 (Environment & Reproduction)
为了确保实验结果的一致性，请按照以下版本配置环境。


### 1. 核心版本要求
本项目基于 Python + Pygame + SDL 搭建 2D 实时射击游戏环境，推荐的开发/运行版本为：

Python == 3.13.1

pygame == 2.6.1

SDL == 2.28.4（由操作系统 / Pygame 底层依赖提供）

### 2. 快速安装依赖
建议在虚拟环境中运行本项目。

**创建并激活虚拟环境**
## Windows
```bash
python -m venv venv
.\venv\Scripts\activate
```

## macOS/Linux
```bash
python13.3 -m venv venv
source venv/bin/activate
```


**安装指定版本依赖可以直接运行以下命令安装精确版本：**
```bash
Bash pip install pygame==2.6.1
```

## 功能说明
以下是各模块的功能说明：

文件名模块功能描述：

**alien_invasion.py**

主入口控制器 (Controller)。负责初始化 Pygame 上下文、事件轮询分发、碰撞检测以及全局状态机流转。

**settings.py**

配置管理。分离了静态设置（分辨率、FPS）与动态设置（随关卡递增的难度系数、速度因子）。

**game_stats.py**

数据持久化。负责追踪生命周期内的关键指标（Score, High Score, Level, HP, Shield）。

**scoreboard.py**

视图层 (View/HUD)。负责将统计数据可视化，绘制得分板、等级以及复合血条 UI。

**ship.py**

玩家实体。封装了玩家飞船的运动学计算、边界限制与图像渲染。

**alien.py**

敌对实体。实现了外星人的初始化逻辑及行级独立运动算法。

**bullet.py**

投射物管理。利用多态性管理 Bullet (玩家向上) 和 AlienBullet (敌人向下) 两种弹道对象。

**button.py**

UI 组件。封装了交互式按钮的绘制与文本渲染逻辑，支持中文显示回退。


## 图层示例

**alien**

<img width="61" height="60" alt="alien" src="https://github.com/user-attachments/assets/ceccb386-1fff-48b6-a855-d9ec255c7138" />


**ship**

<img width="56" height="60" alt="ship" src="https://github.com/user-attachments/assets/b9d9e4ca-8091-4b84-8fdf-d6108830b260" />


**主菜单界面背景**

![background](https://github.com/user-attachments/assets/5ed686e9-b04c-4175-9e71-3fd3b86ef2ef)


**游戏界面背景**

![background2](https://github.com/user-attachments/assets/c9c6e02a-8b0d-49b8-bfe2-36581714c054)


### --end
