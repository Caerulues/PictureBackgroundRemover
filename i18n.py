from PySide6.QtCore import QLocale


TEXTS = {
    "zh": {
        "window_title": "纯色背景去除工具",
        "select_image": "选择图片",
        "export_png": "导出透明 PNG",
        "tolerance": "容差",
        "edge_softness": "边缘柔化",
        "select_image_first": "请先选择图片",
        "done": "完成",
        "saved_to": "已保存到：",
        "preview_placeholder": "请选择图片",
        "tip": (
            "说明：\n"
            "默认使用左上角颜色作为背景色。\n\n"
            "适合白底、黑底、灰底、纯色底图标。"
        ),
    },
    "en": {
        "window_title": "Solid Background Remover",
        "select_image": "Select Image",
        "export_png": "Export Transparent PNG",
        "tolerance": "Tolerance",
        "edge_softness": "Edge Softness",
        "select_image_first": "Please select an image first",
        "done": "Done",
        "saved_to": "Saved to:",
        "preview_placeholder": "Please select an image",
        "tip": (
            "Note:\n"
            "The top-left pixel is used as the background color by default.\n\n"
            "Best for white, black, gray, or solid-color icon backgrounds."
        ),
    },
}


def get_system_language() -> str:
    language = QLocale.system().language()

    if language == QLocale.Language.Chinese:
        return "zh"

    return "en"


def t(key: str) -> str:
    lang = get_system_language()
    return TEXTS.get(lang, TEXTS["en"]).get(key, key)