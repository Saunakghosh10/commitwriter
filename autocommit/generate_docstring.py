import openai
import sys
import os


def generate_docstring(file_path):
    # Load the content of the file
    with open(file_path, "r") as file:
        file_content = file.read()

    # Truncate the content if it's too long
    truncated_content = (
        (file_content[:2000] + "...") if len(file_content) > 2000 else file_content
    )

    # Generate the prompt for GPT-4
    prompt = f'Generate a docstring for the following code:\n\n{truncated_content}\nReturn only the docstring.\n\n"""'

    messages = [
        {"role": "system", "content": "You are an expert software engineer."},
        {"role": "user", "content": prompt},
    ]

    # Call the OpenAI API
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if openai.api_key is None:
        print("Please set your OPENAI_API_KEY environment variable")
        sys.exit(1)

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
    )

    reply = response["choices"][0]["message"]["content"]

    # Get everything before the first """ if there is one
    docstring = reply.split('"""')[0]
    return docstring


if __name__ == "__main__":
    filename = sys.argv[1]
    docstring = generate_docstring(filename)
    print(docstring)
