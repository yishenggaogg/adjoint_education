# 离散伴随教学页 / Discrete adjoint, taught page by page

本项目的主线是离散伴随教学，面向学过微积分、线性代数与数值方法的本科生；最终目标是完整展示工业级非结构网格 RANS 的离散伴随实现（当前尚未实现 RANS）。连续伴随只作为简单算例的独立验证和对比：正文保留结论，原八页附录 A 提供完整推导、可复制运行的参考代码、图和交互，随页面切换中英文，不再另设文档页面。可以为选定的连续 RANS 模型写出形式伴随，但不能把它自动当作含湍流闭合、壁面处理、限幅与边界算法的完整工业离散流程的严格参照。

The teaching path develops discrete adjoints for undergraduates with calculus, linear algebra and numerical-methods background, toward a complete industrial unstructured-grid RANS implementation (not yet implemented). Continuous adjoints are independent checks for simple cases. Main chapters retain conclusions; the original eight pages’ bilingual same-page Appendix A contains full derivations, runnable reference code, figures and interaction. Formal continuous RANS adjoints do not automatically supply a strict reference for the full implemented industrial algorithm.

**十个**单文件、可交互的网页，把有限体积法的**全离散伴随**从头到尾讲一遍：
从一个面上的一维通量开始，把同一个循环依次改写成 primal、matrix-free 前向（$Av$）与
matrix-free 伴随（$A^{\mathsf T}w$），再做前向与伴随求解、几何导数，最后用有限差分逐项校验。
五组算例——**一维 Burgers 方程**、**二维标量对流方程**、**二维标量对流扩散方程**与
**拟一维 Euler 方程**与**二维 Euler 方程**——各有**格心**与**格点**两版。第一次接触离散伴随，请从一维那一对读起。

**Ten** self-contained, interactive web pages that develop the **fully discrete adjoint**
of a finite-volume scheme end to end: starting from the one-dimensional flux on a single
face, the same loop is rewritten as the primal, as matrix-free forward mode ($Av$) and as
matrix-free adjoint mode ($A^{\mathsf T}w$), followed by the forward and the adjoint solve, the
geometric derivatives and a term-by-term finite-difference verification. Five model problems &mdash;
the **one-dimensional Burgers equation**, a **two-dimensional scalar advection
equation**, a **two-dimensional scalar advection&ndash;diffusion equation** and the
**quasi-one-dimensional Euler equations** and **two-dimensional Euler equations** &mdash; each in a **cell-centred** and a **node-centred**
version. If the discrete adjoint is new to you, start with the one-dimensional pair.

| 文件 / File | 算例 / Problem | 格式 / Scheme | 大小 / Size |
|---|---|---|---|
| [`adjoint_1d_cell.html`](adjoint_1d_cell.html) | 一维 Burgers/ 1-D Burgers | **格心** / cell-centred | 835 KB |
| [`adjoint_1d_node.html`](adjoint_1d_node.html) | 一维 Burgers/ 1-D Burgers | **格点** / node-centred | 839 KB |
| [`adjoint_cell.html`](adjoint_cell.html) | 二维对流 / 2-D advection | **格心** / cell-centred | 993 KB |
| [`adjoint_node.html`](adjoint_node.html) | 二维对流 / 2-D advection | **格点** / node-centred | 1036 KB |
| [`adjoint_ad_cell.html`](adjoint_ad_cell.html) | 二维对流扩散 / 2-D advection–diffusion | **格心** / cell-centred | 830 KB |
| [`adjoint_ad_node.html`](adjoint_ad_node.html) | 二维对流扩散 / 2-D advection–diffusion | **格点** / node-centred | 966 KB |
| [`adjoint_q1d_cell.html`](adjoint_q1d_cell.html) | 拟一维 Euler / quasi-1-D Euler | **格心** / cell-centred | 243 KB |
| [`adjoint_q1d_node.html`](adjoint_q1d_node.html) | 拟一维 Euler / quasi-1-D Euler | **格点** / node-centred | 243 KB |
| [`adjoint_euler_cell.html`](adjoint_euler_cell.html) | 二维 Euler / 2-D Euler | **格心** / cell-centred | 146 KB |
| [`adjoint_euler_node.html`](adjoint_euler_node.html) | 二维 Euler / 2-D Euler | **格点** / node-centred | 146 KB |

直接用浏览器打开即可：**没有任何外部依赖**，不联网、不需要构建、不需要服务器。
Just open any of them in a browser — **no external dependencies**, no network, no build step,
no server. Each page has a 中文 / English toggle in the top-right corner.

**在线阅读 / Read online:** <https://yishenggaogg.github.io/adjoint_education/>

**仓库 / Repositories:**
[GitHub](https://github.com/yishenggaogg/adjoint_education) ·
[Gitee](https://gitee.com/gaoyishenggg/adjoint_education) — 内容相同 / identical content

---

### 二维 Euler：无激波首版 / 2-D Euler: initial shock-free case

[格心](adjoint_euler_cell.html)与[格点](adjoint_euler_node.html)使用与二维标量逐点、逐单元一致的基础混合网格，继承其页面样式、双语导航和逐面执行结构。理想气体四分量 Euler、一阶 Rusanov 形式通量、滑移压力壁面、亚声速特征远场；Newton / GS 预处理 GMRES 求解原始问题，计算图提供 matrix-free 状态及几何 JVP/VJP。提供来流马赫数、攻角（弧度）与物面节点坐标的 tangent／adjoint 梯度、完整重算差分及独立复数残差检查。

The [cell](adjoint_euler_cell.html) and [node](adjoint_euler_node.html) pages retain the scalar pages’ indexed base mesh, styling, bilingual navigation and face-loop execution structure. Four-component ideal-gas Euler uses first-order Rusanov-form fluxes, pressure slip walls and a subsonic characteristic far field. Newton / GS-preconditioned GMRES solves the primal problem; scalar-operation tapes provide matrix-free state/geometry JVPs and VJPs. Full-rerun finite differences and independent complex residuals verify Mach, incidence (per radian) and body-coordinate gradients.

当前是教学用低马赫数粗网格算例：三层加密数据未建立可靠载荷精度阶，尚无独立连续 Euler 伴随参考。页面明确区分这些限制与离散求导验证，不把压力数值阻力解释为激波或粘性阻力。

This low-Mach teaching case does not establish a reliable order for pressure loads from its three refinement levels, and has no independent continuous Euler adjoint reference. These limitations are separated from discrete derivative verification; numerical pressure drag is not interpreted as shock or viscous drag.

### Burgers 附录 B / Appendix B

两种 1D 页面新增同页中英文[附录 B：间断与激波伴随](adjoint_1d_cell.html#appendix-shocks)。独立的单元平均 Riemann 实验包含移动激波、驻定激波和稀疏波，一阶／minmod 重构、SSP-RK2、matrix-free tangent 和反向时间 adjoint；可查看网格、时间层、限幅分支、完整重算差分及网格加密结果。详细推导激波位移、连续伴随平台和稳态位置不唯一性，并区分离散求导正确与连续伴随一致性。格点页附录采用相同参考有限体积实现，不改变正文格式。

Both 1D pages include bilingual [Appendix B: discontinuities and shock adjoints](adjoint_1d_node.html#appendix-shocks). An independent cell-average Riemann experiment implements moving/stationary shocks and rarefactions, first-order/minmod reconstruction, SSP-RK2, matrix-free tangents and reverse-time adjoints. Mesh/time/limiter inspection, full-rerun finite differences and refinement studies accompany derivations of shock displacement, continuous-adjoint plateaux and steady nonuniqueness. Discrete derivative correctness is explicitly separated from continuous consistency.

### Burgers 一阶／二阶与 GS / Burgers reconstruction and GS

两页默认 N=8，可切换 8、16、32 个区间；一阶／二阶按钮同步改变完整残差、重构、精确 Jacobian、tangent、adjoint 与固定的离散目标。高级选项提供两种入口闭合、每次 1/2/4 次 GS 扫描、GMRES 重启长度和固定点松弛系数。

Burgers 第 12 节可直接选择每个源项、入口或全部变量，对比前向／中心差分，扫描 10⁻¹ 至 10⁻¹² 并自定义步长。支持绝对／分量相对误差、全部分量最大误差、目标值与原始求解残差表、扰动解及网格上的状态差分。所有扰动使用固定目标场并重解完整离散方程。

Burgers Section 12 provides local source/inlet/all-variable selection, forward/central differences, a 10⁻¹–10⁻¹² sweep and custom steps. Inspect absolute/component-relative errors, all-component maxima, objective values, primal residuals, perturbed solutions and state differences on the mesh. Every perturbation re-solves the full discrete equations with the target frozen.


Both pages default to N=8, with 8/16/32 intervals selectable. Spatial-order changes update the full residual, reconstruction, exact Jacobian, tangent, adjoint and frozen discrete target. Advanced controls select inlet closure, 1/2/4 GS sweeps per application, GMRES restart length and fixed-point relaxation.

一阶近似 Jacobian 在当前状态求值。二阶导数不省略重构；GMRES 使用完整的精确算子，并用固定次数、零初值的 GS 扫描作为右预处理。伴随采用对应反向扫描。复数步长独立收敛复数残差的实部和缩放虚部，不声称与 GMRES 逐轮相同。

The first-order approximate Jacobian is evaluated at the current state. Second-order derivatives retain reconstruction; GMRES uses the complete exact operator with fixed, zero-initialised GS sweeps as right preconditioning, reversed for the adjoint. Complex step converges both the real residual and its scaled imaginary part independently; no per-iteration equivalence with GMRES is claimed.

新版基准（N=8、耗散入口、GS 默认容差）：下表是全部源项与入口分量的最大差除以伴随梯度最大分量；中心差分步长 1e-5，复数步长 1e-30。结果受线性停止容差影响，不应套用旧 Jacobi 的机器精度数字。

Revised baseline (N=8, dissipative inlet, default GS tolerances): maximum difference over every source and inlet component, divided by the largest adjoint-gradient component; central FD step 1e-5 and complex step 1e-30. Linear stopping tolerances affect these results.

| 格式 / Scheme | 阶数 / Order | FD 相对差 / relative difference | CS 相对差 / relative difference |
|---|---|---|---|
| cell | 1 | 1.494e-10 | 1.584e-11 |
| cell | 2 | 2.386e-10 | 9.321e-13 |
| node | 1 | 1.069e-10 | 1.416e-11 |
| node | 2 | 2.405e-10 | 3.878e-13 |

同页附录（使用页面语言按钮切换）：[中文](adjoint_1d_cell.html#appendix-continuous) / [English](adjoint_1d_cell.html#appendix-continuous)。

## 十个页面怎么排布 / How the ten pages are arranged

五组算例，每组两种离散。**十页教学主题相互对应**：前 14 节一一对应，第 12 节是差分验证，第 13 节是复数步长，
第 14 节是精度阶，总结都在最后一节；第 11 节在一维那一对里是对源项与入口值的设计导数，其余四对是几何导数；
十页第 15 节均讨论伴随一致性；一维第 16 节新增 GS 预处理 GMRES，总结移到第 17 节，其余八页总结仍为第 16 节。二维 Euler 第 14 节仅报告网格加密结果，第 15 节只给形式连续分析及限制。一维还包含 $J$ 的误差估计。任意两页都能并排对照：
横着比是**两种格式**；竖着比是**方程**——从一维，到二维纯对流，到加上扩散，再到方程组。

Five model problems, each discretised two ways. All ten have **corresponding teaching topics**: their first
14 sections match one to one, Section 12 being the finite-difference check, Section 13 the complex
step and Section 14 the order of accuracy, and the summary always comes last. Section 11 gives
design derivatives with respect to the sources and the inflow value on the one-dimensional pair
and geometric derivatives on the other four. All ten now discuss adjoint consistency in
Section 15. The Burgers pair adds GS-preconditioned GMRES in Section 16 and concludes in Section 17; the other eight conclude in Section 16. The initial 2-D Euler pair reports refinement without an order claim and only formal continuous analysis. The one-dimensional pair also estimates the error in $J$. Any two can be read side by side: across, the **two schemes**; down, **the
equation** — one dimension, then pure advection in two, then diffusion added, then a system.

| | 格心 / cell-centred | 格点 / node-centred |
|---|---|---|
| **一维 Burgers**/ 1-D Burgers | [`adjoint_1d_cell.html`](adjoint_1d_cell.html) | [`adjoint_1d_node.html`](adjoint_1d_node.html) |
| **二维对流** / 2-D advection | [`adjoint_cell.html`](adjoint_cell.html) | [`adjoint_node.html`](adjoint_node.html) |
| **二维对流扩散** / 2-D advection–diffusion | [`adjoint_ad_cell.html`](adjoint_ad_cell.html) | [`adjoint_ad_node.html`](adjoint_ad_node.html) |
| **拟一维 Euler** / quasi-1-D Euler | [`adjoint_q1d_cell.html`](adjoint_q1d_cell.html) | [`adjoint_q1d_node.html`](adjoint_q1d_node.html) |
| **二维 Euler** / 2-D Euler | [`adjoint_euler_cell.html`](adjoint_euler_cell.html) | [`adjoint_euler_node.html`](adjoint_euler_node.html) |

### 一维直接伴随 / Direct one-dimensional adjoints

Burgers：[格心附录 C](adjoint_1d_cell.html#appendix-c) / [格点附录 C](adjoint_1d_node.html#appendix-c)。拟一维 Euler：[格心附录 C](adjoint_q1d_cell.html#appendix-c) / [格点附录 C](adjoint_q1d_node.html#appendix-c)。

四页的一阶、二阶均提供**显式矩阵＋带主元 LU 直接求解**，这里不采用 matrix-free 求解。Burgers 按面解析组装完整 Jacobian，Euler 通过精确导数列显式组装；随后存储转置矩阵并做 LU、前代和回代。matrix-free 算子只在直接解完成后用于独立残差验证，正文原有迭代路径保留。交互展示完整矩阵、消元步骤、网格伴随值及包含组装的实测耗时。

All four pages offer **explicit matrices and pivoted-LU direct solves** for both spatial orders. This appendix does not use a matrix-free solve. Burgers assembles the complete Jacobian analytically face by face; Euler assembles exact derivative columns. Both store the transpose and use LU plus triangular substitution. Matrix-free products independently verify the final residual only; the main iterative path remains available. Inspect matrices, elimination stages, adjoint mesh values and timings including assembly.

Burgers 新增 168 项检查通过，覆盖两种网格、两种阶数、8／16／32 区间及两种入口闭合，最大直接残差 4.81×10⁻¹⁷。Euler 的 204 项直接法检查通过，最大残差 4.67×10⁻¹⁶。小网格通常适合直接法；计时现场测量，不预设所有设备上的速度排名。

The 168 Burgers checks span both grids/orders, 8/16/32 intervals and both inlet closures (maximum direct residual 4.81×10⁻¹⁷). Euler passed 204 direct-solver checks (maximum residual 4.67×10⁻¹⁶). Small grids favour direct methods; live timings determine the actual ranking.

### 连续伴随与一致性 / Continuous adjoints and consistency

二维 Euler 首版例外：只提供形式方程、壁面变分与验证范围，未提供独立连续参考。The initial 2-D Euler pair provides formal equations and boundary variations, without an independent continuous reference.

正文第 15 节保留一致性结论，原八页同页附录 A 给出分部积分、目标对应的伴随边界条件，以及独立连续解和原离散伴随的加密比较；并区分不一致、无解、不唯一和不稳定，用特征线反例解释边界条件的适定性。完整推导见 [中文版](adjoint_ad_cell.html#appendix-continuous)。

- **对流扩散**：独立有限元连续参考，壁面伴随值为 1，远场按原数值总通量解释为 Robin 条件；验证远场值导数。
- **拟一维 Euler**：等熵原始解与连续伴随边值 ODE，分别检验反设计和推力目标；保留形状导数的端点项。
- **二维纯对流**：原零通量内壁缺少光滑正值连续参考；明确说明限制，并另外计算特征边界对照的解析伴随，不能把对照当成原边界的验证。

Section 15 retains the conclusions; the same-page Appendix A derives the Green identities and objective-dependent boundary conditions, then compares independent continuous references with refined discrete adjoints. It distinguishes inconsistency from nonexistence, nonuniqueness and instability through explicit characteristic examples. The [full English derivation](adjoint_ad_cell.html#appendix-continuous) records assumptions and evidence limits. Advection–diffusion uses an independent FEM reference with wall dual value one and the implemented total-flux Robin far field; quasi-1-D uses an isentropic primal and a continuous dual boundary-value ODE for both objectives. The original scalar zero-flux body has no smooth positive reference of this kind, so its characteristic-boundary contrast is explicitly separate.

二维标量的连续参考面板浏览内嵌的**离线计算结果**；拟一维 Euler 的附录 A 在浏览器中独立积分连续伴随 ODE，并与等熵流场差分比较。它们不引入外部运行依赖。加密误差下降是所测网格族的证据，不是任意网格、激波或边界最大范数的收敛证明。

The six new viewers contain **offline-computed results**, not browser PDE solves, and add no runtime dependencies. Refinement trends are evidence for the tested families, not convergence proofs for arbitrary grids, shocks or boundary maximum norms.

### 横着比：两种格式的边界条件 / Across: what the two schemes do at a boundary

这是每一组里两页的分歧所在。**格心格式**的未知量是单元平均值，边界上没有任何自由度，
所以边界条件只能**弱**加——在通量里给一个外侧状态。**格点格式**的边界节点<u>就在边界上</u>，
它本身就是未知量，所以可以**强**加——直接把它的方程换掉。伴随里对应的是「进循环前清零、
出循环后加回」，而且顺序不能反。五组算例分别展示这些处理：

- **一维 Burgers**：只有入口一个条件 $u(0)=u_{\mathrm{in}}$，出口的通量就是物理通量。格心页把 $u_{\mathrm{in}}$
  当作入口面左侧的 ghost 状态（弱加）；格点页把节点 0 的整行换成 $u_0-u_{\mathrm{in}}$（强加）。
  照搬前向的写法、在伴随循环之后直接覆盖 $y_0\leftarrow w_0$，点积测试就失败。
- **二维对流**：纯对流方程只能在特征线进入区域的地方给边界数据。物面采用零数值通量闭合（不是相容的光滑连续滑移壁面），
  远场按特征方向取来流值或外推——两页都在通量里弱加，**没有**强加，也**没有** Dirichlet 壁面：
  在特征线离开区域的那部分物面上，它会多出一个条件。
- **二维对流扩散**：扩散项让 Dirichlet 壁面 $u=u_w$ 在整条物面上都适定。格心页把 $u_w$
  放进壁面面的通量与最小二乘模板（弱加）；格点页把壁面节点的整行换成 $u_i-u_w$（强加）。
- **拟一维 Euler**：边界条件是内点状态的非线性函数。格心页用特征关系重构一个 ghost 状态
  （弱加）；格点页只替换节点的**部分行**（强加）。

That is where the two pages in each row part company. A **cell-centred** scheme's unknowns are
cell averages and no degree of freedom sits on the boundary, so the conditions can only be
imposed **weakly**, through an outer state in the flux. A **node-centred** scheme's boundary
node <u>is</u> on the boundary and is itself an unknown, so the conditions can be imposed
**strongly**, by replacing its equations — which the adjoint answers with "zero before the
loop, add back after", in that order and no other. The four rows go through this four times:

- **1-D Burgers**: a single condition, $u(0)=u_{\mathrm{in}}$ at the inflow; the flux at the outflow
  is the physical one. The cell-centred page makes $u_{\mathrm{in}}$ the ghost state on the left of
  the inflow face (weak); the node-centred page replaces node 0's whole row by $u_0-u_{\mathrm{in}}$
  (strong). Copying the forward code and overwriting $y_0\leftarrow w_0$ after the adjoint loop
  fails the dot test.
- **2-D advection**: a purely convective equation takes boundary data only where characteristics
  enter. The body uses a zero numerical flux (not a compatible smooth continuum slip wall) and the far field takes the free stream or
  extrapolates, by the characteristic direction — both pages impose everything weakly, through
  the flux. There is **no** strong imposition and **no** Dirichlet wall, which would be one
  condition too many where characteristics leave the body.
- **2-D advection–diffusion**: the diffusion term makes a Dirichlet wall $u=u_w$ well posed
  along the whole body. The cell-centred page puts $u_w$ into the wall faces' flux and the
  least-squares stencils (weak); the node-centred page replaces each wall node's whole row by
  $u_i-u_w$ (strong).
- **Quasi-1-D Euler**: the boundary conditions are nonlinear functions of the interior state.
  The cell-centred page reconstructs a ghost state from characteristic relations (weak); the
  node-centred page replaces **some** of a node's rows (strong).

### 竖着比：从标量到方程组 / Down: from a scalar to a system

| | 一维 Burgers / 1-D Burgers | 二维对流 / 2-D advection | 二维对流扩散 / 2-D advection–diffusion | 拟一维 Euler / quasi-1-D Euler |
|---|---|---|---|---|
| 每个自由度 / Per unknown | 一个数 / one number | 一个数 / one number | 一个数 / one number | 三个数 ρ, ρu, ρE / three |
| 残差 / Residual | 面循环加源项 / a face loop and a source | 一个面循环 / one face loop | **两遍**：先最小二乘梯度、后通量 / **two loops**: least-squares gradients, then fluxes | 面循环加源项 / a face loop and a source |
| 局部导数 / Local derivative | $c_L,c_R$ 及重构链 / flux derivatives and reconstruction chain | 两个数 $c_L,c_R$ / two numbers | 两个数，外加一条经过梯度的路径 / two numbers, plus a path through the gradients | 两个 **3×3 块** / two **3×3 blocks** |
| Jacobian 的一行 / A row of the Jacobian | 一阶三对角，二阶五对角 / tridiagonal at first order, five diagonals at second order | 相邻的未知量 / adjacent unknowns | **邻居的邻居**；Jacobi 迭代只用它的对角元 / **neighbours of neighbours**; the Jacobi iteration uses only its diagonal | 一阶相邻块；二阶扩展到重构邻域 / adjacent blocks at first order; extended reconstruction stencil at second order |
| 源项 / Source term | 有，逐区间常数，就是设计变量 / yes, constant on each interval: the design variables | 没有 / none | 没有 / none | 有，且不经过任何面 / yes, crossing no face |
| 边界条件 / Boundary conditions | 入口值 $u_{\mathrm{in}}$ / the inflow value | 零通量壁面、特征远场 / a zero-flux wall, a characteristic far field | Dirichlet 壁面 $u=u_w$ / a Dirichlet wall | 内点状态的**非线性函数** / **nonlinear functions** of the interior |
| 强加的形状 / Shape of strong imposition | 整行换成 $e_0^{\mathsf T}$ / the whole row becomes $e_0^{\mathsf T}$ | 没有强加 / none | 整行换成 $e_i^{\mathsf T}$ / the whole row becomes $e_i^{\mathsf T}$ | **部分行**换成约束梯度 / **partial rows** become constraint gradients |
| 信息传播 / Information travels | 单向 / one way | 单向（纯对流）/ one way | 双向（扩散）/ both ways (diffusion) | 双向（亚声速）/ both ways (subsonic) |
| 设计变量 / Design variables | 默认 8 个区间源项与 $u_{\mathrm{in}}$ / 8 interval sources by default and $u_{\mathrm{in}}$ | 48 个网格坐标 / 48 mesh coordinates | 48 个网格坐标 / 48 mesh coordinates | 默认 13 个截面积及 3 个边界参数 / 13 areas and 3 boundary parameters by default |

一维那一对：面通量取二维对流页的 $n=1$，二阶时增加面值重构，网格小到每个数组、
整个 Jacobian 都能完整摆在页面上；设计变量换成源项与入口值，所以不需要任何网格导数，一次伴随
求解直接给出全部设计导数（默认 9 个）。二维对流那一对页面在第 2 节的注里说过一句话：「把标量换成状态向量、把局部导数换成块矩阵即可。」
拟一维那一对就是把这句话兑现出来——并且顺带说明，兑现过程中会冒出源项、非线性边界条件
和双向传播这些二维标量模型里根本不存在的东西。对流扩散那一对留在标量上，只加一个二阶项：
梯度要先算出来，残差变成两遍循环，精确 Jacobian 伸到邻居的邻居——伴随要用的精确算子从这里
开始不再只连相邻的未知量，matrix-free 的 Jacobi 迭代却照样只需要它的对角元；Dirichlet 壁面
也在这里才有了适定的位置。

The one-dimensional pair uses the two-dimensional advection face flux with normal $n=1$, adding reconstruction at second order, on a grid small enough for every
array and the whole Jacobian to fit on the page; the design variables are the sources and the
inflow value, so no mesh derivative is needed and one adjoint solve gives all design derivatives (nine by default).
In a note in Section 2 the two-dimensional advection pair makes a promise: "replace the scalar
by a state vector and the local derivatives by block matrices." The quasi-one-dimensional pair
delivers on it — and shows that delivering on it brings out a source term, nonlinear boundary
conditions and two-way propagation, none of which the two-dimensional scalar model contains at all. The
advection–diffusion pair stays with a scalar and adds one second-order term: the gradients have
to be computed first, the residual becomes two loops, and the exact Jacobian reaches the
neighbours of neighbours — the exact operator the adjoint needs no longer couples adjacent
unknowns only, yet the matrix-free Jacobi iteration still needs no more than its diagonal. It is
also where a Dirichlet wall is finally well posed.

## 四个模型问题 / The four model problems

**一维 Burgers / 1-D Burgers**— 带源项的定常 Burgers 方程
$\frac{\mathrm d}{\mathrm dx}\big(\tfrac12u^2\big)=s(x)$，$0<x<1$，$u(0)=u_{\mathrm{in}}=1$；面通量是二维页的
通量取 $n=1$：$h=\tfrac14(u_L^2+u_R^2)-\varepsilon(u_R-u_L)$，$\varepsilon=0.8$；8 个单元（格心）或 9 个节点
（格点）；源项在 8 个区间上逐段为常数，当前设计 $\sigma=0.5$（精确解 $u=\sqrt{1+x}$）；目标是反设计
$J=\tfrac12\sum_iw_i(u_i-\bar u_i)^2$，$\bar u$ 是源项取 $\sin\pi x$ 的区间平均时的解；设计变量是 8 个区间
源项与 $u_{\mathrm{in}}$。

**二维对流 / 2-D advection** — 标量守恒律 $F(u)=\tfrac12u^2\beta$，$\beta=(1,\,0.5)$，常数耗散
$\varepsilon=0.8$；环形 O 型混合网格（8 个四边形 + 16 个三角形，24 个未知量）；内圈物面是
零数值通量闭合（连续相容性限制见第 15 节）、外圈远场特征边界；目标是类似阻力的物面积分；设计变量是全部 48 个
节点坐标。

**二维对流扩散 / 2-D advection–diffusion** — 同一个对流通量（同样的 $\beta$ 与 $\varepsilon$），
加上常数扩散 $\nu=0.5$：$\nabla\cdot(\tfrac12u^2\beta)-\nabla\cdot(\nu\nabla u)=0$；扩散通量是
沿两侧连线的两点差，加上两侧最小二乘梯度（不加权）平均后的非正交修正；网格同上；物面
$u=u_w=0$，远场数值通量使用 $u_\infty=1$、不另加扩散面通量（连续极限按总通量 Robin 条件解释，见第 15 节）；目标是流进物面的总通量；设计变量同样是 48 个
节点坐标。

**拟一维 Euler / quasi-1-D Euler** — 变截面流道 $A(x)=1-0.3\sin^2(\pi x)$，两端为 1、喉部 0.7；
入口给**总压与总温**、出口给**背压**，全场亚声速；Rusanov 通量（耗散系数取两侧平均而非
$\max$，以保可微）；目标有两个可切换：**反设计**（压力分布匹配）与**推力**；设计变量是
13 个截面积及出口背压、入口总压和总温。

一维 Burgers 支持一阶常值和二阶线性重构。原始方程采用一阶近似 Jacobian 的 GS 预估矫正；精确 tangent / adjoint 可选 GS 固定点或 **GS 预处理 GMRES**。一阶矩阵仅参与修正与预处理，精确导数始终对应完整离散残差。拟一维 Euler 同样支持一阶／二阶重构，采用 3×3 块 GS 固定点或 GS 预处理 GMRES；一次预处理从零开始做 12 次 GS 扫描，并对整个映射实施精确转置。二维标量四页保留 Jacobi。

**1-D Burgers** — the steady Burgers equation with a source,
$\frac{\mathrm d}{\mathrm dx}\big(\tfrac12u^2\big)=s(x)$ on $0<x<1$, $u(0)=u_{\mathrm{in}}=1$; the face flux is that
of the two-dimensional pages at $n=1$, $h=\tfrac14(u_L^2+u_R^2)-\varepsilon(u_R-u_L)$, $\varepsilon=0.8$; 8 cells
(cell-centred) or 9 nodes (node-centred); the source is constant on each of the 8 intervals, $\sigma=0.5$ in the
current design (exact solution $u=\sqrt{1+x}$); the objective is inverse design,
$J=\tfrac12\sum_iw_i(u_i-\bar u_i)^2$, with $\bar u$ the solution for the interval averages of $\sin\pi x$; the
design variables are the 8 interval sources and $u_{\mathrm{in}}$.

The Burgers pair supports first-order constant states and second-order linear reconstruction. Its primal uses GS predictor–corrector with a first-order approximate Jacobian; exact tangent and adjoint equations offer GS fixed point or **GS-preconditioned GMRES**. The first-order matrix is used only for correction and preconditioning. Quasi-1-D Euler also supports both orders, 3×3 block-GS defect correction and GS-preconditioned GMRES. Each preconditioner application performs 12 zero-start GS sweeps with an exact transpose of the full map. The four 2-D scalar pages retain Jacobi.

## 每页的各节 / The sections

1. 网格（或流道）/ Mesh, or the duct
2. 方程与面上的一维通量 / The equations and the one-dimensional flux
3. 边界条件 / Boundary conditions
4. 残差 = 循环：收集、计算、分发（对流扩散页是两遍：先梯度、后通量）/ Residual = the loop:
   gather, compute, scatter (two loops on the advection–diffusion pages: gradients, then fluxes)
5. 求解：Jacobian 与迭代（Burgers 与拟一维为 GS，二维 Euler 为 GS-GMRES）/ Jacobian and iteration (GS for Burgers and quasi-1-D; GS-GMRES for 2-D Euler)
6. 目标函数 / The objective function
7. matrix-free 前向：计算 $Av$ / Matrix-free forward
8. matrix-free 伴随：计算 $A^{\mathsf T}w$ / Matrix-free adjoint
9. 前向求解：切线方程 / The forward solve: the tangent equation
10. 伴随求解：伴随方程 / The adjoint solve: the adjoint equation
11. 几何导数（一维页：设计导数）/ Geometric derivatives (the 1-D pages: design derivatives)
12. 验证：对有限差分 / Verification against finite differences
13. 复数步长：独立检查收敛方程的总导数；二维标量四页还逐轮对照 Jacobi 前向迭代 / Complex step: independently check total derivatives of the converged equations; the four 2-D scalar pages also compare Jacobi iterates
14. 精度阶：构造解检验 / Order of accuracy: a manufactured solution
15. 连续伴随与伴随一致性；一维还含 $J$ 的误差估计 / Continuous adjoints and adjoint consistency; the 1-D pair also estimates the error in $J$
16. Burgers 与拟一维 Euler：GS 固定点与 GS 预处理 GMRES；其余六页：总结 / Burgers and quasi-1-D Euler: GS fixed point and GS-preconditioned GMRES; other six: summary
17. Burgers 与拟一维 Euler：总结 / Burgers and quasi-1-D Euler: summary

拟一维新版使用精确 Jacobian 算子 $A_2$ 与一阶近似 $P$，截面积以 $A(x)$ 表示；连续附录使用 $B=F_U$ 表示物理通量 Jacobian。
The quasi-1-D edition distinguishes the exact operator $A_2$, low-order approximation $P$, duct area $A(x)$ and continuous flux Jacobian $B=F_U$.

## 可以动手的地方 / What is interactive

交互面板与图表由数值代码生成；Burgers 新版新增空间阶数、GS 扫描与 GMRES 对照：

- **网格／流道浏览器**：点任意单元或节点，看它的面、法向、守恒量、源项与残差；对流扩散页还画出
  它的最小二乘梯度模板
- **最小二乘梯度**（对流扩散页）：选一个单元或节点，看它的模板、矩阵 $M_i$、每个权重和算出的梯度；
  换成线性场，每个点上的梯度都精确到舍入误差
- **一个面上的通量**：拖动两侧状态，看中心项与耗散项怎样组成数值通量；对流扩散页把扩散通量拆成
  两点差与梯度修正；拟一维页逐面显示一阶／二阶重构及其依赖权重
- **三个循环逐句播放**：primal、tangent、adjoint 各一个，每一行伪代码对应一步，
  数组里的数字随之变化——转置在数据流上长什么样，一眼可见；对流扩散页的每个循环分两遍，
  伴随先倒着走通量那一遍、再倒着走梯度那一遍
- **点积测试**：随机向量，现场验证 $\langle w,Av\rangle=\langle A^{\mathsf T}w,v\rangle$；
  对流扩散格点页可对照错误入口行处理；一维页还检验 GS 预处理的转置关系
- **三个求解过程**：Burgers 与拟一维 Euler 展示 GS 与 GMRES；拟一维提供原始迭代快照、逐块 GS 扫描、前向和伴随真残差。二维标量保留 Jacobi 迭代交互。
- **流进物面的通量**（对流扩散页）：逐个壁面面或壁面节点看它吸收的通量；格点页把一致的反作用量
  与单侧差分公式并排对照
- **拟一维精确算子与低阶矩阵**：精确 tangent／adjoint 沿计算图实施，不组装精确二阶矩阵；另展示一阶近似矩阵与 3×3 块 GS 扫描。
- **拟一维连续伴随**：同页附录 A 展开变分、两端零空间边界、面积及边界数据导数；独立 RK4 射击法支持步数切换。附录 B 提供正激波跳跃与固定界面导数计算，新增独立的全流道激波拟合、未知位置求解与约化标量伴随；并非激波捕捉有限体积伴随或完整连续伴随场。
- **BFGS 反设计**（一维页）：每个候选设计重新求解 primal 和伴随，经回溯接受下降步；入口值不动，因为它和第一个区间的源项几乎可以互相替代
- **复数步长与前向迭代，逐轮对照**（二维标量四页）：选一个设计变量和起点，两条迭代的残差与它们逐轮之差画在一起。
  从收敛流场出发，复数迭代的虚部每一轮都等于前向迭代；从初始流场出发，两者只在收敛时相遇。图下的表把
  复数步长、伴随与中心差分给出的梯度并排列出
- **哪一种检验抓哪一种错误**（一维页）：比较精确导数、两侧共同误用一阶 Jacobian、伴随符号错误；点积检验与独立复数残差检验相互补充。
- **两种入口下的离散伴随与连续伴随**（一维页）：比较全域和固定内部区域误差、首源项导数比、光滑方向导数及入口导数。二阶格点迎风处理仍可能有伴随边界层。
- **差分验证与步长扫描**：二维标量四页可选差分格式（中心／前向）与步长 $h$；一维页按所选参数计算中心差分步长扫描，并独立检查复数步长，逐分量用全链路差分对照伴随梯度；
  底部扫描相对误差随步长的变化，截断与舍入怎样围出最优步长一目了然。拟一维页支持全部面积及边界设计变量（默认 16 个）、中心／前向／后向差分和 12 个步长的完整重求解扫描

Interactive panels show meshes, face fluxes, reconstruction, forward/reverse accumulation, solver residuals and full-rerun gradient checks. The four 2-D scalar pages retain their Jacobi iteration players. The quasi-1-D Euler pair now provides first/second-order reconstruction, primal snapshots, block-GS scans, matrix-free derivatives, GS/GMRES comparison, all area and boundary parameter gradients (16 by default), three finite-difference formulas over 12 step sizes, and independently converged complex residuals. Its same-page continuous appendix solves an independent ODE in the browser; its shock appendix adds independent full-duct shock fitting, an unknown shock position and a reduced scalar adjoint, alongside local jumps and interface analysis. This is not a shock-capturing finite-volume adjoint or a full continuous-adjoint field.

The Burgers pages add a global spatial-order switch, reconstruction and transpose players, a row-by-row GS scan, GS/GMRES work comparisons, source-only BFGS steps with line search, and independently converged complex-step checks. Boundary studies separate interior accuracy, global boundary layers and design sensitivities; second-order node-based upwinding is not automatically adjoint consistent.

## 页面上的数字都是实测的 / Every number is measured

拟一维 Euler 新版完成 1,110 项数值检查，覆盖格心／格点、一阶／二阶、推力／反设计、GS／GMRES，以及全部 16 个设计变量。中心差分（h=10⁻⁵）与伴随的最大绝对差为 2.02×10⁻⁹，复数步长为 1.51×10⁻¹¹；完整状态和参数转置点积差为 1.43×10⁻¹⁴。连续 RK4 射击解与独立配点边值解的最大差为 2.20×10⁻¹¹（推力）、1.40×10⁻¹²（反设计）。二阶最后一档实测状态收敛阶为 1.903（格心）与 1.912（格点）。

The revised quasi-1-D pair passed 1,110 numerical checks across both grids, orders, objectives and solvers, testing all 16 parameters. Maximum absolute gradient differences were 2.02×10⁻⁹ for full-rerun central differences (h=10⁻⁵) and 1.51×10⁻¹¹ for complex step; the joint state/parameter transpose discrepancy was 1.43×10⁻¹⁴. The continuous RK4 shooting solution agrees with independent boundary-value collocation within 2.20×10⁻¹¹ (thrust) and 1.40×10⁻¹² (inverse design). Final-grid second-order state rates are 1.903 (cell) and 1.912 (node).

以下保留二维标量与旧版拟一维一阶 Jacobi 实现的历史校验，**旧版拟一维数据不代表当前二阶／GS 页面**。当前拟一维数据见上段和页面现场计算。连续加密图使用预先独立求解的数据，拟一维连续 ODE 交互则在浏览器中重新计算。

The tables below retain historical checks for the scalar pages and the former first-order quasi-1-D Jacobi implementation. **Historical quasi-1-D values do not describe the current second-order/GS pages.** Use the new results above and live page calculations for the current implementation.

| 页面 / Page | 点积测试 / dot test | 几何点积测试 / geometric dot test | 梯度对全链路差分 / gradient vs full-chain FD | 漏掉一步的后果 / cost of one missing step |
|---|---|---|---|---|
| 二维对流 格心 / 2-D advection, cell | 0 ¹ | 3.6e−11 ² | 4.0e−10 | — |
| 二维对流 格点 / 2-D advection, node | 0 ¹ | 1.1e−10 ² | 3.6e−10 | — |
| 二维对流扩散 格心 / 2-D advection–diffusion, cell | 0 ¹ | — | 3.7e−9 | — |
| 二维对流扩散 格点 / 2-D advection–diffusion, node | 1.9e−16 | — | 3.4e−9 | 56 % ⁴ |
| 拟一维 格心 / quasi-1-D, cell | 4.64e−16 | **1.95e−16** ³ | 3.6e−9 | 10⁻⁴ 到 10⁻¹ / 10⁻⁴ to 10⁻¹ ⁵ |
| 拟一维 格点 / quasi-1-D, node | 6.64e−16 | **4.48e−16** ³ | 2.0e−9 | **108 %** ⁶ |

点积测试是打开页面时点积面板显示的相对误差；几何点积测试，二维对流页是第 11 节正文引用的偏差，
拟一维页是面板上的相对偏差；全链路差分是中心差分、$h=10^{-6}$，每次都重新求解，取所有分量与
伴随梯度之差的最大值，除以梯度的最大分量（拟一维取反设计目标）。「—」表示该页没有这一项。

The dot tests are the relative errors each page's panel shows on opening. The geometric dot
tests are the deviation quoted in Section 11 on the advection pages, and the relative deviation
the panel shows on the quasi-one-dimensional pages. The full-chain differences are central, $h=10^{-6}$, re-solving every time; the
largest difference from the adjoint gradient over all components, divided by the gradient's
largest component (the inverse-design objective on the quasi-one-dimensional pages). A dash
means the page has no such check.

¹ 第一对随机向量恰好逐比特相等；再抽几对，就落在 $10^{-16}$ 到 $10^{-15}$ 之间。
² 被差分步长卡住：二维对流页没有解析的前向几何算子，前向那一侧由中心差分逐列装配。
³ 两个方向都解析，所以落在机器精度——这也说明二维对流页那个 $10^{-11}$ 是差分的锅，不是转置的锅。
⁴ 组装几何梯度前忘记把 $\psi$ 在壁面行上清零：差 0.18，梯度的量级是 0.32。
⁵ 伴随里漏掉源项：点积测试的相对误差，随所取的向量而定。
⁶ 组装几何梯度前忘记把 $\Psi$ 在约束行上清零（反设计；推力目标是 4%）。

¹ the first random pair happens to agree to the last bit; the next few land between $10^{-16}$
and $10^{-15}$. ² limited by the finite-difference step: the 2-D advection pages have no analytic forward
geometric operator, so that side is assembled column by column from central differences.
³ analytic in both directions, hence machine precision — which also shows the $10^{-11}$ of the
advection pages is the differencing, not the transpose. ⁴ $\psi$ not zeroed on the wall rows
before assembling the geometric gradient: off by 0.18 on a gradient of magnitude 0.32. ⁵ the
source term dropped from the adjoint: the dot test's relative error, depending on the vectors.
⁶ $\Psi$ not zeroed on the constrained rows before assembling the geometric gradient (inverse
design; 4% for thrust).

旧版六页第 13 节的复数步长（拟一维为历史数据）（$h=10^{-30}$）：

Historical Section 13 complex-step checks for the former six pages ($h=10^{-30}$):

| 页面 / Page | 逐轮，从 $u^*$ 出发 / per sweep, from $u^*$ | 逐轮，从初始流场出发 / per sweep, from the initial field | 实部，从 $u^*$ 出发 / real part, from $u^*$ | 复数步长对伴随 / complex step vs adjoint | 中心差分对伴随 / central difference vs adjoint |
|---|---|---|---|---|---|
| 二维对流 格心 / 2-D advection, cell | 2.1e−14 | 1.46 | 逐比特 / to the bit | 2.0e−16 | 4.0e−10 |
| 二维对流 格点 / 2-D advection, node | 1.1e−14 | 1.18 | 逐比特 / to the bit | 2.2e−16 | 3.6e−10 |
| 二维对流扩散 格心 / 2-D advection–diffusion, cell | 5.6e−15 | 2.3 | 1.1e−16 ⁹ | 6.7e−16 | 3.7e−9 |
| 二维对流扩散 格点 / 2-D advection–diffusion, node | 2.2e−15 | 6.1 | 1.1e−16 ⁹ | 3.0e−16 | 3.4e−9 |
| 拟一维 格心 / quasi-1-D, cell | 1.3e−14 | 0.40 | 逐比特 / to the bit | 2.0e−15 ／ 1.6e−13 ¹⁰ | 1.1e−10 ／ 3.6e−9 |
| 拟一维 格点 / quasi-1-D, node | 7.4e−15 | 0.30 | 逐比特 / to the bit | 7.2e−16 ／ 5.0e−14 ¹⁰ | 1.0e−10 ／ 2.0e−9 |

两栏「逐轮」是每一轮的 $\max|\operatorname{Im}u_k/h-v_k|$ 在所有设计变量与所有轮次上的最大值，除以 $\max|v|$；
$v_k$ 是第 9 节的前向 Jacobi 迭代。从收敛流场出发，两者每一轮都相同（到舍入误差）；从初始流场出发，
头几轮就差出 $O(1)$，只在收敛时相遇。实部一栏把复数迭代的实部与同一起点的实数 Jacobi 迭代逐轮对照。
两栏梯度的量法与上表相同。

The two "per sweep" columns are the largest $\max|\operatorname{Im}u_k/h-v_k|$ over every design
variable and every sweep, divided by $\max|v|$, where $v_k$ is the forward Jacobi iteration of
Section 9. Started from the converged flow the two agree at every sweep, to round-off; started from
the initial field they part by $O(1)$ in the first sweeps and meet only at convergence. The real-part
column compares the complex iteration's real part with the real Jacobi iteration from the same start,
sweep by sweep. The two gradient columns are measured as in the table above.

⁹ 实数程序用 `Math.hypot` 求 $|n|$，复数程序用开方，两者的末位舍入在部分面上不同，所以实部只差舍入误差，
不逐比特相同。¹⁰ 推力／反设计。反设计的梯度正比于 $p-p_{\mathrm{target}}$，最大分量只有 $10^{-4}$ 量级；
复数迭代的实部是从 $u^*$ 接着走的实数迭代，沿舍入误差平台漂移约 $3\times10^{-15}$，在这么小的梯度面前显了出来。
这不是复数步长的误差。

⁹ The real code takes $|n|$ from `Math.hypot` and the complex code from a square root; the two round
the last bit differently on some faces, so the real part agrees to round-off rather than to the bit.
¹⁰ Thrust / inverse design. The inverse-design gradient is proportional to $p-p_{\mathrm{target}}$,
its largest component only of order $10^{-4}$; the complex run's real part is the real iteration
continued from $u^*$, which wanders along its round-off floor by about $3\times10^{-15}$, and that
shows against so small a gradient. It is not an error of the complex step.

每一对页面的第 14 节都测格式的精度阶，网格族都由基础网格逐次一致加密得到。伴随给出的是
离散格式的精确导数，而格式的精度阶决定这个导数离连续问题的导数有多远：

- **一维 Burgers**：对照精确单元平均值／节点值，在 N=8…256 上测得一阶与二阶原始解和固定物理扰动 tangent 的网格收敛。默认耗散边界下，二阶内部伴随接近二阶，但全域误差因边界层趋近半阶；连续伴随仍是适定的终端值问题。格心迎风入口改善一致性，格点二阶迎风对照仍有边界层。具体数据随页面边界选项同步切换。
- **二维对流**：一阶，但来得很慢——七层网格上 $L_2$ 阶格心从 0.42 爬到 0.87，格点从 0.47 爬到
  0.82。在这张不规则网格上，格心格式的截断误差几乎不随网格变化，解的误差靠相邻单元之间的抵消
  （超收敛）照样减小。构造解问题的物面按特征方向处理；若照搬本页在每个壁面面上规定通量的做法，
  迎风侧壁面上的最大误差不收敛——那里多了一个条件。
- **二维对流扩散**：只有扩散时两种格式都是二阶（$L_2$ 范数下格心 1.94、2.02、2.01，格点 1.99、
  2.09、2.08）；完整方程受耗散项限制，只有一阶。
- **拟一维 Euler**：一阶，而且很快就到了（$L_2$ 阶格心 0.80、0.91、0.96、0.98、0.99）。两端两个
  边界控制体的截断误差是 $O(1)$，解的误差照样是一阶。

Section 14 of every pair measures the scheme's order, on a mesh family refined uniformly from the
base mesh. The adjoint gives the exact derivative of the discrete scheme; the scheme's order
decides how far that derivative is from the continuous problem's:

- **1-D Burgers**: first- and second-order primal/tangent convergence is measured against exact cell averages or point values on N=8…256. The tangent uses a fixed physical perturbation. With dissipative boundaries, second-order interior adjoint errors approach order two while global errors approach order one-half because of a boundary layer; the continuous adjoint remains well posed. Cell-based upwinding improves consistency, but second-order node-based upwinding can retain a boundary layer. Live tables follow the selected boundary closure.
- **2-D advection**: first order, reached slowly — over seven meshes the $L_2$ order climbs from
  0.42 to 0.87 cell-centred and from 0.47 to 0.82 node-centred. On this irregular mesh the
  cell-centred truncation error hardly changes; the solution error falls anyway, through
  cancellation between neighbouring cells (supraconvergence). The manufactured problem treats
  the body by characteristics: prescribing the flux on every wall face, as the page's wall does,
  leaves a max error on the windward wall that does not converge — one condition too many there.
- **2-D advection–diffusion**: diffusion alone is second order for both schemes (in the $L_2$
  norm 1.94, 2.02 and 2.01 cell-centred, 1.99, 2.09 and 2.08 node-centred), while the full
  equation is only first order, held back by the dissipation.
- **Quasi-1-D Euler**: first order, and quickly (cell-centred $L_2$ orders 0.80, 0.91, 0.96,
  0.98, 0.99). The two boundary control volumes carry an $O(1)$ truncation error; the solution
  error is first order all the same.

反设计目标还有一个更强的检验：目标压力取自一条**已知**的流道，于是在那条流道上 $L$ 与
$\mathrm dL/\mathrm dA$ 都**逐比特为零**——梯度在一个独立构造的最优点上归零，比任何差分
对照都更有说服力。

The inverse-design objective carries a stronger check still: its target pressures come from a
**known** duct, so on that duct both $L$ and $\mathrm dL/\mathrm dA$ are **zero to the last
bit** — a gradient vanishing at an independently constructed optimum is better evidence than
any finite-difference comparison.

第 12 节还专门演示了差分校验本身的陷阱：步长取大取小都会让“验证”看起来像失败，
而点积测试是精确恒等式，根本不含步长。第 13 节的复数步长也没有这个陷阱：它不做减法，步长取 $10^{-30}$。

Section 12 also demonstrates the trap in finite-difference verification itself — too large or
too small a step makes a correct gradient look wrong — which is why the dot-product test,
an exact identity with no step size in it, is the more reliable check. The complex step of
Section 13 has no such trap either: it subtracts nothing, and its step is $10^{-30}$.

---

## 维护：两个仓库的同步 / Keeping the two repositories in sync

本项目同时放在 GitHub 与 Gitee，**内容完全相同**：GitHub 是主仓库（网页由 GitHub Pages
从这里发布，每次推送自动重新部署），Gitee 是镜像（Gitee 已不再提供 Pages 服务）。

The project lives on both GitHub and Gitee with **identical content**. GitHub is primary — the
site is served by GitHub Pages from that repository and redeploys on every push — and Gitee is
a mirror (Gitee no longer offers a Pages service).

本地把 `origin` 配成**同时推送到两个仓库**，所以一条 `git push` 就能更新两边：

The local clone has `origin` configured to **push to both**, so a single `git push` updates
both repositories:

```bash
git clone https://github.com/yishenggaogg/adjoint_education.git
cd adjoint_education
# 第一条会替换默认的 push 地址，第二条再追加，所以两条都要执行
# the first line replaces the default push URL, the second appends — both are needed
git remote set-url --add --push origin https://github.com/yishenggaogg/adjoint_education.git
git remote set-url --add --push origin git@gitee.com:gaoyishenggg/adjoint_education.git
```

配置完成后 `git remote -v` 里 `origin` 会有一个 fetch 地址、两个 push 地址；
`git push` 的输出会出现**两段**，每个仓库一段。Gitee 用 SSH，GitHub 用 HTTPS（`gh auth`）。

Afterwards `git remote -v` shows one fetch URL and two push URLs for `origin`, and `git push`
prints **two** result blocks, one per repository.

检查两边是否一致 / Check that the two are in step:

```bash
git ls-remote https://github.com/yishenggaogg/adjoint_education.git refs/heads/main
git ls-remote git@gitee.com:gaoyishenggg/adjoint_education.git refs/heads/main
```

两个 SHA 相同即同步。若在某个平台的网页端直接改过文件，推送会被拒绝（该仓库多出你本地没有的提交）；
此时先 `git pull gitee main --rebase`（或 `github`）把对方的提交取回来再推，**不要用 `--force`**，
那会抹掉网页端的改动。

If the two SHAs differ — typically because a file was edited in one platform's web UI — the
push is rejected for that remote. Rebase the other side's commits in first with
`git pull gitee main --rebase` (or `github`) and push again. **Do not use `--force`**: it would
discard whatever was committed through the web UI.

---

## 许可 / License

© 2026 Yisheng Gao

本仓库的十个页面、连续伴随推导与本 README 以 **知识共享 署名 4.0 国际（CC BY 4.0）** 许可发布：
您可以自由地共享与改编，包括用于商业目的，只要给出**适当署名**、提供许可协议的链接，
并说明是否作了修改。完整条款见 [`LICENSE`](LICENSE)。

The ten pages, continuous-adjoint derivation and this README are licensed under a
**Creative Commons Attribution 4.0 International License (CC BY 4.0)**. You are free to share
and adapt the material, including for commercial purposes, so long as you give appropriate
credit, provide a link to the licence, and indicate if changes were made. Full terms in
[`LICENSE`](LICENSE).

<https://creativecommons.org/licenses/by/4.0/>

建议的署名 / Suggested attribution:

> Yisheng Gao，《非结构网格格心／格点格式的二维标量方程离散伴随》，CC BY 4.0，
> <https://github.com/yishenggaogg/adjoint_education>

## 二维纯对流扩展 / Scalar-advection extensions

两页保留原正文、静态图、逐句播放器及附录 A，在原有各节末尾嵌入光滑特征边界模型的一阶／二阶扩展。精度开关仅控制新增面板；原零通量模型独立保留，数值不混用。新增内容包括最小二乘重构、面积分、matrix-free tangent／adjoint、GS 预处理 GMRES、全部 49 个参数的三种差分及 12 个步长扫描、复数步长和精度阶对照。同页附录 B 推导并计算新模型的连续伴随。

Both pages preserve their original prose, static diagrams, statement-by-statement players and Appendix A. Each existing section embeds a smooth characteristic-boundary extension with first/second-order reconstruction. The selector controls only the added panels; the original zero-flux problem remains separate. Extensions include least-squares reconstruction, face quadrature, matrix-free tangent/adjoint, GS-preconditioned GMRES, three finite-difference formulas over 12 steps for all 49 parameters, complex step and refinement comparisons. Same-page Appendix B derives and computes the new model’s continuous adjoint.

## 拟一维 Euler 参数与激波拟合实验 / Quasi-1-D Euler parameter and shock-fitting experiments

光滑算例可选择 6／12／24 个网格区间、面积收缩深度、出口背压、入口总压和总温，连续参考使用同一组参数。差分节分别展示原始求解容差与伴随线性容差对梯度验证的影响。固定默认参数的离线精度阶表与当前交互结果明确区分。

The smooth case exposes 6/12/24 grid intervals, contraction depth, back pressure, inlet total pressure and total temperature. Its continuous reference uses the same parameters. The finite-difference section independently varies primal and adjoint linear tolerances. Offline default-parameter refinement data remain explicitly separate.

附录 B.5 采用独立阻塞流道：等熵光滑区域与正激波跳跃决定出口压力，求根得到激波位置；约化伴随给出背压梯度。交互提供马赫数图、界面位移项、遗漏界面项的错误梯度、重求激波位置的差分和守恒检查，并内嵌完整实现。新增验证包括 21 组参数／连续参考／容差检查及 108 项激波拟合检查。

Appendix B.5 uses an independent choked duct: isentropic smooth regions and normal-shock jumps determine exit pressure, whose root fixes shock position. A reduced adjoint provides back-pressure gradients. The experiment includes a Mach plot, interface-motion contribution, the incorrect gradient when that term is omitted, full-rerun finite differences, conservation checks and complete embedded source. Added validation covers 21 parameter/reference/tolerance cases and 108 shock-fitting checks.
