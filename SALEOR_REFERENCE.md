# Saleor 只读参考规则

## 固定版本

- 官方仓库：`https://github.com/saleor/saleor`
- 当前教材版本：tag `3.23.25`
- 当前 commit：`bcb559a79ccafadb21bf9d337ef1dc6b74bd77a2`
- 历史比较 commit：`7e57a29b9f0dd6e93ab77998b93b0d2fe37fcdd6`（2017-12-30）
- 本地只读路径：`.references/saleor`

`.references/` 已被忽略。教材不修改、格式化、提交或推送 Saleor 源码。

## 验证命令

```bash
git -C .references/saleor describe --tags --exact-match HEAD
git -C .references/saleor rev-parse HEAD
git -C .references/saleor status --short
git -C .references/saleor show -s --format='%H %aI %s' \
  7e57a29b9f0dd6e93ab77998b93b0d2fe37fcdd6
```

`status --short` 必须为空。历史文件只通过 `git show <commit>:<path>` 阅读，不切换当前 checkout。

## 记录格式

```text
已核验事实：tag/commit + path:symbol + 读取命令
工程推断：根据哪些差异推断，不能写成历史事实
未验证：需要 issue/PR/ADR、测试或生产运行证据的部分
```
