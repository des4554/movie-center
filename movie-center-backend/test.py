import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
def add_laplace_noise(data, epsilon):
    """为数据添加拉普拉斯噪声"""
    scale = 1.0 / epsilon
    noise = np.random.laplace(0, scale, data.shape)
    return data + noise

epsilons = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2, 3, 4, 5, 6, 7, 8, 100]# 隐私预算越小，隐私保护越强，但数据准确性越低
raw_data = np.array([5.0, 4.4, 3.2, 4.1, 2.9])
for epsilon in epsilons:
    processed_data = add_laplace_noise(raw_data, epsilon)
    print("e:", epsilon, "data:", processed_data)