# USTC助教统分助手
## 介绍
* statistic.py：成绩统计，可以自动绘制直方图，计算中位数、平均数、前百分之40分数线等统计量，并生成csv统计表。
* query.py：运行于80号端口的一个Web服务器（端口号可以更改），支持模糊查分和准确查分。模糊查分时会生成一张灰度图，根据成绩和排名计算灰度，图片越黑代表考得越好（灰度范围可能取0~255的任意值，且已归一化，即比有人取0也必有人取255）。如果老师要求暂不支持准确查分，可以在相关注释处的代码进行更改。
## 文件层次
* templates：存放web的静态文件
* data.txt：学生成绩，仿照相同格式填写即可
* \*.py：程序源码
## 灰度计算方法
* 求出排名，注意最**低**分排名为0，排名值越大分数越低。
* 归一化排名。排名更新为原始排名/排名最大值。
* 成绩归一化，成绩=(原始成绩-最低分)/(最高分-最低分)
* 最终综合分数=0.3\*成绩+0.7\*排名，权重可以根据实际情况调整。
* 像素值=(1-分数)*255

当然，以上计算方法可以仅作了解，只要知道考得越好图片越黑就行了。
## 注意事项
生成QQ号证明时应选择完整学号，比如要选择PB20114514而不是PB\*\*\*\*\*\*\*\*，否则系统将无法根据认证返回的学号查找分数。
## 部署示例
http://47.108.160.172:7777/