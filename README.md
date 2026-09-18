# 离散伴随教学页 / Discrete adjoint, taught page by page

**四个**单文件、可交互的网页，把有限体积法的**全离散伴随**从头到尾讲一遍：
从一个面上的一维通量开始，把同一个循环依次改写成 primal、matrix-free 前向（$Av$）与
matrix-free 伴随（$A^{\mathsf T}w$），再做伴随求解、几何导数，最后用有限差分逐项校验。
两组算例——**二维标量方程**与**拟一维 Euler 方程**——各有**格心**与**格点**两版。

**Four** self-contained, interactive web pages that develop the **fully discrete adjoint**
of a finite-volume scheme end to end: starting from the one-dimensional flux on a single
face, the same loop is rewritten as the primal, as matrix-free forward mode ($Av$) and as
matrix-free adjoint mode ($A^{\mathsf T}w$), followed by the adjoint solve, the geometric
derivatives and a term-by-term finite-difference verification. Two model problems &mdash;
a **two-dimensional scalar equation** and the **quasi-one-dimensional Euler equations**
&mdash; each in a **cell-centred** and a **node-centred** version.

| 文件 / File | 算例 / Problem | 格式 / Scheme | 大小 |
|---|---|---|---|
| [`adjoint_cell.html`](adjoint_cell.html) | 二维标量 / 2-D scalar | **格心** / cell-centred | 516 KB |
| [`adjoint_node.html`](adjoint_node.html) | 二维标量 / 2-D scalar | **格点** / node-centred | 677 KB |
| [`adjoint_q1d_cell.html`](adjoint_q1d_cell.html) | 拟一维 Euler / quasi-1-D Euler | **格心** / cell-centred | 194 KB |
| [`adjoint_q1d_node.html`](adjoint_q1d_node.html) | 拟一维 Euler / quasi-1-D Euler | **格点** / node-centred | 174 KB |

直接用浏览器打开即可：**没有任何外部依赖**，不联网、不需要构建、不需要服务器。
Just open any of them in a browser — **no external dependencies**, no network, no build step,
no server. Each page has a 中文 / English toggle in the top-right corner.

**在线阅读 / Read online:** <https://yishenggaogg.github.io/adjoint_education/>

**仓库 / Repositories:**
[GitHub](https://github.com/yishenggaogg/adjoint_education) ·
[Gitee](https://gitee.com/gaoyishenggg/adjoint_education) — 内容相同 / identical content

---

## 四个页面怎么排布 / How the four pages are arranged

两组算例，每组两种离散。**四页结构完全平行**（都是 12 节），所以任意两页都能并排对照：
横着比是**两种格式**，竖着比是**标量与方程组**。

Two model problems, each discretised two ways. All four are **strictly parallel** — 12 sections
each — so any two can be read side by side: across, the **two schemes**; down, **a scalar
against a system**.

| | 格心 / cell-centred | 格点 / node-centred |
|---|---|---|
| **二维标量** / 2-D scalar | [`adjoint_cell.html`](adjoint_cell.html) | [`adjoint_node.html`](adjoint_node.html) |
| **拟一维 Euler** / quasi-1-D Euler | [`adjoint_q1d_cell.html`](adjoint_q1d_cell.html) | [`adjoint_q1d_node.html`](adjoint_q1d_node.html) |

### 横着比：两种格式的边界条件 / Across: what the two schemes do at a boundary

这是每一组里两页的分歧所在。**格心格式**的未知量是单元平均值，边界上没有任何自由度，
所以边界条件只能**弱**加——在通量里给一个外侧状态。**格点格式**的边界节点<u>就在边界上</u>，
它本身就是未知量，所以可以**强**加——直接把它的方程换掉。伴随里对应的是「进循环前清零、
出循环后加回」，而且顺序不能反。

That is where the two pages in each row part company. A **cell-centred** scheme's unknowns are
cell averages and no degree of freedom sits on the boundary, so the conditions can only be
imposed **weakly**, through an outer state in the flux. A **node-centred** scheme's boundary
node <u>is</u> on the boundary and is itself an unknown, so the conditions can be imposed
**strongly**, by replacing its equations — which the adjoint answers with "zero before the
loop, add back after", in that order and no other.

### 竖着比：标量与方程组 / Down: a scalar against a system

| | 二维标量 / 2-D scalar | 拟一维 Euler / quasi-1-D Euler |
|---|---|---|
| 每个自由度 / Per unknown | 一个数 / one number | 三个数 ρ, ρu, ρE / three |
| 局部导数 / Local derivative | 两个数 $c_L,c_R$ / two numbers | 两个 **3×3 块** / two **3×3 blocks** |
| 源项 / Source term | 没有 / none | 有，且不经过任何面 / yes, crossing no face |
| 边界条件 / Boundary conditions | 常数或外推 / a constant, or extrapolation | 内点状态的**非线性函数** / **nonlinear functions** of the interior |
| 强加的形状 / Shape of strong imposition | 整行换成 $e_i^{\mathsf T}$ / the whole row becomes $e_i^{\mathsf T}$ | **部分行**换成约束梯度 / **partial rows** become constraint gradients |
| 信息传播 / Information travels | 单向（纯对流）/ one way | 双向（亚声速）/ both ways |
| 设计变量 / Design variables | 48 个网格坐标 / 48 mesh coordinates | 13 个截面积 / 13 duct areas |

二维那一对页面结尾写过一句话：「把标量换成状态向量、把局部导数换成块矩阵即可。」
拟一维那一对就是把这句话兑现出来——并且顺带说明，兑现过程中会冒出源项、非线性边界条件
和双向传播这些标量模型里根本不存在的东西。

The two-dimensional pair closes with a promise: "replace the scalar by a state vector and the
local derivatives by block matrices." The quasi-one-dimensional pair delivers on it — and shows
that delivering on it brings out a source term, nonlinear boundary conditions and two-way
propagation, none of which the scalar model contains at all.

## 两个模型问题 / The two model problems

**二维标量 / 2-D scalar** — 标量守恒律 $F(u)=\tfrac12u^2\beta$，$\beta=(1,\,0.5)$，常数耗散
$\varepsilon=0.8$；环形 O 型混合网格（8 个四边形 + 16 个三角形，24 个未知量）；内圈物面、
外圈远场特征边界；目标是类似阻力的物面积分；设计变量是全部 48 个节点坐标。

**拟一维 Euler / quasi-1-D Euler** — 变截面流道 $A(x)=1-0.3\sin^2(\pi x)$，两端为 1、喉部 0.7；
入口给**总压与总温**、出口给**背压**，全场亚声速；Rusanov 通量（耗散系数取两侧平均而非
$\max$，以保可微）；目标有两个可切换：**反设计**（压力分布匹配）与**推力**；设计变量是
13 个截面积。

Both are first order with no reconstruction, solved by Newton with a dense LU, and every
constant quoted on the pages is measured live rather than written into the text.

## 每页的 12 节 / The twelve sections

1. 网格（或流道）/ Mesh, or the duct
2. 方程与面上的一维通量 / The equations and the one-dimensional flux
3. 边界条件 / Boundary conditions
4. 残差 = 循环：收集、计算、分发 / Residual = the loop: gather, compute, scatter
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

- **网格／流道浏览器**：点任意单元或节点，看它的面、法向、守恒量、源项与残差
- **一个面上的通量**：拖动两侧状态，看中心项与耗散项怎样组成数值通量；拟一维页还能逐个面载入收敛解，
  看质量与能量通量在各面上相同、中心项与耗散项却各自在变
- **三个循环逐句播放**：primal、tangent、adjoint 各一个，每一行伪代码对应一步，
  数组里的数字随之变化——转置在数据流上长什么样，一眼可见
- **点积测试**：随机向量，现场验证 $\langle w,Av\rangle=\langle A^{\mathsf T}w,v\rangle$
- **两个求解过程**：primal 的 Newton 迭代逐轮播放；伴随方程的块 Jacobi 迭代逐面、逐次播放
- **精确 Jacobian 的组装**：拟一维页逐面播放 `jacobian(u, A)`——每个面的两个 3×3 块、边界块 $c_R+c_L\,\partial\mathbf B/\partial\mathbf u$、源项行、被替换的约束行——最后与中心差分对照；Newton 用的就是它
- **边界块与它的秩**：拟一维格心页把两个边界 Jacobian 和它们的秩算出来
- **梯度面板**：格点页把「忘记清零 $\Psi$」的后果和正确结果画在一起
- **差分验证与步长扫描**：自选差分格式（中心／前向）与步长 $h$，逐分量用全链路差分对照伴随梯度；
  底部扫描相对误差随步长的变化，截断与舍入怎样围出最优步长一目了然。拟一维页把梯度画成流道壁上的箭头，
  点一个面（或节点）就扫描那个分量

Nine to fourteen interactive panels per page, every figure generated from code and numbered
in reading order. The three loops can be played statement by
statement, with the arrays updating as each pseudocode line executes; the flux on one face
can be taken apart term by term; the exact Jacobian can be watched being assembled block by
block, boundary terms included; the Newton solve and the block-Jacobi adjoint solve can be
stepped through; and the shape gradient can be checked against full-chain differences at any
step and scheme, with its error swept against the step size, component by component.

## 页面上的数字都是实测的 / Every number is measured

页面引用的每一个数值都是在浏览器里现场算出来的，不是写死的文字：

| 检验 / Check | 二维格心 | 二维格点 | 拟一维格心 | 拟一维格点 |
|---|---|---|---|---|
| 点积测试 $\langle w,Av\rangle=\langle A^{\mathsf T}w,v\rangle$ | 8.9e−16 | 6.7e−16 | 2.2e−16 | 2.9e−16 |
| 几何点积测试 / geometric dot test | 4.0e−11 ¹ | 1.0e−10 ¹ | **4.6e−16** ² | **3.4e−16** ² |
| 梯度对全链路差分 / gradient vs full-chain FD | 5.4e−11 | 5.1e−11 | 4.4e−9 | 1.0e−9 |
| 漏掉一步的后果 / cost of one missing step | — | 0.31 ³ | 1.0e−2 ⁴ | **108 %** ⁵ |

¹ 被差分步长卡住：二维页没有解析的前向几何算子。
² 两个方向都解析，所以落在机器精度——这也说明二维页那个 $10^{-11}$ 是差分的锅，不是转置的锅。
³ 清零／加回顺序写反。 ⁴ 伴随里漏掉源项。 ⁵ 组装几何梯度前忘记把 $\Psi$ 在约束行上清零。

¹ limited by the finite-difference step: the 2-D pages have no analytic forward geometric
operator. ² analytic in both directions, hence machine precision — which also shows the
$10^{-11}$ above is the differencing, not the transpose. ³ zero-and-add-back in the wrong
order. ⁴ the source term dropped from the adjoint. ⁵ $\Psi$ not zeroed on the constrained
rows before assembling the geometric gradient.

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

本仓库的两个页面与本 README 以 **知识共享 署名 4.0 国际（CC BY 4.0）** 许可发布：
您可以自由地共享与改编，包括用于商业目的，只要给出**适当署名**、提供许可协议的链接，
并说明是否作了修改。完整条款见 [`LICENSE`](LICENSE)。

The two pages in this repository and this README are licensed under a
**Creative Commons Attribution 4.0 International License (CC BY 4.0)**. You are free to share
and adapt the material, including for commercial purposes, so long as you give appropriate
credit, provide a link to the licence, and indicate if changes were made. Full terms in
[`LICENSE`](LICENSE).

<https://creativecommons.org/licenses/by/4.0/>

建议的署名 / Suggested attribution:

> Yisheng Gao，《非结构网格格心／格点格式的二维标量方程离散伴随》，CC BY 4.0，
> <https://github.com/yishenggaogg/adjoint_education>
