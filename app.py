import argparse
import google.generativeai as genai
import json
import os
import time

# Configure the Gemini API key
genai.configure(api_key="<YOUR_API_KEY>")

def list_files(directory='.', level=0, max_depth=None):
    """Recursively lists all files and directories up to a specified depth."""
    result = ''
    try:
        if max_depth is not None and level >= max_depth:
            return

        dirs = []
        files = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                dirs.append(item)
            else:
                files.append(item)

        dirs.sort()
        files.sort()

        for dir_name in dirs:
            result += f"{'\t' * level}{dir_name}/\n"
            subresult = list_files(os.path.join(directory, dir_name), level + 1, max_depth)
            if subresult:
                result += subresult

        for file_name in files:
            result += f"{'\t' * level}{file_name}\n"

    except Exception as e:
        print(f"Error: {e}")
    return result

def extract_context_from_files(limit, path='.', depth=0, max_file_size=3 * 1024 * 1024):
    """Recursively extracts data from files in the directory and subdirectories up to a given limit."""
    extracted_data = []

    if depth >= limit:
        return extracted_data

    try:
        for entry in os.scandir(path):
            if entry.is_file():
                try:
                    if os.path.getsize(entry.path) <= max_file_size:
                        with open(entry.path, "r", encoding="utf-8") as f:
                            extracted_data.append(f"{entry.path}:\n{f.read()}\n")
                except Exception as e:
                    print(f"Error reading {entry.path}: {e}")
            elif entry.is_dir():
                extracted_data.extend(extract_context_from_files(limit, entry.path, depth + 1, max_file_size))
    except Exception as e:
        print(f"Error extracting context from {path}: {e}")

    return "".join(extracted_data)

def call_gemini_api(prompt, context=None):
    """Calls the Gemini API with the provided prompt and optional context."""
    try:
        if context:
            prompt = f"{context}\n{prompt}"

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        if response.candidates:
            return response.candidates[0].content.parts[0].text
        else:
            return "No response from AI."
    except Exception as e:
        return f"Error: {e}"

def write_to_file(output, filename):
    """Writes the given output to a specified markdown file."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(output)
        print(f"Output saved to {filename}")
    except Exception as e:
        print(f"Error saving to file {filename}: {e}")

def main():
    start_time = time.time()

    parser = argparse.ArgumentParser(description="An app to call the Gemini API with context and prompt.")
    parser.add_argument(
        "-p", 
        "--prompt", 
        type=str, 
        # required=True, 
        help="Text prompt for the LLM. [Required]"
    )
    parser.add_argument(
        "-f",
        "--files", 
        nargs="?",
        const=1,
        type=int,
        help="Appends files of the current directory up to a depth. Use -f or -f <depth>. Default is 1."
    )
    parser.add_argument(
        "-fs",
        "--filesystem", 
        nargs="?", 
        const=3, 
        type=int, 
        help="Appends file system of the current directory up to a depth. Use -fs or -fs <depth>. Default is 3."
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Shows the entire prompt to be sent to the LLM"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Saves the output to a specified .md file."
    )
    parser.add_argument( # only LLM query without quotes
        "positional_prompt", 
        nargs="*", 
        help="Positional arguments used as the prompt if no flags are provided."
    )

    args = parser.parse_args()

    # Combine positional arguments as prompt if no --prompt flag is provided
    if not args.prompt and args.positional_prompt:
        args.prompt = " ".join(args.positional_prompt)

    if not args.prompt:
        print("Error: No prompt provided. Use -p or provide a prompt as positional arguments.")
        return

    context = ''
    if args.filesystem:
        context += "file system:\n" + list_files(max_depth=args.filesystem) + "\n"
    if args.files:
        context += "files:\n" + extract_context_from_files(args.files) + "\n"

    final_prompt = context + args.prompt
    if args.test:
        print(final_prompt)
    else:
        response = call_gemini_api(final_prompt)

        if args.output:
            write_to_file(response, args.output)
        else:
            response = response.replace('\\n', '\n').replace('**', '')
            print(response)

    end_time = time.time()
    print(f"Execution Time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
