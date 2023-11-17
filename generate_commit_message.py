import openai
import sys
import os


def generate_commit_message(diff):
    # Generate the prompt for GPT-4
    prompt = f"Write a descriptive and concise commit message based on the following diffs:\n\n{diff}\n\nCommit message:"

    # Call the OpenAI API
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if openai.api_key is None:
        print("Please set your OPENAI_API_KEY environment variable")
        sys.exit(1)

    messages = [
        {
            "role": "system",
            "content": "You are committing your code changes to your GitHub repo.",
        },
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

    reply = response["choices"][0]["message"]["content"].strip()
    return reply


if __name__ == "__main__":
    diff = sys.argv[1]
    commit_message = generate_commit_message(diff)
    print(commit_message)
