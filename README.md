# 离散伴随教学页 / Discrete adjoint, taught page by page

**六个**单文件、可交互的网页，把有限体积法的**全离散伴随**从头到尾讲一遍：
从一个面上的一维通量开始，把同一个循环依次改写成 primal、matrix-free 前向（$Av$）与
matrix-free 伴随（$A^{\mathsf T}w$），再做伴随求解、几何导数，最后用有限差分逐项校验。
三组算例——**二维标量对流方程**、**二维标量对流扩散方程**与**拟一维 Euler 方程**——
各有**格心**与**格点**两版。

**Six** self-contained, interactive web pages that develop the **fully discrete adjoint**
of a finite-volume scheme end to end: starting from the one-dimensional flux on a single
face, the same loop is rewritten as the primal, as matrix-free forward mode ($Av$) and as
matrix-free adjoint mode ($A^{\mathsf T}w$), followed by the adjoint solve, the geometric
derivatives and a term-by-term finite-difference verification. Three model problems &mdash;
a **two-dimensional scalar advection equation**, a **two-dimensional scalar
advection&ndash;diffusion equation** and the **quasi-one-dimensional Euler equations**
&mdash; each in a **cell-centred** and a **node-centred** version.

| 文件 / File | 算例 / Problem | 格式 / Scheme | 大小 / Size |
|---|---|---|---|
| [`adjoint_cell.html`](adjoint_cell.html) | 二维对流 / 2-D advection | **格心** / cell-centred | 495 KB |
| [`adjoint_node.html`](adjoint_node.html) | 二维对流 / 2-D advection | **格点** / node-centred | 565 KB |
| [`adjoint_ad_cell.html`](adjoint_ad_cell.html) | 二维对流扩散 / 2-D advection–diffusion | **格心** / cell-centred | 499 KB |
| [`adjoint_ad_node.html`](adjoint_ad_node.html) | 二维对流扩散 / 2-D advection–diffusion | **格点** / node-centred | 664 KB |
| [`adjoint_q1d_cell.html`](adjoint_q1d_cell.html) | 拟一维 Euler / quasi-1-D Euler | **格心** / cell-centred | 390 KB |
| [`adjoint_q1d_node.html`](adjoint_q1d_node.html) | 拟一维 Euler / quasi-1-D Euler | **格点** / node-centred | 373 KB |

直接用浏览器打开即可：**没有任何外部依赖**，不联网、不需要构建、不需要服务器。
Just open any of them in a browser — **no external dependencies**, no network, no build step,
no server. Each page has a 中文 / English toggle in the top-right corner.

**在线阅读 / Read online:** <https://yishenggaogg.github.io/adjoint_education/>

**仓库 / Repositories:**
[GitHub](https://github.com/yishenggaogg/adjoint_education) ·
[Gitee](https://gitee.com/gaoyishenggg/adjoint_education) — 内容相同 / identical content

---

## 六个页面怎么排布 / How the six pages are arranged

三组算例，每组两种离散。**六页结构完全平行**（都是 12 节），所以任意两页都能并排对照：
横着比是**两种格式**；竖着比是**方程**——从纯对流，到加上扩散，再到方程组。

Three model problems, each discretised two ways. All six are **strictly parallel** — 12 sections
each — so any two can be read side by side: across, the **two schemes**; down, **the equation**
— pure advection, then diffusion added, then a system.

| | 格心 / cell-centred | 格点 / node-centred |
|---|---|---|
| **二维对流** / 2-D advection | [`adjoint_cell.html`](adjoint_cell.html) | [`adjoint_node.html`](adjoint_node.html) |
| **二维对流扩散** / 2-D advection–diffusion | [`adjoint_ad_cell.html`](adjoint_ad_cell.html) | [`adjoint_ad_node.html`](adjoint_ad_node.html) |
| **拟一维 Euler** / quasi-1-D Euler | [`adjoint_q1d_cell.html`](adjoint_q1d_cell.html) | [`adjoint_q1d_node.html`](adjoint_q1d_node.html) |

### 横着比：两种格式的边界条件 / Across: what the two schemes do at a boundary

这是每一组里两页的分歧所在。**格心格式**的未知量是单元平均值，边界上没有任何自由度，
所以边界条件只能**弱**加——在通量里给一个外侧状态。**格点格式**的边界节点<u>就在边界上</u>，
它本身就是未知量，所以可以**强**加——直接把它的方程换掉。伴随里对应的是「进循环前清零、
出循环后加回」，而且顺序不能反。三组算例把这件事走了三遍：

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
loop, add back after", in that order and no other. The three rows go through this three times:

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

| | 二维对流 / 2-D advection | 二维对流扩散 / 2-D advection–diffusion | 拟一维 Euler / quasi-1-D Euler |
|---|---|---|---|
| 每个自由度 / Per unknown | 一个数 / one number | 一个数 / one number | 三个数 ρ, ρu, ρE / three |
| 残差 / Residual | 一个面循环 / one face loop | **两遍**：先最小二乘梯度、后通量 / **two loops**: least-squares gradients, then fluxes | 面循环加源项 / a face loop and a source |
| 局部导数 / Local derivative | 两个数 $c_L,c_R$ / two numbers | 两个数，外加一条经过梯度的路径 / two numbers, plus a path through the gradients | 两个 **3×3 块** / two **3×3 blocks** |
| Jacobian 的一行 / A row of the Jacobian | 相邻的未知量 / adjacent unknowns | **邻居的邻居**；求解器只用一阶近似 $\tilde A$ / **neighbours of neighbours**; the solver uses the first-order $\tilde A$ | 左右相邻的块（块三对角）/ the neighbouring blocks (block tridiagonal) |
| 源项 / Source term | 没有 / none | 没有 / none | 有，且不经过任何面 / yes, crossing no face |
| 边界条件 / Boundary conditions | 零通量壁面、特征远场 / a zero-flux wall, a characteristic far field | Dirichlet 壁面 $u=u_w$ / a Dirichlet wall | 内点状态的**非线性函数** / **nonlinear functions** of the interior |
| 强加的形状 / Shape of strong imposition | 没有强加 / none | 整行换成 $e_i^{\mathsf T}$ / the whole row becomes $e_i^{\mathsf T}$ | **部分行**换成约束梯度 / **partial rows** become constraint gradients |
| 信息传播 / Information travels | 单向（纯对流）/ one way | 双向（扩散）/ both ways (diffusion) | 双向（亚声速）/ both ways (subsonic) |
| 设计变量 / Design variables | 48 个网格坐标 / 48 mesh coordinates | 48 个网格坐标 / 48 mesh coordinates | 13 个截面积 / 13 duct areas |

二维对流那一对页面在第 2 节的注里说过一句话：「把标量换成状态向量、把局部导数换成块矩阵即可。」
拟一维那一对就是把这句话兑现出来——并且顺带说明，兑现过程中会冒出源项、非线性边界条件
和双向传播这些标量模型里根本不存在的东西。对流扩散那一对留在标量上，只加一个二阶项：
梯度要先算出来，残差变成两遍循环，精确 Jacobian 伸到邻居的邻居——伴随要用的精确算子和
求解器用的近似矩阵从这里开始分家；Dirichlet 壁面也在这里才有了适定的位置。

In a note in Section 2 the two-dimensional advection pair makes a promise: "replace the scalar
by a state vector and the local derivatives by block matrices." The quasi-one-dimensional pair
delivers on it — and shows that delivering on it brings out a source term, nonlinear boundary
conditions and two-way propagation, none of which the scalar model contains at all. The
advection–diffusion pair stays with a scalar and adds one second-order term: the gradients have
to be computed first, the residual becomes two loops, and the exact Jacobian reaches the
neighbours of neighbours — which is where the exact operator the adjoint needs and the
approximate matrix the solver uses part ways. It is also where a Dirichlet wall is finally well
posed.

## 三个模型问题 / The three model problems

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

三组的对流通量都是一阶、不做重构。对流页与拟一维页用精确 Jacobian 的 Newton 法求解（稠密 LU）；
对流扩散页的求解器只用一阶近似 Jacobian（只含相邻未知量），Newton 法因此变成线性收敛的亏量修正，
伴随方程用同一个矩阵的转置迭代，收敛速率与原始迭代相同。

The convective fluxes are first order with no reconstruction throughout. The advection and
quasi-one-dimensional pages solve by Newton with the exact Jacobian and a dense LU; the
advection–diffusion pages give the solver only the first-order Jacobian (adjacent unknowns
only), which turns Newton into a linearly converging defect correction, and iterate the adjoint
equation with the transpose of the same matrix, at the same rate as the primal.

## 每页的 12 节 / The twelve sections

1. 网格（或流道）/ Mesh, or the duct
2. 方程与面上的一维通量 / The equations and the one-dimensional flux
3. 边界条件 / Boundary conditions
4. 残差 = 循环：收集、计算、分发（对流扩散页是两遍：先梯度、后通量）/ Residual = the loop:
   gather, compute, scatter (two loops on the advection–diffusion pages: gradients, then fluxes)
5. 求解：Jacobian 与 Newton 法 / The solve: the Jacobian and Newton
6. 目标函数 / The objective function
7. matrix-free 前向：计算 $Av$ / Matrix-free forward
8. matrix-free 伴随：计算 $A^{\mathsf T}w$ / Matrix-free adjoint
9. 求解伴随方程 / Solving the adjoint equation
10. 几何导数 / Geometric derivatives
11. 验证：对有限差分 / Verification against finite differences
12. 总结 / Summary

## 可以动手的地方 / What is interactive

每页 9–14 个交互面板，图全部由代码生成，按正文顺序编号（图 1、图 2……）：

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
  对流扩散格点页可以把壁面的转置换成照搬前向的错误写法，看它怎样失败
- **两个求解过程**：primal 的 Newton 迭代逐轮播放；伴随方程的迭代逐轮播放（对流页与拟一维页是
  Jacobi 迭代，逐面、逐次；对流扩散页用一阶矩阵的转置，并把原始迭代的收敛曲线画在一起）。
  收敛曲线都越过停止判据，一直画到舍入误差平台：曲线变平，才说明已经收敛到机器精度
- **流进物面的通量**（对流扩散页）：逐个壁面面或壁面节点看它吸收的通量；格点页把一致的反作用量
  与单侧差分公式并排对照
- **精确 Jacobian 的组装**：拟一维页逐面播放 `jacobian(u, A)`——每个面的两个 3×3 块、边界块 $c_R+c_L\,\partial\mathbf B/\partial\mathbf u$、源项行、被替换的约束行——最后与中心差分对照；Newton 用的就是它
- **边界块与它的秩**：拟一维格心页把两个边界 Jacobian 和它们的秩算出来
- **梯度面板**：拟一维格点页把「忘记清零 $\Psi$」的后果和正确结果画在一起
- **差分验证与步长扫描**：自选差分格式（中心／前向）与步长 $h$，逐分量用全链路差分对照伴随梯度；
  底部扫描相对误差随步长的变化，截断与舍入怎样围出最优步长一目了然。拟一维页把梯度画成流道壁上的箭头，
  点一个面（或节点）就扫描那个分量

Nine to fourteen interactive panels per page, every figure generated from code and numbered
in reading order. The three loops can be played statement by statement, with the arrays
updating as each pseudocode line executes (on the advection–diffusion pages each loop runs in
two passes, and the adjoint walks back through the flux pass before the gradient pass); the
flux on one face can be taken apart term by term, the diffusive flux into its two-point part and
its gradient correction; a least-squares gradient can be taken apart weight by weight, and seen
to be exact on a linear field; the exact Jacobian can be watched being assembled block by block,
boundary terms included; the Newton
solve and the adjoint iteration can be stepped through, past the stopping criterion down to the
round-off floor, where the curve goes flat; the flux into the body can be read wall
face by wall face, or wall node by wall node against the one-sided formula; and the shape
gradient can be checked against full-chain differences at any step and scheme, with its error
swept against the step size, component by component.

## 页面上的数字都是实测的 / Every number is measured

交互面板里的数字在页面加载时由页面自己的脚本现场计算；正文、表格与静态图里引用的数值，
事先用同一份模型代码算出。各页的校验结果：

The numbers in the interactive panels are computed live by each page's own scripts as it loads;
the values quoted in the text, the tables and the static figures were computed in advance from
the same model code. The checks, page by page:

| 页面 / Page | 点积测试 / dot test | 几何点积测试 / geometric dot test | 梯度对全链路差分 / gradient vs full-chain FD | 漏掉一步的后果 / cost of one missing step |
|---|---|---|---|---|
| 二维对流 格心 / 2-D advection, cell | 1.2e−16 | 4.0e−11 ² | 3.1e−10 | — |
| 二维对流 格点 / 2-D advection, node | 3.7e−16 | 1.0e−10 ² | 2.5e−10 | — |
| 二维对流扩散 格心 / 2-D advection–diffusion, cell | 0 ¹ | — | 8.8e−10 | — |
| 二维对流扩散 格点 / 2-D advection–diffusion, node | 1.9e−16 | — | 1.1e−9 | 56 % ⁴ |
| 拟一维 格心 / quasi-1-D, cell | 5.30e−16 | **1.95e−16** ³ | 4.4e−9 | 10⁻⁴ 到 10⁻¹ / 10⁻⁴ to 10⁻¹ ⁵ |
| 拟一维 格点 / quasi-1-D, node | 1.38e−16 | **3.73e−16** ³ | 1.0e−9 | **108 %** ⁶ |

点积测试是打开页面时点积面板显示的相对误差；几何点积测试，二维对流页是第 10 节正文引用的偏差，
拟一维页是面板上的相对偏差；全链路差分是中心差分、$h=10^{-6}$，每次都重新求解，取所有分量与
伴随梯度之差的最大值，除以梯度的最大分量（拟一维取反设计目标）。「—」表示该页没有这一项。

The dot tests are the relative errors each page's panel shows on opening. The geometric dot
tests are the deviation quoted in Section 10 on the advection pages, and the relative deviation
the panel shows on the quasi-one-dimensional pages. The full-chain differences are central, $h=10^{-6}$, re-solving every time; the
largest difference from the adjoint gradient over all components, divided by the gradient's
largest component (the inverse-design objective on the quasi-one-dimensional pages). A dash
means the page has no such check.

¹ 第一对随机向量恰好逐比特相等；再抽几对，就落在 $10^{-16}$ 量级。
² 被差分步长卡住：二维对流页没有解析的前向几何算子，前向那一侧由中心差分逐列装配。
³ 两个方向都解析，所以落在机器精度——这也说明二维对流页那个 $10^{-11}$ 是差分的锅，不是转置的锅。
⁴ 组装几何梯度前忘记把 $\psi$ 在壁面行上清零：差 0.18，梯度的量级是 0.32。
⁵ 伴随里漏掉源项：点积测试的相对误差，随所取的向量而定。
⁶ 组装几何梯度前忘记把 $\Psi$ 在约束行上清零（反设计；推力目标是 4%）。

¹ the first random pair happens to agree to the last bit; the next few land at the $10^{-16}$
level. ² limited by the finite-difference step: the 2-D advection pages have no analytic forward
geometric operator, so that side is assembled column by column from central differences.
³ analytic in both directions, hence machine precision — which also shows the $10^{-11}$ of the
advection pages is the differencing, not the transpose. ⁴ $\psi$ not zeroed on the wall rows
before assembling the geometric gradient: off by 0.18 on a gradient of magnitude 0.32. ⁵ the
source term dropped from the adjoint: the dot test's relative error, depending on the vectors.
⁶ $\Psi$ not zeroed on the constrained rows before assembling the geometric gradient (inverse
design; 4% for thrust).

对流扩散那一对还在第 12 节做了制造解精度阶研究：在由基础网格均匀细分得到的四层同族网格上，
只有扩散时两种格式都是二阶（$L_2$ 范数下格心 1.94、2.02、2.01，格点 1.99、2.09、2.08）；
完整方程受耗散项限制，只有一阶。伴随给出的是离散格式的精确导数，而格式的精度阶决定这个导数
离连续问题的导数有多远。

The advection–diffusion pair adds an order study in Section 12, with a manufactured solution on
four meshes made from the base mesh by uniform subdivision: diffusion alone is second order for
both schemes (in the $L_2$ norm 1.94, 2.02 and 2.01 cell-centred, 1.99, 2.09 and 2.08
node-centred), while the full equation is only first order, held back by the dissipation. The
adjoint gives the exact derivative of the discrete scheme; the scheme's order decides how far
that derivative is from the continuous problem's.

反设计目标还有一个更强的检验：目标压力取自一条**已知**的流道，于是在那条流道上 $L$ 与
$\mathrm dL/\mathrm dA$ 都**逐比特为零**——梯度在一个独立构造的最优点上归零，比任何差分
对照都更有说服力。

The inverse-design objective carries a stronger check still: its target pressures come from a
**known** duct, so on that duct both $L$ and $\mathrm dL/\mathrm dA$ are **zero to the last
bit** — a gradient vanishing at an independently constructed optimum is better evidence than
any finite-difference comparison.

第 11 节还专门演示了差分校验本身的陷阱：步长取大取小都会让“验证”看起来像失败，
而点积测试是精确恒等式，根本不含步长。

Section 11 also demonstrates the trap in finite-difference verification itself — too large or
too small a step makes a correct gradient look wrong — which is why the dot-product test,
an exact identity with no step size in it, is the more reliable check.

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

本仓库的六个页面与本 README 以 **知识共享 署名 4.0 国际（CC BY 4.0）** 许可发布：
您可以自由地共享与改编，包括用于商业目的，只要给出**适当署名**、提供许可协议的链接，
并说明是否作了修改。完整条款见 [`LICENSE`](LICENSE)。

The six pages in this repository and this README are licensed under a
**Creative Commons Attribution 4.0 International License (CC BY 4.0)**. You are free to share
and adapt the material, including for commercial purposes, so long as you give appropriate
credit, provide a link to the licence, and indicate if changes were made. Full terms in
[`LICENSE`](LICENSE).

<https://creativecommons.org/licenses/by/4.0/>

建议的署名 / Suggested attribution:

> Yisheng Gao，《非结构网格格心／格点格式的二维标量方程离散伴随》，CC BY 4.0，
> <https://github.com/yishenggaogg/adjoint_education>
