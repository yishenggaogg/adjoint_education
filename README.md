# Discrete adjoint: interactive lessons

Twenty self-contained, interactive web pages that teach the **fully discrete adjoint** of a finite-volume scheme from start to finish, for undergraduates with a background in calculus, linear algebra and numerical methods. The teaching path leads toward a complete discrete adjoint for industrial unstructured-grid RANS: the 2-D RANS&ndash;SA pages are online (the complete discrete adjoint on a teaching mesh, comparing an adjoint-inconsistent and an adjoint-consistent inflow treatment); industrial scale is still ahead. Continuous adjoints appear only as independent checks for simple cases (Appendix A of the pages); a formal continuous RANS adjoint is not automatically a strict reference for a full industrial algorithm.

**Read online:** <https://yishenggaogg.github.io/adjoint_education/> &mdash; English by default, with a Chinese / English toggle at the top of every page.

**Repositories:** [GitHub](https://github.com/yishenggaogg/adjoint_education) &middot; [Gitee](https://gitee.com/gaoyishenggg/adjoint_education) &mdash; identical content.

Chinese text: see the **中文** block at the end of this page.

## Pages

Eight model problems &mdash; 1-D Burgers, 2-D scalar advection, 2-D advection&ndash;diffusion, quasi-1-D Euler, 1-D laminar Navier&ndash;Stokes, 2-D Euler, 2-D laminar Navier&ndash;Stokes and 2-D RANS&ndash;SA &mdash; each in a cell-centred and a node-centred version (2-D RANS&ndash;SA also as an adjoint-consistent pair), plus a cell-centred and a node-centred page for 1-D viscous Burgers. If the discrete adjoint is new to you, start with the 1-D Burgers pair.

| 文件 / File | 算例 / Problem | 格式 / Scheme | 大小 / Size |
|---|---|---|---|
| [`adjoint_1d_cell.html`](adjoint_1d_cell.html) | 一维 Burgers/ 1-D Burgers | **格心** / cell-centred | 2704 KB |
| [`adjoint_1d_node.html`](adjoint_1d_node.html) | 一维 Burgers/ 1-D Burgers | **格点** / node-centred | 2765 KB |
| [`adjoint_cell.html`](adjoint_cell.html) | 二维对流 / 2-D advection | **格心** / cell-centred | 2578 KB |
| [`adjoint_node.html`](adjoint_node.html) | 二维对流 / 2-D advection | **格点** / node-centred | 2835 KB |
| [`adjoint_ad_cell.html`](adjoint_ad_cell.html) | 二维对流扩散 / 2-D advection–diffusion | **格心** / cell-centred | 2346 KB |
| [`adjoint_ad_node.html`](adjoint_ad_node.html) | 二维对流扩散 / 2-D advection–diffusion | **格点** / node-centred | 2622 KB |
| [`adjoint_q1d_cell.html`](adjoint_q1d_cell.html) | 拟一维 Euler / quasi-1-D Euler | **格心** / cell-centred | 2314 KB |
| [`adjoint_q1d_node.html`](adjoint_q1d_node.html) | 拟一维 Euler / quasi-1-D Euler | **格点** / node-centred | 2342 KB |
| [`adjoint_euler_cell.html`](adjoint_euler_cell.html) | 二维 Euler / 2-D Euler | **格心** / cell-centred | 2510 KB |
| [`adjoint_euler_node.html`](adjoint_euler_node.html) | 二维 Euler / 2-D Euler | **格点** / node-centred | 2641 KB |
| [`adjoint_ns1d_cell.html`](adjoint_ns1d_cell.html) | 一维层流 N–S / 1-D laminar N–S | **格心** / cell-centred | 1570 KB |
| [`adjoint_ns1d_node.html`](adjoint_ns1d_node.html) | 一维层流 N–S / 1-D laminar N–S | **格点** / node-centred | 1558 KB |
| [`adjoint_ns2d_cell.html`](adjoint_ns2d_cell.html) | 二维层流 N–S / 2-D laminar N–S | **格心** / cell-centred | 4367 KB |
| [`adjoint_ns2d_node.html`](adjoint_ns2d_node.html) | 二维层流 N–S / 2-D laminar N–S | **格点** / node-centred | 4637 KB |
| [`adjoint_rans_cell.html`](adjoint_rans_cell.html) | 二维 RANS–SA / 2-D RANS–SA | **格心** / cell-centred | 1480 KB |
| [`adjoint_rans_node.html`](adjoint_rans_node.html) | 二维 RANS–SA / 2-D RANS–SA | **格点** / node-centred | 1507 KB |
| [`adjoint_rans_dc_cell.html`](adjoint_rans_dc_cell.html) | 二维 RANS–SA，伴随一致 / 2-D RANS–SA, adjoint-consistent | **格心** / cell-centred | 1478 KB |
| [`adjoint_rans_dc_node.html`](adjoint_rans_dc_node.html) | 二维 RANS–SA，伴随一致 / 2-D RANS–SA, adjoint-consistent | **格点** / node-centred | 1511 KB |
| [`adjoint_burgers_viscous_cell.html`](adjoint_burgers_viscous_cell.html) | 一维黏性 Burgers（独立页）/ 1-D viscous Burgers (independent page) | **格心** / cell-centred | 6192 KB |
| [`adjoint_burgers_viscous_node.html`](adjoint_burgers_viscous_node.html) | 一维黏性 Burgers（独立页）/ 1-D viscous Burgers (independent page) | **格点** / node-centred | 9490 KB |

Each page is one HTML file: open it in a browser &mdash; no network, no build step, no server.

## What the pages do

- **One lesson on every page.** The equation and what it is for, the mesh, the flux on a face; then the same loop written as the primal, as a matrix-free tangent ($Av$) and as a matrix-free adjoint ($A^{\mathsf T}w$); the forward and adjoint solves; design and geometric derivatives; and a term-by-term check against finite differences and the complex step. Each page opens with a roadmap from the design inputs to the gradient.
- **Interactive.** Meshes, face fluxes, statement-by-statement players for the primal, tangent and adjoint, dot-product tests, solver residuals, step-size sweeps and refinement studies run in the browser. Nothing plays by itself, and under the system's reduced-motion setting the Play button is disabled with a short note.
- **Measured, not quoted.** Every number on the pages comes from an actual computation: live in the browser, or offline results that were solved independently and embedded in the page.

## Python

[`python/burgers_viscous/`](python/burgers_viscous/README.md) holds the sparse Python solver, the gradient checks and the measured data behind the viscous Burgers pages (run up to 65,536 cells; the node-centred scheme is in `node/`).

## Formal proofs

The current positive, shock-free 1D mathematical case is formally complete within the stated solution classes and certificate assumptions. The unified Lean audit covers 5210 theorem roots in 597 modules; concrete JavaScript/binary64 execution is not certified.

The dated status notes behind this statement (in Chinese) are in the **中文** block at the end of this page. Their links point to the proof workspace (`docs/`), which is kept outside this repository and is not published here.

## Keeping the two repositories in sync

GitHub is primary (the site is served by GitHub Pages from it and redeploys on every push); Gitee is a mirror. Configure `origin` to push to both, so one `git push` updates both:

```bash
git remote set-url --add --push origin https://github.com/yishenggaogg/adjoint_education.git
git remote set-url --add --push origin git@gitee.com:gaoyishenggg/adjoint_education.git
```

The first line replaces the default push URL and the second appends, so both are needed. Compare the two sides with `git ls-remote <url> refs/heads/main`. If the SHAs differ (a file was edited in a web UI), rebase the other side's commits in first (`git pull gitee main --rebase`, or `github`) and push again; **never use `--force`**, it would discard what was committed through the web UI.

## License

&copy; 2026 Yisheng Gao

The pages of this repository, the continuous-adjoint derivations and this README are licensed under a **Creative Commons Attribution 4.0 International License (CC BY 4.0)**. You are free to share and adapt the material, including for commercial purposes, so long as you give appropriate credit, provide a link to the licence, and indicate if changes were made. Full terms in [`LICENSE`](LICENSE). <https://creativecommons.org/licenses/by/4.0/>

Suggested attribution:

> Yisheng Gao，《非结构网格格心／格点格式的二维标量方程离散伴随》，CC BY 4.0，
> <https://github.com/yishenggaogg/adjoint_education>

<details>
<summary><b>中文</b></summary>

## 离散伴随教学页

二十个自包含、可交互的网页，把有限体积法的**全离散伴随**从头到尾讲一遍，面向学过微积分、线性代数与数值方法的本科生。教学主线最终走向工业级非结构网格 RANS 的完整离散伴随：二维 RANS–SA 的页面已经上线（教学网格上完整的离散伴随，并对照伴随不一致与伴随一致两种来流处理），工业级规模仍待推进。连续伴随只作为简单算例的独立验证和对比（各页附录 A）；可以为选定的连续 RANS 模型写出形式伴随，但不能把它自动当作含湍流闭合、壁面处理、限幅与边界算法的完整工业离散流程的严格参照。

**在线阅读：** <https://yishenggaogg.github.io/adjoint_education/>，默认英文，每页顶部可切换中文 / English。

**仓库：** [GitHub](https://github.com/yishenggaogg/adjoint_education) · [Gitee](https://gitee.com/gaoyishenggg/adjoint_education)，内容相同。

### 页面

八组算例——一维 Burgers、二维标量对流、二维标量对流扩散、拟一维 Euler、一维层流 Navier–Stokes、二维 Euler、二维层流 Navier–Stokes 与二维 RANS–SA——各有格心与格点两版（二维 RANS–SA 另有伴随一致的一对），另有两个独立的黏性 Burgers 页（格心与格点）。第一次接触离散伴随，请从一维 Burgers 那一对读起。页面表格见上方（文件、算例、格式与大小的列同时标有中英文）。每页都是单个 HTML 文件：不联网、不需要构建、不需要服务器，直接用浏览器打开即可。

### 各页做什么

- **每页同一条主线。**方程与它的作用、网格、面上的通量；再把同一个循环依次写成 primal、matrix-free 前向（$Av$）与 matrix-free 伴随（$A^{\mathsf T}w$）；前向与伴随求解；设计变量与几何导数；最后用有限差分与复数步长逐项校验。每页开头有一幅从设计输入到梯度的路线图。
- **可以动手。**网格、面通量、primal／tangent／adjoint 逐句播放器、点积测试、求解残差、步长扫描与加密实验都在浏览器里运行；任何内容都不会自动播放，系统设置为“减少动态效果”时播放键停用并附一句说明。
- **数字都是实测的。**页面上的每个数字都来自实际计算：浏览器现场计算，或独立求解后内嵌的离线结果。

### Python

[`python/burgers_viscous/`](python/burgers_viscous/README.md)：黏性 Burgers 两页背后的稀疏 Python 程序、梯度检查与实测数据（已实跑到 65,536 个单元；格点格式在 `node/`）。

### 数学证明进展

本节的链接指向证明工作区 `docs/`；它保存在本仓库之外，没有在这里发布。

**一维算例的 Lean 数学证明已完成：** [统一形式化入口与范围](docs/burgers1d_convergence/formal_case/README.md)覆盖当前无激波正值 Burgers 算例的一阶／二阶、格心／完整格点和现有两种入口：容许根存在唯一性、物理状态收敛、连续／离散伴随梯度一致性、FD／CS，以及任意固定有限阶混合变分的实际残差到 PDE 极限。求解停止误差与残差求值误差分别保留，不依赖求解算法。[统一审计](docs/burgers1d_convergence/formal_case/verification_result.json)通过 **5210 条定理、597 个模块**，只含 Lean 标准基础公理。二阶格点迎风伴随仍有入口层；其正确结论包括有限 Lp 收敛与梯度一致，而非全域一致收敛。具体 binary64 程序执行认证不在这次数学完成声明内。

<!-- muscl-convex-current-start -->
**二阶真实状态差的整体收缩与前向剖面收敛（2026-09-29）：** [94 条定理、16 个模块](docs/burgers1d_shocks/adjoint_muscl_convex/README.md)全部开发编译和传递公理预检通过，555 项目源码闭包与冻结父链一致；已冻结并启动 555 项目模块的空目录独立审计，尚未宣称独立通过。完整选择配置的凸性保留相同权重在重复位置的相关性；实际两阶段系数误差、出口储能、左右尾部与核心矩阵合并，得到两个原时间层之差的全能量每步收缩因子 999/1000，无残余 forcing。原前向轨道相对第 33 层在整个无限格点 l1 中 Cauchy，整条时间序列收敛到同一个 primalProfile，并有显式几何误差、可求和绝对误差、单调／区间／奇对称／尾部界以及原 RK primal 不动点方程。该唯一性仅指这条原轨道的极限，不是所有不动点唯一。

后续 [16 条核心算子极限定理](docs/burgers1d_shocks/pending_muscl_equilibrium/README.md)已开发编译通过：原两个真实阶段的 25×33 核心矩阵、投影自由矩阵和质量方向趋于由同一个前向剖面决定的极限，保留原误差半径。固定任意输入的一步核心输出也有极限；不是全空间 selected tangent 算子收敛。

**仍未闭合：** 远场 limiter 切换／平局控制、完整切向长期响应、二次平台跨子列唯一性、全域伴随强极限与完整场、原源及左右边界、含终端的整段强迹。一般耗散移动激波、其余非中心相位、稀疏波和更广浮点认证仍在完整目标中。[当前恢复入口](docs/burgers1d_shocks/pending_muscl_convex/NEXT.md)。
<!-- muscl-convex-current-end -->

<!-- muscl-secant-current-start -->
**二阶非线性状态差分与核心耗散（2026-09-29）：** [67 条定理、9 个模块](docs/burgers1d_shocks/adjoint_muscl_secant/README.md)已独立审计通过：539 项目模块全部空目录重新编译，2542.75 秒，实际会话 99237 退出码 0，零项目产物复用；标准公理、递归冻结内容与两页原源码嵌入已复核。原 minmod 有限差分的凸割线、两个真实 Euler 阶段的矩阵表示和零核心质量耗散均已证明。本 67 条包仍保留尾部二次型，后续整体尾部与前向收敛由下述 94 条新包处理。二次平台唯一性仍未证明。[恢复入口](docs/burgers1d_shocks/pending_muscl_secant/NEXT.md)。

**浮点完成状态已更新：** 指定 n=243 算例的完整初始化、27 步前向、目标、切向、反传及最终梯度总审计已经通过：13,519 条定理／1,285 项目模块／19745.20 秒／实际退出码 0，标准公理、冻结内容、获证结果序列化及原 JS 全存储值比较均通过。最终位模式 `3fd950333be6ef16`。这不覆盖任意输入、一般 JS 语言语义精化或浮点网格渐近；下文旧阶段的“完整浮点仍运行”以本段及成功报告为准。
<!-- muscl-secant-current-end -->

<!-- muscl-incoming-current-start -->
**二阶完整响应与含初始时刻的局部极限（2026-09-29）：** [140 条新定理、21 个模块](docs/burgers1d_shocks/adjoint_muscl_incoming/README.md)已独立审计通过：563 个项目模块全部空目录重新编译，2637.28 秒，实际退出码 0，零项目产物复用；逐条标准公理、递归冻结内容及两页原运行时嵌入复核通过。此前 92 条前沿外传播包已独立通过：491 项目模块／2414.28 秒／实际退出码 0，公理、递归冻结内容及两页源码嵌入复核通过。

新证明保留任意前沿外输入进入内部后产生的全部响应，用增广能量吸收外部 forcing，质量项保留为显式常数底。固定有限支撑零质量输入的完整 l1 响应衰减；当剩余步数足够于支撑半径时，位置随网格变化的脉冲也满足统一混合，不再假设种子位于当前前沿内。固定 33 步的原局部范数界与零质量分解把结果延伸到所有起始层，包括第 0 层，并接回实际有限两阶段及完整转置循环。

对固定原实数参数 `L=1,R=-1,a=1/2,alpha=6/5,T=7/216,n=9(2m+1)`，令 `rho(B)=(T-B)/10000`。原场在 **`0<=t<=B<T, |x-1/2|<=rho(B)`** 上与同一个 t=T/2 的实际中心值之差一致趋零。同一个实际子列因此在所有这些条带上一致趋于一个常数；线性目标整族趋于 3/2，二次目标沿同一子列场／完整梯度分别趋于 c／2c，`c<=-71/2250<0`。这次包含初始时刻的正宽空间段，未将它扩张成整个初始空间层。

**仍未闭合：** 全空间统一伴随界、完整 ProductL1 紧性和全域强极限存在、二次常数的精确值与跨子列唯一性、完整二阶场及原源／边界极限、包含终端时刻的整段强迹估计；其他参数、非中心其余相位、一般耗散移动激波、稀疏波和更广浮点输入／渐近认证继续保留。140 条新包现已独立通过。[恢复入口](docs/burgers1d_shocks/pending_muscl_incoming/NEXT.md)。
<!-- muscl-incoming-current-end -->

<!-- muscl-exterior-current-start -->
**二阶前沿外传播与物理场截断（2026-09-29）：** [92 条新定理、12 个模块](docs/burgers1d_shocks/adjoint_muscl_exterior/README.md)已独立审计通过：491 个项目模块全部空目录重编译，2414.28 秒，实际退出码 0，零项目产物复用；92 条根的标准基础公理、递归冻结内容及两页原运行时嵌入复核通过。原精确实数参数仍为 `L=1,R=-1,a=1/2,alpha=6/5,T=7/216,n=9(2m+1)`，两个目标及页面原算法不变。

原 inactive limiter 在常值 primal 区域的任意 tangent 精确等于常系数 LF／RK。任意输入在第 s 层后演化 K 步，其最终前沿外输出精确等于相应常系数演化；两侧前沿外绝对质量至多为输入绝对质量的两倍。有限支撑传播半径已收紧为 `max(2s,r)+2K`，完整有限两阶段及原转置配对已连接。

对 `|i|<=2s+K` 的单位脉冲，原两侧前沿外质量至多 `2*(7/10)^K`，相应有界终端数据的完整反传贡献至多 `2B*(7/10)^K`。在 m>=1 和原步数条件下，有限网格余量自动成立。两个实际归一化目标均有 B=2；因此删除终端 primal 前沿外部分引起的物理场差，在 `0<=t<=B<T`、`|x-1/2|<=1/18` 上一致不超过 `4*(7/10)^reverseIndex(m,B)`，并随加密趋零，包含初始时刻。

**本 92 条包的范围限制：** 本包尚未控制任意前沿外输入进入前沿内部后的全部响应；辅助终端截断场的完整极限也未证明。全域统一界、完整 ProductL1 紧性与强极限存在、二次跨子列唯一性、源项与左右边界极限仍未闭合。新 92 条已独立审计通过；后续任意输入完整响应正在新开发包中继续。[当前恢复入口](docs/burgers1d_shocks/pending_muscl_exterior/NEXT.md)。
<!-- muscl-exterior-current-end -->

<!-- muscl-front-mixing-current-start -->
**二阶局部极限与平台值（2026-09-29）：** [71 条新定理、12 个模块](docs/burgers1d_shocks/adjoint_muscl_local_limits/README.md)已独立审计通过：**530 个项目模块全部空目录重编译，2633.27 秒，实际退出码 0**，零项目产物复用；71 条根的标准基础公理、递归冻结内容和页面源码映射均已复核。范围仍为原精确实数 `L=1,R=-1,a=1/2,alpha=6/5,T=7/216,n=9(2m+1)` 及两个目标，保留原 minmod 选支、两阶段、ghost、ceil／reverse floor、中点权重、位置种子和 dual/h。

新增实际非零质量能量稳定性、中央单位脉冲的统一绝对质量与一阶绝对矩界。原伴随场在每个固定内部激波条带上最终一致有界，并构造出**同一个实际加密子列**在所有这类条带上一致趋于同一常数；这项局部存在性不假设完整 ProductL1 极限存在。

**线性目标：** 原仿射终端权重精确给出中心误差 `<=h*C`，因此整族在每个固定内部条带上一致趋于 **3/2**。原初始中心值也趋于 3/2，每个给定实际强极限的左右共同迹都等于 3/2。

**二次目标：** 用一个固定零质量种子消去最初 33 步过渡，并证明原完整位置梯度精确等于初始中心场的两倍。结合已审计的梯度严格反例，同一个实际子列的条带场／完整梯度分别趋于 `c／2c`，其中 **c<=-71/2250<0**。每个给定实际强 ProductL1 极限的唯一常数共同迹也满足这个负界，不能取参考值 0；二次精确平台与跨子列一致性仍未知。

**共同常数迹父包已独立完成：** [76 条／17 模块](docs/burgers1d_shocks/adjoint_muscl_constant_trace/README.md)通过 **496 个项目模块全新编译，2393.77 秒，实际退出码 0**，零项目产物复用，逐条公理、递归冻结内容和页面嵌入复核通过。每个给定实际强极限具有构造出的可测、局部可积、唯一时间常数共同强迹；原前向全部存储层空间误差 `<=13h/10`，两目标终端空间误差 `<=31h/10`。没有从仅有 ProductL1 收敛推断端点迹。此前物理条带 80 条／479 项目模块及一般种子零质量衰减 61 条／256 项目模块保持独立通过。

**仍未闭合：** 全空间与时间端点的统一场界、完整 ProductL1 紧性与强极限存在；二次精确平台和跨子列唯一性；完整二阶场及原源／左右边界极限、整段时间强迹误差。初始中心标量收敛不等于整个初始空间层收敛。其他参数与相位、一般耗散移动激波、稀疏波和完整浮点总审计仍在完整目标中。[当前恢复入口](docs/burgers1d_shocks/pending_muscl_stability/NEXT.md)。
<!-- muscl-front-mixing-current-end -->

<!-- noncentral-current-start -->
**非中心驻定最新进展（2026-09-29）：** [原平移与实际梯度极限包](docs/burgers1d_shocks/adjoint_noncentral_cone/README.md)的 **42 条定理、8 模块已独立审计通过**：321 个项目模块全部从空目录重新编译，589.81 秒。原一阶 L=1,R=-1,a=3/10,alpha>=1,T>0,alpha*T<=1/100，n=20r+25 下，原初始 dual/h 趋于线性 13/10／二次 0，完整二次位置梯度趋于 0。

[非中心物理条带、共同迹与源密度包](docs/burgers1d_shocks/adjoint_noncentral_trace/README.md)的 **28 条定理、5 模块已独立审计通过**：298 个项目模块全部从空目录重新编译，578.84 秒，实际退出码 0。正宽物理条带上的一致平台收敛接到每个预先指定的同一实际强极限，原左右全时间共同迹为线性 13/10／二次 0，实际内部密度为 13/5／0。

[非中心完整场、整族唯一性与左右通量包](docs/burgers1d_shocks/adjoint_noncentral_field/README.md)的 **66 条定理、24 模块已独立审计通过**：357 个项目模块全部从空目录重新编译，714.25 秒，实际退出码 0。上述固定位置和网格族内，两种目标的完整场、强乘积时空 L1、整个 [0,T] 上的一致空间 L1、共同迹弱问题、一般 C2 源配对与左右真实 RK 通量分别收敛到同一个显式非中心场。公理及递归冻结内容复核通过。边界结论是测试配对收敛。

[一族非中心位置与网格相位扩展](docs/burgers1d_shocks/adjoint_aligned_stationary/README.md)的 **34 条定理、6 模块已独立审计通过**：300 个项目模块全部空目录重新编译，581.16 秒，实际退出码 0，标准基础公理和递归冻结内容复核通过。p<=q<=2p 时，a=(2p+1)/(2(2q+1))、n=(2q+1)(2r+1) 的原中点对齐及加密索引已证明；同一实际极限的全时间共同迹为线性 1+a／二次 0，内部密度为 2(1+a)／0。

[新参数族完整场与时间一致收敛](docs/burgers1d_shocks/adjoint_aligned_field/README.md)的 **38 条定理、14 模块已独立审计通过**：332 个项目模块全部从空目录重新编译，632.47 秒，实际退出码 0，零项目产物复用。逐条公理集合、递归冻结源码和原页面嵌入已复核。新参数族整族及任意加密索引的强乘积 L1、整个 [0,T] 上的一致空间 L1、实际极限唯一性及同一完整共同迹弱问题均已闭合。该新族一般 C2 整族源项及左右原边界通量的后续 **21 条定理、8 模块已独立审计通过**：374 个项目模块全部空目录重新编译，698.08 秒，实际退出码 0，零项目产物复用；逐条公理、递归冻结源码和原页面嵌入已复核。完整场、共同迹、一般源项和左右真实通量的联合证书现已在同一个原参数族闭合，边界结论为测试配对极限。a=3/10,n=20r+25 的这些配对已由上述 66 条闭合。任意非对齐相位、偶数网格、a>1/2、长时间、一般耗散移动激波、二阶完整场、稀疏波与完整浮点总审计仍未完成。
<!-- noncentral-current-end -->

<!-- stationary-amplitude-current-start -->
**任意正振幅中心驻定激波（2026-09-29）：** [振幅扩展包](docs/burgers1d_shocks/adjoint_stationary_scaling/README.md)的 **76 条定理、10 个模块已独立审计通过**：315 个项目模块全部从空目录重编译，699.49 秒，实际退出码 0，不复用项目编译产物，公理仅含 Lean 标准基础公理。精确实数原一阶 `L=c,R=-c,c>0,a=1/2,A>=max(1,c),T>0`、中心奇数 `n=2m+1,m>=4` 下，原实际场的整族强乘积时空 L1 极限、整个 `[0,T]` 上的一致空间 L1 极限、任意加密族唯一性和同一实际极限的共同强迹已闭合。线性平台 3/2、二次平台 0；每个终端前固定正宽物理条带上的平台一致收敛也已证明。保留实际 ceil、两个真实 RK 阶段、ghost、目标和完整反传。原 JS stationary 输入仍固定 1,-1，未宣称页面支持任意振幅。

[任意振幅的原源项与边界通量扩展](docs/burgers1d_shocks/adjoint_stationary_scaling_flux/README.md)的 **30 条定理、6 个模块已独立审计通过**：337 个项目模块全部从空目录重新编译，701.72 秒，不复用项目产物，逐条公理检查通过。原反应密度为线性 3c／二次 0，左右真实两阶段通量分别接到上述同一个实际场；保留 h、h(n+1) 采样和非零右状态 -c。边界结论是测试配对收敛，不声称通量点值或强 L1 收敛。[当前运行与剩余义务](docs/burgers1d_shocks/pending_stationary_scaling/NEXT.md)。其他驻定相位、一般 alpha 移动激波、二阶场及完整浮点执行等总目标保持不变。
<!-- stationary-amplitude-current-end -->

<!-- stationary-even-current-start -->
**中心偶数网格驻定进展（2026-09-29）：** 精确实数原一阶 `L=1,R=-1,a=1/2,n=2m`、每个固定 `alpha>=1,T>0` 下，[状态与局部收缩包](docs/burgers1d_shocks/adjoint_stationary_even/README.md)的 53 条定理、[边界损失与终层局部化包](docs/burgers1d_shocks/adjoint_stationary_even_kernel/README.md)的 72 条定理，以及[原完整核混合与反传包](docs/burgers1d_shocks/adjoint_stationary_even_mixing/README.md)的 23 条定理均已独立审计通过。

[实际物理场与同一个极限的共同强迹包](docs/burgers1d_shocks/adjoint_stationary_even_trace/README.md)的 **42 条定理、9 个模块已独立审计通过**：300 个项目模块全部从空目录重新编译，569.71 秒，逐条公理只含 Lean 标准基础公理。原 sourceRun、dual/h、reverse floor 和空间采样已接通；每个预先给定的实际强时空极限保持为同一个 W，其左右全时间共同强迹为 q，实际内部反应密度为 2q，原离散反应配对也接到同一密度。保留原 ceil、两个真实 RK 阶段、有限 ghost 和完整反传。

[偶数实际平台包](docs/burgers1d_shocks/adjoint_stationary_even_value/README.md)的 **48 条定理、8 个模块已独立审计通过**：325 个项目模块全部空目录重编译，613.89 秒，逐条公理只含 Lean 标准基础公理。线性平台 3/2、二次平台 0、实际内部密度 3／0已识别，并保留同一个实际强极限。两个中央种子的平均仅用于证明，原输出未修改，半格坐标及 h(R+1) 尾部误差保留。

[偶数完整场与全网格扩展](docs/burgers1d_shocks/adjoint_stationary_even_field/README.md)的 **44 条定理、17 个模块已独立审计通过**：380 个项目模块全部空目录重编译，727.81 秒，逐条公理只含 Lean 标准基础公理。偶数整族完整场、时间一致空间 L1、唯一性、一般 C2 源项及左右真实通量均接到同一个连续场；精确合并奇偶索引后覆盖中心单位振幅的全部原 n=k+8 网格及任意加密族。

[任意正振幅全网格扩展](docs/burgers1d_shocks/adjoint_stationary_all_scaling/README.md)的 **33 条定理、7 个模块已独立审计通过**：403 个项目模块全部空目录重编译，746.40 秒，实际退出码 0，零项目产物复用。原 L=c,R=-c,c>0,a=1/2,A>=max(1,c),T>0、全部原 n=k+8 网格的完整实际场、共同迹、时间一致空间 L1、密度 3c／0 和左右真实通量联合证书已闭合。成功报告、公理集合、递归冻结源码和两页原运行时嵌入已复核。非中心驻定相位、一般移动 alpha、二阶场、稀疏波及完整浮点总审计仍在总目标中。[当前运行与下一步](docs/burgers1d_shocks/pending_stationary_even/NEXT.md)。

<!-- stationary-even-current-end -->

**指定算例的完整浮点审计已通过（2026-09-29）：** 原 n=243、L=1,R=-1,a=1/2,alpha=6/5,T=7/216、驻定二阶二次目标的完整初始化、27 个前向 RK 步、目标、全部切向、倒序反传及两个最终点积已认证。13,519 条定理、1,285 个项目模块全部从空目录重新编译，零项目产物复用，19745.20 秒，实际会话 76672 退出码 0。逐条公理仅含标准基础公理，递归冻结源码与获证结果序列化均通过；与原 JavaScript 的 101,780 个存储标量位模式匹配，JVP/VJP 最终位模式均为 `3fd950333be6ef16`（约 0.3955200276356988）。这是一个完整成功输入的算术程序证书及原运行时逐项比对，不是任意输入、一般 JavaScript 语言语义精化、浮点网格渐近或 limiter 折点经典导数的证明。 [成功报告](docs/burgers1d_shocks/adjoint_binary64_full/full_verification_result.json)。

<!-- binary64-program-current-start -->
**浮点完整程序与首步证书（2026-09-29）：** [新程序包](docs/burgers1d_shocks/adjoint_binary64_program/README.md)的 **58 条定理、28 个模块已独立审计通过**：55 个项目模块全部从隔离空目录重新编译，耗时 561.40 秒，不复用项目编译产物；逐条公理仅含 Lean 标准基础公理。证明包含正负零、正规／进位／次正规舍入检查器、请求轨迹和数组组合，以及原 n=243、驻定二阶、T=7/216、alpha=6/5、二次目标的输入／初值和**第一个完整 RK 步**。两个真实阶段、半步混合与守恒误差均已接通，对任何符合算术合同的实现得到相同首步结果和获证轨迹。

同一程序的全 27 步精确有理数执行接受 722,516 次算术请求，与未修改 JavaScript 的全部存储结果共 101,780 个标量位模式匹配；最终反传观测仍为 `3fd950333be6ef16`。**完整执行比较是观察，尚不是最终梯度的内核证书。** 剩余 26 步、全部切向／反传与最终梯度的内核认证及更广参数范围仍须继续；一般 alpha 移动激波与二阶场极限目标保持不变。
<!-- binary64-program-current-end -->

<!-- stationary-current-start -->
**中心驻定激波的平台与完整场进展（2026-09-29）：** [实际平台值包](docs/burgers1d_shocks/adjoint_stationary_value/README.md)的 **41 条定理、8 个模块**已独立审计通过：289 个项目模块全新编译，522.66 秒，无项目缓存复用，公理仅含 Lean 标准基础公理。精确实数原一阶 `L=1,R=-1,a=1/2,n=2m+1`、每个固定 `alpha>=1,T>0`，已识别同一个实际极限的全时间共同迹：线性 **q=3/2**、二次 **q=0**，原内部密度分别为 **3、0**。原物理场在每个终端前固定正宽条带上一致趋于相应平台。

[完整场包](docs/burgers1d_shocks/adjoint_stationary_field/README.md)的 **47 条定理、16 个模块**也已独立审计通过：306 个项目模块全新编译，566.19 秒。两目标的每个实际强极限均被识别为同一原 `BurgersSpatial.field`，整条中心奇数网格序列及任意加密族强时空 L1 收敛、极限唯一，并在整个 `[0,T]` 上以空间 L1 范数一致收敛。显式极限不依赖固定 alpha，但不声称网格阈值统一于所有 alpha。

原反应项和左右实际边界通量的[后续包](docs/burgers1d_shocks/adjoint_stationary_boundary/README.md) **52 条定理、15 个模块已独立审计通过**：321 个项目模块全部从空目录全新编译，595.15 秒，公理仅含 Lean 标准基础公理。一般紧支撑 C2 测试的整族密度极限、原两阶段左右通量到同一实际场的分别测试配对极限均已接通；保留 h、h(n+1) 取样及右状态 -1。不声称通量点值或强 L1 收敛。[后续审计与剩余义务](docs/burgers1d_shocks/pending_stationary_boundary/NEXT.md)。其他网格相位／振幅、一般 alpha 移动激波、二阶伴随场、完整浮点执行和恢复一般参考一致性的格式改造证明仍未完成。以下驻定历史段落的“平台待识别”已被 41 条平台值包推进；其他历史待办以本段及当前问题表为准。
<!-- stationary-current-end -->

**一般耗散参数的中心驻定激波共同强迹已独立审计通过（2026-09-29）：** [70 条混合／实际场定理](docs/burgers1d_shocks/adjoint_stationary_mixing/README.md)与[19 条同极限共同迹／密度定理](docs/burgers1d_shocks/adjoint_stationary_trace/README.md)均已通过独立审计。前包 113 个项目模块全新编译、188.92 秒；后包 281 个项目模块全新编译、507.94 秒，均不复用项目编译产物，逐条公理仅含 Lean 标准基础公理。原 `L=1,R=−1,a=1/2,n=2m+1`、每个固定 `α≥1,T>0`，已证明原双种子全时间后缀混合、两目标 `dual/h` 及实际物理场的固定条带振荡消失。对任意中心奇数加密族的每个预先给定强时空极限 W，同一个 W 的代表具有左右全时间共同强迹 q，原实际内部反应密度为 **2q**，原离散反应测试配对接到同一密度。保留原 ceil、两个真实 RK 阶段、有限边界及原场，没有更换数值极限。**驻定 q 的具体值／时间常数、完整场唯一性和驻定边界通量逐项极限尚未识别**；偶数网格、非中心相位／其他振幅、一般 α 移动激波、二阶场及完整浮点执行仍开放。[后续平台与完整场义务](docs/burgers1d_shocks/pending_stationary_trace/NEXT.md)。

**一般测试反应项已闭合（2026-09-29）：** [25 条新定理、8 个模块](docs/burgers1d_shocks/adjoint_general_flux/README.md)已通过[独立审计](docs/burgers1d_shocks/adjoint_general_flux/verification_result.json)：386 个项目模块，337 个全新编译、49 个固定已审计整数产物复用，耗时 648.86 秒。原一阶移动激波 L=1、R=0、α=6/5、固定 0<T≤1/4、a∈[1/5,3/5] 范围内，两种目标的同一实际证书，对允许接触空间边界和时间端点的紧支撑 C² 测试，原反应项均收敛到实际常数迹 d 的沿线配对。线性目标覆盖全网格及任意加密族，密度为 1+a+T/2。原两阶段源项、跳跃矩和 ceil 保留，二次 d 未被指定为参考值。

**两种目标的实际场端点与左右边界通量已闭合（2026-09-29）：** [19 条新定理、6 个模块](docs/burgers1d_shocks/adjoint_actual_boundary/README.md)已通过[独立审计](docs/burgers1d_shocks/adjoint_actual_boundary/verification_result.json)：416 个项目模块，367 个全新编译、49 个固定已审计整数产物复用，耗时 714.40 秒。在原一阶移动激波 `L=1,R=0,α=6/5,0<T≤1/4,a∈[1/5,3/5]` 范围，对线性与二次目标的每个预先给定原收敛证书，同一个实际常数 d 决定完整场、整个 `[0,T]` 的空间 L¹ 时间代表及其子列时间一致收敛。原左右真实两阶段边界通量，对任意紧支撑 C² 测试分别收敛到同一实际场的左端物理通量配对和右端零通量。保留原采样位置 h、h(n+1)，不假定边界单元逐点收敛，也不声称通量点值或强 L¹ 收敛。二次 d 未被替换为参考值；下述固定相位包进一步完成其声明网格族的平台识别与完整场唯一性。

**线性边界通量包的审计已通过：** [30 条定理、7 个模块](docs/burgers1d_shocks/adjoint_boundary_flux/README.md)的[独立审计](docs/burgers1d_shocks/adjoint_boundary_flux/verification_result.json)已完成，覆盖 410 个项目模块（361 个全新编译、49 个固定已审计整数产物复用），耗时 703.38 秒。线性目标覆盖全网格及任意加密族；其后的上述 19 条定理完成两种目标沿各自实际证书子列的逐项边界识别。下列历史阶段的相关边界待办以本段和上段为准。

**两个固定相位族的平台与完整极限已闭合（2026-09-29）：** [53 条定理、14 个模块](docs/burgers1d_shocks/adjoint_phase_limit/README.md)已通过[独立审计](docs/burgers1d_shocks/adjoint_phase_limit/verification_result.json)：509 个项目模块，460 个全新编译、49 个固定已审计整数产物复用，耗时 922.10 秒。固定 `L=1,R=0,α=6/5,a=13/40,T=7/2400`，原 `n=100(48m+1)` 与 `n=100(48m+5)` 两族的实际共同迹分别精确刻画为 `d₊=6367/9600+(6367/4800)e₁`、`d₋=6367/9600+(6367/4800)e₅`，其中 e 是实际无限轨道的唯一能量极限。每族完整梯度、强时空 L¹ 场、闭时间区间上一致空间 L¹ 场、原反应密度及左右真实两阶段边界通量测试配对均收敛到由同一个 d 决定的极限。`d₊−d₋>6×10⁻¹¹`，故相位内唯一性成立，跨相位非唯一性与参考源密度不一致的严格反例继续成立。该精确刻画不是有理数闭式，也未给出未经认证的小数值。

**所有奇数偏移族的完整极限扩展已独立审计通过（2026-09-29）：** [40 条定理、12 个模块](docs/burgers1d_shocks/adjoint_phase_offsets/README.md)已通过[独立审计](docs/burgers1d_shocks/adjoint_phase_offsets/verification_result.json)：520 个项目模块，471 个全新编译、49 个固定已审计整数产物复用，耗时 938.25 秒。固定上述物理参数，对每个固定自然数 r 的原网格族 `n=100(48m+2r+1)`，已证明实际平台 `d_r=6367/9600+(6367/4800)e_(2r+1)`、整族完整梯度／强时空 L¹ 场／时间一致空间 L¹ 场极限、原源项及左右边界通量测试配对极限。平台满足 `d_(r+24)=d_r`，归约到 24 个余类；不声称这些平台两两不同。相位内唯一性已闭合，偶数偏移、其他初相位及其他物理参数仍未分类。所有新定理只依赖 Lean 标准基础公理，原运行时与两页精确嵌入保持不变。

**原浮点平局舍入接口与 ghost ca 运算已独立审计通过（2026-09-29）：** [32 条定理、6 个模块](docs/burgers1d_shocks/adjoint_binary64_rounding/README.md)通过[独立审计](docs/burgers1d_shocks/adjoint_binary64_rounding/verification_result.json)：27 个项目模块全部从隔离空目录全新编译，45.81 秒，公理仅含 Lean 标准基础公理。已证明规范 binary64 表示／奇偶性唯一、NearestEven 输出唯一、正规相邻区间（含平局）、2 的幂下方进位平局及负数反射。原 ghost `ca[0]=L/2+alpha/2` 在 L=1、alpha=1.2 时确实是半 ulp 平局，其 round-to-even 结果位模式为 `3ff199999999999a`；原运行时 24 组运行、464 个真实 RK 阶段核对一致。还严格证明旧的 UniqueNearest 合同允许此原表达式算错，故完整运行必须补入平局规则。新合同额外要求输入绝对值不超过 2^1023，避免约束溢出行为。**这只认证该表达式与通用舍入引理，完整 RK／limiter／反传及最终梯度、全部次正规与正负零位语义仍未认证。** [下一步完整运行义务](docs/burgers1d_shocks/pending_binary64_full/NEXT.md)。

**原浮点时钟与精确实数时钟的差异已认证：** [16 条定理、2 个模块](docs/burgers1d_shocks/adjoint_binary64_clock/README.md)已通过[独立审计](docs/burgers1d_shocks/adjoint_binary64_clock/verification_result.json)，23 个项目模块全部从隔离目录全新编译，耗时 42.76 秒。原 `n=100,T=7/2400,α=6/5` 中，八次相关 binary64 舍入逐项认证后得到原 ceil 步数为 2，既有精确实数模型步数为 1；原 JavaScript 位模式全部匹配。该结果只认证初始化时钟，尚未认证完整 RK／limiter／反传执行。[完整浮点运行的后续义务及观测](docs/burgers1d_shocks/pending_binary64_full/NEXT.md)单独保存，运行观测不计为形式化证明。

**驻定原核的边界损失与共同终层局部化已独立审计通过（2026-09-29）：** [91 条定理、12 个模块](docs/burgers1d_shocks/adjoint_stationary_kernel/README.md)已通过[独立审计](docs/burgers1d_shocks/adjoint_stationary_kernel/verification_result.json)：50 个项目模块全部从隔离空目录全新编译，不复用项目编译产物，耗时 93.26 秒。新定理的传递公理仅含 Lean 标准基础公理，原运行时与两页精确嵌入保持不变。对同一 `L=1,R=−1,a=1/2,n=2m+1`、每个固定 `α≥1,T>0`，已接通完整原 RK 矩阵与实际后缀、随 α 变化的指数矩收缩、累计截边损失及原／guarded 分布距离。原 ceil 的线性网格步数上界使边界误差在所有实际后缀和固定物理中心条带种子间一致趋零。对于 `K≥τm`、`|j−(m+1)|≤dτm/4`（`d=7/(80α²),0<τ≤1`），原分布在同一个终层的中心窗口外质量一致可小，窗口半径可在网格加密前固定。该阶段之后，顶部 70+19 条定理已在同一中心奇数范围完成全时间混合及同一个实际极限的共同强迹；本段仅记录当时的边界／局部化阶段。[当前后续义务](docs/burgers1d_shocks/pending_stationary_mixing/NEXT.md)已更新。

**一般耗散参数的驻定状态界与局部伴随核收缩已独立审计通过（2026-09-29）：** [64 条定理、9 个模块](docs/burgers1d_shocks/adjoint_stationary_reference/README.md)已通过[独立审计](docs/burgers1d_shocks/adjoint_stationary_reference/verification_result.json)：38 个项目模块全部从隔离空目录全新编译，没有复用项目编译产物，耗时 71.92 秒。全部新定理的传递公理仅含 Lean 标准基础公理。原 `L=1,R=−1,a=1/2,n=2m+1`、每个固定 `α≥1,T>0` 下，已证明原有限网格和两个真实 Euler 阶段的统一状态剖面／几何尾界、完整 RK 内部列的向内漂移 `>7/(80α²)`，以及距中心不超过 w 格的种子在 w 步后的共同中心质量 `≥(91/3200)^w` 与分布距离 `≤2(1−(91/3200)^w)`。包括 `α=1`，保留原 ceil 和边界质量损失；“至少 2 步”在充分细奇数网格上自动成立。该阶段本身仅给局部收缩；顶部 70+19 条定理已通过多块混合和同一二维极限传递，在同一中心奇数范围补齐共同强迹。[后续证明义务](docs/burgers1d_shocks/pending_stationary_mixing/NEXT.md)已列出。

**完整实际场与线性目标全网格收敛已闭合（2026-09-29）：** [41 条新定理、13 个模块](docs/burgers1d_shocks/adjoint_general_field/README.md)已通过[独立审计](docs/burgers1d_shocks/adjoint_general_field/verification_result.json)：392 个项目模块，343 个从隔离目录全新编译、49 个固定已审计整数产物复用，耗时 673.91 秒。在原一阶移动激波 `L=1,R=0,α=6/5,0<T≤1/4,a∈[1/5,3/5]` 范围，两种目标的每个实际强子列极限均被识别为同一个原 `BurgersSpatial.field` 中由实际常数迹 d 决定的完整时空场。终端配对通过同一个时间连续空间 L¹ 代表延伸，任意测试分离、完整标签覆盖和保测度坐标完成全域拼接。线性目标 d=1+a+T/2，因此原全网格及任意加密族均强时空 L¹ 收敛到指定参考场，极限唯一。实际场等价类有满足实际源系数 d 的完整连续共同迹弱问题的规范代表；线性目标即参考源。**原离散边界通量的逐项连续极限仍未识别；不能用规范代表的边界点值代替这个证明。二次 d 的精确识别和相位内唯一性仍待完成，已有跨相位反例保持有效。** 原运行时和两页精确嵌入复核不变。

**时间一致连接已独立审计通过（2026-09-29）：** [13 条新定理、5 个模块](docs/burgers1d_shocks/adjoint_general_time/README.md)已通过[独立审计](docs/burgers1d_shocks/adjoint_general_time/verification_result.json)：395 个项目模块，346 个从隔离目录全新编译、49 个固定已审计整数产物复用，耗时 654.94 秒，逐条公理仅含 Lean 标准基础公理。时空类相同的实际证书，其时间连续空间 L¹ 代表在整个 [0,T] 相同；线性参考场的精确 min/max 公式给出 L¹ 时间变化界，由此识别所有时间切片，并证明原全网格及任意加密族在 [0,T] 上以空间 L¹ 范数一致收敛到指定参考场，包含初始和终端时刻。范围仍为固定允许 T、a 下的原一阶移动激波 L=1、R=0、α=6/5，不声称网格阈值统一于全部参数。这 13 条接续上述 41 条完整场定理；原离散边界通量逐项极限仍未完成。

**线性目标的实际平台值与参考源密度已闭合（2026-09-28）：** [21 条新定理、7 个模块](docs/burgers1d_shocks/adjoint_general_linear/README.md)已通过[独立审计](docs/burgers1d_shocks/adjoint_general_linear/verification_result.json)：378 个项目模块，329 个从隔离目录全新编译、49 个固定已审计整数产物复用，耗时 634.51 秒。范围为原一阶移动激波 `L=1,R=0,α=6/5,0<T≤1/4,a∈[1/5,3/5]` 的线性目标、全部原网格相位。原核终层尾部与质量保留、真实仿射终端数组及完整转置配对给出实际 `dual/h` 在每个 `0≤t≤B<T, |x−X(t)|≤7(T−B)/5120` 条带上一致趋于 `1+a+T/2`，阈值统一于全部允许 a、t、x。每个预先给定的实际强子列极限的左右完整强迹和实际内部源密度均被识别为这个参考常数，原离散反应配对沿同一证书子列收敛到相应密度配对。没有更换数值极限，也没有从缩小单元的样本值直接推出场或迹的值。**线性平台值现已识别；完整空间场、连续边界与全场唯一性仍待连接。二次目标的实际平台值及相位内唯一性仍未识别，其已有双相位反例保持有效。** [后续完整场义务](docs/burgers1d_shocks/pending_general_linear/NEXT.md)单独列出。

**同一个原极限的恒定激波平台已闭合（2026-09-28）：** [24 条新定理、6 个模块](docs/burgers1d_shocks/adjoint_general_plateau/README.md)已通过[独立审计](docs/burgers1d_shocks/adjoint_general_plateau/verification_result.json)：371 个项目模块，322 个从隔离目录全新编译、49 个固定已审计整数产物复用，耗时 623.45 秒。范围为原一阶移动激波 `L=1,R=0,α=6/5,0<T≤1/4,a∈[1/5,3/5]`，两种目标及全部原网格相位。对每个实际强子列极限，存在常数 d，使同一个左右全时间强迹 q=d 几乎处处，实际反应密度也为 d，原离散反应配对收敛到该密度配对。每个 `0<A<B<T` 内，激波两侧半宽 `0<δ<7(T−B)/5120` 的实际场也等于 d 几乎处处。证明由原空间振荡消失、强迹身份、右侧真实特征剖面以及连通区间上的可数拼接得到，没有预设 d 的参考值。**本阶段只证明时间常数；后续线性包已识别线性目标 d=1+a+T/2。二次目标 d 的精确值、相位内唯一性及完整实际连续边界仍未识别。** 所有这些结论采用精确实数语义。

**原全时间共同迹与实际单一密度已闭合：** [11 条新定理、3 个模块](docs/burgers1d_shocks/adjoint_general_density/README.md)已通过[独立审计](docs/burgers1d_shocks/adjoint_general_density/verification_result.json)：365 个项目模块（316 个全新编译、49 个固定已审计产物复用），耗时 609.85 秒。它接续下述 27 条全网格共同迹定理，证明默认移动激波的原左右迹几乎处处相等、同一个 q 具有左右完整 `[0,T]` 条带极限，并且原实际密度 ρ=q。内部弱平衡及原离散反应配对极限均使用这个 q；每个预先给定的原强子列极限都具有这些性质。实际 q 未被指定为参考平台，既有双相位非唯一反例保持有效；其余范围见[状态索引](docs/burgers1d_shocks/adjoint_connection_status.md)。

**默认一阶移动激波的全网格共同强迹已闭合：** [27 条新定理、5 个模块](docs/burgers1d_shocks/adjoint_general_trace/README.md)已通过[独立审计](docs/burgers1d_shocks/adjoint_general_trace/verification_result.json)：361 个项目模块，312 个从隔离目录全新编译、49 个哈希固定的已审计整数产物复用，耗时 598.77 秒。对 `L=1,R=0,α=6/5,0<T≤1/4,a∈[1/5,3/5]`，原时间取样与空间重构已将全相位离散混合传到同一个二维强极限，得到原共同强迹；两种目标、全部原网格相位和任意严格递增网格族均覆盖。同一证书保留正确终端、特征剖面、全时间单侧迹与实际反应密度。一般 α、驻定激波、实际迹值和相位内唯一性、完整连续边界、二阶场、稀疏波及完整浮点执行仍未完成；已有严格反例继续否定一般二次参考一致性及全网格唯一性。后续 11 条共同密度定理也已独立审计通过，见上段。下文保留历史阶段记录，当前义务见[状态索引](docs/burgers1d_shocks/adjoint_connection_status.md)。

**默认一阶移动激波的全相位原反向混合：** [63 条 Lean 定理、11 个模块](docs/burgers1d_shocks/adjoint_general_mixing/README.md)已通过[独立审计](docs/burgers1d_shocks/adjoint_general_mixing/verification_result.json)：194 个项目模块（145 个全新编译、49 个固定已审计产物复用），耗时 289.04 秒。指定同层尾部、移动窗口共同质量及有符号多块收缩已接到原有限 RK 核，边界缺陷明确保留。在步数不少于固定正数乘 n 的原时间区间内，对固定物理激波邻域，任意两个原种子的分布差一致趋零，覆盖默认 α 的移动激波全部允许初相位。已连接任意有界终端数组的原 reverseLayer，以及页面两种目标的实际 dual/h。下一步是同一个二维强极限的共同强迹传递；一般参数、驻定激波、二阶场及完整浮点执行仍未完成，见[当前状态索引](docs/burgers1d_shocks/adjoint_connection_status.md)。

**原完整 RK 定量回返与累计边界损失已闭合：** [81 条 Lean 定理、12 个模块](docs/burgers1d_shocks/adjoint_general_return/README.md)已通过[独立审计](docs/burgers1d_shocks/adjoint_general_return/verification_result.json)，覆盖 132 个项目模块（83 个全新编译、49 个固定已审计整数产物复用），耗时 188.70 秒。对默认一阶移动激波 `L=1,R=0,α=6/5`、固定 `0<T≤1/4`、全部页面初始位置及所有原网格相位，固定物理条带内的单位种子在具有线性于 n 步数的原时间窗内，曾回到激波窗口且未被边界停止过程丢弃的质量一致趋于 1。原 ceil、真实两阶段和有限边界均保留。这尚未证明终层窗口占有率、全时间反向混合或一般共同强迹。下列旧阶段的回返／边界损失待办在上述范围内已补齐，当前剩余问题以[统一状态索引](docs/burgers1d_shocks/adjoint_connection_status.md)为准。

**原完整 RK 向内漂移阶段：** [15 条 Lean 定理](docs/burgers1d_shocks/adjoint_general_drift/README.md)已独立审计通过，120 个项目模块（71 个全新编译、49 个固定已审计整数产物复用）。对默认移动激波的所有初始相位和原时间层，已将两层状态窗口接到完整 RK 的精确位移公式：固定正时间、足够细网格下，253h 物理窗口外的内部种子相对实际激波每步向内平均位移至少 7/160 个单元。公式保留真实第一 Euler 三邻点。边界质量损失、多步回返和全时间混合仍待证明，一般共同强迹未闭合。

**原有限网格统一窗口阶段：** [26 条 Lean 定理](docs/burgers1d_shocks/adjoint_general_boundary/README.md)已独立审计通过，110 个项目模块（61 个全新编译、49 个固定已审计整数证书产物复用）。对默认一阶移动激波、页面全部初始位置／正时间及所有网格相位，原两阶段累计参考边界误差一致趋零，参考状态窗口已传给原有限轨道：物理激波中心 252h 外左侧≥4/5、右侧≤1/5。存储层和第一 Euler 层使用各自实际时刻，保留原 ceil。完整 RK 的移动窗口回返、全时间反向混合和一般共同强迹仍未完成。

**前一参考局部化与原有限边界连接阶段：** [46 条 Lean 定理](docs/burgers1d_shocks/adjoint_general_reference/README.md)已独立审计通过，覆盖 104 个项目模块（55 个全新编译、49 个固定已审计整数证书产物复用）。默认一阶移动激波的无限参考在所有存储层和真实第一 Euler 层都有固定移动状态窗口及几何尾界；原有限／无限比较显式累计两个输入层的边界误差，不再要求传播范围不触边，并已接到原任意相位与 ceil 时钟。累计边界误差的一致消失已由上面的新包补齐；移动窗口回返、全时间混合和一般共同强迹仍待完成。

**一般共同强迹方向的新进展：** [39 条局部化与原 RK 传播定理](docs/burgers1d_shocks/adjoint_general_localization/README.md)已独立审计通过，23 个项目模块全部从空目录新编译。任意相位已构造半单元内的中心参考相位，原存储层和真实第一 Euler 层的单元 L¹ 预算收紧为 `6(L−R)/5`，并接通移位逐点比较。参考两侧状态间隔可经每侧扩宽 11 个单元传给原两层；默认 α=6/5、原步数≥2 时，完整原 RK 又具有统一相邻传播下界及固定内部窗口共同正质量。参考轨道的一般统一局部化、移动窗口回返和全时间混合仍待证明，故一般共同强迹尚未闭合。

**一般相位与原 ceil 时钟的最新连接：** [26 条 Lean 定理](docs/burgers1d_shocks/adjoint_general_clock/README.md)已通过独立审计，16 个项目模块全部从空目录新编译。对一阶原 LF／SSP-RK2，任意初始相位与原时钟扰动下的存储层和真实第一 Euler 层均获得统一单元 L¹ 比较；相邻网格相位的存储层物理误差不超过 `17(L−R)/(10n)`，同层比较的物理时刻差不超过一个 CFL 步。这为一般共同强迹提供前向状态估计；一般反向混合、共同强迹及相位内唯一性仍未证明。

**激波证明最新状态（2026-09-28）：** [统一状态索引](docs/burgers1d_shocks/adjoint_connection_status.md)区分当前结论与下文历史阶段记录。一阶二次梯度及伴随场的一般全序列唯一性已被严格反例否定。二阶固定正时间反例的 88 条定理已独立审计闭合长期两阶段 Q 控制和完整原梯度分离，265 个项目模块全部从空目录编译通过；上游 149 条联合能量定理已通过独立审计。[原 binary64 选支反例](docs/burgers1d_shocks/adjoint_binary64_branch/README.md)的 40 条定理已独立审计通过：n=243 原浮点中心严格右选、精确实数左选，原初始斜率 JVP 反号；另有 [13 条有界执行接口定理](docs/burgers1d_shocks/adjoint_binary64_execution/README.md)已独立审计，消除区间外舍入约定的依赖。完整浮点目标梯度、一般共同强迹、相位内识别和完整连续边界仍未认证。

**激波扩展：** [现有 Riemann 激波的数学证明与 Lean 核验](docs/burgers1d_shocks/README.md)现有 **861 条定理、105 个模块**。此前原一阶 LF／两阶段 SSP-RK2、固定 ghost 和 ceil 时间步的强紧性、精确初值、有限域熵边界、强迹、BLN、PDE 收缩、唯一性与全序列收敛均已建立。[完整显式解闭合](docs/burgers1d_shocks/explicit_shock_closed.md)进一步独立证明完整移动分片函数的弱积分与熵边界，包含激波触边和出域，再由唯一性将原全序列及任意加密族的极限明确识别为该解析函数；空间 L¹ 误差在整个 [0,T] 上一致趋零。主定理无 `huniq`、`hkato` 或候选显式解身份前提。范围为下降 Riemann 激波的精确实数前向模型；正时间伴随、二阶 minmod 和具体 binary64 执行认证未由此结论推出。

**激波弱伴随的特征表示：** [从任意弱解到全域特征剖面的 Lean 证明](docs/burgers1d_shocks/characteristic_rectangle/README.md)新增 **53 条定理、8 个模块**，直接从已有弱积分证书推出左右完整侧域上的 `v(t,x)=F₋(x−Lt)`、`v(t,x)=F₊(x−Rt)`（几乎处处），并证明给定解的剖面在坐标投影上几乎处处唯一。二维保测度剪切、矩形分布分离、有理矩形覆盖和可数拼接均已形式化，不预设特征传播、BV 或连续性。后续的[共同强迹下整体唯一性证明](docs/burgers1d_shocks/weak_uniqueness/README.md)现已接通。

**共同强迹下的整体唯一性：** [完整 Lean 证明与审计](docs/burgers1d_shocks/weak_uniqueness/README.md)新增 **98 条定理、15 个模块**，直接从原 `WeakAdjoint`、终端／严格伴随入流数据和原始窄带共同迹推出 `q=c`，以及候选解与规范场在整个时空域上几乎处处相等，并证明存在性和规范特征代表。光滑侧别截断、窄带误差极限、终端之后下降的特征测试和可数覆盖均在 Lean 内完成；不额外假设特征传播、BV、连续性或内部迹识别。结论限定于当前单个直线移动激波模型，唯一性针对 Lebesgue 等价类。

**原格式离散到连续的连接：** [反向稳定性、总变差和一般相位梯度极限](docs/burgers1d_shocks/discrete_bridge/README.md)新增 **58 条定理、7 个模块**，直接使用页面原一阶 LF／SSP-RK2、固定 ghost、ceil 步长与原目标，证明物理反向伴随上界、完整反向总变差不增，以及初始激波位置参数上的区间／分布梯度收敛。区间极限已识别为上述唯一连续弱伴随规范代表的位置配对，覆盖移动／驻定激波、全部网格奇偶性及对齐参数。本阶段给出位置参数上的分布极限，后续伴随场紧性见下段；数值极限的完整弱式及一般参数共同强迹仍待识别；固定参数网格族的最新共同迹见后文。

**原数值伴随场的时空紧性与终端迹：** [完整证明与独立核验](docs/burgers1d_shocks/adjoint_compactness/README.md)新增 **61 条定理、9 个模块**，对固定 T>0 证明原程序 λ=W/h 的实际反向层在任意加密族上具有强时空 L¹ 收敛子列，并对整个 [0,T] 上的空间 L¹ 范数一致收敛。终端总变差、反向时间模量、Jordan 空间紧性和每个时刻的左右空间极限均由原格式推出；同一极限的终端迹已识别为 (1+x)G′(u(T,x))。覆盖原两目标、全部网格相位及奇偶性。剩余工作是实际极限的完整弱问题、一般参数共同强迹及相位内极限识别；下文双相位反例已排除完整网格场收敛到任何单一强时空 L¹ 极限。

**原转置弱平衡与源项配对极限：** [完整证明与独立核验](docs/burgers1d_shocks/adjoint_weak_balance/README.md)新增 **72 条定理、10 个模块**，从原反向 RK 推出保留状态跳跃源项和边界通量的精确弱平衡，证明通量与求积误差趋零，并接到实际 λ=W/h 重构的时空 Lebesgue 积分。沿此前同一收敛子列，伴随与显式前向激波的通量乘积通过极限，所有内部光滑测试的原源项配对同时收敛，并满足不含测试导数的零阶界；联合可测代表、时间一致收敛和正确终端迹均属于同一极限。源项的后续激波线定位见下段。

**源项极限的激波线定位：** [完整证明与独立核验](docs/burgers1d_shocks/adjoint_reaction_support/README.md)新增 **52 条定理、7 个模块**，将下降状态的跳跃一阶矩精确识别为实际空间 L¹ 误差，保留原 RK 中间状态和 ceil 时间求和，证明极限源项配对由测试函数沿真实激波线的时间 L¹ 范数控制。测试在线上几乎处处为零时配对为零，沿线取值相同的测试具有相同配对；结论覆盖激波触边及出域。已接回原紧支撑 C² 测试类和原积分表达式，得到同一数值极限的激波外弱方程，并保留正确终端迹。源项密度及固定参数共同强迹已有后续扩展；一般参数共同迹、空间边界数据及各相位极限识别仍待完成；全网格唯一强极限已被下文反例否定。

**数值极限的两侧特征传播：** [完整证明与独立核验](docs/burgers1d_shocks/adjoint_characteristics/README.md)新增 **16 条定理、5 个模块**，直接从已经证明的内部激波外方程推出同一个原数值极限的全局表示 λ=F₋(x−Lt)／F₊(x−Rt)，并证明剖面局部可积、继承 14α 上界，以及同一场的剖面几乎处处唯一。保留原数值子列、正确终端迹和源项沿线定位；不预设完整 WeakAdjoint、特征传播或共同迹，也不要求激波始终留在域内。源项密度及固定参数共同强迹见后续扩展；一般参数共同强迹仍待闭合；下文已构造两个不同的实际强子列极限。

**左右各自的强激波迹：** [完整证明与独立核验](docs/burgers1d_shocks/adjoint_individual_traces/README.md)新增 **28 条定理、6 个模块**，由有界可测特征剖面、单侧 Lebesgue 微分、时间支配收敛和保测度条带变换，证明同一个原数值极限的左右强迹存在。使用原二维 `stripError` 和完整 ε→0⁺ 极限，未假设共同迹。页面两类激波的参数满足所需严格内域条件；一般参数下仍需证明两迹相等、识别平台，再识别实际弱问题；一般全网格唯一收敛已被下文反例否定；后文已完成源项密度和固定参数网格族的共同强迹。[实现与证明状态对照](docs/burgers1d_shocks/adjoint_connection_status.md)单独列出尚未完成的位置梯度和二阶问题。

**原反应项的显式激波密度：** [完整证明与独立核验](docs/burgers1d_shocks/adjoint_reaction_density/README.md)新增 **45 条定理、8 个模块**，将同一个原数值极限的两侧强迹扩展到 [0,T]，并对全部原紧支撑 C² 内部测试证明 ρ=(L−s)q₋+(s−R)q₊=(L−R)(q₋+q₊)/2。原 `reactionPair` 沿同一子列收敛到该密度配对，密度可积且满足 (L−R)14α 上界。证明使用原测试的精确局部化、消失条带误差及两侧实际通量，没有预设完整弱伴随。一般参数的两迹相等、预定平台、完整边界平衡、各相位场极限及二阶渐近仍待完成；固定参数网格族的共同强迹见后文。

**原累计量凹性与端点参数极限：** [完整证明与独立核验](docs/burgers1d_shocks/adjoint_primitive/README.md)新增 **72 条定理、10 个模块**，累计量差分在每一步都等于原 LF／SSP-RK2 状态，保留实际两端通量和原 ceil 步长；证明全相位参数凹性与统一增量界。原线性目标及开相位原反向梯度已精确写成累计量及其导数的组合。利用既有原前向质量收敛，进一步证明全部网格上的左端参数增量趋零、右端增量趋于 (L−R)Δa。该冻结阶段的割线极限与对齐点选支接口已在下述线性梯度阶段闭合；二次目标、一般共同迹和二阶模式的后续状态分别见下文。

**原一阶线性目标位置梯度收敛：** [完整证明与独立核验](docs/burgers1d_shocks/adjoint_linear_gradient/README.md)新增 **33 条定理、7 个模块**，通过凹函数的左右割线夹逼与原目标增量极限，证明原线性反向梯度沿全部 `n=k+8` 收敛到 `(L−R)(1+a+sT)`。覆盖对齐点右选支、网格奇偶性及 `T=0`；原 `ceil` 步长、固定 ghost、单元平均和完整 RK 反传均保留。原初始种子单元中的 `dual/h` 也收敛到 `1+a+sT`。页面移动激波与驻定激波的线性目标已有直接推论。二次目标的一般梯度收敛已由下述严格反例否定；一般参数共同强迹、完整伴随场极限和二阶渐近仍须单独处理。

**原位置切向量向激波的集中：** [完整证明与独立核验](docs/burgers1d_shocks/adjoint_tangent_measure/README.md)新增 **51 条定理、8 个模块**。由原切向与累计右导数的逐单元对应，证明全部相位的切向质量、一阶及二阶空间矩极限，继而证明中心二阶矩、绝对距离矩和固定激波邻域外质量趋零。每个 Lipschitz 空间测试的原切向配对都趋于激波点配对。原二次目标梯度进一步严格等价于 `h∑(U_h−s)V_h→0`；空间权重误差已消除；下述无条件反例进一步严格否定这一原状态—切向乘积的一般趋零结论。

**页面默认 α=1.2 的二次梯度反例已完成 Lean 总连接：** [无条件定理与核验](docs/burgers1d_shocks/adjoint_phase_grid/README.md)保留原 `ceil` 步数、固定 ghost、单元平均初值、两个 RK 阶段及原反向梯度。固定 `(L,R)=(1,0),a=13/40,T=7/2400`，沿 `n_m=100(48m+1)`，原二次位置梯度误差最终满足 `g_{n_m}−6367/9600>3·10⁻¹¹`，因此一般连续一致性不成立。[实际无限能量](docs/burgers1d_shocks/adjoint_phase_energy/README.md)与有限网格总连接本轮新增 **66 条定理、9 个模块**；最终审计覆盖 347 个依赖模块，其中 298 个新编译、49 个此前已完整审计且逐字节固定的整数证书产物复用。总定理不再保留能量、收缩或计算前提。α 与页面默认值一致，T 是合法固定输入、非默认展示时间；结论使用精确实数语义，未认证 binary64 执行。

**共同强迹方向的原反向层指数混合：** [51 条新定理与独立核验](docs/burgers1d_shocks/adjoint_shock_mixing/README.md)沿默认 α=1.2、原固定参数子序列，将任意单位种子的无限格点传播接入实际有限网格和 `reverseLayer`。原第 48m 层、激波附近半径 p−m 的单元窗口内，任意两个伴随值之差由 `40M(181/162)^47(10/9)(7/9)^(p−m)` 控制。353 个模块的审计通过，其中 304 个新编译、49 个固定已审计产物复用。[历史二维连接推导](docs/burgers1d_shocks/adjoint_shock_mixing/TRACE_CONNECTION.md)保持冻结；其固定参数网格族的二维传递已由下述新阶段完成，一般参数及全部相位仍未闭合。

**固定参数原网格族的共同强迹已闭合：** [50 条新定理与二维总连接](docs/burgers1d_shocks/adjoint_common_trace_mesh/README.md)将上述混合界接到同一个原物理重构极限。对 `L=1,R=0,α=6/5,a=13/40,T=7/2400,n_p=100(48p+1)`，原线性与二次目标均有强收敛子列及原 `HasCommonShockTrace`；也可从该网格族的任意严格递增子列开始提取。总定理不含两迹相等或反射相等前提，并保留全部既有终端、特征及反应密度结论。独立审计通过 360 个依赖模块，其中 311 个新编译、49 个固定已审计整数产物复用。一般参数／全网格、共同迹具体值、完整弱边界平衡及二阶渐近仍未闭合。

**原二次伴随场的连续参考极限已被严格反例否定：** [41 条新定理与场反例](docs/burgers1d_shocks/adjoint_field_counterexample/README.md)沿同一原固定参数网格族，将初始种子梯度偏差传到固定物理区间，得到初始空间 L¹ 距离至少 `10⁻¹⁵`；原时间模量使偏差持续到固定正时间区间，最终时空 L¹ 距离至少 `2.5·10⁻³³`。原 T 保持 `7/2400`，没有随网格缩短。371 个依赖模块的审计通过，其中 322 个新编译、49 个固定已审计产物复用。每个强子列极限都与页面规范场分离；此前共同强迹仍成立，但不存在任何等价代表能成为预定完整 `CommonTraceSolution`。因此一般规范场一致性不是尚待补证的真命题。实际迹值、相位内极限唯一性和二阶渐近仍待完成；失败条件已由下述新阶段定位于预定源项的内部弱式。

**一阶反例的源项失败已严格定位：** [36 条新定理与总证书](docs/burgers1d_shocks/adjoint_source_counterexample/README.md)在同一原参数网格族上证明：任意强数值极限的左右迹及实际反应密度，在任意 `0<A<B≤T/208` 的平均值均至少为 `6367/9600+10⁻¹¹`。内部测试唯一确定密度，因此没有任何等价代表满足参考源项的 `InteriorDensityBalance` 或原 `WeakAdjoint`，无须附加预定边界数据。正确终端、原共同强迹及原离散反应密度收敛仍由同一证书保留。审计通过 378 个模块，其中 329 个新编译、49 个固定已审计整数产物复用。实际源密度的精确值仍未识别；后续双相位反例已否定一般非规范全序列唯一性。

**原一阶二次梯度没有任何单一实数极限：** [32 条新定理与双相位反例](docs/burgers1d_shocks/adjoint_phase_nonunique/README.md)保留同一原参数 `L=1,R=0,α=6/5,a=13/40,T=7/2400`。原 `100(48m+1)`、`100(48m+5)` 两族梯度相对参考值的偏差分别最终大于 `3·10⁻¹¹`、小于 `−3·10⁻¹¹`，从而排除完整梯度序列的任何实数极限。原第五步整数证书、无限尾部、真实返回轨道、新有限网格和完整反传均已接通。审计通过 354 个模块，其中 305 个新编译、49 个已审计产物复用。

**原伴随场存在两个不同的强时空极限：** [53 条新定理与完整场反例](docs/burgers1d_shocks/adjoint_phase_field/README.md)把上述负相位梯度接到原物理反向场，在固定早期条带上证明每个负相位强极限至多为 `c_ref−10⁻¹¹`；正相位极限至少为 `c_ref+10⁻¹¹`。两类 L¹ 等价类严格不同，且原紧性保证两类强子列极限实际存在。因此全网格场不收敛到任何单一强时空 L¹ 场，包括非规范场。388 个模块通过独立审计，其中 339 个新编译、49 个已审计产物复用。未断言单个相位自身极限唯一；一般共同迹、实际密度和边界识别、二阶长期尾部及 binary64 仍未完成。

**二阶 minmod 的完整原 RK／VJP 连接：** [39 条新定理与独立核验](docs/burgers1d_shocks/adjoint_muscl_rk/README.md)证明原 limiter 选支、逐面与逐斜率散射、两个真实 Euler 状态和任意步转置配对完全对应。27 个模块全部从空目录核验。原驻定 Riemann 算例 `n=9, α=6/5, a=1/2, T=7/216` 的完整二次选支梯度和原反传配对均为 `−6202880081929027/27831388078080000 < −1/5`。这是精确有限网格证书；固定正时间的二阶渐近收敛或不收敛尚未证明。

**二阶驻定候选的原状态对称性与固定时间网格：** [20 条新定理与独立审计](docs/burgers1d_shocks/adjoint_muscl_stationary/README.md)证明原 MUSCL Euler／RK 在任意步数下保持反对称，中心 Riemann 初值在完整层和第一 Euler 中间层的中心值严格为零，中心非零等幅斜率按原规则选择左切向增量。固定 `T=7/216,n_m=9(2m+1)` 的原 ceil 步数严格为 `2m+1`、`dt/h=7/24`。29 个依赖模块全部从隔离空目录编译。该冻结阶段之后，有限／无限连接已由下述新阶段完成；其余分支、长期切向及终端乘积的渐近估计仍未闭合。

**二阶原有限／无限轨道和完整反传已精确连接：** [34 条新定理与独立审计](docs/burgers1d_shocks/adjoint_muscl_embedding/README.md)覆盖驻定候选 `n_m=9(2m+1)` 的所有实际时间层和两个真实 Euler 阶段，保留原 ceil、ghost、端点零斜率、初值与选支。35 个项目模块全部从隔离空目录编译。原二次位置反向梯度精确等于 `3E_(2m+1)+2P_(2m+1)/n_m`，原中点权重产生的一阶矩未被删去；无限切向有符号质量为 1，有限物理切向质量为 2。完整梯度表达式的长期估计仍未证明，不能据此声称二阶固定正时间渐近反例已完成。

**二阶驻定候选的全步状态稳定性已证明：** [50 条新定理与独立审计](docs/burgers1d_shocks/adjoint_muscl_shape/README.md)从原 limiter 和通量分拆推出 Euler 相邻差下界 `19/40`、RK 下界 `1961/3200`，从而保持所有实际阶段单调下降及 `[-1,1]` 盒界；原有限层总变差为 2，两个阶段的中心始终激活并左选。40 个模块全部从隔离空目录编译。另有保留假设的梯度反例充分判据：若原终层切向非负、右侧反射占优，且核心不对称乘积最终有统一正下界，则完整原梯度与零参考值保持固定负偏差。这三个长期条件仍未证明，二阶渐近反例尚未闭合。

**二阶驻定候选的统一几何尾部和核心间隔已证明：** [62 条新定理与独立审计](docs/burgers1d_shocks/adjoint_muscl_barrier/README.md)证明原全部 RK／Euler 状态两侧缺额不超过 `(3/25)(1/5)^(r−1)`，故中心左状态始终至少为 `22/25`。原 RK 步后核心缺额至少 `1/40`，紧邻状态差至少 `1/1000`，从而确定中心两旁的严格左／右选支。46 个项目模块全部从隔离空目录编译。原有限网格在每个实际时间层相对精确驻定单元平均的加权误差至多 `3/(10n)`，这不是相对间断点值解的同一个 L¹ 范数。二阶完整梯度的反例判据仍需实际切向非负、右侧反射优势和统一正的左右切向差；尚无无条件二阶渐近反例。

**二阶核心切向的实际进入条件已解除：** [62 条新定理与独立审计](docs/burgers1d_shocks/adjoint_muscl_tangent/README.md)精确认证原前三个 RK 步进入核心切向窗口，证明有符号质量到局部尾部控制的连接，以及两个实际 Euler 输入层下的条件窗口不变性。52 个项目模块全部从隔离空目录编译。新的完整梯度判据只需每个 K≥3 的存储层和第一 Euler 层满足外部切向绝对质量 ≤1/50，即可推出每个 m≥1 的原梯度 ≤−61/1125。全局切向非负、逐点反射优势和丢弃中点一阶矩均不需要。实际长期绝对尾部界仍未证明，尚无无条件二阶渐近反例。

**单一尾部总量界不能直接用作不变性归纳：** [8 条严格辅助反例定理](docs/burgers1d_shocks/adjoint_muscl_tail_obstruction/README.md)在原实际第 3 步 primal 上构造非负、质量为 1、满足核心窗口且外部绝对质量等于 1/50 的测试切向，但一次原 Euler 后外部绝对质量严格增大。53 个依赖模块全部重新编译。测试向量不是实际 Riemann 位置切向；此证书仅排除粗总量不变性路线，实际长期尾部仍需更强空间控制。

**第二邻居实际选支已闭合并接回原有限 limiter：** [50 条新定理与独立审计](docs/burgers1d_shocks/adjoint_muscl_sharp_tail/README.md)将全步 primal 尾部的几何因子收紧到 1/12，并从原第 3 步起得到核心缺额 ≥1/20、第二单元缺额 ≥1/1000 和第二邻居向外状态差 ≥1/6000。由此 j=−2/+2 的严格左／右选支在存储层、两个 Euler 输出和原有限 slopeJVP 中均已认证。57 个项目模块全部重新编译。在尚未证明的实际两阶段长期 Q≤1/50 前提下，另得到核心切向差 ≤21/100 和两个核心切向分量的严格正下界。长期切向尾部及二阶无条件渐近结论仍未完成。

**二阶原严格前沿与实际双选支表示已证明：** [36 条新定理与独立审计](docs/burgers1d_shocks/adjoint_muscl_front/README.md)将全部原 RK 扰动／切向支撑收紧至半径 2K，证明整个前沿的严格跳跃及三个实际阶段的精确 limiter 激活区间；同一个左右选支在每个格点同时表示实际状态和位置切向的斜率，并接回原有限内部 slopeJVP。61 个项目模块全部从隔离空目录编译。区外原 inactive 规则保持不变，该等价表示仅适用于实际切向，不替换任意输入的 Jacobian。保留完整中点一阶矩后，条件梯度界加强为 −71/1125；两个实际阶段的长期 Q≤1/50 仍未证明，二阶无条件渐近反例尚未完成。

**二阶有限时间切向证书与全时间窄状态区域已独立审计：** [33 步整数区间包](docs/burgers1d_shocks/adjoint_muscl_interval/README.md)的 272 条定理经 172 个模块全新编译通过独立审计；[边界储能包](docs/burgers1d_shocks/adjoint_muscl_boundary/README.md)的 11 条定理经 124 个模块全新编译通过。[新的 48 条定理](docs/burgers1d_shocks/adjoint_muscl_primal_box/README.md)已通过 107 个项目模块全部重新编译的独立审计：原第 33 步起的所有存储层及两个 Euler 输出保持具体有理状态区域，第 1…17 格实际切向选支已确定并接回原有限网格。该无限时间结论只控制原状态及选支。[联合切向候选](docs/burgers1d_shocks/pending_muscl_stationary/joint_core_candidate/README.md)另已通过精确有理矩阵检查，两阶段 Q 上界均低于 1/50；其中两个实际阶段的通用矩阵语义已独立审计，具体联合证书与原无限轨道的完整能量连接仍待形式化，二阶无条件梯度渐近仍未形式化闭合。

**原核心矩阵与具体质量坐标：** [68 条原矩阵定理](docs/burgers1d_shocks/adjoint_muscl_joint_model/README.md)已独立审计通过，115 个项目模块全部重新编译。两个实际阶段、完整核心 RK、独立状态盒误差及有理到实数身份均已连接。[具体核心质量坐标](docs/burgers1d_shocks/adjoint_muscl_core_coordinates/README.md)的 77 条定理已通过 129 个项目模块全部新编译的独立审计；包含原 33 格输入分解、质量方向残差、具体 P≥I/2000 的 Gram 证书和实际核心能量。32 维联合耗散证书、原总能量入口与全时间 Q 仍未闭合。

**二阶尾部比较算子的全分支能量收缩已证明：** [257 条新定理与独立审计](docs/burgers1d_shocks/adjoint_muscl_storage/README.md)认证原 α=6/5、ν=7/24 常系数比较递推在 q=37/50 权重下的任意有限长度平方增益 ≤199/200，允许两个阶段所有空间左右选择。16 个储能矩阵、64 个模式转换及精确递推身份均经内核检查，56 个项目模块全部从隔离空目录编译。原 LF 通量系数身份和局部变系数误差界也已证明。原实际半无限尾部、核心输入及两个阶段的全局变系数误差仍未联合控制；因此长期 Q≤1/50 和二阶无条件渐近反例尚未闭合。



**原一阶终态二次梯度的相位反例：** [数学论证与核验](docs/burgers1d_shocks/adjoint_phase_counterexample/README.md)对固定 `α=1,a=13/40,T=7/2000` 和 `n_m=100(40m+1)`，用精确有理数核心检查、无限尾部估计与返回映射收缩，证明终态乘积 `E_m` 最终大于 `10⁻⁹`，从而原二次梯度不趋于连续参考值。这是一份计算机辅助数学反例，**尚未完成整个 Lean 总证书**；新增 26 条 Lean 定理覆盖局部模板、无限步递推、原网格相位及条件反证，该 α=1 冻结阶段保持原状；上述 α=1.2 阶段已另行完成无条件 Lean 总反例。原页面代码保持不变。

**原 RK 时间积分的乘积极限：** [完整证明与独立核验](docs/burgers1d_shocks/adjoint_time_product/README.md)新增 **57 条定理、8 个模块**。从保留两端 ghost 测试值的原转置恒等式出发，将全部边界配对误差控制为实际切向质量损失，证明两个真实 RK 阶段的累计 `UV`、`(U−s)V` 和二次梯度配对极限。阶段时间积分的 `(U−s)V` 趋零，二次配对趋于连续参考梯度的时间积分；扩散修正保留并证明消失。时间积分中的抵消不能决定终态乘积；上面的新反例针对终态二次梯度，一般参数共同强迹与二阶渐近仍待完成。

The single interior straight-shock common-trace weak-adjoint existence and uniqueness theorem is complete modulo null sets. The original first-order reverse scheme has strong spacetime subsequence compactness, uniform-in-time spatial L1 convergence, the correct terminal trace, and a vanishing weak-balance defect. The same limit now has both full-time one-sided strong shock traces and the explicit interior reaction density rho=(L-R)(q_minus+q_plus)/2; the original discrete reaction pairing converges to this density pairing for every original compact C2 interior test. The original first-order linear-target position gradient now converges along all meshes, including aligned right branches and zero time, and its shrinking initial-cell dual/h sample has the correct limit. The actual selected tangent measures now concentrate at the physical shock along every mesh: mass and first/second spatial moments converge, and all Lipschitz test pairings have the expected Dirac limit. Quadratic-target gradient convergence is reduced exactly to vanishing of the unweighted state-tangent velocity mass. An exact-rational computer-assisted mathematical proof now gives a strictly positive terminal interaction along a mesh subsequence at the original default alpha=1.2, with fixed a=13/40 and T=7/2400; thus the universal quadratic-target gradient convergence claim is false. The default-alpha counterexample is now an unconditional Lean theorem: the complete 48-step certificate, all infinite tails, actual state/tangent recurrence, terminal energy, original fixed-ghost finite-grid embedding and original reverse gradient are connected. Along cells=100(48m+1), the gradient error above 6367/9600 is eventually strictly greater than 3e-11; the final isolated audit covers 347 project modules (298 fresh builds and 49 byte-identical previously audited integer-certificate artifacts). This remains an exact-real result, not a binary64 execution certificate. Its actual RK-stage time integral is now proved to vanish, and the stage-integrated quadratic pairing converges to the continuous quadratic gradient time integral; these averaged statements do not settle the terminal interaction. A new 51-theorem audit connects exponential seed mixing to the original finite-grid reverseLayer on expanding shock windows of this fixed-parameter mesh subsequence; a further 50-theorem audit now completes the two-dimensional reconstruction and common-trace transfer for both original targets on that mesh family. The original HasCommonShockTrace is obtained for the same spacetime limit, with no assumed trace or reflection equality, and extraction may start from any strict subfamily. Its isolated dependency audit covers 360 project modules (311 fresh builds and 49 byte-identical audited integer artifacts). A separate 39-theorem audit connects the full selected MUSCL RK tangent to the literal face/limiter-scatter VJP for arbitrary step count and certifies a nonzero original one-step Riemann quadratic gradient. A further 41-theorem audit now proves a strict original quadratic adjoint-field counterexample: on the same fixed-parameter mesh family, the spacetime L1 distance from the canonical continuous field is eventually at least 2.5e-33, and every strong subsequential limit remains separated. The proof propagates the original gradient gap to a fixed spatial interval and then a fixed positive time interval; the final time T remains fixed. Original common-trace limits exist, but no equivalent representative belongs to the full prescribed CommonTraceSolution class. Thus universal canonical field consistency is false. A new 36-theorem audit identifies the failed condition: the actual trace and reaction-density means exceed the canonical value by at least 1e-11 on every early interval inside (0,T/208). The prescribed interior source equation fails for every a.e. representative of every strong limit of any diverging subfamily, independently of boundary or endpoint data. Its audit covers 378 modules, including 329 fresh builds and 49 fixed audited integer artifacts. A separate 20-theorem audit proves exact MUSCL primal antisymmetry, zero center at both primal stage states, literal center tie selection, and the fixed-positive-time stationary mesh clock; its 29-module closure is freshly compiled. A new 34-theorem audit, with all 35 dependency modules freshly compiled, connects the original finite state and selected tangent at every actual layer to the same infinite MUSCL trajectory. It identifies the full original reverse quadratic gradient as 3E+2P/n with the midpoint first moment retained, and proves signed tangent mass conservation. A further 50-theorem audit, with all 40 project dependencies freshly compiled, proves all-step original MUSCL primal monotonicity, box bounds, finite total variation 2, and permanently active left center selection at both actual stages. Its full-gradient sign criterion remains conditional on unproved tangent nonnegativity, right-reflection dominance, and a uniform positive core bias. A subsequent 62-theorem audit, with all 46 project modules freshly compiled, proves a uniform geometric primal envelope, U_-1>=22/25, strict nearest-core limiter choices, and an original weighted cell-average error <=3/(10n) at every actual layer. This cell-average norm is not the spatial L1 norm against the pointwise discontinuous shock. The gradient criterion still assumes unproved tangent nonnegativity, right-reflection dominance and a uniform positive V1-V_-1. A further 62-theorem audit, with all 52 project modules freshly compiled, certifies exact three-step entry into a core tangent window and reduces the full original gradient bound to absolute outer mass <=1/50 at both actual RK input layers for every K>=3. This new route does not require global tangent positivity or pointwise reflected dominance, and retains the original first moment. Its infinite-time tail hypothesis remains unproved. A new 50-theorem audit, with all 57 project modules freshly compiled, sharpens the original primal tail factor to 1/12 and proves strict actual limiter choices at -2/+2 from step 3, including both Euler outputs and the literal finite slopeJVP. Positive core tangent component bounds are proved only under the still-unproved actual two-stage absolute-tail bound. General common traces, exact actual trace values, actual boundary identification, within-phase limit identification and second-order gradient asymptotics remain unresolved. A subsequent exact-real two-phase counterexample now rules out every real limit of the full quadratic gradient sequence and every strong spacetime L1 limit of the full original adjoint-field sequence; two distinct actual strong subsequential field limits exist.

**两族共同强迹与实际源密度分离：** [28 条 Lean 定理及独立审计](docs/burgers1d_shocks/adjoint_phase_trace/README.md)已完成，覆盖 399 个项目模块（350 个新编译、49 个固定已审计整数产物复用）。同一固定反例中，正、负两个原网格族都具有共同强迹、正确终端及实际离散反应极限；二次目标的实际源密度在任意早期区间 (A,B) 上，其积分差至少为 `2·10⁻¹¹(B−A)>0`。两族不同的实际强极限均不满足预定参考源项弱方程，修改零测集代表不能修复；连续参考弱解唯一性定理继续成立。一般参数共同迹、相位内精确识别、完整边界、二阶实际长期尾部界和 binary64 仍未闭合。

**二阶整数格点能量与原两阶段残差：** [51 条 Lean 定理及独立审计](docs/burgers1d_shocks/adjoint_muscl_lattice/README.md)已完成，111 个项目模块全部新编译。任意空间选支的比较 RK 递推在支撑有下界的整个整数格点上具有平方增益 ≤199/200；半无限估计保留边界储能。两个原实际 Euler 阶段、完整 RK 及其残差已精确接入，得到每一步的带权能量估计，两个完整残差平方和仍保留。

**二阶双侧远尾与有限近尾判据：** [左尾截断 33 条定理](docs/burgers1d_shocks/adjoint_muscl_cutoff/README.md)和[双侧连接 57 条定理](docs/burgers1d_shocks/adjoint_muscl_two_sided/README.md)均已通过独立审计，分别将 117、128 个项目模块全部新编译。原反射选支、两个真实阶段的远尾能量及其到绝对切向质量的转换已闭合。若两侧第 4–7 格带权平方和每步 ≤10⁻⁸，且 K≥3 两个实际层的第 2–7 格绝对切向和均 ≤0.0185，则两阶段 Q≤1/50、完整原梯度 ≤−71/1125。**这些有限近尾条件的无限时间成立性仍未证明，二阶无条件渐近反例尚未完成。** 一般共同强迹、相位内极限识别、完整实际边界和 binary64 也仍未闭合，详见[统一状态索引](docs/burgers1d_shocks/adjoint_connection_status.md)。

**二阶有限进入与长期控制接口：** [15 条定理及独立审计](docs/burgers1d_shocks/adjoint_muscl_near_entry/README.md)已完成，130 个项目模块全部新编译；原前三步带界、第三层两个实际阶段的 Q≤1/50，以及只使用过去输入的因果尾部界已认证。[33 步整数区间证书](docs/burgers1d_shocks/adjoint_muscl_interval/README.md)的 272 条定理与[保留双侧边界储能](docs/burgers1d_shocks/adjoint_muscl_boundary/README.md)的 11 条定理均已通过独立审计。前者将有限两阶段 Q 控制推进到第 32 层，后者保留可参与联合核心估计的非负边界二次型；都未将有限进入或含输入估计外推成无限时间不变性。

<details>
<summary>历史推进记录与各阶段证明说明（阶段待办以当前统一入口为准）</summary>

**一维基准的数学证明 / 1-D baseline proofs:** [带源 Burgers 的一阶／二阶格心与格点证明](docs/burgers1d_convergence/README.md)覆盖现有耗散／迎风入口、前向与 tangent 收敛、伴随边界层及完整目标梯度收敛，不依赖求解算法。一阶证明每层网格的正值盒内存在唯一根；二阶进一步证明所有整数 $n\ge4$ 均存在唯一的重构容许解，给出统一显式二阶状态误差界，并证明光滑方向梯度的二阶收敛。二阶格点迎风入口仍有尖锐的全域 $L^2$ 半阶伴随层。一维 Lean 形式化尚未完成。The exact-real proofs retain the actual reconstruction, nodal constraint and source weights. Second-order uniqueness holds globally on the stated reconstruction polytope; analytic bounds and exact rational certificates establish existence and a uniform second-order error bound for every integer mesh n >= 4. Roots outside that polytope and floating-point execution are not certified.

[参数邻域与联合极限扩展](docs/burgers1d_convergence/second_order_parameter_proof.md)证明状态和目标函数的前三阶设计导数在共同数据邻域内统一收敛，并给出有限差分／复数步长与网格加密的联合及迭代极限。Uniform parameter derivatives through order three, including the design Hessian, and joint/iterated mesh and differentiation-step limits are proved in exact arithmetic.

[一维 Lean 覆盖与审计](docs/burgers1d_convergence/lean_formalization.md)已加入实际二阶模板、Fréchet 导数、所有网格的完整统一稳定性、四种格式全域唯一性、根存在判据、复数残差及误差传递定理；[常源基准的二阶 PDE 收敛](docs/burgers1d_convergence/lean_baseline_convergence.md)已覆盖四种格式、所有 n>=2048 及实际物理重构；[正弦目标的前向链](docs/burgers1d_convergence/lean_sine_convergence.md)已覆盖所有 n>=16384；[实际目标泛函](docs/burgers1d_convergence/lean_objective_convergence.md)已证明 816004h² 误差界，并分离前向与目标状态各自的停止／求值误差以及目标求值误差；剩余粗网格和参数梯度链仍有未闭合接口。[浮点误差与求解容差分析](docs/burgers1d_convergence/inexact_floating_point_analysis.md)区分离散、求解和舍入误差，并给出当前 Euclidean 停止范数、FD 与复数步长保持二阶精度的充分尺度。

新增[实际参数导数与伴随梯度证明](docs/burgers1d_convergence/lean_parameter_derivatives.md)：对 n>=16384 的两组参考数据，半径 10⁻⁷ 的参数邻域内每层存在唯一容许根；根与目标均 Fréchet 可微，伴随表示全部设计方向的真导数，且前向／目标／伴随停止与求值误差分别保留。最新[基准点切向与连续／离散伴随梯度收敛](docs/burgers1d_convergence/lean_tangent_gradient_convergence.md)已证明当前基准点上有界 Lipschitz 源项方向的二阶切向和伴随梯度一致性，并接通停止／求值误差趋零的联合极限；整个参数邻域的梯度网格极限与高阶 PDE 极限仍待形式化；物理伴随场与边界层见后续扩展。

新增 [FD／CS 实际分支与联合极限](docs/burgers1d_convergence/lean_fd_cs_convergence.md)：已证明邻近复根存在唯一性和真实部分容许性，基准点中心差分／复数步长均以 O(h²+t²) 收敛到连续梯度，无需 h/t 比值条件；非精确 FD 的目标误差／步长和 CS 的归一化虚部残差预算分别保留。整个实参数邻域内固定网格的步长极限也已证明。

新增[一阶所有整数网格的 Lean 前向证明](docs/burgers1d_convergence/lean_first_order_convergence.md)：两组实际数据、格心／格点与两种入口，在每个 n≥4 上均存在唯一容许根；样本、物理场和目标误差分别不超过 40h、41h、81h。停止与残差求值误差独立保留，节点入口约束缺陷也已纳入。后续[一阶参数与伴随梯度证明](docs/burgers1d_convergence/lean_first_order_derivatives.md)已补齐所有网格上半径 10⁻⁴ 的参数邻域、实际导数、切向物理收敛及 300(M+L)h 的连续／离散伴随梯度误差界，停止和求值预算独立趋零时仍收敛。

新增[一阶 FD／CS 的 Lean 证明](docs/burgers1d_convergence/lean_first_order_fd_cs.md)：在全部 n≥4 上证明中心差分和复数步长的 6000t²‖d‖³ 步长误差、实际邻近复根存在唯一性及完整复数原始／约化方程等价。基准点两种梯度以 O(h+t²) 趋于连续伴随梯度，允许网格和步长独立趋零；求解停止量与求值包围分别进入非精确误差定理。后续[一阶物理伴随与入口层](docs/burgers1d_convergence/lean_first_order_adjoint_inlet.md)已补齐有限 Lp 强收敛、耗散入口尖锐下界、全域一致当且仅当迎风，以及完整格点约束乘子的真转置、渐近与独立误差预算。最新[一阶误差分项与六证书 PDE 极限](docs/burgers1d_convergence/lean_first_order_adjoint_separate_errors.md)已证明近似前向／目标引起的伴随系数扰动、六项独立预算及完整格点约束反馈，并直接接通有限 Lp、内部一致及全域一致性分类。完整参数邻域的梯度网格极限、高阶 PDE 极限及复解析分支等剩余 Lean 接口仍保留。

新增[参数实解析性与高阶导数](docs/burgers1d_convergence/lean_parameter_analyticity.md)：两阶实际根与目标在现有有限参数开邻域内实解析，所有迭代 Fréchet 导数仍解析；一阶自由／完整根和二阶完整根的 Hessian 具有网格无关上界。

后续[实际二阶、三阶变分方程](docs/burgers1d_convergence/lean_higher_variation_equations.md)已证明真实高阶导数满足完整隐式方程，保留入口载荷 Hessian、完整格点约束和目标端点半权重；三阶状态导数具有网格无关界，实际目标的二阶、三阶公式已接通。后续扩展已接通至三阶的 PDE 网格极限，四阶及更高仍待证明。

新增[连续函数空间参数与精确投影](docs/burgers1d_convergence/lean_bounded_source_parameter_space.md)：连续积分 PDE 的正值解在 R×L∞ 到 C([0,1]) 的一致范数下实解析，真一至三阶公式及全部迭代导数解析性已证明。精确区间平均投影范数不超过 1，严格还原两组参考数据，并与两阶完整离散根的一至三阶求导相容。一般有界方向和高阶导数的网格收敛仍待闭合。

</details>

**SA 连续伴随推导稿 / SA continuous-adjoint derivation:** [二维可压缩 RANS–SA 的完整耦合推导](docs/sa2d/continuous_adjoint.md)保留标准 SA 的阻尼、非线性扩散、可变物性、涡量与壁距导数，并给出五个耦合方程和边界式；[数值核验记录](docs/sa2d/verification.md)包含局部导数与 Green 恒等式检查；[Lean 形式化记录](docs/sa2d/formal_verification.md)列出无激波范围下 53 个已核验核心定理及尚未关闭的分析接口。这是研究推导稿，尚未实现 RANS–SA 原始／伴随边值求解或真实算例梯度验证。The derivation includes the full five-field coupling and boundary form; local derivative and Green-identity checks do not constitute a RANS–SA BVP or physical-gradient validation.

#### 二维标量对流

新增[一阶格心／格点离散收敛证明](docs/scalar2d_convergence/convergence.md)：针对现有光滑特征边界模型，在明确的网格正则性条件下推导稳态解的存在唯一性与 `L²` 误差上界 `C√h`，并提供源代码一致性核对、五级网格结果及独立 Lean 代数／估计审计。该固定光滑模型的全三角形格心 PDE／网格总定理现已形式化；无约束二阶重构与伴随梯度收敛不包含在已证明结论内。

[数学收敛总定理与完整推导](docs/scalar2d_convergence/mathematical_convergence_theorem.md)：当前光滑特征边界模型在源坐标全三角形格心中点加密族上的数学证明已闭合。每层离散方程在 `0 < u_K <= 5/4` 内存在唯一解，该解自动满足 `[4/5,6/5]`；存在网格无关常数，使平方 L2 误差不超过 `C 2^(-k)`，因此整个序列收敛到指定的光滑 PDE 解，L2 范数保证 `O(sqrt(h))`。总定理不要求求解迭代、初始化、停止规则或证书搜索。Lean 库现有 765 个定理、131 个证明模块，详见[形式化范围与审计](docs/scalar2d_convergence/formal_status.md)。[非零残差误差界](docs/scalar2d_convergence/inexact_convergence.md)及历史求解算法证明作为独立扩展保留。新增[非均匀三角网格收敛定理](docs/scalar2d_convergence/graded_mesh_convergence.md)：保留面局部尺度，利用形状正则性证明 `sum_f ell_f delta_f² <= 6 sigma V h`，从而在明确几何证书条件下得到每层离散解存在唯一、平方 L2 误差 `C h` 和整个序列收敛；无需二分加密、嵌套或准均匀网格。最新[从三角网格几何出发的收敛总定理](docs/scalar2d_convergence/triangle_geometry_convergence.md)进一步从合法三角剖分与统一几何界构造完整分析证书：物理分区、Green 恒等式、法向闭合、面积和、采样估计及非特征边界可达性均在 Lean 内推导；边界可达性由正面积散度证明，无需额外路径假设。因此一般非均匀三角形族也获得离散解存在唯一、平方 L2 误差 `C h` 与强收敛的完整数学证明。网格正定向、不重叠、覆盖、面配对及边界位置仍是合法剖分的定义条件；未声称任意坐标列表自动满足这些条件。任意数据、二阶、SA 与伴随梯度收敛另属后续问题。

[格点中位对偶收敛证明](docs/scalar2d_convergence/nodal_convergence.md)现已完成一般全三角形网格族的数学与 Lean 证明：从原三角形坐标构造格点集合、六片中位分区及全局格点控制体，推导 Green 恒等式、法向闭合、边界可达性与每层离散解存在唯一。保留程序的聚合法向模耗散和两段真实折面积分，由形状正则性与原三角形面计数得到 `sum ell delta² <= 96 rho area(Omega) h`，进而证明真实格点控制体上的平方 L2 误差 `<= C h` 与全序列强收敛。无需准均匀、格点邻接数界或求解算法假设。仍需合法原网格、统一几何界和最大尺度趋零；未声称验证了 JavaScript 或浮点执行。

#### 一维 Burgers、Euler 与激波的其他进展

新增[有界源项参数邻域的一致收敛](docs/burgers1d_convergence/lean_bounded_neighborhood_convergence.md)：在共同 R×L∞ 参数空间中，一阶（n≥4）和二阶（n≥16384）实际模板均已证明整球前向和离散目标 O(h) 收敛，保留原入口、实际正弦目标及端点半权重。独立停止／残差求值误差可随网格趋零；连续目标真一至三阶导数及全部迭代导数解析性亦已接通。后续已证明一般有界方向的梯度算子极限，状态切向物理场与高阶导数极限仍分别追踪。

新增[一般有界方向的伴随梯度收敛](docs/burgers1d_convergence/lean_bounded_gradient_convergence.md)：两阶实际离散目标的梯度在 R×L∞ 算子范数下收敛，并在每个固定严格内球上一致；一般连续伴随 PDE、入口 aλ(0) 项、真实原始转置表示已闭合。七项停止／求值误差分别趋零时，允许参数和有界方向随网格变化，计算梯度仍趋近对应连续真导数。

新增[有界源项切向场与 Hessian 的 PDE 极限](docs/burgers1d_convergence/lean_bounded_tangent_hessian_convergence.md)：两组参考球中，两阶真实状态的一阶／二阶参数导数已证明采样算子范数及原物理重构的一致极限，实际目标 Hessian 也收敛。范围为固定严格内球、全部统一有界方向和全闭空间区间；后续三阶 PDE 极限见下方扩展；一般参数处非精确高阶残差连接仍未完成。

新增[有界源项三阶参数导数的 PDE 极限](docs/burgers1d_convergence/lean_bounded_third_convergence.md)：通过完整四阶变分方程及网格无关界，已将两阶真实状态与实际目标的算子收敛推进至三阶，并证明三阶变分在原物理重构下对严格内球、有界方向三元组和全闭区间一致收敛。一般参数处非精确高阶残差连接、四阶及更高 PDE 极限仍未完成。

新增[一般参数处非精确切向与二阶变分收敛证书](docs/burgers1d_convergence/lean_inexact_parameter_variations.md)：两阶切向的独立停止／求值预算已接到物理场极限；一阶直接处理完整原始切向残差及格点入口反馈，二阶 Hessian 进一步保留八项独立预算。全链条不假设求解器收敛；一阶 Hessian 后续已保留完整入口乘积反馈并接通八项独立预算；三阶误差链已接通（见后续16项证书扩展）；具体浮点执行认证仍待补齐。

新增[非精确三阶变分的16项误差证书](docs/burgers1d_convergence/lean_inexact_third_variations.md)：两阶格式的实际三阶残差已接到全闭区间物理一致极限，保留全部三个交叉项、完整格点入口反馈和误差乘积，独立分离主解、三个切向、三个 Hessian 与三阶变分的停止／求值预算。

新增[有界参数差分极限](docs/burgers1d_convergence/lean_bounded_difference_limits.md)：两阶中心有限差分的固定实步长网格极限、两种迭代极限、一般有界方向 FD／CS 联合极限及非精确 FD 分离预算已接通。另有[连续复解精确表示](docs/burgers1d_convergence/lean_continuous_complex_pair.md)，保留完整入口和积分 PDE；固定非零复数步长的离散网格比较仍待证明。

新增[1D Euler 页面 B.8 Roe 固定输入的严格反例](docs/euler1d_shock_convergence/capture/roe_page_phase_nonconvergence.md)：独立 Roe 冻结层/完整增广逆及 C¹ 真根构造给三个解析相位的压力梯度极限约 1.390108、2.145405、1.809748，连续值约 1.699205。保存默认背压也保持为其实际 dyadic 有理值，独立位置盒认证与无限偶数相位子列给梯度误差下极限>0.3；原解和目标值仍收敛。科学图与23帧动画已加入。默认全部细网格根身份、binary64 全程序、B.6 默认网格极限及完整 Euler Lean 仍未证明。

新增[正时间激波伴随梯度一致性](docs/burgers1d_shocks/positive_time_adjoint/README.md)：对居中驻定 Burgers 激波和全部奇数格网，保留一阶 LF、原 SSP-RK2、取整时间步与有限域边界，证明完整反向伴随等于实际离散目标的位置导数，并趋于连续激波梯度。线性／二次目标分别具有 `12 A alpha T h`／`2 A² (1+alpha T) sqrt(h)` 的误差上界；95 个新增 Lean 定理独立审计，原 861 定理前向证明保留。一般移动激波、任意网格相位、二阶重构及整个连续伴随场另属未闭合范围。

新增[一般网格相位与二阶扩展检查](docs/burgers1d_shocks/general_phase/README.md)：42 个 Lean 定理将一阶完整时间推进的导数／伴随等价性推广到一般左右状态及所有闭相位，包含网格面左右导数；同时认证正时间移动激波目标不可微反例、minmod tie 的选支障碍和原二阶 Euler 阶段的负雅可比项。一般移动二次目标所需的速度矩缺陷已明确。原二阶数值诊断出现相位相关的持续梯度偏差，且通过原反向伴随和差分复核；无限网格不收敛未形式化，一般移动／二阶梯度一致性也未宣称完成。

### 两个仓库的同步

GitHub 是主仓库（网页由 GitHub Pages 从这里发布，每次推送自动重新部署），Gitee 是镜像。把 `origin` 配成同时推送到两个仓库，一条 `git push` 就能更新两边：命令见上方英文部分（第一条替换默认的 push 地址，第二条再追加，两条都要执行）。用 `git ls-remote <url> refs/heads/main` 比较两边是否一致；若某个平台的网页端直接改过文件而 SHA 不同，先 `git pull gitee main --rebase`（或 `github`）取回对方的提交再推，**不要用 `--force`**，那会抹掉网页端的改动。

### 许可

© 2026 Yisheng Gao。本仓库的页面、连续伴随推导与本 README 以 **知识共享 署名 4.0 国际（CC BY 4.0）** 许可发布：您可以自由地共享与改编，包括用于商业目的，只要给出**适当署名**、提供许可协议的链接，并说明是否作了修改。完整条款见 [`LICENSE`](LICENSE)。

</details>
