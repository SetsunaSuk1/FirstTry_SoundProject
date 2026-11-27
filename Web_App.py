import streamlit as st
import matplotlib.pyplot as plt
import io
from scipy.io import wavfile
import test  # 调用test模块

st.set_page_config(layout="wide", page_title="海豚声学信号处理")
st.title("🐬 海洋哺乳动物声学信号处理工具")
st.markdown("上传一段 `.wav` 音频，自动进行**带通滤波**并对比时频图。")

st.sidebar.header("滤波器参数设置")
# 限制滑块的最大值，防止超过奈奎斯特频率
lowcut = st.sidebar.slider("低截频率 (Hz)", min_value=0, max_value=5000, value=4000, step=100)
highcut = st.sidebar.slider("高截频率 (Hz)", min_value=5000, max_value=22000, value=15000, step=500)

uploaded_file = st.file_uploader("请选择你的音频文件", type=["wav"])

if uploaded_file is not None:
    try:
        fs, data = wavfile.read(io.BytesIO(uploaded_file.read()))

        if len(data.shape) > 1:
            data = data[:, 0]
        if data.dtype != 'float32':
            data = data.astype('float32') / 32768.0

        st.success(f"读取成功！采样率: {fs} Hz, 时长: {len(data) / fs:.2f} 秒")

        # 添加参数安全检查
        if lowcut >= highcut:
            st.error("⚠️ 参数错误：低截频率不能大于或等于高截频率！请拖动滑块调整。")
        elif highcut >= fs / 2:
            st.warning(f"⚠️ 提示：高截频率不能超过奈奎斯特频率 ({fs / 2} Hz)。")
        else:
            # 核心计算
            filtered_data = test.apply_bandpass_filter(data, fs, lowcut, highcut)
            fig = test.plot_comparison(data, filtered_data, fs, lowcut, highcut)

            # 使用 st.empty() 占位，确保每次重绘时覆盖旧图
            plot_placeholder = st.empty()
            plot_placeholder.pyplot(fig)
            # 清理内存，防止图越叠越多导致浏览器卡死
            plt.close(fig)

    except Exception as e:
        st.error(f"文件处理失败: {e}")