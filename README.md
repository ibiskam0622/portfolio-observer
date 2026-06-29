# 组合观察 · 独立观察站

独立 SPA，绕过原网站前端直接调用 http://43.161.221.88:16888/api/...

数据源：
- `/api/portfolios` — 组合列表
- `/api/portfolio-info` — 净值/收益/说明
- `/api/portfolio-position` — 持仓（市场/行业/个股）
- `/api/profit-chart` — 收益曲线

API 返数字都是「亿分比」整数，前端除以 1e9 还原。
