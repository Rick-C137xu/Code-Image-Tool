# 代码自动拆分截图工具

这个工具用于把较长的 Python 代码文件按固定行数拆成多张 PNG 图片。图片会带代码高亮、真实行号和顶部小标题，方便插入 Word/WPS 实验报告。

现在默认效果是接近 PyCharm 深色主题：深色背景、左侧行号、代码高亮、顶部显示文件名和行号范围。

## 文件夹结构

```text
Code_Image_Tool/
├── code_to_images.py
├── README.md
├── input_code/
│   └── .gitkeep
└── code_images/
    └── .gitkeep
```

- `code_to_images.py`：主脚本。
- `input_code`：放待截图的 Python 代码文件。
- `code_images`：保存自动生成的 PNG 图片。

## 第一次使用前安装依赖

在命令行进入本文件夹后运行：

```bash
pip install pillow pygments
```

如果脚本提示缺少依赖，也按这条命令安装。

## 最简单使用方法

把自己的 `.py` 文件放到 `input_code` 文件夹里，然后运行：

```bash
python code_to_images.py
```

如果没有指定文件，脚本会自动读取 `input_code` 中第一个 `.py` 文件。

## 指定文件使用方法

```bash
python code_to_images.py --file input_code/main.py
```

生成图片会保存到 `code_images` 文件夹中，命名类似：

```text
main_part_001.png
main_part_002.png
main_part_003.png
```

## 修改每张图片行数

默认每张图片 50 行。图片太长时可以减少行数：

```bash
python code_to_images.py --file input_code/main.py --lines 40
```

## 修改字体大小

默认字体大小是 20。图片看起来太小可以调大：

```bash
python code_to_images.py --file input_code/main.py --font-size 24
```

## 修改字体

脚本支持通过 `--font` 指定字体：

```bash
python code_to_images.py --file input_code/main.py --font "Microsoft YaHei"
```

也可以使用更像代码编辑器的字体：

```bash
python code_to_images.py --file input_code/main.py --font "Consolas"
python code_to_images.py --file input_code/main.py --font "JetBrains Mono"
```

说明：

- 如果更在意代码等宽效果，可以用 `Consolas` 或 `JetBrains Mono`。
- 如果中文注释显示异常，建议用 `Microsoft YaHei`。
- 当前默认字体是 `Microsoft YaHei`，优先保证中文注释正常显示。

## 修改主题

默认主题是 `pycharm-dark`，尽量接近 PyCharm 深色编辑器效果：

```bash
python code_to_images.py --file input_code/main.py --style pycharm-dark
```

说明：

- `pycharm-dark` 是手动模拟 PyCharm 深色主题，不是自动读取你当前 PyCharm 设置。
- 当前版本已经补全 `Punctuation`、`Operator`、`Name`、`Text` 等 token，括号、逗号、点号、普通变量和函数调用在深色背景上都会使用浅灰色，不会再发黑。
- 不建议自动读取 PyCharm 主题文件，因为 JetBrains 主题配置和 Pygments token 并不是一一对应的，直接转换反而容易出现颜色错位。

如果想用白底实验报告风格：

```bash
python code_to_images.py --file input_code/main.py --style default
```

也可以使用 Pygments 自带主题，例如：

```bash
python code_to_images.py --file input_code/main.py --style monokai
```

## 清空旧图片重新生成

默认不会清空 `code_images`，避免误删之前生成的图片。确认要清空旧 PNG 后重新生成时，加上 `--clear`：

```bash
python code_to_images.py --file input_code/main.py --clear
```

注意：`--clear` 只会删除 `code_images` 文件夹里的 `.png` 图片。

## 中文变成 ???? 的原因和解决方法

如果代码文件实际是 GBK/ANSI 编码，却按 UTF-8 读取，中文注释就可能变成乱码，甚至在图片里显示成 `????`。

现在脚本会自动按顺序尝试：

```text
utf-8-sig
utf-8
gbk
gb18030
cp936
```

读取成功后，终端会输出实际使用的编码，例如：

```text
使用编码：gbk
```

如果全部失败，脚本会用 `errors="replace"` 兜底读取，并提示文件编码可能异常。中文仍然显示异常时，建议先试：

```bash
python code_to_images.py --file input_code/main.py --font "Microsoft YaHei"
```

如果还是不正常，可以用编辑器把代码文件另存为 `UTF-8` 编码后再生成。

## 常见问题

### 找不到文件怎么办

确认 `.py` 文件已经放进 `input_code` 文件夹。也可以直接指定文件：

```bash
python code_to_images.py --file input_code/main.py
```

### 中文注释显示异常怎么办

先使用中文字体：

```bash
python code_to_images.py --file input_code/main.py --font "Microsoft YaHei"
```

再确认代码文件编码是否是 UTF-8、GBK、GB18030 或 CP936。

### 图片太长怎么办

减少每张图片行数：

```bash
python code_to_images.py --file input_code/main.py --lines 35
```

### 图片太小怎么办

调大字体：

```bash
python code_to_images.py --file input_code/main.py --font-size 24
```

### 生成图片太多怎么办

增加每张图片行数：

```bash
python code_to_images.py --file input_code/main.py --lines 70
```

## 推荐命令

平时推荐这样生成 PyCharm 深色风格图片：

```bash
python code_to_images.py --file input_code/main.py --lines 50 --clear --style pycharm-dark --font "Microsoft YaHei"
```

## 实验报告中的推荐写法

由于完整源代码行数较多，正文仅展示主要功能模块代码截图，完整代码已按行号拆分为多张图片作为附件提交。
