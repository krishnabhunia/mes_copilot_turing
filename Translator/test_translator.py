import subprocess


def run_normal():
    lang_list = ['zh', 'es', 'fr', 'de', 'nl', 'it', 'hu', 'pt', 'fi', 'sv']
    for lang in lang_list:
        print(f"Execution started for : 'en' '{lang}'")
        run_test('en', lang)
        print(f"Execution started for : '{lang}' 'en'")
        run_test(lang, 'en')
        print("Loop complete")


def run_test(exist_lang, new_lang):
    # Define the script and arguments
    script_name = "translator.py"

    # Execute the script with arguments
    try:
        result = subprocess.run(
            ["python", script_name, exist_lang, new_lang],
            capture_output=True,
            text=True,
            check=True
        )
        print("Output:", result.stdout)
        print("Errors:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    run_normal()
