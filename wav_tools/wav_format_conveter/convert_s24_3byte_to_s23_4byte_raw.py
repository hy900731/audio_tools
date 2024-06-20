import wave
import numpy as np

# 输入和输出文件名
input_file = 'rather_be_48K_s24_5s.wav'
output_file = 'output_4byte_aligned.raw'

# 打开输入 WAV 文件
with wave.open(input_file, 'rb') as wav_in:
    # 获取音频参数
    params = wav_in.getparams()
    num_channels, samp_width, frame_rate, num_frames, comp_type, comp_name = params
    
    # 确保输入文件是 3-byte 对齐格式
    assert samp_width == 3, "Input file should be 3-byte aligned format"

    # 读取音频数据
    frames = wav_in.readframes(num_frames)
    
    # 将数据转换为 numpy 数组，每个采样点占3个字节
    audio_data = np.frombuffer(frames, dtype=np.uint8)
    
    # 创建新的数组来存储 4-byte 对齐的数据
    audio_data_4byte_aligned = np.zeros((len(audio_data) // 3 * 4,), dtype=np.uint8)
    
    # 将每个采样点的数据扩展为 4-byte 对齐格式
    for i in range(len(audio_data) // 3):
        audio_data_4byte_aligned[i * 4 + 0] = audio_data[i * 3 + 0]
        audio_data_4byte_aligned[i * 4 + 1] = audio_data[i * 3 + 1]
        audio_data_4byte_aligned[i * 4 + 2] = audio_data[i * 3 + 2]
        audio_data_4byte_aligned[i * 4 + 3] = 0  # 最后一个字节填充为 0
    
    # 写入输出 raw 文件
    with open(output_file, 'wb') as raw_out:
        raw_out.write(audio_data_4byte_aligned.tobytes())

print(f"音频数据已提取并保存为：{output_file}")