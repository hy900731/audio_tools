import librosa
import soundfile as sf
import os
import sys

def adjust_gain(input_file, output_dir, gain_db):
    # 确保输出目录存在，如果不存在则创建
    os.makedirs(output_dir, exist_ok=True)

    # 读取音频文件
    y, sr = librosa.load(input_file)

    # 应用增益
    y_adjusted = librosa.effects.preemphasis(y, coef=gain_db)

    # 构造输出文件路径
    filename = os.path.splitext(os.path.basename(input_file))[0] + '_adjusted.wav'
    output_file = os.path.join(output_dir, filename)

    # 保存调整后的音频
    sf.write(output_file, y_adjusted, sr)

    print(f"调整后的音频已保存到: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法: python script.py <输入文件路径> <输出目录> <增益增量（dB）>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    gain_db = float(sys.argv[3])

    adjust_gain(input_file, output_dir, gain_db)