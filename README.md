# 离散伴随教学页 / Discrete adjoint, taught page by page

**八个**单文件、可交互的网页，把有限体积法的**全离散伴随**从头到尾讲一遍：
从一个面上的一维通量开始，把同一个循环依次改写成 primal、matrix-free 前向（$Av$）与
matrix-free 伴随（$A^{\mathsf T}w$），再做前向与伴随求解、几何导数，最后用有限差分逐项校验。
四组算例——**一维 Burgers 方程**（入门）、**二维标量对流方程**、**二维标量对流扩散方程**与
**拟一维 Euler 方程**——各有**格心**与**格点**两版。第一次接触离散伴随，请从一维那一对读起。

**Eight** self-contained, interactive web pages that develop the **fully discrete adjoint**
of a finite-volume scheme end to end: starting from the one-dimensional flux on a single
face, the same loop is rewritten as the primal, as matrix-free forward mode ($Av$) and as
matrix-free adjoint mode ($A^{\mathsf T}w$), followed by the forward and the adjoint solve, the
geometric derivatives and a term-by-term finite-difference verification. Four model problems &mdash;
the **one-dimensional Burgers equation** (introductory), a **two-dimensional scalar advection
equation**, a **two-dimensional scalar advection&ndash;diffusion equation** and the
**quasi-one-dimensional Euler equations** &mdash; each in a **cell-centred** and a **node-centred**
version. If the discrete adjoint is new to you, start with the one-dimensional pair.

| 文件 / File | 算例 / Problem | 格式 / Scheme | 大小 / Size |
|---|---|---|---|
| [`adjoint_1d_cell.html`](adjoint_1d_cell.html) | 一维 Burgers（入门）/ 1-D Burgers (introductory) | **格心** / cell-centred | 532 KB |
| [`adjoint_1d_node.html`](adjoint_1d_node.html) | 一维 Burgers（入门）/ 1-D Burgers (introductory) | **格点** / node-centred | 549 KB |
| [`adjoint_cell.html`](adjoint_cell.html) | 二维对流 / 2-D advection | **格心** / cell-centred | 676 KB |
| [`adjoint_node.html`](adjoint_node.html) | 二维对流 / 2-D advection | **格点** / node-centred | 748 KB |
| [`adjoint_ad_cell.html`](adjoint_ad_cell.html) | 二维对流扩散 / 2-D advection–diffusion | **格心** / cell-centred | 610 KB |
| [`adjoint_ad_node.html`](adjoint_ad_node.html) | 二维对流扩散 / 2-D advection–diffusion | **格点** / node-centred | 775 KB |
| [`adjoint_q1d_cell.html`](adjoint_q1d_cell.html) | 拟一维 Euler / quasi-1-D Euler | **格心** / cell-centred | 558 KB |
| [`adjoint_q1d_node.html`](adjoint_q1d_node.html) | 拟一维 Euler / quasi-1-D Euler | **格点** / node-centred | 541 KB |

直接用浏览器打开即可：**没有任何外部依赖**，不联网、不需要构建、不需要服务器。
Just open any of them in a browser — **no external dependencies**, no network, no build step,
no server. Each page has a 中文 / English toggle in the top-right corner.

**在线阅读 / Read online:** <https://yishenggaogg.github.io/adjoint_education/>

**仓库 / Repositories:**
[GitHub](https://github.com/yishenggaogg/adjoint_education) ·
[Gitee](https://gitee.com/gaoyishenggg/adjoint_education) — 内容相同 / identical content

---

## 八个页面怎么排布 / How the eight pages are arranged

四组算例，每组两种离散。**八页结构完全平行**：前 14 节一一对应，第 12 节是差分验证，第 13 节是复数步长，
第 14 节是精度阶，总结都在最后一节；第 11 节在一维那一对里是对源项与入口值的设计导数，其余三对是几何导数；
一维那一对还多一节（第 15 节：伴随一致性与 $J$ 的误差估计），所以它的总结是第 16 节。任意两页都能并排对照：
横着比是**两种格式**；竖着比是**方程**——从一维，到二维纯对流，到加上扩散，再到方程组。

Four model problems, each discretised two ways. All eight are **strictly parallel**: their first
14 sections match one to one, Section 12 being the finite-difference check, Section 13 the complex
step and Section 14 the order of accuracy, and the summary always comes last. Section 11 gives
design derivatives with respect to the sources and the inflow value on the one-dimensional pair
and geometric derivatives on the other three, and the one-dimensional pair adds a section
(Section 15: adjoint consistency and estimating the error in $J$), so its summary is Section 16. Any two can be read side by side: across, the **two schemes**; down, **the
equation** — one dimension, then pure advection in two, then diffusion added, then a system.

| | 格心 / cell-centred | 格点 / node-centred |
|---|---|---|
| **一维 Burgers**（入门）/ 1-D Burgers (introductory) | [`adjoint_1d_cell.html`](adjoint_1d_cell.html) | [`adjoint_1d_node.html`](adjoint_1d_node.html) |
| **二维对流** / 2-D advection | [`adjoint_cell.html`](adjoint_cell.html) | [`adjoint_node.html`](adjoint_node.html) |
| **二维对流扩散** / 2-D advection–diffusion | [`adjoint_ad_cell.html`](adjoint_ad_cell.html) | [`adjoint_ad_node.html`](adjoint_ad_node.html) |
| **拟一维 Euler** / quasi-1-D Euler | [`adjoint_q1d_cell.html`](adjoint_q1d_cell.html) | [`adjoint_q1d_node.html`](adjoint_q1d_node.html) |

### 横着比：两种格式的边界条件 / Across: what the two schemes do at a boundary

这是每一组里两页的分歧所在。**格心格式**的未知量是单元平均值，边界上没有任何自由度，
所以边界条件只能**弱**加——在通量里给一个外侧状态。**格点格式**的边界节点<u>就在边界上</u>，
它本身就是未知量，所以可以**强**加——直接把它的方程换掉。伴随里对应的是「进循环前清零、
出循环后加回」，而且顺序不能反。四组算例把这件事走了四遍：

- **一维 Burgers**：只有入口一个条件 $u(0)=u_{\mathrm{in}}$，出口的通量就是物理通量。格心页把 $u_{\mathrm{in}}$
  当作入口面左侧的 ghost 状态（弱加）；格点页把节点 0 的整行换成 $u_0-u_{\mathrm{in}}$（强加）。
  照搬前向的写法、在伴随循环之后直接覆盖 $y_0\leftarrow w_0$，点积测试就失败。
- **二维对流**：纯对流方程只能在特征线进入区域的地方给边界数据。物面是无粘壁面（通量为零），
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
  enter. The body is an inviscid wall (zero flux) and the far field takes the free stream or
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
| 局部导数 / Local derivative | 两个数 $c_L,c_R$ / two numbers | 两个数 $c_L,c_R$ / two numbers | 两个数，外加一条经过梯度的路径 / two numbers, plus a path through the gradients | 两个 **3×3 块** / two **3×3 blocks** |
| Jacobian 的一行 / A row of the Jacobian | 左右相邻（三对角）/ left and right neighbours (tridiagonal) | 相邻的未知量 / adjacent unknowns | **邻居的邻居**；Jacobi 迭代只用它的对角元 / **neighbours of neighbours**; the Jacobi iteration uses only its diagonal | 左右相邻的块（块三对角）/ the neighbouring blocks (block tridiagonal) |
| 源项 / Source term | 有，逐区间常数，就是设计变量 / yes, constant on each interval: the design variables | 没有 / none | 没有 / none | 有，且不经过任何面 / yes, crossing no face |
| 边界条件 / Boundary conditions | 入口值 $u_{\mathrm{in}}$ / the inflow value | 零通量壁面、特征远场 / a zero-flux wall, a characteristic far field | Dirichlet 壁面 $u=u_w$ / a Dirichlet wall | 内点状态的**非线性函数** / **nonlinear functions** of the interior |
| 强加的形状 / Shape of strong imposition | 整行换成 $e_0^{\mathsf T}$ / the whole row becomes $e_0^{\mathsf T}$ | 没有强加 / none | 整行换成 $e_i^{\mathsf T}$ / the whole row becomes $e_i^{\mathsf T}$ | **部分行**换成约束梯度 / **partial rows** become constraint gradients |
| 信息传播 / Information travels | 单向 / one way | 单向（纯对流）/ one way | 双向（扩散）/ both ways (diffusion) | 双向（亚声速）/ both ways (subsonic) |
| 设计变量 / Design variables | 8 个区间源项与 $u_{\mathrm{in}}$ / 8 interval sources and $u_{\mathrm{in}}$ | 48 个网格坐标 / 48 mesh coordinates | 48 个网格坐标 / 48 mesh coordinates | 13 个截面积 / 13 duct areas |

一维那一对是入门：方程、通量与循环都和二维对流页相同，只是法向取 $n=1$，网格小到每个数组、
整个 Jacobian 都能完整摆在页面上；设计变量换成源项与入口值，所以不需要任何网格导数，一次伴随
求解直接给出全部 9 个导数。二维对流那一对页面在第 2 节的注里说过一句话：「把标量换成状态向量、把局部导数换成块矩阵即可。」
拟一维那一对就是把这句话兑现出来——并且顺带说明，兑现过程中会冒出源项、非线性边界条件
和双向传播这些二维标量模型里根本不存在的东西。对流扩散那一对留在标量上，只加一个二阶项：
梯度要先算出来，残差变成两遍循环，精确 Jacobian 伸到邻居的邻居——伴随要用的精确算子从这里
开始不再只连相邻的未知量，matrix-free 的 Jacobi 迭代却照样只需要它的对角元；Dirichlet 壁面
也在这里才有了适定的位置。

The one-dimensional pair is the way in: the equation, the flux and the loop are those of the
two-dimensional advection pages with the normal taken as $n=1$, on a grid small enough for every
array and the whole Jacobian to fit on the page; the design variables are the sources and the
inflow value, so no mesh derivative is needed and one adjoint solve gives all nine derivatives.
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

**一维 Burgers / 1-D Burgers**（入门）— 带源项的定常 Burgers 方程
$\frac{\mathrm d}{\mathrm dx}\big(\tfrac12u^2\big)=s(x)$，$0<x<1$，$u(0)=u_{\mathrm{in}}=1$；面通量是二维页的
通量取 $n=1$：$h=\tfrac14(u_L^2+u_R^2)-\varepsilon(u_R-u_L)$，$\varepsilon=0.8$；8 个单元（格心）或 9 个节点
（格点）；源项在 8 个区间上逐段为常数，当前设计 $\sigma=0.5$（精确解 $u=\sqrt{1+x}$）；目标是反设计
$J=\tfrac12\sum_iw_i(u_i-\bar u_i)^2$，$\bar u$ 是源项取 $\sin\pi x$ 的区间平均时的解；设计变量是 8 个区间
源项与 $u_{\mathrm{in}}$。

**二维对流 / 2-D advection** — 标量守恒律 $F(u)=\tfrac12u^2\beta$，$\beta=(1,\,0.5)$，常数耗散
$\varepsilon=0.8$；环形 O 型混合网格（8 个四边形 + 16 个三角形，24 个未知量）；内圈物面是
无粘壁面（通量为零）、外圈远场特征边界；目标是类似阻力的物面积分；设计变量是全部 48 个
节点坐标。

**二维对流扩散 / 2-D advection–diffusion** — 同一个对流通量（同样的 $\beta$ 与 $\varepsilon$），
加上常数扩散 $\nu=0.5$：$\nabla\cdot(\tfrac12u^2\beta)-\nabla\cdot(\nu\nabla u)=0$；扩散通量是
沿两侧连线的两点差，加上两侧最小二乘梯度（不加权）平均后的非正交修正；网格同上；物面
$u=u_w=0$，远场 $u_\infty=1$、扩散通量为零；目标是流进物面的总通量；设计变量同样是 48 个
节点坐标。

**拟一维 Euler / quasi-1-D Euler** — 变截面流道 $A(x)=1-0.3\sin^2(\pi x)$，两端为 1、喉部 0.7；
入口给**总压与总温**、出口给**背压**，全场亚声速；Rusanov 通量（耗散系数取两侧平均而非
$\max$，以保可微）；目标有两个可切换：**反设计**（压力分布匹配）与**推力**；设计变量是
13 个截面积。

四组的对流通量都是一阶、不做重构。八页的 primal、切线、伴随三个方程都用**同一个 Jacobi 迭代**
求解（拟一维页是 3×3 的块 Jacobi）：每一轮算一次残差（切线方程里是 residual_d，伴随方程里是
residual_b），再除以精确 Jacobian 的对角元（块），矩阵既不形成也不分解。网格这么小，最快的办法
本是直接 LU 分解，但那样体现不出 matrix-free；Jacobi 是最简单的迭代法，天然 matrix-free，而且
三个迭代矩阵同谱，进入渐近阶段以后三条收敛曲线以同一个速率下降——各页把它们画在一起。

**1-D Burgers** (introductory) — the steady Burgers equation with a source,
$\frac{\mathrm d}{\mathrm dx}\big(\tfrac12u^2\big)=s(x)$ on $0<x<1$, $u(0)=u_{\mathrm{in}}=1$; the face flux is that
of the two-dimensional pages at $n=1$, $h=\tfrac14(u_L^2+u_R^2)-\varepsilon(u_R-u_L)$, $\varepsilon=0.8$; 8 cells
(cell-centred) or 9 nodes (node-centred); the source is constant on each of the 8 intervals, $\sigma=0.5$ in the
current design (exact solution $u=\sqrt{1+x}$); the objective is inverse design,
$J=\tfrac12\sum_iw_i(u_i-\bar u_i)^2$, with $\bar u$ the solution for the interval averages of $\sin\pi x$; the
design variables are the 8 interval sources and $u_{\mathrm{in}}$.

The convective fluxes are first order with no reconstruction throughout. All eight pages solve the
primal, the tangent and the adjoint equation with **one and the same Jacobi iteration** (block
Jacobi with 3×3 blocks on the quasi-one-dimensional pages): every sweep evaluates the residual
once (residual_d in the tangent equation, residual_b in the adjoint equation) and divides by the
diagonal (blocks) of the exact Jacobian; no matrix is formed or factorised. On meshes this small
a direct LU would be fastest, but it would show nothing about matrix-free. Jacobi is the simplest
iteration there is and matrix-free by construction, and the three iteration matrices share one
spectrum, so once asymptotic the three convergence curves fall at the same rate — the pages plot
them together.

## 每页的各节 / The sections

1. 网格（或流道）/ Mesh, or the duct
2. 方程与面上的一维通量 / The equations and the one-dimensional flux
3. 边界条件 / Boundary conditions
4. 残差 = 循环：收集、计算、分发（对流扩散页是两遍：先梯度、后通量）/ Residual = the loop:
   gather, compute, scatter (two loops on the advection–diffusion pages: gradients, then fluxes)
5. 求解：Jacobian 与 Jacobi 迭代 / The solve: the Jacobian and Jacobi
6. 目标函数 / The objective function
7. matrix-free 前向：计算 $Av$ / Matrix-free forward
8. matrix-free 伴随：计算 $A^{\mathsf T}w$ / Matrix-free adjoint
9. 前向求解：切线方程 / The forward solve: the tangent equation
10. 伴随求解：伴随方程 / The adjoint solve: the adjoint equation
11. 几何导数（一维页：设计导数）/ Geometric derivatives (the 1-D pages: design derivatives)
12. 验证：对有限差分 / Verification against finite differences
13. 复数步长：公式与实现；从收敛流场出发，复数迭代每一轮都等于前向迭代；用它验证梯度（一维页还有
    「哪一种检验抓哪一种错误」）/ The complex step: the formula and how to implement it; started from the
    converged flow, the complex iteration is the forward iteration at every sweep; the gradient checked
    by it (the 1-D pages add "which check catches which bug")
14. 精度阶：构造解检验 / Order of accuracy: a manufactured solution
15. 总结；一维页的第 15 节是伴随一致性与 $J$ 的误差估计，总结是第 16 节 / Summary; on the 1-D pages
    Section 15 is adjoint consistency and estimating the error in $J$, and the summary is Section 16

拟一维页把 Jacobian 记作 $J$（那里 $A$ 是截面积），所以第 7、8 节在那两页算的是 $Jv$ 与 $J^{\mathsf T}w$。
The quasi-one-dimensional pages write the Jacobian $J$, because $A$ is the duct area there, so Sections 7
and 8 compute $Jv$ and $J^{\mathsf T}w$ on those two pages.

## 可以动手的地方 / What is interactive

每页 10–15 个交互面板，图全部由代码生成，按正文顺序编号（图 1、图 2……）：

- **网格／流道浏览器**：点任意单元或节点，看它的面、法向、守恒量、源项与残差；对流扩散页还画出
  它的最小二乘梯度模板
- **最小二乘梯度**（对流扩散页）：选一个单元或节点，看它的模板、矩阵 $M_i$、每个权重和算出的梯度；
  换成线性场，每个点上的梯度都精确到舍入误差
- **一个面上的通量**：拖动两侧状态，看中心项与耗散项怎样组成数值通量；对流扩散页把扩散通量拆成
  两点差与梯度修正；拟一维页还能逐个面载入收敛解，看质量与能量通量在各面上相同、中心项与耗散项
  却各自在变
- **三个循环逐句播放**：primal、tangent、adjoint 各一个，每一行伪代码对应一步，
  数组里的数字随之变化——转置在数据流上长什么样，一眼可见；对流扩散页的每个循环分两遍，
  伴随先倒着走通量那一遍、再倒着走梯度那一遍
- **点积测试**：随机向量，现场验证 $\langle w,Av\rangle=\langle A^{\mathsf T}w,v\rangle$；
  对流扩散格点页与一维格点页可以把被替换那一行的转置换成照搬前向的错误写法，看它怎样失败
- **三个求解过程**：primal、切线、伴随三个 Jacobi 迭代逐轮播放（对流页与拟一维页还逐面播放
  切线与伴随那一轮内部的循环），三条收敛曲线画在一起：进入渐近阶段以后它们平行。
  收敛曲线都越过停止判据，一直画到舍入误差平台：曲线变平，才说明已经收敛到机器精度
- **流进物面的通量**（对流扩散页）：逐个壁面面或壁面节点看它吸收的通量；格点页把一致的反作用量
  与单侧差分公式并排对照
- **精确 Jacobian 的组装**：拟一维页逐面播放 `jacobian(u, A)`——每个面的两个 3×3 块、边界块 $c_R+c_L\,\partial\mathbf B/\partial\mathbf u$、源项行、被替换的约束行——最后与中心差分对照；块 Jacobi 用的就是它的对角块
- **边界块与它的秩**：拟一维格心页把两个边界 Jacobian 和它们的秩算出来
- **梯度面板**：拟一维格点页把「忘记清零 $\Psi$」的后果和正确结果画在一起
- **BFGS 反设计**（一维页）：每一步一次 primal、一次伴随求解，看 8 个源项逐步回到目标值、$J$ 降到
  $10^{-20}$ 以下；入口值不动，因为它和第一个区间的源项几乎可以互相替代
- **复数步长与前向迭代，逐轮对照**（每页）：选一个设计变量和起点，两条迭代的残差与它们逐轮之差画在一起。
  从收敛流场出发，复数迭代的虚部每一轮都等于前向迭代；从初始流场出发，两者只在收敛时相遇。图下的表把
  复数步长、伴随与中心差分给出的梯度并排列出
- **哪一种检验抓哪一种错误**（一维页）：几种常见的伴随错误放在一张表里，点积测试与梯度检验（对复数步长）
  都在页面上现场算。转置错误点积测试一眼就能看出；flux() 里的导数错误、没收敛的伴随求解、组装梯度的符号
  错误都能通过点积测试，只有梯度检验抓得到
- **两种入口下的离散伴随与连续伴随**（一维页）：切换入口处理与网格，看入口旁那层伴随边界层出现、消失，
  以及 $\mathrm dJ/\mathrm d\sigma_1$ 的连续与离散之比
- **差分验证与步长扫描**：自选差分格式（中心／前向；一维页还有复数步长）与步长 $h$，逐分量用全链路差分对照伴随梯度；
  底部扫描相对误差随步长的变化，截断与舍入怎样围出最优步长一目了然。拟一维页把梯度画成流道壁上的箭头，
  点一个面（或节点）就扫描那个分量

Ten to fifteen interactive panels per page, every figure generated from code and numbered
in reading order. The three loops can be played statement by statement, with the arrays
updating as each pseudocode line executes (on the advection–diffusion pages each loop runs in
two passes, and the adjoint walks back through the flux pass before the gradient pass); the
flux on one face can be taken apart term by term, the diffusive flux into its two-point part and
its gradient correction; a least-squares gradient can be taken apart weight by weight, and seen
to be exact on a linear field; the exact Jacobian can be watched being assembled block by block,
boundary terms included; the primal, tangent and adjoint Jacobi iterations can be stepped through,
their three curves drawn together, past the stopping criterion down to the round-off floor, where
the curves go flat; the flux into the body can be read wall
face by wall face, or wall node by wall node against the one-sided formula; and the shape
gradient can be checked against full-chain differences at any step and scheme, with its error
swept against the step size, component by component. On every page the complex step, which
needs no compromise on the step size, is run against the forward iteration: started from the
converged flow the two agree at every sweep, started from the initial field they meet only at
convergence, and the gradient it gives is set beside the adjoint's and the central difference's.
On the one-dimensional pages the adjoint gradient drives a BFGS inverse design, one primal and one
adjoint solve per step, and the eight sources can be watched returning to their target values; a
table shows which of several common
adjoint bugs the dot test catches and which only the gradient check does; and a panel switches
the inflow treatment and the grid to show the adjoint's boundary layer at the inflow come and go.

## 页面上的数字都是实测的 / Every number is measured

交互面板里的数字在页面加载时由页面自己的脚本现场计算；正文、表格与静态图里引用的数值，
事先用同一份模型代码算出。各页的校验结果：

The numbers in the interactive panels are computed live by each page's own scripts as it loads;
the values quoted in the text, the tables and the static figures were computed in advance from
the same model code. The checks, page by page:

| 页面 / Page | 点积测试 / dot test | 几何点积测试 / geometric dot test | 梯度对全链路差分 / gradient vs full-chain FD | 漏掉一步的后果 / cost of one missing step |
|---|---|---|---|---|
| 一维 Burgers 格心 / 1-D Burgers, cell | 0 ¹ | — | 1.9e−10 | — |
| 一维 Burgers 格点 / 1-D Burgers, node | 5.4e−14 ⁷ | — | 1.9e−10 | 43 ⁸ |
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
⁷ 这一对随机向量的 $\langle w,Av\rangle$ 本身只有 0.0061，相对误差因此比 $10^{-16}$ 大。
⁸ 照搬前向的写法、在伴随循环之后直接覆盖 $y_0\leftarrow w_0$：点积测试的相对误差（同一对向量）。

¹ the first random pair happens to agree to the last bit; the next few land between $10^{-16}$
and $10^{-15}$. ² limited by the finite-difference step: the 2-D advection pages have no analytic forward
geometric operator, so that side is assembled column by column from central differences.
³ analytic in both directions, hence machine precision — which also shows the $10^{-11}$ of the
advection pages is the differencing, not the transpose. ⁴ $\psi$ not zeroed on the wall rows
before assembling the geometric gradient: off by 0.18 on a gradient of magnitude 0.32. ⁵ the
source term dropped from the adjoint: the dot test's relative error, depending on the vectors.
⁶ $\Psi$ not zeroed on the constrained rows before assembling the geometric gradient (inverse
design; 4% for thrust). ⁷ for this random pair $\langle w,Av\rangle$ itself is only 0.0061, which
inflates the relative error above $10^{-16}$. ⁸ the forward code copied, overwriting
$y_0\leftarrow w_0$ after the adjoint loop: the dot test's relative error (same pair).

每一页第 13 节的复数步长（$h=10^{-30}$）：

The complex step of Section 13 ($h=10^{-30}$), page by page:

| 页面 / Page | 逐轮，从 $u^*$ 出发 / per sweep, from $u^*$ | 逐轮，从初始流场出发 / per sweep, from the initial field | 实部，从 $u^*$ 出发 / real part, from $u^*$ | 复数步长对伴随 / complex step vs adjoint | 中心差分对伴随 / central difference vs adjoint |
|---|---|---|---|---|---|
| 一维 Burgers 格心 / 1-D Burgers, cell | 7.9e−16 | 1.1 | 逐比特 / to the bit | 2.9e−16 | 1.9e−10 |
| 一维 Burgers 格点 / 1-D Burgers, node | 7.0e−16 | 1.0 | 逐比特 / to the bit | 1.2e−16 | 1.9e−10 |
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

- **一维 Burgers**：不用构造解，精确解就是 $u=\sqrt{u_{\mathrm{in}}^2+2\int_0^xs\,\mathrm dt}$。解与 $J$ 都是一阶
  （$N=8$ 到 1024，$L_2$ 阶格心 0.99→1.00，格点 1.22→1.01）。离散伴随对照连续伴随
  $\lambda(x)=\int_x^1(u-\bar u)/u\,\mathrm dt$：内部一阶；入口旁第一个控制体（格点页是节点 1）里的误差却最终不随网格减小，趋于
  $-\lambda(0)\,r=8.0\times10^{-3}$，$r=-c_R/c_L=0.23$——入口旁那个面的通量依赖 $u_1$（$c_R\neq0$），转置之后
  相当于在伴随的出口多加了一个条件 $\psi_0=0$。这层边界层每往里一个控制体误差乘一次 $r$，所以伴随的 $L_2$ 阶趋于 ½。
  第 15 节把入口旁的那个面换成迎风通量 $\tfrac12u_L^2$：边界层消失，伴随的 $L_2$ 阶回到 1.00；连续伴随给的
  $\mathrm dJ/\mathrm d\sigma_1$ 与离散伴随之比从 1.30（$=1/(1-r)$，加密不变）回到 1（格点页回到 2：被替换的
  那一行丢掉了半个区间上的源项）。用粗网格伴随估计 $J$ 的误差，格心页换成迎风入口才是二阶，本页的入口只有
  一阶；格点页两种入口都是二阶。
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

- **1-D Burgers**: no manufactured solution is needed, the exact one being
  $u=\sqrt{u_{\mathrm{in}}^2+2\int_0^xs\,\mathrm dt}$. The solution and $J$ are first order ($N=8$ to 1024;
  $L_2$ orders 0.99 → 1.00 cell-centred, 1.22 → 1.01 node-centred). Against the continuous adjoint
  $\lambda(x)=\int_x^1(u-\bar u)/u\,\mathrm dt$ the discrete one is first order inside, but its error next
  to the inflow (the first cell; node 1 on the node-centred page) does not shrink in the end: it tends to
  $-\lambda(0)\,r=8.0\times10^{-3}$, $r=-c_R/c_L=0.23$. The flux on the face next to the inflow depends on $u_1$
  ($c_R\neq0$); transposed, that adds a condition, $\psi_0=0$, at the adjoint's outflow. The error in this boundary layer is multiplied by $r$ with every control
  volume inwards, so the adjoint's $L_2$ order tends to ½. Section 15 gives the face next to the
  inflow the upwind flux $\tfrac12u_L^2$: the layer disappears and the adjoint's $L_2$ order returns
  to 1.00; the ratio of the continuous to the discrete adjoint's $\mathrm dJ/\mathrm d\sigma_1$ goes
  from 1.30 ($=1/(1-r)$, whatever the grid) back to 1 (to 2 on the node-centred page, whose replaced
  row drops the source on half an interval). Estimating the error in $J$ with the coarse-grid
  adjoint is second order on the cell-centred page only with the upwind inflow, first order with
  the page's own; the node-centred page is second order with either.
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

本仓库的八个页面与本 README 以 **知识共享 署名 4.0 国际（CC BY 4.0）** 许可发布：
您可以自由地共享与改编，包括用于商业目的，只要给出**适当署名**、提供许可协议的链接，
并说明是否作了修改。完整条款见 [`LICENSE`](LICENSE)。

The eight pages in this repository and this README are licensed under a
**Creative Commons Attribution 4.0 International License (CC BY 4.0)**. You are free to share
and adapt the material, including for commercial purposes, so long as you give appropriate
credit, provide a link to the licence, and indicate if changes were made. Full terms in
[`LICENSE`](LICENSE).

<https://creativecommons.org/licenses/by/4.0/>

建议的署名 / Suggested attribution:

> Yisheng Gao，《非结构网格格心／格点格式的二维标量方程离散伴随》，CC BY 4.0，
> <https://github.com/yishenggaogg/adjoint_education>
