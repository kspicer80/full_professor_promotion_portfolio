import subprocess

def convert_markdown_to_pdf_with_pandoc():
    input_file = "full_professor_promotion_reflection.html"
    output_file = "test.pdf"

    # Get pandoc command ready:
    pandoc_command = [
        "pandoc",
        #"--citeproc",
        input_file,
        "--variable=colorlinks:true",
        "--variable=linkcolor:red",
        "--variable=urlcolor:blue",
        "-o",
        output_file
    ]

    try:
        subprocess.run(pandoc_command, check=True)
        print("Conversion to PDF has been successful—file name:", output_file)
    except subprocess.CalledProcessError as error:
        print("Conversion to PDF failed:", error)

if __name__ == "__main__":
    convert_markdown_to_pdf_with_pandoc()