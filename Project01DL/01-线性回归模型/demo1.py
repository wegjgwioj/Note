# ## 4. Python 代码实战 (使用 Scikit-learn)

#下面是一个简单的 Python 示例，模拟房屋面积与价格的关系并进行预测。

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 1. 准备数据
# 模拟数据：X代表面积，y代表价格
# 真实关系假设：价格 = 0.15 * 面积 + 10 + 噪声
np.random.seed(0)
X = 2000 * np.random.rand(50, 1)  # 生成50个0-2000之间的面积数据
y = 0.15 * X + 10 + np.random.randn(50, 1) * 20  # 加上一些随机噪声

# 2. 创建并训练模型
model = LinearRegression()
model.fit(X, y)

# 3. 获取模型参数
w = model.coef_[0][0]
b = model.intercept_[0]
print(f"学习到的模型公式: y = {w:.2f}x + {b:.2f}")

# 4. 进行预测
X_new = np.array([[1500]])  # 预测一个1500平米的房子
y_predict = model.predict(X_new)
print(f"1500平米房子的预测价格: {y_predict[0][0]:.2f}")

# 5. 可视化结果 (如果运行环境支持)
# plt.scatter(X, y, color='blue', label='真实数据')
# plt.plot(X, model.predict(X), color='red', linewidth=2, label='预测直线')
# plt.xlabel('房屋面积')
# plt.ylabel('价格')
# plt.legend()
# plt.show()
