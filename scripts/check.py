#!/usr/bin/env python3
"""按 CONTRIBUTING.md 的规则检查清单。只用标准库。

    python3 scripts/check.py              # 检查格式、中英文对应，并向 GitHub 核对每个仓库
    python3 scripts/check.py --offline    # 不联网，只查格式和中英文对应
    python3 scripts/check.py --base origin/main
                                          # 审 PR 用：这次新增或改动的条目按收录条件严格检查，
                                          # 原有条目过期、归档只提醒，不算这个 PR 的错

联网检查要读环境变量 GITHUB_TOKEN 或 GH_TOKEN（公开仓库的只读令牌就够）。
有错误时退出码为 1；提醒不影响退出码。
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

FILES = ["README.md", "README.zh-CN.md"]
ENTRY = re.compile(r"^- (🏢 )?\[([^\]]+)\]\(https://github\.com/([^)\s]+)\)(?: ⭐(\d+))? — (\S.*)$")
REPO = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9._-]+$")
MAX_AGE_DAYS = 90
MIN_STARS = 10


def parse(text):
    """返回 (条目, 格式错误)。条目带上它是第几个小节，用来比对中英文的位置。"""
    entries, errors, section = [], [], -1
    for no, line in enumerate(text.split("\n"), 1):
        if line.startswith("#"):
            section += 1
            continue
        if not line.startswith("- ") or "](https://github.com/" not in line:
            continue
        m = ENTRY.match(line)
        if not m:
            errors.append((no, "格式不对，应为「- [owner/repo](https://github.com/owner/repo) ⭐星数 — 一句话」：" + line[:80]))
            continue
        corp, text_, repo, stars, _ = m.groups()
        if not REPO.match(repo):
            errors.append((no, f"链接要指到仓库首页：{repo}"))
            continue
        if text_ != repo:
            errors.append((no, f"链接文字 {text_} 和链接里的仓库 {repo} 不一致"))
        if stars is not None and int(stars) < MIN_STARS:
            errors.append((no, f"{repo}：星数不到 {MIN_STARS} 不写"))
        entries.append({"line": no, "section": section, "repo": repo, "corp": bool(corp), "stars": stars})
    seen = {}
    for e in entries:
        key = e["repo"].lower()
        if key in seen:
            errors.append((e["line"], f"{e['repo']} 重复了，第 {seen[key]} 行已经有"))
        seen.setdefault(key, e["line"])
    return entries, errors


def compare(en, zh):
    """两份 README 的条目要一一对应：同一个小节、同一个位置、同样的 🏢 和星数。"""
    errors = []
    # 先报只在一边出现的，再去掉它们逐条比位置，免得少一条就整片错位
    names = [{e["repo"].lower() for e in side} for side in (en, zh)]
    for side, name, other in ((en, FILES[0], names[1]), (zh, FILES[1], names[0])):
        for e in side:
            if e["repo"].lower() not in other:
                errors.append(f"{name} 第 {e['line']} 行的 {e['repo']} 在另一份里没有")
    both = names[0] & names[1]
    en = [e for e in en if e["repo"].lower() in both]
    zh = [e for e in zh if e["repo"].lower() in both]
    for a, b in zip(en, zh):
        where = f"{FILES[0]} 第 {a['line']} 行 / {FILES[1]} 第 {b['line']} 行"
        if a["repo"].lower() != b["repo"].lower() or a["section"] != b["section"]:
            errors.append(f"{where}：中英文不在同一个位置（{a['repo']} / {b['repo']}），后面的不再逐条比")
            break
        if a["corp"] != b["corp"]:
            errors.append(f"{where}：{a['repo']} 的 🏢 两边不一致")
        if a["stars"] != b["stars"]:
            errors.append(f"{where}：{a['repo']} 的星数两边不一致")
    return errors


def fetch(repos, token):
    """一次查一批仓库。查不到的（404、私有、被封）值为 None。"""
    out = {}
    for start in range(0, len(repos), 50):
        chunk = repos[start:start + 50]
        fields = "nameWithOwner isArchived pushedAt owner{__typename}"
        query = "query{" + " ".join(
            'r%d: repository(owner:%s, name:%s){%s}' % (i, json.dumps(r.split("/")[0]), json.dumps(r.split("/")[1]), fields)
            for i, r in enumerate(chunk)) + "}"
        req = urllib.request.Request(
            "https://api.github.com/graphql", data=json.dumps({"query": query}).encode(),
            headers={"Authorization": "bearer " + token, "User-Agent": "awesome-dsh-fde-check"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = json.load(resp)
        except urllib.error.URLError as err:
            sys.exit(f"查询 GitHub 失败：{err}")
        data = body.get("data")
        if data is None:
            sys.exit("查询 GitHub 失败：" + json.dumps(body.get("errors"), ensure_ascii=False)[:300])
        for i, r in enumerate(chunk):
            out[r] = data.get(f"r{i}")
    return out


def base_repos(ref):
    """基准版本里已有的仓库（小写）。取不到基准时返回 None。"""
    p = subprocess.run(["git", "show", f"{ref}:{FILES[0]}"], capture_output=True, text=True)
    if p.returncode != 0:
        return None
    return {e["repo"].lower() for e in parse(p.stdout)[0]}


def main():
    ap = argparse.ArgumentParser(description="按 CONTRIBUTING.md 的规则检查清单")
    ap.add_argument("--offline", action="store_true", help="不联网，只查格式和中英文对应")
    ap.add_argument("--base", help="审 PR 用的基准（如 origin/main）：原有条目过期、归档只提醒")
    args = ap.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    errors, warnings, parsed = [], [], []
    for name in FILES:
        entries, errs = parse(open(name, encoding="utf-8").read())
        parsed.append(entries)
        errors += [f"{name} 第 {no} 行：{msg}" for no, msg in errs]
    en, zh = parsed
    errors += compare(en, zh)

    if not args.offline:
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if not token:
            sys.exit("联网检查需要 GITHUB_TOKEN 或 GH_TOKEN；只查格式请加 --offline")
        old = base_repos(args.base) if args.base else None
        if args.base and old is None:
            warnings.append(f"取不到基准 {args.base}，全部条目按新增检查")
        info = fetch(sorted({e["repo"] for e in en}), token)
        now = datetime.datetime.now(datetime.timezone.utc)
        for e in en:
            repo, got = e["repo"], info[e["repo"]]
            where = f"{FILES[0]} 第 {e['line']} 行 {repo}"
            # 原有条目慢慢过期不是这个 PR 的错，只提醒；定期检查（不带 --base）时才算错
            aging = warnings if old is not None and repo.lower() in old else errors
            if got is None:
                aging.append(f"{where}：仓库打不开（删除、转私有或改名后失效）")
                continue
            if got["nameWithOwner"] != repo:
                aging.append(f"{where}：仓库现在叫 {got['nameWithOwner']}，请更新链接")
            if got["isArchived"]:
                aging.append(f"{where}：仓库已归档")
            days = (now - datetime.datetime.fromisoformat(got["pushedAt"].replace("Z", "+00:00"))).days
            if days > MAX_AGE_DAYS:
                aging.append(f"{where}：{days} 天没有提交，超过 {MAX_AGE_DAYS} 天")
            if e["corp"] and got["owner"]["__typename"] != "Organization":
                warnings.append(f"{where}：带 🏢，但仓库在个人账号下，请人工确认是不是厂商自己的")

    for w in warnings:
        print("提醒  " + w)
    for err in errors:
        print("错误  " + err)
    print(f"{len(en)} 个条目，{len(errors)} 个错误，{len(warnings)} 个提醒")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
