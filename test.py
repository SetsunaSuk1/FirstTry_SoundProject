
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import os

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

#读取文件
file_path = os.path.join('data/sample_AtlanticSpottedDolphin_1961_6102500A.wav')

#读取音频
try:
    fs, data = wavfile.read(file_path)
    print(f"✅ 读取成功！采样率: {fs} Hz, 时长: {len(data)/fs:.2f} 秒")
except Exception as e:
    print("读取失败，请检查文件路径是否正确：", e)
    exit()

# 如果音频是双声道（立体声），取左声道
if len(data.shape) > 1:
    data = data[:, 0]

# 4. 画图：上面画波形，下面画声谱图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# --- 上半部分：波形图 ---
time = np.arange(len(data)) / fs
ax1.plot(time, data, color='blue', linewidth=0.5)
ax1.set_title('Waveform (波形图)')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude')

# --- 下半部分：声谱图 ---
# 这里使用 scipy 的 spectrogram 函数
# nperseg 越大，频率分辨率越高，时间分辨率越低。
f, t, Sxx = signal.spectrogram(data, fs, nperseg=1024, noverlap=512)

# 官方图的范围是 0-21kHz
# Sxx 是能量谱，用 10*log10(Sxx) 转成 dB
ax2.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='inferno')
ax2.set_title('Spectrogram (声谱图)')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Frequency (kHz)')

# 限制 Y 轴在 0-21kHz 之间（大约 21000 Hz）
ax2.set_ylim(0, 21000)

# 显示颜色条
cbar = plt.colorbar(ax2.collections[0], ax=ax2)
cbar.set_label('Intensity (dB)')

plt.tight_layout()
plt.show()