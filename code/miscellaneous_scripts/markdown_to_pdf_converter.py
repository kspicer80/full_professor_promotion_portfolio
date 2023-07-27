import subprocess

def convert_markdown_to_pdf_with_pandoc():
    input_file = r"stripped_sidenote_tags.md"
    output_file = r"test_1.pdf"

    # Get pandoc command ready:
    pandoc_command = [
        "pandoc",
        input_file,
        "-V colorlinks=true",
        "-V linkcolor=blue",
        "-V urlcolor=blue",
        "-o",
        output_file
    ]

    try:
        subprocess.run(pandoc_command, check=True)
        print("Conversion to .pdf has been successful!")
    except subprocess.CalledProcessError as error:
        print("Conversion failed:", error)

if __name__ == "__main__":
    convert_markdown_to_pdf_with_pandoc()