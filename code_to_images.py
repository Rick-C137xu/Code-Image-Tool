import argparse
import sys
from io import BytesIO
from pathlib import Path


DEFAULT_INPUT_DIR = Path("input_code")
DEFAULT_OUTPUT_DIR = Path("code_images")
DEFAULT_LINES_PER_IMAGE = 50
DEFAULT_FONT_SIZE = 20
DEFAULT_STYLE = "pycharm-dark"
DEFAULT_FONT_NAME = "Microsoft YaHei"
ENCODINGS_TO_TRY = ["utf-8-sig", "utf-8", "gbk", "gb18030", "cp936"]
FONT_FILE_CANDIDATES = {
    "jetbrains mono": [
        "C:/Windows/Fonts/JetBrainsMono-Regular.ttf",
        "C:/Windows/Fonts/JetBrainsMonoNL-Regular.ttf",
    ],
    "consolas": [
        "C:/Windows/Fonts/consola.ttf",
    ],
    "microsoft yahei mono": [
        "C:/Windows/Fonts/msyh.ttc",
    ],
    "microsoft yahei": [
        "C:/Windows/Fonts/msyh.ttc",
    ],
    "微软雅黑": [
        "C:/Windows/Fonts/msyh.ttc",
    ],
    "simhei": [
        "C:/Windows/Fonts/simhei.ttf",
    ],
}


def import_dependencies():
    try:
        from PIL import Image, ImageDraw, ImageFont
        from pygments import highlight
        from pygments.formatters import ImageFormatter
        from pygments.lexers import PythonLexer
        from pygments.style import Style
        from pygments.token import (
            Comment,
            Error,
            Generic,
            Keyword,
            Literal,
            Name,
            Number,
            Operator,
            Other,
            Punctuation,
            String,
            Text,
            Whitespace,
        )
        from pygments.util import ClassNotFound
    except ImportError:
        print("缺少运行依赖，请先运行：pip install pillow pygments")
        sys.exit(1)

    return {
        "Image": Image,
        "ImageDraw": ImageDraw,
        "ImageFont": ImageFont,
        "highlight": highlight,
        "ImageFormatter": ImageFormatter,
        "PythonLexer": PythonLexer,
        "Style": Style,
        "tokens": {
            "Comment": Comment,
            "Error": Error,
            "Generic": Generic,
            "Keyword": Keyword,
            "Literal": Literal,
            "Name": Name,
            "Number": Number,
            "Operator": Operator,
            "Other": Other,
            "Punctuation": Punctuation,
            "String": String,
            "Text": Text,
            "Whitespace": Whitespace,
        },
        "ClassNotFound": ClassNotFound,
    }


def build_pycharm_dark_style(Style, tokens):
    Comment = tokens["Comment"]
    Error = tokens["Error"]
    Generic = tokens["Generic"]
    Keyword = tokens["Keyword"]
    Literal = tokens["Literal"]
    Name = tokens["Name"]
    Number = tokens["Number"]
    Operator = tokens["Operator"]
    Other = tokens["Other"]
    Punctuation = tokens["Punctuation"]
    String = tokens["String"]
    Text = tokens["Text"]
    Whitespace = tokens["Whitespace"]

    class PyCharmDarkStyle(Style):
        background_color = "#1E1F22"
        default_style = "#BCBEC4"
        line_number_color = "#6C707A"
        line_number_background_color = "#24252A"

        styles = {
            Text: "#BCBEC4",
            Whitespace: "#BCBEC4",
            Error: "#F75464",
            Other: "#BCBEC4",
            Keyword: "#CF8E6D",
            Keyword.Constant: "#CF8E6D",
            Keyword.Declaration: "#CF8E6D",
            Keyword.Namespace: "#CF8E6D",
            Keyword.Pseudo: "#CF8E6D",
            Keyword.Reserved: "#CF8E6D",
            Keyword.Type: "#CF8E6D",
            Name: "#BCBEC4",
            Name.Attribute: "#BCBEC4",
            Name.Builtin: "#56A8F5",
            Name.Builtin.Pseudo: "#56A8F5",
            Name.Class: "#BDAE8B",
            Name.Constant: "#9876AA",
            Name.Decorator: "#B3AE60",
            Name.Entity: "#BCBEC4",
            Name.Exception: "#BDAE8B",
            Name.Function: "#DCDCAA",
            Name.Function.Magic: "#DCDCAA",
            Name.Label: "#BCBEC4",
            Name.Namespace: "#BCBEC4",
            Name.Other: "#BCBEC4",
            Name.Property: "#BCBEC4",
            Name.Tag: "#CF8E6D",
            Name.Variable: "#BCBEC4",
            Name.Variable.Class: "#BCBEC4",
            Name.Variable.Global: "#BCBEC4",
            Name.Variable.Instance: "#BCBEC4",
            Name.Variable.Magic: "#BCBEC4",
            Literal: "#BCBEC4",
            Literal.Date: "#BCBEC4",
            String: "#6AAB73",
            String.Affix: "#6AAB73",
            String.Backtick: "#6AAB73",
            String.Char: "#6AAB73",
            String.Delimiter: "#6AAB73",
            String.Doc: "italic #7A8B73",
            String.Double: "#6AAB73",
            String.Escape: "#CF8E6D",
            String.Heredoc: "#6AAB73",
            String.Interpol: "#6AAB73",
            String.Other: "#6AAB73",
            String.Regex: "#6AAB73",
            String.Single: "#6AAB73",
            String.Symbol: "#6AAB73",
            Number: "#2AACB8",
            Operator: "#BCBEC4",
            Operator.Word: "#CF8E6D",
            Punctuation: "#BCBEC4",
            Comment: "italic #7A8B73",
            Comment.Hashbang: "#7A8B73",
            Comment.Multiline: "italic #7A8B73",
            Comment.Preproc: "#B3AE60",
            Comment.PreprocFile: "#6AAB73",
            Comment.Single: "italic #7A8B73",
            Comment.Special: "bold italic #7A8B73",
            Generic: "#BCBEC4",
            Generic.Deleted: "#F75464",
            Generic.Emph: "italic #BCBEC4",
            Generic.Error: "#F75464",
            Generic.Heading: "bold #DCDCAA",
            Generic.Inserted: "#6AAB73",
            Generic.Output: "#BCBEC4",
            Generic.Prompt: "#6C707A",
            Generic.Strong: "bold #BCBEC4",
            Generic.Subheading: "#DCDCAA",
            Generic.Traceback: "#F75464",
        }

    return PyCharmDarkStyle


def parse_args():
    parser = argparse.ArgumentParser(
        description="把 Python 代码按行数拆分成多张带行号的 PNG 图片。"
    )
    parser.add_argument("--file", help="指定要转换的 Python 文件，例如 input_code/main.py")
    parser.add_argument(
        "--lines",
        type=int,
        default=DEFAULT_LINES_PER_IMAGE,
        help=f"每张图片包含的代码行数，默认 {DEFAULT_LINES_PER_IMAGE}",
    )
    parser.add_argument(
        "--style",
        default=DEFAULT_STYLE,
        help=f"高亮主题，默认 {DEFAULT_STYLE}，可用 default、monokai 等 Pygments 主题",
    )
    parser.add_argument(
        "--font-size",
        type=int,
        default=DEFAULT_FONT_SIZE,
        help=f"字体大小，默认 {DEFAULT_FONT_SIZE}",
    )
    parser.add_argument(
        "--font",
        default=DEFAULT_FONT_NAME,
        help=f"图片字体，默认 {DEFAULT_FONT_NAME}，中文异常时建议使用 Microsoft YaHei",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="生成前清空 code_images 中旧的 PNG 图片，默认不会清空",
    )
    return parser.parse_args()


def find_input_file(file_arg):
    if file_arg:
        path = Path(file_arg)
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(
                f"找不到输入文件：{path}\n请把 .py 文件放到 input_code 里，或者用 --file 指定路径。"
            )
        return path

    py_files = sorted(DEFAULT_INPUT_DIR.glob("*.py"))
    if not py_files:
        raise FileNotFoundError(
            "没有找到可转换的 Python 文件。\n"
            "请把 .py 文件放到 input_code 文件夹里，或者用 --file 指定路径。"
        )
    return py_files[0]


def read_text_auto_encoding(file_path):
    last_error = None

    for encoding in ENCODINGS_TO_TRY:
        try:
            text = file_path.read_text(encoding=encoding)
            print(f"使用编码：{encoding}")
            return text
        except UnicodeDecodeError as error:
            last_error = error

    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        raise OSError(f"读取文件失败：{error}") from error

    print("使用编码：utf-8(errors=replace)")
    print(f"提示：文件编码可能异常，已用替换方式兜底读取。原始错误：{last_error}")
    return text


def read_code_lines(path):
    return read_text_auto_encoding(path).splitlines()


def clear_old_images(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    for image_path in output_dir.glob("*.png"):
        image_path.unlink()


def resolve_font_for_formatter(font_name):
    if Path(font_name).exists():
        return font_name

    for candidate in FONT_FILE_CANDIDATES.get(font_name.lower(), []):
        if Path(candidate).exists():
            return candidate

    return font_name


def get_title_font(ImageFont, font_name, font_size):
    font_candidates = [
        font_name,
        "Microsoft YaHei Mono",
        "Microsoft YaHei",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msyhl.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]

    for candidate in font_candidates:
        try:
            if Path(candidate).exists() or not any(sep in candidate for sep in ["/", "\\"]):
                return ImageFont.truetype(candidate, font_size)
        except OSError:
            continue

    return ImageFont.load_default()


def is_dark_style(style_name):
    return style_name.lower() in {"pycharm-dark", "monokai", "native", "fruity"}


def add_title(Image, ImageDraw, ImageFont, code_image, title, font_name, font_size, style_name):
    title_font = get_title_font(ImageFont, font_name, max(font_size - 2, 14))
    padding_x = 16
    padding_y = 8
    title_gap = 0

    dark = is_dark_style(style_name)
    bg_color = "#1E1F22" if dark else "#FFFFFF"
    title_color = "#BCBEC4" if dark else "#303030"

    measure_image = Image.new("RGB", (1, 1), bg_color)
    draw = ImageDraw.Draw(measure_image)
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_height = bbox[3] - bbox[1]

    title_bar_height = padding_y * 2 + title_height
    new_width = max(code_image.width, bbox[2] - bbox[0] + padding_x * 2)
    new_height = title_bar_height + title_gap + code_image.height
    result = Image.new("RGB", (new_width, new_height), bg_color)

    draw = ImageDraw.Draw(result)
    draw.text((padding_x, padding_y), title, fill=title_color, font=title_font)
    result.paste(code_image.convert("RGB"), (0, title_bar_height + title_gap))
    return result


def resolve_style(style_name, deps):
    if style_name.lower() == "pycharm-dark":
        return build_pycharm_dark_style(deps["Style"], deps["tokens"])
    return style_name


def render_chunk(
    chunk_text,
    line_start,
    title,
    output_path,
    style_name,
    font_name,
    font_size,
    deps,
):
    Image = deps["Image"]
    ImageDraw = deps["ImageDraw"]
    ImageFont = deps["ImageFont"]
    highlight = deps["highlight"]
    ImageFormatter = deps["ImageFormatter"]
    PythonLexer = deps["PythonLexer"]
    ClassNotFound = deps["ClassNotFound"]

    dark = is_dark_style(style_name)
    style = resolve_style(style_name, deps)
    formatter_font = resolve_font_for_formatter(font_name)

    try:
        formatter = ImageFormatter(
            style=style,
            font_name=formatter_font,
            font_size=font_size,
            line_numbers=True,
            line_number_start=line_start,
            line_pad=5,
            image_pad=14,
            line_number_fg="#6C707A" if dark else "#666666",
            line_number_bg="#24252A" if dark else "#F4F4F4",
        )
    except ClassNotFound:
        raise ValueError(
            f"找不到主题：{style_name}。可以试试 pycharm-dark、default、friendly、monokai。"
        )
    except Exception as error:
        if error.__class__.__name__ not in {"FontNotFound", "OSError"}:
            raise
        raise ValueError(
            f"字体加载失败：{font_name}。\n"
            "可以改用 --font \"Microsoft YaHei\"，或确认系统已安装该字体。"
        ) from error

    buffer = BytesIO()
    highlight(chunk_text, PythonLexer(), formatter, outfile=buffer)
    buffer.seek(0)

    code_image = Image.open(buffer).convert("RGB")
    final_image = add_title(
        Image,
        ImageDraw,
        ImageFont,
        code_image,
        title,
        formatter_font,
        font_size,
        style_name,
    )
    final_image.save(output_path)


def generate_images(input_file, lines, style, font, font_size, clear):
    if lines <= 0:
        raise ValueError("--lines 必须是大于 0 的整数。")
    if font_size <= 0:
        raise ValueError("--font-size 必须是大于 0 的整数。")

    deps = import_dependencies()
    output_dir = DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    if clear:
        clear_old_images(output_dir)

    code_lines = read_code_lines(input_file)
    total_lines = len(code_lines)
    if total_lines == 0:
        raise ValueError("输入文件是空的，没有可生成的代码图片。")

    stem = input_file.stem
    image_count = 0

    for start_index in range(0, total_lines, lines):
        end_index = min(start_index + lines, total_lines)
        chunk_lines = code_lines[start_index:end_index]
        chunk_text = "\n".join(chunk_lines) + "\n"
        line_start = start_index + 1
        line_end = end_index
        image_count += 1

        title = f"{input_file.name} 第 {line_start}-{line_end} 行"
        output_path = output_dir / f"{stem}_part_{image_count:03d}.png"
        render_chunk(
            chunk_text,
            line_start,
            title,
            output_path,
            style,
            font,
            font_size,
            deps,
        )

    return total_lines, image_count, output_dir


def main():
    args = parse_args()

    try:
        input_file = find_input_file(args.file)
        total_lines, image_count, output_dir = generate_images(
            input_file=input_file,
            lines=args.lines,
            style=args.style,
            font=args.font,
            font_size=args.font_size,
            clear=args.clear,
        )
    except (FileNotFoundError, ValueError, OSError) as error:
        print(error)
        sys.exit(1)

    print("生成完成！")
    print(f"输入文件路径：{input_file.resolve()}")
    print(f"总行数：{total_lines}")
    print(f"每张图片行数：{args.lines}")
    print(f"生成图片数量：{image_count}")
    print(f"输出文件夹路径：{output_dir.resolve()}")


if __name__ == "__main__":
    main()
