# 05 - 用动画观察 B+Tree 分裂

这一节不再写一棵树，而是把 `04-bplus_tree.py` 中不容易靠日志看清的结构变化放慢观察。

## 实验器材

- 在线动画：[ChalmersGU Data Structure Visualizations](https://chalmersgu-data-structure-courses.github.io/visualization/)
- 源码与许可证：[ChalmersGU-data-structure-courses/visualization](https://github.com/ChalmersGU-data-structure-courses/visualization)
- License：FreeBSD

这是外部实验器材，不是本教材源码。它的仓库也明确提醒：动画代码偏向展示，不适合当成算法实现教材；真正要读的是上一节的最小实现。

## 输入什么

1. 打开页面，选择 `B+ Tree`。
2. 重置动画；如果页面允许选择阶数，使用较小的阶数，让分裂更早发生。
3. 依次插入：`10, 20, 30, 40, 50, 60, 70, 80`。
4. 每次只插入一个 key，等动画结束后再插入下一个。
5. 使用 Find 查找 `30`，再查找一个不存在的 `35`。

## 观察什么

| 时刻 | 观察重点 | 为什么会这样 |
| --- | --- | --- |
| 叶子第一次装满 | 一个叶子变成两个叶子 | 单页容量有限，溢出后必须 split |
| 父节点出现 separator | separator 指向右侧孩子的最小 key | 查找时用它判断应该进入哪个孩子 |
| root 再次溢出 | 新 root 出现，树高增加 1 | root 没有父节点可接收 separator |
| Find 30 | 先走内部节点，最后才到叶子 | B+Tree 的完整记录只放在叶子 |

不要只数动画里的方框。回到本地运行：

```bash
python3 02-Database/04-bplus_tree.py
```

对照输出中的 `I[...]`（内部节点）、`L[...]`（叶子节点），找到同样的 split 和 separator。

## 费曼复述

如果范围查询需要 `30 <= key <= 70`，第一次定位到 `30` 所在叶子后，为什么不必重新从 root 查找 `40、50、60、70`？
