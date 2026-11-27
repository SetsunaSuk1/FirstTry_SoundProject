import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def load_audio(file_path):
    """读取音频并统一转换为浮点数格式"""
    fs, data = wavfile.read(file_path)
    if len(data.shape) > 1:
        data = data[:, 0]
    if data.dtype != 'float32':
        data = data.astype('float32') / 32768.0
    return fs, data


def apply_bandpass_filter(data, fs, lowcut, highcut, order=4):
    """应用巴特沃斯带通滤波器"""
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    filtered_data = signal.filtfilt(b, a, data)
    return filtered_data


def plot_comparison(data, filtered_data, fs, lowcut, highcut):
    """画四宫格对比图，返回 matplotlib 的 figure 对象"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    time = np.arange(len(data)) / fs

    # 原始数据
    axes[0, 0].plot(time, data, color='blue', linewidth=0.5)
    axes[0, 0].set_title('原始波形')
    axes[0, 0].set_ylabel('Amplitude')

    f, t, Sxx = signal.spectrogram(data, fs, nperseg=1024, noverlap=512)
    axes[1, 0].pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='inferno')
    axes[1, 0].set_title('原始声谱图')
    axes[1, 0].set_ylabel('Frequency (Hz)')
    axes[1, 0].set_xlabel('Time (s)')
    axes[1, 0].set_ylim(0, min(21000, fs / 2))

    # 滤波后数据
    axes[0, 1].plot(time, filtered_data, color='green', linewidth=0.5)
    axes[0, 1].set_title(f'滤波后波形 ({lowcut} - {highcut} Hz)')

    f_f, t_f, Sxx_f = signal.spectrogram(filtered_data, fs, nperseg=1024, noverlap=512)
    axes[1, 1].pcolormesh(t_f, f_f, 10 * np.log10(Sxx_f + 1e-10), shading='gouraud', cmap='inferno')
    axes[1, 1].set_title('滤波后声谱图')
    axes[1, 1].set_xlabel('Time (s)')
    axes[1, 1].set_ylim(0, min(21000, fs / 2))

    plt.tight_layout()
    return fig


# 保留一个入口，如果你直接在 PyCharm 运行 test.py，依然能出图
if __name__ == "__main__":
    file_path = os.path.join('data', 'sample_AtlanticSpottedDolphin_1961_6102500A.wav')
    fs, data = load_audio(file_path)
    filtered_data = apply_bandpass_filter(data, fs, 4000, 15000)
    fig = plot_comparison(data, filtered_data, fs, 4000, 15000)
    plt.show()