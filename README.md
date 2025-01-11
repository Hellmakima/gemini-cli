# Gemini API Usage Program

This lightweight utility is designed for interacting with the Gemini API. It generates responses based on user-provided prompts and optional context extracted from files or directory structures. It’s ideal for small-scale projects due to the token limit of the Gemini API.

https://github.com/user-attachments/assets/4d341d30-1f41-44d8-bea3-dcf149d5a911


## Features

- **Custom Prompts**: Send any prompt to the Gemini API for a response.
- **File Context**: Add content from files within a directory, up to a specified depth.
- **Directory Structure**: Include a list of files and folders as part of the context.
- **Save Responses**: Export API responses to a `.md` file for documentation.
- **Test Mode**: Preview the combined prompt and context before submitting it.

## Limitations

- **No Persistent Context**: Context must be explicitly provided for each query; nothing is retained across runs.
- **Token Constraints**: The API has a token limit, capping the combined size of the prompt and context.
  
## Future Enhancements

- Contextual error diagnosis by capturing terminal logs.
- Persistent context storage for streamlined workflows.
- Improved terminal output formatting for better readability.
- Support for specifying individual files as context.

## Requirements

- Python 3.6+
- `google-generativeai` library  
  *(Install with `pip install google-generativeai`)*

## Setup

1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install google-generativeai
   ```
3. Replace the placeholder API key in the code with your own:
   ```python
   genai.configure(api_key="<YOUR_API_KEY>")
   ```
4. **Optional**: Create a standalone executable using `pyinstaller`:
   ```bash
   pyinstaller --onefile app.py
   ```
   Move the generated executable (found in the `dist` folder) to a directory included in your `PATH`, such as `/usr/local/bin` on Linux or `bin` on Windows. This allows you to call `gemini` from anywhere in your terminal:
   ```bash
   gemini Your prompt here
   ```

## Usage

Run the program with various options to customize your interaction with the Gemini API.

### Basic Command
```bash
python app.py when will i be happy?
```

### Options

- **`-p`, `--prompt`**: Specify the main prompt for the API.
  ```bash
  python app.py -p "Explain relativity."
  ```
  Or pass prompts directly as positional arguments:
  ```bash
  python app.py Explain relativity simply.
  ```

- **`-f`, `--files`**: Include content from files in the current directory up to a certain depth (default: 1).
  ```bash
  python app.py -p "Summarize these files." -f 2
  ```

- **`-fs`, `--filesystem`**: Include a list of the file system’s structure up to a specified depth (default: 3).
  ```bash
  python app.py -p "Describe this directory." -fs 4
  ```

- **`-t`, `--test`**: Preview the full prompt and context before sending it to the API.
  ```bash
  python app.py -p "What is AI?" -t
  ```

- **`-o`, `--output`**: Save the response to a `.md` file.
  ```bash
  python app.py -p "Document this." -o output.md
  ```

## Examples

### Basic Prompt
```bash
python app.py -p "What is the capital of Japan?"
```

### Add Context from Files and Directories
```bash
python app.py -p "Summarize these files." -fs 2 -f 1
```

### Test Mode
Preview the entire prompt and context:
```bash
python app.py -p "Analyze this directory." -fs 2 -f 1 -t
```

### Save the Output
Save the response to a markdown file:
```bash
python app.py -p "Write an essay on AI ethics." -o ai_ethics.md
```

## Notes

- **API Key**: Use your Gemini API key for functionality.
- **File Size Limit**: Files exceeding 3 MB are skipped to avoid token overflows. Smaller prompts and context are better for results.

## License

This project is open-source and free to use for any purpose.
