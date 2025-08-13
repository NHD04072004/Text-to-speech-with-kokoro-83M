import os
import wave


def read_txt(file_path) -> str:
    """
    Reads a text file and returns its content as a string.

    Args:
        file_path (str): The path to the text file.

    Returns:
        str: The content of the text file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    return content.strip()

def concat_wav(input_files: list[str], output_file):
    data = []
    for file in input_files:
        with wave.open(file, "rb") as w:
            data.append([w.getparams(), w.readframes(w.getnframes())])

    with wave.open(output_file, "wb") as output:
        output.setparams(data[0][0])
        for i in range(len(data)):
            output.writeframes(data[i][1])