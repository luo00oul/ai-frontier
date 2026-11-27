"""最小世界模型教学实验；Python 3，无外部依赖。"""
actions = [((k * 7) % 21 - 10) / 10 for k in range(30)]
deltas = [0.8 * a + 0.1 for a in actions]
am, ym = sum(actions) / len(actions), sum(deltas) / len(deltas)
w = sum((a-am)*(y-ym) for a,y in zip(actions,deltas)) / sum((a-am)**2 for a in actions)
b = ym - w * am
print(f'训练样本: {len(actions)}, w={w:.3f}, b={b:.3f}')
test_actions = [-0.93, -0.37, 0.17, 0.59, 0.94]
mae = sum(abs((0.8*a+0.1)-(w*a+b)) for a in test_actions)/len(test_actions)
print(f'固定留出行动上的 MAE: {mae:.8f}')
for bias in (0, 0.05):
    real = predicted = 0.0
    for _ in range(10):
        real += 0.8 * 1.0 + 0.1
        predicted += w * 1.0 + b + bias
    print(f'模型偏移={bias:.2f}, 十步真实={real:.3f}, 预测={predicted:.3f}, 误差={abs(real-predicted):.3f}')
assert abs(w-0.8) < 1e-10 and abs(b-0.1) < 1e-10
