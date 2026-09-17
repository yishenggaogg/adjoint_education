# 离散伴随教学页 / Discrete adjoint, taught page by page

两个**单文件、可交互**的网页，把非结构网格有限体积法的**全离散伴随**从头到尾讲一遍：
从一个面上的一维通量开始，把同一个循环依次改写成 primal、matrix-free 前向（$Av$）与
matrix-free 伴随（$A^{\mathsf T}w$），再做伴随求解、几何导数 $\mathrm dR/\mathrm dX$、
$\mathrm dL/\mathrm dX$，最后用有限差分逐项校验。

Two **self-contained, interactive** web pages that develop the **fully discrete adjoint**
of an unstructured finite-volume scheme end to end: starting from the one-dimensional flux
on a single face, the same loop is rewritten as the primal, as matrix-free forward mode
($Av$) and as matrix-free adjoint mode ($A^{\mathsf T}w$), followed by the adjoint solve,
the geometric derivatives $\mathrm dR/\mathrm dX$ and $\mathrm dL/\mathrm dX$, and a
term-by-term finite-difference verification.

| 文件 / File | 格式 / Scheme | 大小 |
|---|---|---|
| [`adjoint_cell.html`](adjoint_cell.html) | **格心**格式（单元中心有限体积）/ **cell-centred** finite volume | 516 KB |
| [`adjoint_node.html`](adjoint_node.html) | **格点**格式（中位对偶控制体）/ **node-centred** median-dual | 677 KB |

直接用浏览器打开即可：**没有任何外部依赖**，不联网、不需要构建、不需要服务器。
Just open either file in a browser — **no external dependencies**, no network, no build step,
no server. Each page has a 中文 / English toggle in the top-right corner.

---

## 两个页面讲的是同一件事的两种格式

两页结构完全平行，都是 12 节，用的是**同一张网格**、同一个标量方程、同一个目标函数，
只有未知量的位置不同——因此可以并排对照阅读。

The two pages are strictly parallel — 12 sections each, the **same mesh**, the same scalar
equation and the same objective. Only the location of the unknowns differs, so they can be
read side by side.

| | 格心 / cell-centred | 格点 / node-centred |
|---|---|---|
| 未知量 / Unknowns | 24 个单元平均值 / 24 cell averages | 24 个节点值 / 24 nodal values |
| 循环 / Loop | 面循环，48 个面 / face loop, 48 faces | 边循环，80 个面 / edge loop, 80 faces |
| 面的构成 / Faces | 32 内部 + 8 壁面 + 8 远场 | 48 个对偶面 + 32 个边界半面 |
| $A$ 的非零元 / nnz | 88 | 120 |
| 无滑移 / No-slip | **弱**加：通量里取常数右状态 $u_R=u_w$ / **weak**: a constant right state inside the flux | **强**加：整行换成 $u_i-u_w$ / **strong**: whole-row replacement |

物面无滑移的这一处差别正是两页的重点：格心格式物面上**没有**自由度，只能弱加；
格点格式壁面节点**本身就是未知量**，所以强加才是真实做法，代价是 primal 换行、tangent
覆盖行、adjoint 在循环**前**清零、循环**后**加回——四处动作必须一致。

That single difference is the point of the pair: a cell-centred scheme has **no** degree of
freedom on the body and can only impose no-slip weakly, whereas a node-centred scheme has the
wall node **as an unknown**, so strong imposition is what a solver really does — at the price
of a replaced row in the primal, an overwritten row in the tangent, and a zeroing **before**
the loop with an add-back **after** it in the adjoint. All four must agree.

## 模型问题 / The model problem

- 标量守恒律 $F(u)=\tfrac12u^2\beta$，$\beta=(1,\,0.5)$，一阶、无重构，常数耗散 $\varepsilon=0.8$
- 环形（O 型）混合网格：贴壁一层四边形（8 个）+ 外层三角形（16 个）
- 内圈物面，外圈远场特征边界（4 个入流 + 4 个出流，开关在 $u^*$ 处冻结）
- Newton 固定跑 60 轮并检查判据 $\max_i|\delta u_i|<10^{-13}$，稠密 LU
- 目标函数：类似阻力的物面积分 $L=\sum_{\text{wall}}\tfrac12u^2(n\cdot e)$
- 设计变量：全部节点坐标，共 48 个分量

A scalar conservation law on a hybrid annular O-mesh, first order with no reconstruction and
constant dissipation; an inviscid or no-slip body on the inner ring, a characteristic
far-field on the outer ring with the switch frozen at $u^*$; Newton with a dense LU; a
drag-like surface integral as the objective; and all 48 node coordinates as design variables.

## 每页的 12 节 / The twelve sections

1. 网格 / Mesh — 单元与面，或对偶控制体的构造
2. 方程与面上的一维通量 / The equation and the one-dimensional flux
3. 边界条件 / Boundary conditions
4. 残差 = 循环：收集、计算、分发 / Residual = the loop: gather, compute, scatter
5. 求解：Jacobian 与 Newton 法 / The solve: the Jacobian and Newton
6. 目标函数 / The objective function
7. matrix-free 前向：计算 $Av$ / Matrix-free forward: computing $Av$
8. matrix-free 伴随：计算 $A^{\mathsf T}w$ / Matrix-free adjoint: computing $A^{\mathsf T}w$
9. 求解伴随方程 / Solving the adjoint equation
10. 几何导数 $\mathrm dR/\mathrm dX$ 与 $\mathrm dL/\mathrm dX$ / Geometric derivatives
11. 验证：$\mathrm dL/\mathrm dX$ 对有限差分 / Verification against finite differences
12. 总结 / Summary

## 可以动手的地方 / What is interactive

每页 6–7 个交互面板，12–14 幅图全部由代码生成：

- **网格浏览器**：点任意单元／节点，看它的面、法向、残差各项与 $u^*$ 处的值
- **一维通量**：拖滑块，看中心项与耗散项怎么合成通量
- **三个循环逐句播放**：primal、tangent、adjoint 各一个，每一行伪代码对应一步，
  数组里的数字随之变化——转置在数据流上长什么样，一眼可见
- **Newton 与 Jacobi 面板**：逐轮、逐面播放
- **点积测试**：随机向量，现场验证 $\langle w,Av\rangle=\langle A^{\mathsf T}w,v\rangle$
- **梯度与步长扫描**：逐个设计变量把有限差分误差随 $h$ 的曲线扫出来

Six to seven interactive panels per page and 12–14 generated figures. The three loops can be
played statement by statement, with the arrays updating as each pseudocode line executes.

## 页面上的数字都是实测的 / Every number is measured

页面引用的每一个数值都是在浏览器里现场算出来的，不是写死的文字：

| 检验 / Check | 格心 | 格点 |
|---|---|---|
| 点积测试 $\langle w,Av\rangle=\langle A^{\mathsf T}w,v\rangle$ | 8.9e−16 | 6.7e−16 |
| 清零／加回顺序写反 / with the zero-and-add-back order reversed | — | 0.31 |
| 梯度对全链路中心差分 / gradient vs full-chain central differences | 5.4e−11 | 5.1e−11 |
| 前向 vs 伴随的求解次数 / solves: forward vs adjoint | 48 : 1 | 48 : 1 |

第 11 节还专门演示了差分校验本身的陷阱：步长取大取小都会让“验证”看起来像失败，
而点积测试是精确恒等式，根本不含步长。

Section 11 also demonstrates the trap in finite-difference verification itself — too large or
too small a step makes a correct gradient look wrong — which is why the dot-product test,
an exact identity with no step size in it, is the more reliable check.
