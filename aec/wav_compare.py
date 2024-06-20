import librosa
import numpy as np

def normalize_audio_energy(audio):
    # 计算音频的均方根（RMS）能量
    rms = np.sqrt(np.mean(audio**2))
    
    # 对音频进行归一化
    normalized_audio = audio / rms
    
    return normalized_audio

def find_best_alignment(audio_file1, audio_file2):
    # 加载音频文件
    y1, sr1 = librosa.load(audio_file1)
    y2, sr2 = librosa.load(audio_file2)
    
    # 归一化音频能量
    y1_normalized = normalize_audio_energy(y1)
    y2_normalized = normalize_audio_energy(y2)
    
    # 计算交叉相关
    cross_corr = np.correlate(y1_normalized, y2_normalized, mode='full')
    offset = np.argmax(cross_corr) - len(y2_normalized) + 1
    
    return offset

def compare_aligned_audio(audio_file1, audio_file2, offset):
    # 加载音频文件
    y1, sr1 = librosa.load(audio_file1)
    y2, sr2 = librosa.load(audio_file2)
    
    # 对齐两个音频文件
    y2_aligned = y2[max(0, -offset):min(len(y2), len(y1) - offset)]
    
    # 提取MFCC特征
    mfccs1 = librosa.feature.mfcc(y=y1, sr=sr1)
    mfccs2 = librosa.feature.mfcc(y=y2_aligned, sr=sr2)
    
    # 对齐MFCC矩阵的长度
    min_frames = min(mfccs1.shape[1], mfccs2.shape[1])
    mfccs1 = mfccs1[:, :min_frames]
    mfccs2 = mfccs2[:, :min_frames]
    
    # 计算MFCC特征的欧几里得距离
    distance = np.linalg.norm(mfccs1 - mfccs2)
    
    return distance

# 两个音频文件的路径
audio_file1 = '/home/haiyong/Music/wav/rather_be_48k_s32_5s.wav'
audio_file2 = '/home/haiyong/Music/wav/test_48k_s32_chan2.wav'

# 找到最佳对齐位置
offset = find_best_alignment(audio_file1, audio_file2)

# 比较两个音频文件
distance = compare_aligned_audio(audio_file1, audio_file2, offset)
print("音频文件之间的欧几里得距离:", distance)