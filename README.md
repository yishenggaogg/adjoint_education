# Discrete adjoint: interactive lessons

Nineteen self-contained, interactive web pages that teach the **fully discrete adjoint** of a finite-volume scheme from start to finish, for undergraduates with a background in calculus, linear algebra and numerical methods. The teaching path leads toward a complete discrete adjoint for industrial unstructured-grid RANS: the 2-D RANS&ndash;SA pages are online (the complete discrete adjoint on a teaching mesh, comparing an adjoint-inconsistent and an adjoint-consistent inflow treatment); industrial scale is still ahead. Continuous adjoints appear only as independent checks for simple cases (Appendix A of the pages); a formal continuous RANS adjoint is not automatically a strict reference for a full industrial algorithm.

**Read online:** <https://yishenggaogg.github.io/adjoint_education/> &mdash; English by default, with a Chinese / English toggle at the top of every page.

**Repositories:** [GitHub](https://github.com/yishenggaogg/adjoint_education) &middot; [Gitee](https://gitee.com/gaoyishenggg/adjoint_education) &mdash; identical content.

Chinese text: see the **中文** block at the end of this page.

## Pages

Eight model problems &mdash; 1-D Burgers, 2-D scalar advection, 2-D advection&ndash;diffusion, quasi-1-D Euler, 1-D laminar Navier&ndash;Stokes, 2-D Euler, 2-D laminar Navier&ndash;Stokes and 2-D RANS&ndash;SA &mdash; each in a cell-centred and a node-centred version (2-D RANS&ndash;SA also as an adjoint-consistent pair), plus one independent viscous Burgers page. If the discrete adjoint is new to you, start with the 1-D Burgers pair.

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
| [`adjoint_burgers_viscous.html`](adjoint_burgers_viscous.html) | 一维黏性 Burgers（独立页）/ 1-D viscous Burgers (independent page) | **格心** / cell-centred（附录 B：格点 / App. B nodal） | 6682 KB |

Each page is one HTML file: open it in a browser &mdash; no network, no build step, no server.

## What the pages do

- **One lesson on every page.** The equation and what it is for, the mesh, the flux on a face; then the same loop written as the primal, as a matrix-free tangent ($Av$) and as a matrix-free adjoint ($A^{\mathsf T}w$); the forward and adjoint solves; design and geometric derivatives; and a term-by-term check against finite differences and the complex step. Each page opens with a roadmap from the design inputs to the gradient.
- **Interactive.** Meshes, face fluxes, statement-by-statement players for the primal, tangent and adjoint, dot-product tests, solver residuals, step-size sweeps and refinement studies run in the browser. Nothing plays by itself, and under the system's reduced-motion setting the Play button is disabled with a short note.
- **Measured, not quoted.** Every number on the pages comes from an actual computation: live in the browser, or offline results that were solved independently and embedded in the page.

## Python

[`python/burgers_viscous/`](python/burgers_viscous/README.md) holds the sparse Python solver, the gradient checks and the measured data behind the viscous Burgers page (run up to 65,536 cells).

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

十九个自包含、可交互的网页，把有限体积法的**全离散伴随**从头到尾讲一遍，面向学过微积分、线性代数与数值方法的本科生。教学主线最终走向工业级非结构网格 RANS 的完整离散伴随：二维 RANS–SA 的页面已经上线（教学网格上完整的离散伴随，并对照伴随不一致与伴随一致两种来流处理），工业级规模仍待推进。连续伴随只作为简单算例的独立验证和对比（各页附录 A）；可以为选定的连续 RANS 模型写出形式伴随，但不能把它自动当作含湍流闭合、壁面处理、限幅与边界算法的完整工业离散流程的严格参照。

**在线阅读：** <https://yishenggaogg.github.io/adjoint_education/>，默认英文，每页顶部可切换中文 / English。

**仓库：** [GitHub](https://github.com/yishenggaogg/adjoint_education) · [Gitee](https://gitee.com/gaoyishenggg/adjoint_education)，内容相同。

### 页面

八组算例——一维 Burgers、二维标量对流、二维标量对流扩散、拟一维 Euler、一维层流 Navier–Stokes、二维 Euler、二维层流 Navier–Stokes 与二维 RANS–SA——各有格心与格点两版（二维 RANS–SA 另有伴随一致的一对），另有一个独立的黏性 Burgers 页。第一次接触离散伴随，请从一维 Burgers 那一对读起。页面表格见上方（文件、算例、格式与大小的列同时标有中英文）。每页都是单个 HTML 文件：不联网、不需要构建、不需要服务器，直接用浏览器打开即可。

### 各页做什么

- **每页同一条主线。**方程与它的作用、网格、面上的通量；再把同一个循环依次写成 primal、matrix-free 前向（$Av$）与 matrix-free 伴随（$A^{\mathsf T}w$）；前向与伴随求解；设计变量与几何导数；最后用有限差分与复数步长逐项校验。每页开头有一幅从设计输入到梯度的路线图。
- **可以动手。**网格、面通量、primal／tangent／adjoint 逐句播放器、点积测试、求解残差、步长扫描与加密实验都在浏览器里运行；任何内容都不会自动播放，系统设置为“减少动态效果”时播放键停用并附一句说明。
- **数字都是实测的。**页面上的每个数字都来自实际计算：浏览器现场计算，或独立求解后内嵌的离线结果。

### Python

[`python/burgers_viscous/`](python/burgers_viscous/README.md)：黏性 Burgers 页背后的稀疏 Python 程序、梯度检查与实测数据（已实跑到 65,536 个单元）。

### 两个仓库的同步

GitHub 是主仓库（网页由 GitHub Pages 从这里发布，每次推送自动重新部署），Gitee 是镜像。把 `origin` 配成同时推送到两个仓库，一条 `git push` 就能更新两边：命令见上方英文部分（第一条替换默认的 push 地址，第二条再追加，两条都要执行）。用 `git ls-remote <url> refs/heads/main` 比较两边是否一致；若某个平台的网页端直接改过文件而 SHA 不同，先 `git pull gitee main --rebase`（或 `github`）取回对方的提交再推，**不要用 `--force`**，那会抹掉网页端的改动。

### 许可

© 2026 Yisheng Gao。本仓库的页面、连续伴随推导与本 README 以 **知识共享 署名 4.0 国际（CC BY 4.0）** 许可发布：您可以自由地共享与改编，包括用于商业目的，只要给出**适当署名**、提供许可协议的链接，并说明是否作了修改。完整条款见 [`LICENSE`](LICENSE)。

</details>
