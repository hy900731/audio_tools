import wave
import numpy as np

# 定义输入和输出文件名
input_file = 'rather_be_48K_s24_5s.wav'
output_file = 'output_4byte.wav'

with wave.open(input_file, 'rb') as wav_in:
    params = wav_in.getparams()
    num_channels = params.nchannels
    sample_width = params.sampwidth
    frame_rate = params.framerate
    num_frames = wav_in.getnframes()

    frames = wav_in.readframes(num_frames)

if sample_width == 3:
    samples = np.frombuffer(frames, dtype=np.uint8)
    # 将3字节数据扩展为4字节数据
    # 假设3字节数据按little-endian顺序排列（如果是big-endian，需相应调整）
    samples4byte = np.empty((len(samples) // 3, 4), dtype=np.uint8)
    samples4byte[:, :3] = samples.reshape(-1, 3)
    samples4byte[:, 3] = 0  # 第四个字节补0
    frames_out = samples4byte.flatten().tobytes()
else:
    frames_out = frames

with wave.open(output_file, 'wb') as wav_out:
    wav_out.setparams((num_channels, sample_width, frame_rate, num_frames, params.comptype, params.compname))
    wav_out.writeframes(frames_out)

print(f"转换完成：{output_file}")