# ArkStar
arknights的数据集合与工具。

非常简陋，功能缺失，测试没有，异常不考虑，写得也很难看，英语语法都有问题，连写着闹着玩玩的程度也不到。可能之后会继续完善，可能就弃坑不管。

# 数据集合
建设中……

可能就咕咕咕了。

# 部署
暂时自行解决。

游戏画面目前需要保持1920x1080横屏状态，同时只存在一个设备开启adb调试。

# 使用哲（？）学

## 数据规划
under construction...

可能就咕咕咕了。

## 掉落检测
工具目前可以在关卡结束时自动识别屏内的掉落物品和掉落数量，但不稳定。

掉落检测从原本的灰度匹配拟改为基于特征点的匹配（本项目`ArkStar`仅作学习用途）。首先提供了自动将掉落物品图片进行突出特征的处理后拆分生成物品特征图的工具，并从特征图中取出不受图像缩放与色差影响的特征点。此后再次使用时，与预设特征点比较从而找到对应的掉落物品编码，从数据库中提取出名称。

掉落数量是对切分出来的数字图片调用`tesseract`进行OCR识别。

代码现在存在和分辨率有关的硬编码，限制非常大。`tesseract`的准确率也比较堪忧。

接下来要做的是去除对硬编码坐标的依赖，将掉落物品识别扩展到对仓库识别。在此之上，完善数据集合收集部分，也许能和现有数据集合的上传接口对接。

有缘再改。

## 辅助工具
辅助工具并非项目重点。

仅能自动化自动代理某一单一关卡，能够获取掉落物品截图，没有从代理失败中恢复的机制，而且也没有任何异常处理、没有考虑任何特殊情况。

使用工具前，明确为什么玩游戏。根据作者独断而带有偏见的思考，举例如下

* 极为重复且占用精力的动作大概率没有乐趣
* 研究关卡的（极限）过法大概率有乐趣
* 欣赏立绘，看舟游沙雕图大概率有乐趣
* 写极为复杂的自动化操作非常没有乐趣
* 作者技术太辣鸡，也没有时间

有其他自动化工具项目，自律程度很高，也许那个会更符合辅助工具的定位。