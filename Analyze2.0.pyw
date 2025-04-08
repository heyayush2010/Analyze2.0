import zipfile
import os
import tkinter as tk
import http.client
import base64
from urllib.parse import urlparse

# Function to decompile a ZIP file
def decompile_zip(zip_path):
    try:
        # Open the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # List all the files in the zip
            zip_contents = zip_ref.namelist()
            result = f"Files in the ZIP archive '{zip_path}':\n"
            for file_name in zip_contents:
                result += f"\nDecompiling {file_name}:\n"
                with zip_ref.open(file_name) as file:
                    file_content = file.read()
                    result += file_content.decode() + "\n"
                    result += "=" * 40 + "\n"  # Print separator for readability
            return result
    except FileNotFoundError:
        return f"Error: The file at '{zip_path}' was not found."
    except zipfile.BadZipFile:
        return f"Error: '{zip_path}' is not a valid ZIP file."
    except Exception as e:
        return f"An error occurred: {e}"

# Function to decompile other code/executable files
def decompile_other_file(file_path):
    try:
        # Get the file extension
        file_name, file_extension = os.path.splitext(file_path)

        # Handle the file based on its extension
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return f"Decompiled content of {file_path}:\n\n{content}\n" + "=" * 40
        return f"Error: '{file_extension}' files cannot be decompiled with this tool."
    except FileNotFoundError:
        return f"Error: The file at '{file_path}' was not found."
    except Exception as e:
        return f"An error occurred: {e}"

# Function to handle the user input for "Decompile URL"
def decompile_url_action():
    url = url_entry.get().strip()  # Get the user input for URL
    if url:
        content = decompile_url(url)
        text_box.delete(1.0, tk.END)  # Clear previous content
        text_box.insert(tk.END, content)

# Function to fetch content from a URL using http.client and encrypt the connection using Base64
def decompile_url(url):
    try:
        # Base64 encode the URL
        encoded_url = base64.b64encode(url.encode()).decode()

        # Parse the URL to extract components like domain and path
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path if parsed_url.path else "/"

        # Create an HTTPS connection (use 'http.client' for basic functionality)
        conn = http.client.HTTPSConnection(host)

        # Send the GET request
        conn.request("GET", path)

        # Get the response
        response = conn.getresponse()

        # Check if the response was successful
        if response.status == 200:
            content = response.read().decode()
            return f"Decompiled content from URL '{url}' (Base64 encoded URL: {encoded_url}):\n\n{content}\n" + "=" * 40
        else:
            return f"Error: Failed to retrieve content from '{url}', Status Code: {response.status}"
    except http.client.HTTPException as e:
        return f"An error occurred while fetching the URL content: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

# Function to handle the user input for "Decompile ZIP"
def decompile_zip_action():
    zip_path = zip_entry.get().strip()  # Get the user input for ZIP file path
    if zip_path:
        content = decompile_zip(zip_path)
        text_box.delete(1.0, tk.END)  # Clear previous content
        text_box.insert(tk.END, content)

# Function to handle the user input for "Decompile Code/Executable"
def decompile_code_action():
    file_path = code_entry.get().strip()  # Get the user input for code/executable file path
    if file_path:
        content = decompile_other_file(file_path)
        text_box.delete(1.0, tk.END)  # Clear previous content
        text_box.insert(tk.END, content)

# Create the main tkinter window
root = tk.Tk()
root.title("Analyze")
root.geometry("600x500")
root.config(bg="white")

# Add a label and entry for the ZIP file path
zip_label = tk.Label(root, text="Enter the full path to the ZIP file:", font=("Arial", 12))
zip_label.pack(pady=5)
zip_entry = tk.Entry(root, width=70, font=("Arial", 12))
zip_entry.pack(pady=5)
zip_entry.insert(tk.END, "e.g., C:/path/to/your.zip")  # Placeholder for guidance

# Add a button for "Decompile ZIP"
decompile_zip_button = tk.Button(root, text="Decompile ZIP", command=decompile_zip_action, font=("Arial", 14), bg="grey", fg="white")
decompile_zip_button.pack(pady=10)

# Add a label and entry for the code/executable file path
code_label = tk.Label(root, text="Enter the full path to the code/executable file:", font=("Arial", 12))
code_label.pack(pady=5)
code_entry = tk.Entry(root, width=70, font=("Arial", 12))
code_entry.pack(pady=5)
code_entry.insert(tk.END, "e.g., C:/path/to/your_script.py")  # Placeholder for guidance

# Add a button for "Decompile Code/Executable"
decompile_code_button = tk.Button(root, text="Decompile Code/Executable", command=decompile_code_action, font=("Arial", 14), bg="grey", fg="white")
decompile_code_button.pack(pady=10)

# Add a label and entry for the URL to decompile
url_label = tk.Label(root, text="Enter the URL to decompile:", font=("Arial", 12))
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=70, font=("Arial", 12))
url_entry.pack(pady=5)
url_entry.insert(tk.END, "e.g., https://example.com")  # Placeholder for guidance

# Add a button for "Decompile URL"
decompile_url_button = tk.Button(root, text="Decompile URL", command=decompile_url_action, font=("Arial", 14), bg="grey", fg="white")
decompile_url_button.pack(pady=10)

# Add a text box for showing the decompiled content
text_box = tk.Text(root, wrap=tk.WORD, width=70, height=15, bg="lightgrey", font=("Arial", 12))
text_box.pack(padx=10, pady=10)

# Start the GUI loop
root.mainloop()