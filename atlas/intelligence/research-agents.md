[产业地图](../README.md) · [Anthropic 经营与估值](anthropic.md) · [预测](../../predictions/README.md)

# 科研代理的瓶颈是取得可检验的结果

*Formal mathematics already has a cheap way to reject many errors. Research with physical instruments needs its own feedback, controls and measurement economics.*

## 一次合作留下了三层证据

1. **发现。** Levent Alpöge 在 11 月 20 日的作者说明中写明自己与 Claude 合作，交代关键数学方向、人与模型的分工及形式化档案。 [作者说明和原始档案入口](https://alpo.ge/remark.pdf)。
2. **形式化核验。** Lean FRO 与 Mathlib Initiative 的联合声明核对了命题、编译与可信依赖、定理一致性及多种内核检查结果。独立核验者还公布了核验入口和日志。项目查阅了核验入口和结果，完整的约 1700 万行证明未在本地重编。 [联合声明](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/) · [MIT 核验资料](https://math.mit.edu/~drew/grh/) · [第三方核验入口](https://github.com/Infatoshi/rh-verification-receipts/blob/main/verify_main.lean)。
3. **解释。** Waterloo 的 Michael Rubinstein 已公开专注于 ζ 函数的解释草稿，第二版日期为 11 月 22 日。其工作同时提供了独立核验说明。可读性和后续数学使用会随更多研究者复查而变化。 [解释稿与独立检查](https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/)。

最有用的学习不是估计一次新闻的震撼程度，而是追踪下一个学科能否具备同样廉价的结果检查：规划、执行、获得反馈，修改方案后再问一次。

## 自动化实验室已经出现可测的闭环

A-Lab 把计算候选、自动化合成和表征连在一起，在论文所选材料任务中报告实际实验产出。其价值是让每轮都能回到仪器结果。换一种材料体系、仪器、验证标准或实验场地，结果仍需独立验证。 [Nature 论文](https://www.nature.com/articles/s41586-023-06734-w)。

AI 科研的可服务市场可按「年度合格任务量 × 每个合格结果的净付费」分行业研究。衡量成本最好包括失败重跑、人审、仪器使用和排队。实验室的反馈通常比代码验证慢。能质控、校准并交付结果的实验服务商可能拿走一部分利润；只比模型标价很难说明钱会流向哪里。

## 给工程师的比较口径

同一批由领域专家预先定义的数据或任务，比较现行流程、有代理协作和更多任务委托三种条件。分别记任务成功率、返工、耗时、现金支出和人审时间。METR 的固定软件任务研究可作为方法参考，其时距使用人类完成该任务所需时间表示难度。同样要保留专家与非专家的对照，并计入失败。 [METR 方法与局限](https://metr.org/time-horizons/) · [OpenAI 科研任务研究](https://openai.com/index/research-acceleration-jagged-frontier/)。

如果不同学科无法复现收益，或核验与返工花掉了节约的时间，应对相应领域下调预期。值得跟踪的主体包括模型商 Anthropic、OpenAI 与 Google DeepMind，以及提供独立评估的 METR、能接收真实仪器反馈的自动化实验室和商业药物研究平台。
