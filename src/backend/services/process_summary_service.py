import os
from services.bedrock_service import process_obj

def process_individual_summary(input_folder, output_folder):
    # List all subfolders in Formatted-Texts
    subfolders = [subfolder for subfolder in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, subfolder))]

    for subfolder in subfolders:
        input_subfolder_path = os.path.join(input_folder, subfolder)
        output_subfolder_path = os.path.join(output_folder, subfolder)

        # Create the subfolder in Summarized-Texts
        if not os.path.exists(output_subfolder_path):
            os.makedirs(output_subfolder_path)

        # Process .txt files inside the subfolder
        for filename in os.listdir(input_subfolder_path):
            if filename.endswith(".txt"):
                input_file_path = os.path.join(input_subfolder_path, filename)
                output_file_path = os.path.join(output_subfolder_path, filename)

                # Read the content of the text file
                with open(input_file_path, "r", encoding="utf-8") as file:
                    text_content = file.read()

                # Call the Bedrock service to generate the summary
                try:
                    summary = process_obj(text_content, type_summary="individual")
                    
                    # Save the summary to the output file
                    with open(output_file_path, "w", encoding="utf-8") as output_file:
                        output_file.write(summary)

                    print(f"\nSummary generated for {filename} and saved in {output_file_path}")
                except Exception as e:
                    print(f"\nError generating summary for {filename}: {e}")

def process_final_summary(input_folder, output_file):
    # List all subfolders in Summarized-Texts
    subfolders = [subfolder for subfolder in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, subfolder))]
    
    # Text content variable to store the content of all summarized files
    text_content = ""  
    
    for subfolder in subfolders:
        input_subfolder_path = os.path.join(input_folder, subfolder)
    
        for filename in os.listdir(input_subfolder_path):
            if filename.endswith(".txt"):
                input_file_path = os.path.join(input_subfolder_path, filename)
                
                # Read the content of the summarized text file
                with open(input_file_path, "r", encoding="utf-8") as file:
                    
                    # Concatenate the content of all summarized files
                    text_content += file.read() + "\n\n"
                    
    # Call the Bedrock service to generate the final summary
    try:
        summary = process_obj(text_content, type_summary="final")
                    
        output_file_path = os.path.join(output_file)    
        
        # Save the final summary to the output file
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(summary)
        
        print(f"Final summary generated and saved in {output_file_path}\n")
    except Exception as e:
        print(f"\nError generating final summary: {e}\n")
