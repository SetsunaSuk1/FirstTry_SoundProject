# Bioacoustics Data Processing (First Try)
开始日期：2026 11 25
这是我在大二上学期尝试处理海洋哺乳动物声信号的第一次尝试。

## 目前完成的工作
- 从 Watkins Marine Mammal Sound Database 下载了 Atlantic Spotted Dolphin (大西洋斑海豚) 的原始音频数据。
- 使用 Python 读取音频并绘制了时域波形图。
- 使用 `scipy.signal.spectrogram` 绘制了时频图（声谱图），并与官方给出的声谱图进行了对比验证。
- 观察到了海豚 click 信号的能量集中在约 4-10 kHz，以及约 17.5 kHz 处存在明显的设备/环境干扰线。

## 环境依赖
- Python 3.10
- numpy, matplotlib, scipy

## 处理结果
这是我用 Python 跑出的波形图和声谱图：
![处理结果](Try_Figure_1.png)

## 下一步计划
- 尝试加入带通滤波器（如 4-15 kHz），滤除高频干扰。
- 学习如何用阈值法自动检测 click 信号。

## 2026-11-28 更新：交互式网页应用
- 将核心算法（音频读取、带通滤波、画图）封装到 `test.py` 中，作为独立的处理模块。
- 使用 Streamlit 开发了 `Web_App.py` 前端界面，直接调用底层模块。
- 实现了滤波参数的实时调整与可视化对比。并且加入了异常保护机制（防止参数超出奈奎斯特频率导致崩溃）。
- 解决 Streamlit 状态刷新导致图表重复渲染的 Bug（使用 `st.empty()` 和 `plt.close()`）。
![网页界面](Streamlit_UI.png)
