# Awesome DSH FDE

[English](./README.md) | 中文

给**前线部署工程师（FDE）** 的 DeepSeek Harness（DSH）企业落地清单：把 DSH 带进一家公司时，接入系统、接入数据、管住权限、按行业找现成能力，分别可以用什么。

> **收录口径**
> - 插件来自 [dshfind.com](https://dshfind.com) 的插件快照（2026-11-03，共 26,253 个仓库）。只收能安装、没被标记为风险、没有归档的项目，再按企业场景人工挑选。星数是快照当天的数字。
> - 🏢 表示项目发布在厂商或机构自己的 GitHub 组织下。这不等于 DeepSeek 官方认证，上线前请自己核实。
> - DSH 还是开发者预览版，插件 API 会有破坏性变更。收录不代表已在生产环境验证，请先在试点环境里跑通。
> - 发现错漏或想推荐项目，见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 目录

- [FDE 实践要点](#fde-实践要点)
- [企业平台与治理](#企业平台与治理)
- [身份、安全与合规](#身份安全与合规)
- [可观测与运维](#可观测与运维)
- [IM 与协作](#im-与协作)
- [办公文档](#办公文档)
- [数据库与数据分析](#数据库与数据分析)
- [知识库与检索](#知识库与检索)
- [浏览器与桌面自动化（老系统取数）](#浏览器与桌面自动化老系统取数)
- [行业方案](#行业方案)
  - [财务与 ERP](#财务与-erp)
  - [金融与投研](#金融与投研)
  - [法律与知识产权](#法律与知识产权)
  - [医疗与生命科学](#医疗与生命科学)
  - [制造与工程](#制造与工程)
  - [电商与零售](#电商与零售)
  - [政务与招投标](#政务与招投标)
  - [人力资源](#人力资源)
  - [营销与内容](#营销与内容)
  - [科研](#科研)
- [案例与文章](#案例与文章)
- [相关清单](#相关清单)

## FDE 实践要点

从各类部署文章和社区项目里归纳出来的做法，不是官方规范。

1. **先问「用谁的身份调」。** 企业系统大多按人鉴权。共享服务账号只适合只读的公共数据；按人的数据要用员工自己的令牌、OAuth 委托，或由平台签发的短期身份令牌（JWT），让源系统自己判权限，不要在 Agent 侧再复制一套。
2. **再问「在哪里调」。** 有接口的系统走服务端；只能在内网访问、要用员工登录态、只能靠网页操作的老系统，放在员工本机用浏览器自动化，不要在服务器上存员工密码。
3. **先只读，写操作要审批。** 第一期只开放查询类工具；写操作要有人工确认，并记进审计日志。
4. **敏感数据在进模型之前脱敏**，例如身份证号、手机号、银行卡号。
5. **统一入口。** 模型调用走企业网关（额度、审计），企业系统聚合成一个 MCP 端点，员工的 DSH 只配一处。
6. **插件也要准入审核。** 上架前跑静态扫描和健康检查，并锁定版本。
7. **分阶段推进**：先在本机跑通，再挑一个部门、一个场景试点，最后再考虑私有化部署和全员推广。社区文章普遍建议按「1 个月 / 3 个月 / 6 个月」规划。
8. **注意已知的安全问题**：早期版本出现过本地控制接口导致的沙箱逃逸（见[案例与文章](#案例与文章)），间接提示注入的成功率也不低。请及时升级，不要把 Web UI 直接暴露到公网。

## 企业平台与治理

- [hikariming/dsh-ee](https://github.com/hikariming/dsh-ee) — 面向 DSH 的自托管企业平台：接入企业系统和知识库、搭建 AI 微应用，经审核、按权限下发给每位员工。
- [himovo/movo](https://github.com/himovo/movo) ⭐517 — 把 DSH 变成自托管的企业 Agent 平台，包含知识库、深度研究、内容生成、浏览器自动化和管理后台。
- 🏢 [iflytek/skillhub](https://github.com/iflytek/skillhub) ⭐5367 — 科大讯飞开源的企业级技能仓库：技能包版本管理、RBAC 与审计日志，支持 Docker / Kubernetes 私有部署。
- [01men/ybkkasi](https://github.com/01men/ybkkasi) ⭐66 — 企业 AI 资产治理：MCP 服务、技能、Agent 统一台账，包含生命周期状态、85 个权限点、按部门 × Agent × 技能的成本归集和审计。
- [aiworkskills/deepseek-harness-server](https://github.com/aiworkskills/deepseek-harness-server) — 让已有业务系统接入 DSH，不改 DSH 源码：OAuth 委托身份、每用户独立运行时、业务 API 对象级授权。
- [git4oc/DSH-BOOT](https://github.com/git4oc/DSH-BOOT) — 基于 DSH 内核的多租户 Agent 平台：租户隔离、安全审计、审批、配额计费、会话持久化。
- [slywalker2006/dsh-passwords](https://github.com/slywalker2006/dsh-passwords) ⭐81 — 服务器级网关：远程访问、自动 HTTPS、子用户权限与配额、强制沙箱、审计日志。
- [xgone/dsh-remote](https://github.com/xgone/dsh-remote) ⭐45 — 在浏览器里安全地远程使用 DSH：登录、MFA 两步验证、角色权限。
- [pointer-a/dsh-server-login](https://github.com/pointer-a/dsh-server-login) ⭐32 — 多租户 DSH 托管：用户注册后经管理员审核，各自获得隔离的 DSH 环境。
- [mickymultani/deepseek-harness-enterprise-suite](https://github.com/mickymultani/deepseek-harness-enterprise-suite) — 企业插件、治理控制和连接器模板的开源合集（早期项目）。

## 身份、安全与合规

- [PensiveFei/dsh-secure-audit](https://github.com/PensiveFei/dsh-secure-audit) ⭐86 — 只读的安全合规插件：检测提示注入、脱敏中文个人信息、审计本地配置，输出可复现的报告。
- [PerryLink/dsh-mask](https://github.com/PerryLink/dsh-mask) ⭐16 — 个人信息脱敏中间件：姓名、手机号、身份证号、银行卡号、密钥在发给模型前换成占位符，显示时再还原；还原表只保存在内存里。
- [toby-bridges/api-relay-audit](https://github.com/toby-bridges/api-relay-audit) ⭐905 — 审计 API 中转和模型代理：检测提示注入、模型偷换、工具调用被改写、SSE 异常等。
- [delta-box/deltabox-lite](https://github.com/delta-box/deltabox-lite) ⭐304 — 轻量的 Agent 沙箱：可以查看改动、提交或回滚。
- [SteelUnion/dsh-confirm-gate](https://github.com/SteelUnion/dsh-confirm-gate) ⭐60 — 统计每轮里的持久化操作次数，超过阈值就提醒、让模型停下并请求确认。
- [openguardrails/OpenGuardrailsBench](https://github.com/openguardrails/OpenGuardrailsBench) ⭐60 — 可复现的 AI 护栏评测基准，覆盖安全、隐私和策略，含中英文用例（0.1 版是合成数据的试点）。
- [Eligahyu/dsh-sentinel-scanner](https://github.com/Eligahyu/dsh-sentinel-scanner) — 插件安全体检：静态扫描代码执行、凭据、外传、混淆、安装脚本，给出 0～100 的风险分。适合用在插件准入审核里。
- 🏢 [omdsh-dev/dsh-plugin-check](https://github.com/omdsh-dev/dsh-plugin-check) ⭐26 — 插件健康检查：清单格式、patch 格式、构建陷阱。
- [feely0208/dsh-bundle-cn-skills](https://github.com/feely0208/dsh-bundle-cn-skills) — 中文合规技能集：对外文案红线、AI 生成内容标识、个人信息保护对照、密钥扫描。全部离线运行。

## 可观测与运维

- [loongsuite/dsh-plugin](https://github.com/loongsuite/dsh-plugin) ⭐31 — OpenTelemetry 链路追踪：每轮对话生成一棵 GenAI span 树（模型调用、首字延迟、工具执行、token 用量），经 OTLP 发到 Jaeger、Tempo、Langfuse 等。
- 🏢 [TencentCloud/tencentcloud-agentobs-sdk-dsh](https://github.com/TencentCloud/tencentcloud-agentobs-sdk-dsh) ⭐14 — 把 DSH 的 trace 直接上报到腾讯云日志服务（CLS），不需要另外部署 OTLP 收集器。
- [tma1-ai/dsh-otel](https://github.com/tma1-ai/dsh-otel) ⭐10 — 把 trace、指标、日志写进 GreptimeDB，自带 7 个 Grafana 看板，看每次运行花了多少 token、钱和时间。
- [guhanfei-ai/dsh-grafana](https://github.com/guhanfei-ai/dsh-grafana) — 在对话里查 Grafana 的看板、指标、告警。
- [runzhliu/deepseek-harness-docker](https://github.com/runzhliu/deepseek-harness-docker) ⭐146 — 社区维护的 Docker / Kubernetes 打包：加固镜像、Compose、Helm Chart。
- 🏢 [huaweicloud/huaweicloud-devkit](https://github.com/huaweicloud/huaweicloud-devkit) ⭐70 — 华为云官方的 Agent 插件：技能、MCP 工具、安全护栏、云端沙箱。
- [caoyiwei850/dsh-ssh-ops](https://github.com/caoyiwei850/dsh-ssh-ops) ⭐48 — 在对话里操作 SSH，内置高危命令保护，侧栏有终端。
- [Khorsheed/dsh-ankh-guard](https://github.com/Khorsheed/dsh-ankh-guard) — 自托管运维守护：Agent 改完代码先跑构建和测试再重启，起不来就自动回滚。

## IM 与协作

- [xmanrui/dsh-im](https://github.com/xmanrui/dsh-im) ⭐3148 — 扫码或填机器人凭据，把飞书、微信、钉钉、企业微信、QQ、Slack 等 9 个渠道接入 DSH。
- 🏢 [DingTalk-Real-AI/dsh-dingtalk](https://github.com/DingTalk-Real-AI/dsh-dingtalk) ⭐21 — 钉钉连接器。
- 🏢 [omdsh-dev/dsh-lark](https://github.com/omdsh-dev/dsh-lark) ⭐59 — 飞书 / Lark 机器人渠道。
- [zhuiyueya/dsh-im-gateway](https://github.com/zhuiyueya/dsh-im-gateway) ⭐59 — 聚合 20 多个聊天平台的 IM 网关。
- [THEWOLFWALKER/dsh-notifier](https://github.com/THEWOLFWALKER/dsh-notifier) ⭐59 — 通知与远程控制：28 个外发渠道，6 种入站控制方式。
- [nicecx/dsh-relay](https://github.com/nicecx/dsh-relay) — 把审批和提问转发到聊天渠道，各渠道共用一套适配器接口。
- [wxkingstar/SpecFusion](https://github.com/wxkingstar/SpecFusion) ⭐76 — 在对话里搜索 20 个中国开放平台的 6.5 万多篇 API 文档，适合写企业系统对接代码时用。

## 办公文档

- 🏢 [dream-num/univer-workspace](https://github.com/dream-num/univer-workspace) ⭐2267 — 开源的办公工作区，人和 Agent 在里面一起创建、协作、审阅文档。
- 🏢 [dream-num/dsh-univer-office](https://github.com/dream-num/dsh-univer-office) ⭐660 — 给 DSH 一个真正的办公环境：表格、文档、幻灯片、关系表，改动有版本，多 Agent 各自在隔离的工作区里改。
- 🏢 [FylarOpen/dsh-fylar-office-editor](https://github.com/FylarOpen/dsh-fylar-office-editor) ⭐263 — 基于 Fylar Office SDK 的 Office 预览、编辑和 DOCX 生成。
- [sueccku/dsh-plugin-wps-office-next](https://github.com/sueccku/dsh-plugin-wps-office-next) ⭐29 — 用中文对话操作 WPS 表格、文字、演示，支持批量转 PDF。
- [copylee711/dsh-office](https://github.com/copylee711/dsh-office) ⭐20 — 直接修改已经打开的 Word / Excel / PowerPoint，改动实时可见（Windows）。
- 🏢 [omdsh-dev/dsh-office](https://github.com/omdsh-dev/dsh-office) ⭐30 — 生成、读取、编辑 xlsx / pdf / pptx。
- [HuanLinOTO/dsh-plugin-mineru](https://github.com/HuanLinOTO/dsh-plugin-mineru) ⭐51 — 用 MinerU 把 PDF、图片、Office 文件转成结构化的 Markdown / JSON，适合做知识库入库前的预处理。
- [17897693/dsh-wen](https://github.com/17897693/dsh-wen) — 办公文档读写与格式互转，内置离线 OCR，能处理中文扫描件。
- [liustack/pptwise](https://github.com/liustack/pptwise) ⭐27 — 在本机生成可编辑的真 PPT（不是 HTML），不需要 API key。

## 数据库与数据分析

- 🏢 [omdsh-dev/dsh-data-agent](https://github.com/omdsh-dev/dsh-data-agent) ⭐217 — 连接数据库，用对话做数据分析，产出业务洞察。
- [niuhuoshan/dsh-connect](https://github.com/niuhuoshan/dsh-connect) — 数据源连接：发现元数据、AI 语义建模、只读 SQL、调用固定的 HTTP API。
- [mengqi1436/dsh-db-tool](https://github.com/mengqi1436/dsh-db-tool) — 对话式数据库管理：支持 8 种数据库，按项目授权，危险操作需要确认。
- [OtterMind/sqlx](https://github.com/OtterMind/sqlx) — 给 Agent 用的数据库命令行：数据源配置加密存放，按需启动原生或 JDBC 驱动。
- [duyanta123/dsh-data-insight](https://github.com/duyanta123/dsh-data-insight) — 用 DuckDB 分析 CSV，生成图表和报告。
- [Onenightcarnival/dsh-toolkit](https://github.com/Onenightcarnival/dsh-toolkit) — 数据库工作台、S3 存储、OpenTelemetry 导出、浏览器控制。
- [nomicore-ai/nomicore](https://github.com/nomicore-ai/nomicore) — 自带描述的受治理数据核心：表结构、权限归属、校验规则和语义说明跟着数据走。
- [duhu2000/dsh-mcp-connector](https://github.com/duhu2000/dsh-mcp-connector) ⭐103 — MCP 数据市场连接器：企业、金融、法律、专利、科研数据；支持 OAuth、API key、HTTP / stdio。

## 知识库与检索

- [Soren-ABT/dsh-knowledge](https://github.com/Soren-ABT/dsh-knowledge) ⭐89 — 知识库与 RAG：分块、本地 embedding、混合检索、管理面板。
- [PerryLink/dsh-library](https://github.com/PerryLink/dsh-library) ⭐24 — 本地文档库：语义与关键词混合检索、多样性重排、引用核对；不需要下载模型。
- [Rxiain/dsh-openviking](https://github.com/Rxiain/dsh-openviking) ⭐19 — 接入 OpenViking 的检索、资源管理、自动召回和会话记忆。
- [chenkezhen480/pinakes-rs](https://github.com/chenkezhen480/pinakes-rs) — 自托管知识服务：由大模型维护的 wiki 加业务图谱，读取时不经过大模型和数据库；提供 HTTP 和 MCP 接口。
- [mingzeng21/dsh-obsidian](https://github.com/mingzeng21/dsh-obsidian) ⭐40 — 连接本地 Obsidian 库：搜索、读写、移动笔记。
- [poco-ai/Agentero](https://github.com/poco-ai/Agentero) ⭐1074 — 人与 Agent 协作的研究工作区：带引用的 PDF 问答、资料库、写作。

## 浏览器与桌面自动化（老系统取数）

没有接口的老系统，往往只能这样拿数据。建议跑在员工本机，用员工自己的登录态。

- [Fisfzy/dsh-ego-browser](https://github.com/Fisfzy/dsh-ego-browser) ⭐409 — 接入给 Agent 用的 Chromium：语义快照、语义定位点击、表单填充、按任务隔离浏览器空间。
- [drscrewdriver/dsh-browser-cdp](https://github.com/drscrewdriver/dsh-browser-cdp) ⭐24 — 通过 CDP 接入真实的 Chrome，支持实时截图回传和导入登录态。
- [angelky7/dsh-browser-control](https://github.com/angelky7/dsh-browser-control) ⭐53 — Chrome 扩展加 DSH 插件，直接操作员工自己的浏览器。
- [SheepofSheep/dsh-doyourweb](https://github.com/SheepofSheep/dsh-doyourweb) ⭐40 — 引用并操作已经打开的 Chrome / Edge 标签页。
- [anweat/dsh-browser](https://github.com/anweat/dsh-browser) ⭐31 — 自带 Playwright（Chromium）的浏览器运行时。
- 🏢 [Tabbit-Browser/dsh-tabbit](https://github.com/Tabbit-Browser/dsh-tabbit) ⭐121 — Tabbit 浏览器的 DSH 插件。
- [momasiku/dsh-pilot](https://github.com/momasiku/dsh-pilot) ⭐145 — Windows 桌面自动化：CAD、WPS、浏览器、发微信。
- [Anionex/dsh-computer-use](https://github.com/Anionex/dsh-computer-use) ⭐89 — macOS 电脑控制：以无障碍接口为主，拒绝基于过期界面状态的操作，按范围授权。
- [dttxorg/deepseekeyes](https://github.com/dttxorg/deepseekeyes) — 可审计的视觉与跨平台电脑控制，每一步都留证据。
- [monagisa/dsh-plugin-shop-accounts](https://github.com/monagisa/dsh-plugin-shop-accounts) — 一个店铺一个 Chrome 档案，登录一次长期复用，定时检测和续期登录态。「多账号 + 网页登录态」的管理方式可以参考它。

## 行业方案

### 财务与 ERP

- [EthanYoQ/Invoice-Downloader](https://github.com/EthanYoQ/Invoice-Downloader) ⭐533 — 从邮箱批量收集 PDF / OFD / XML 电子发票，OCR 识别、分类归档、生成 Excel 汇总，为报销做准备。
- [988hj7tczd-oss/dsh-invoice-tools](https://github.com/988hj7tczd-oss/dsh-invoice-tools) — 把中国电子发票 PDF 解析成结构化 JSON 并核对金额，生成报销单。
- [zhang787jun/dsh-finance](https://github.com/zhang787jun/dsh-finance) — 财务与会计工作流，改编自 Anthropic 的 Finance 示例。
- [maxmilian/dsh-odoo](https://github.com/maxmilian/dsh-odoo) — 只读的 Odoo ERP 工具，可以选择开启受限的「创建草稿」。先只读、写操作受限，这是很好的示范。

### 金融与投研

- [PerryLink/dsh-industry-research](https://github.com/PerryLink/dsh-industry-research) ⭐215 — 行业与公司研究：方法论技能、产业链梳理、政策和新闻跟踪、可审计的研究报告。
- [PerryLink/dsh-research-report](https://github.com/PerryLink/dsh-research-report) ⭐212 — 可验证的研究报告引擎：每条结论绑定证据快照，报告封存后可以防篡改核验。
- [hancao97/hanai-investment-dsh](https://github.com/hancao97/hanai-investment-dsh) ⭐120 — 本地运行的 A 股研究工作台：行情看板、估值、带版本的报告。
- [davidalmeida90/finance-agent-kit](https://github.com/davidalmeida90/finance-agent-kit) — 股票估值技能和数据 MCP（SEC 文件、行业 beta）。

### 法律与知识产权

- 🏢 [yuandian-ailaw/yuandian_dsh_plugin](https://github.com/yuandian-ailaw/yuandian_dsh_plugin) — 华语元典法律数据插件。
- [duhu2000/qcc-mcp-legal-oauth](https://github.com/duhu2000/qcc-mcp-legal-oauth) — 一键 OAuth 授权，连接企查查的法规和案例数据 MCP。按人授权的接法可以参考它。
- [MiaoQichuan/new-litigation-visualization](https://github.com/MiaoQichuan/new-litigation-visualization) ⭐141 — 诉讼可视化工具集：时间轴、大事记表、庭审对抗图、法律关系图。
- [yuc16/PatentRadar](https://github.com/yuc16/PatentRadar) ⭐67 — 输入专利公开号，输出竞品侵权分析报告。
- [ai-tools-mtl/Aurify](https://github.com/ai-tools-mtl/Aurify) — 专利撰写把关：先检索中国专利判断值不值得写，再走完技术交底书全流程。
- [ByronLeeeee/dsh-legal-dashboard](https://github.com/ByronLeeeee/dsh-legal-dashboard) — 按案件组织的法律工作台和文书工具。
- [wesky820/dsh-law](https://github.com/wesky820/dsh-law) — 本地法律工作台：案件看板、日程与期限管理。

### 医疗与生命科学

- [sagirimo/BioDSH](https://github.com/sagirimo/BioDSH) ⭐65 — 面向临床医生和湿实验科学家的生物信息 Agent 桌面端，支持离线模式。
- [bowang-lab/dsh-medomni](https://github.com/bowang-lab/dsh-medomni) — 医学影像分析插件。
- [wp-a/dsh-academic-paper-search](https://github.com/wp-a/dsh-academic-paper-search) — 中文学术论文检索：引用核验、引文图谱、MeSH 和临床试验检索。

### 制造与工程

- [27painter/dsh-sw-cad](https://github.com/27painter/dsh-sw-cad) — SolidWorks 和 AutoCAD 自动化（Windows，COM 接口）。
- [LAU-MARS/dsh-cad](https://github.com/LAU-MARS/dsh-cad) ⭐32 — 2D / 3D CAD 插件。
- [AmethystLuna/embedded-workbench](https://github.com/AmethystLuna/embedded-workbench) ⭐29 — 嵌入式 C/C++ 工程：FreeRTOS、Keil、HardFault 排查等固件技能。
- [JoeyZzZzZz/treasure-map](https://github.com/JoeyZzZzZz/treasure-map) — 经 MCP 提供固件分析：识别危险调用，比较两个版本之间改了哪些函数。
- [Fantasality/dsh-origin-plugin](https://github.com/Fantasality/dsh-origin-plugin) ⭐36 — 在对话里驱动 OriginLab 做科学绘图，有 74 个工具（Windows）。
- [liuhange789/data-asset-inspector](https://github.com/liuhange789/data-asset-inspector) — 30 个数据核查插件：数据资产登记、政务数据检查、反洗钱合规、BIM 清点、管线巡检。

### 电商与零售

- [lunw/shopline-ai-toolkit-dsh](https://github.com/lunw/shopline-ai-toolkit-dsh) — SHOPLINE 开发者 MCP 桥接和 SHOPLINE 技能。
- [Tulipe1735/dsh-plugin-kefu](https://github.com/Tulipe1735/dsh-plugin-kefu) — 电商客服台：商品知识库、有依据的回复、转人工队列，对接千牛 / 京麦的开放平台。
- [mirror9933/dsh-pixmart](https://github.com/mirror9933/dsh-pixmart) — 电商图片生成：主图、详情图、广告图、白底图。
- [shine-233/dsh-waimao](https://github.com/shine-233/dsh-waimao) — 外贸获客：搜客、WhatsApp 客服审核台、邮件跟进、CRM、报价单 PDF。

### 政务与招投标

- [linhut/gongwen-skill](https://github.com/linhut/gongwen-skill) ⭐99 — 按 GB/T 9704 处理公文全流程：格式检查与修复、Word 原生修订和批注、事实核验。
- [ExElectron/dsh-tool-hongtou](https://github.com/ExElectron/dsh-tool-hongtou) ⭐27 — 生成标准红头公文：大模型只出结构化提纲，版式由确定性渲染生成。
- [Ramenne/DeepSeek-Harness-Gov](https://github.com/Ramenne/DeepSeek-Harness-Gov) — DSH 政务版：政务办事 WebUI 和红头公文插件。
- [maike-china/rejection-check](https://github.com/maike-china/rejection-check) — 标书废标项检查：提取无效投标和废标条款，做三轮风险检查，生成 PDF 报告。
- [zslzxy/aitoubiaoling-bid-review](https://github.com/zslzxy/aitoubiaoling-bid-review) — 审核商务标、技术标的风险。

### 人力资源

- [Viy1204/recruiting-copilot](https://github.com/Viy1204/recruiting-copilot) ⭐105 — 招聘工作流：岗位梳理、在 BOSS 直聘和猎聘寻源初筛、简历评估、面试安排、候选人台账和日报。
- [MaxHou-infinity/dsh-scout](https://github.com/MaxHou-infinity/dsh-scout) — 基于证据的公司尽调和岗位背调。

### 营销与内容

- 🏢 [redfox-data/redfox-community-dsh](https://github.com/redfox-data/redfox-community-dsh) — 红狐数据：100 多个社媒数据技能，覆盖抖音、小红书、快手、B 站、公众号、微博、TikTok 等。
- [jerryjiao/dsh-wewrite](https://github.com/jerryjiao/dsh-wewrite) — 公众号写作流水线：定时任务默认只存进草稿箱，群发永远由人来点。
- [aiworkskills/dsh-wechat-article](https://github.com/aiworkskills/dsh-wechat-article) — 公众号运营：选题、写稿、排版、配图、发布。
- [Finderchangchang/brewreel](https://github.com/Finderchangchang/brewreel) ⭐178 — 用便宜的模型做竖版宣传片，自带广告法用语校验。

### 科研

- [1692775560/dsh-Mimir-Academic-research](https://github.com/1692775560/dsh-Mimir-Academic-research) ⭐553 — 科研工作台：LaTeX 边写边编译、arXiv 文献管理、实验追踪、GPU 服务器任务编排。
- [Vncntvx/dsh-zotero](https://github.com/Vncntvx/dsh-zotero) ⭐58 — 在对话里检索和阅读 Zotero 文献，并核查文献引用。

## 案例与文章

截至 2026-11，**公开资料里还找不到具名企业、带量化结果的 DSH 生产案例**。下面是比较有参考价值的部署指南、评估和安全研究；文中自称的效果数据都没有独立核实。

- [DeepSeek Harness 实操指南——企业落地要跨五个台阶](https://www.53ai.com/news/OpenSourceLLM/2026082496831.html)（53AI）— 环境、模型、权限、插件开发、行业知识封装五步。举了 HR 的例子：把社保查询、公积金计算、背调发起分别做成插件。另外给出 1 / 3 / 6 个月的分阶段路线。
- [DeepSeek Harness 企业级部署解决方案](https://www.toutiao.com/article/7680883943696056838/)（今日头条）— 总结了直接用 Demo 配置上线后遇到的问题：任务丢失、沙箱逃逸、权限失控、会话没有持久化、并发卡死。
- [DeepSeek Harness 企业级智能体构建案例实训](https://deepseek.csdn.net/6a82cb06662f9a54cb9dd38a.html)（CSDN）— 一套 FDE 交付流程：业务调研 → 知识底座 → 标准化技能（合同审核、报表分析、工单处理）→ 注册检索插件、技能插件和企业 API 连接器 → 配置沙箱、日志和限流 → 灰度上线。
- [DeepSeek Harness Review: Production Readiness](https://wavect.io/blog/deepseek-harness-enterprise-review/)（Wavect）— 结论是适合做受控的工程试点。
- [DeepSeek Harness Sandbox Escape and Agent Containment](https://labs.cloudsecurityalliance.org/research/csa-research-note-deepseek-harness-sandbox-escape-20260910-c/)（CSA）— 本地控制接口（默认端口 3080）鉴权有缺陷，导致沙箱逃逸；0.1.1-rc.2 及更早的版本受影响。
- [DeepSeek Harness in Developer Preview](https://www.marktechpost.com/2026/08/17/deepseek-ai-releases-deepseek-harness-in-developer-preview/)（MarkTechPost）— 定位是开发者基础设施；受监管的企业可以本地试点，用于私有代码库编程、模型评估、审批策略等。
- [DeepSeek Harness (dsh): Installed and Benchmarked](https://flowtivity.ai/blog/deepseek-harness-open-source-agent-explained/)（Flowtivity）— 建议现阶段用于评估和原型，等 API 稳定后再决定是否上生产。
- [DeepSeek Harness 架构分析与实践指南](https://intl.cloud.baidu.com/en/article/8946258)（百度智能云）— 提到在金融、客服、IT 运维中的应用和效果数据，但没有点名企业。
- [DeepSeek Harness：日活 154 万，将建设官方插件市场](https://www.ithome.com/1/023/011.htm)（IT 之家）— 官方数据：第三方插件约 3.5 万个；官方欢迎企业以插件形式接入产品和服务。

## 相关清单

- [dshfind.com](https://dshfind.com) — DSH 插件导航与学习站，也是本清单的数据来源。
- [libukai/awesome-deepseek-harness](https://github.com/libukai/awesome-deepseek-harness) — 通用的 DSH 资源清单。
- [the-beating-light-of-the-nail/awesome-dsh-plugin-stock](https://github.com/the-beating-light-of-the-nail/awesome-dsh-plugin-stock) — 股票、金融、量化方向的插件清单。

## 许可

[CC0 1.0](./LICENSE)
