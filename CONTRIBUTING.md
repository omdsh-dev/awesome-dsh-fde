# Contributing / 贡献指南

## English

Suggest a project by opening an issue or a pull request. Please:

- Add the entry to **both** `README.md` and `README.zh-CN.md`, in the same section and position.
- Use the format `- [owner/repo](https://github.com/owner/repo) ⭐stars — one sentence on what it does for an enterprise.` Omit the star count if it is under 10.
- Only add 🏢 if the repository lives under the vendor's or institution's own GitHub organization.
- Entries must be installable, maintained (pushed within the last 90 days), not archived, and clearly useful in a company setting.
- Case studies need a public source. Mark self-reported numbers as unverified.
- Red-team, jailbreak and other offensive tooling is out of scope.

Before opening a pull request, run `python3 scripts/check.py --offline` (format and English/Chinese parity) or, with `GITHUB_TOKEN` set, `python3 scripts/check.py` (also checks that each repository exists, is not archived and was pushed within 90 days). CI runs the same check on every pull request.

## 中文

通过 issue 或 PR 推荐项目。请注意：

- **同时**修改 `README.md` 和 `README.zh-CN.md`，放在相同的分类和位置。
- 格式：`- [owner/repo](https://github.com/owner/repo) ⭐星数 — 一句话说明它在企业里能做什么。` 星数不到 10 可以不写。
- 只有仓库在厂商或机构自己的 GitHub 组织下，才加 🏢。
- 收录条件：能安装、在维护（90 天内有提交）、没有归档，并且在企业场景里确实有用。
- 案例要有公开来源；对方自己报的数据要注明「未核实」。
- 不收红队、越狱等攻击类工具。

提 PR 前可以先跑 `python3 scripts/check.py --offline`（格式、中英文是否对应）；设了 `GITHUB_TOKEN` 时跑 `python3 scripts/check.py`，还会核对每个仓库是否存在、有没有归档、90 天内有没有提交。每个 PR 的 CI 会跑同样的检查。
