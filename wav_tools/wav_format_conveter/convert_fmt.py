import wave
import numpy as np
import sys
import struct

def convert_wav_format(input_file, output_file, output_width):
    try:
        # 打开输入WAV文件
        with wave.open(input_file, 'rb') as wf:
            # 读取WAV文件的基本信息
            params = wf.getparams()
            num_channels = params.nchannels
            input_width = params.sampwidth
            frame_rate = params.framerate
            num_frames = params.nframes
            comp_type = params.comptype
            comp_name = params.compname

            # 读取音频数据
            audio_data = wf.readframes(num_frames)

        int_data = []
        # 将字节数据转换为numpy数组
        if input_width == 1:
            audio_array = np.frombuffer(audio_data, dtype=np.int8)
        elif input_width == 2:
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
        elif input_width == 3:
            audio_array = np.frombuffer(audio_data, dtype=np.int8)
            # TODO: 执行效率太低
            for i in range(0, len(audio_array), 3):
                # 将三个字节按小端序解析为一个 int32
                num_bytes = struct.pack('<bbbb', audio_array[i], audio_array[i+1], audio_array[i+2], 0)
                num_int32 = struct.unpack('<i', num_bytes)[0]
                int_data.append(num_int32)

            audio_array = np.array(int_data)
        elif input_width == 4:
            audio_array = np.frombuffer(audio_data, dtype=np.int32)
        else:
            print(f"不支持的输入数据格式：{input_width} bytes。")
            return

        audio_array = audio_array.astype(np.int32)
        if (input_width - output_width) > 0:
            audio_array = (audio_array >> ((input_width - output_width) * 8))
        else:
            audio_array = (audio_array << ((output_width - input_width) * 8))
        # 根据输出宽度进行数据处理
        if output_width == 1:
            audio_array = audio_array.astype(np.int8)
        elif output_width == 2:
            audio_array = audio_array.astype(np.int16)
        elif output_width == 3:
            np.left_shift(audio_array, 8).astype(np.int32)  # 将32位整数转换为24位整数
        elif output_width == 4:
            # 32位整数转换为32位整数（无需转换）
            pass
        else:
            print(f"不支持的输出数据格式：{output_width} bytes。")
            return

        # 将numpy数组转换回字节数据
        audio_data = audio_array.tobytes()
        if output_width == 3:
            new_byte_stream = b''
            for i in range(0, len(audio_data), 4):
                new_byte_stream += audio_data[i:i+3]

            audio_data = new_byte_stream

        # 打开输出WAV文件
        with wave.open(output_file, 'wb') as wf:
            # 设置输出WAV文件的参数，保持与输入文件相同的其他参数
            wf.setparams((num_channels, output_width, frame_rate, num_frames, comp_type, comp_name))
            
            # 写入音频数据
            wf.writeframes(audio_data)

        print(f"已将 {input_file} 的数据格式从 s{input_width * 8} 转换为 s{output_width * 8}，并保存为 {output_file}。")

    except Exception as e:
        print(f"发生错误：{e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法: python script.py <输入文件路径> <输出文件路径> <输出采样宽度bytes>")
        sys.exit(1)

    input_file = sys.argv[1]  # 输入文件路径
    output_file = sys.argv[2]  # 输出文件路径
    output_width = int(sys.argv[3])  # 输出采样宽度（字节）

    # 自动获取输入文件的采样宽度
    with wave.open(input_file, 'rb') as wf:
        input_width = wf.getsampwidth()

    convert_wav_format(input_file, output_file, output_width)