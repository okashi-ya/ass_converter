# ass_converter
一个可以将B站弹幕转换成ass字幕格式的工具。

开发：古守のお菓子屋

链接：https://space.bilibili.com/253052708

### 用法
将需要转换的弹幕文件放入danmu目录下，运行ass_converter.bat。

---
#### 当前支持转换的类型
+ 录播姬的xml格式弹幕（支持碎片弹幕自动整合）【推荐】
+ MatsuriICU的json格式弹幕【推荐】
+ MatsuriICU的xml格式弹幕
+ Danmakus的json格式弹幕【推荐】
+ Danmakus的xml格式弹幕

### 注意
1.同一场直播的弹幕会互相合并至同一个文件内，且不会去重。故本身支持碎片弹幕整合，所以也尽可能不要将一场直播中弹幕时间有交集的片段进行一次性转换。会导致弹幕重复。

2.Matsuri的xml格式弹幕因内容中没有开始时间等信息，故不要修改其本身的文件名！否则会转换出错。

3.Matsuri的弹幕如果是仅包含同传弹幕（网页端下载时选择的），则需要将ass_converter/config.py中MatsuriICUFullDanmu改为False。

4.Danmakus的xml格式弹幕并非标准xml格式，在代码侧是做了特殊处理的。可能会不稳定。

## 功能模块
### ass_io I/O交互
	ass文件写入
	ass_writer.py
	
	弹幕文件读取
	danmu_file_reader.py
### filter 过滤器
	弹幕过滤器
	danmu_filter.py
### loader 加载器
	加载器工厂类
	loader_factory.py
	
	基本加载器抽象类定义
	base_loader.py
	
	B站录播姬的xml格式弹幕加载器
	bililive_recorder_xml_loader.py
	
	yDanmakus的json格式弹幕加载器
	danmakus_json_loader.py
	
	Danmakus的xml格式弹幕加载器
	danmakus_xml_loader.py
	
	MatsuriICU的json格式弹幕加载器
	matsuri_icu_json_loader.py
	
	MatsuriICU的xml格式弹幕加载器
	matsuri_icu_xml_loader.py
### log 日志
	日志实现
	logger.py
### config.py 配置文件

