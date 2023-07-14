import subprocess

input_file = r"G:\My Drive\full_professor_promotion_portfolio\full_professor_promotion_reflection_markdown_test.md"
output_file = r"G:\My Drive\full_professor_promotion_portfolio\full_professor_promotion_reflection_with_watermark.pdf"
#watermark_text = "DRAFT"

# Convert Markdown to PDF using Pandoc with watermark
latex_code = r"""
\usepackage{draftwatermark}
"""

subprocess.run(["pandoc", input_file, "-o", output_file, "--pdf-engine=xelatex",
                "--variable", "header-includes:"+latex_code,
                "-V", "colorlinks=true", "-V", "linkcolor=red", "-V", "urlcolor=blue"])