## 解释说明：

1. adjust_gain 函数接受三个参数：input_file（输入音频文件路径）、output_dir（输出目录路径）和 gain_db（增益增量，以分贝dB为单位）。

```py
os.makedirs(output_dir, exist_ok=True) 确保输出目录存在，如果不存在则创建。

librosa.load(input_file) 用于加载输入音频文件。

librosa.effects.preemphasis 函数应用增益。

os.path.splitext(os.path.basename(input_file))[0] + '_adjusted.wav' 生成调整后音频的文件名。

sf.write(output_file, y_adjusted, sr) 保存调整后的音频到指定的输出文件。

if __name__ == "__main__": 确保脚本可以直接运行，并处理命令行参数。
```

2. sys.argv 用于获取命令行输入的参数。sys.argv[0] 是脚本本身的名称，sys.argv[1] 是输入文件路径，sys.argv[2] 是输出目录路径，sys.argv[3] 是增益增量（以分贝dB为单位）

## 使用

```py
python volume.py input.wav output_directory 3.0
这会将 input.wav 文件调整增益为 3dB，并将结果保存到 output_directory 目录中。
```