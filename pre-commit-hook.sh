#!/bin/bash

# Function to add documentation using the Python script
add_documentation() {
    local file=$1
    # Call the Python script and capture the output
    docstring=$(python generate_docstring.py "$file")
    exit_status=$?

    # Check if the Python script executed successfully
    if [ $exit_status -ne 0 ]; then
        echo "Error generating docstring for $file. Exiting..."
        exit 1
    fi

    # Prepend documentation to the file if docstring is generated
    if [ ! -z "$docstring" ]; then
        # Enclose the docstring in triple quotes for Python files
        echo -e "\"\"\"\n$docstring\n\"\"\"\n$(cat $file)" > $file
        # Add file again to staging area after modification
        git add "$file"
    fi
}

# Iterate over each staged file
for file in $(git diff --cached --name-only); do
    # Check if file has more than 10 lines and it is a Python file
    if [[ $(wc -l < "$file") -gt 10 && "$file" == *.py ]]; then
        add_documentation "$file"
    fi
done

# Generate diffs for staged files
diffs=$(git diff --cached)

# Call the Python script to generate a commit message
commit_message=$(python generate_commit_message.py "$diffs")
exit_status=$?

# Check if the Python script executed successfully
if [ $exit_status -ne 0 ]; then
    echo "Error generating commit message. Exiting..."
    exit 1
fi

# If a commit message was generated, use it for the commit
if [ ! -z "$commit_message" ]; then
    git commit -m "$commit_message"
else
    echo "No commit message was generated. Exiting..."
    exit 1
fi