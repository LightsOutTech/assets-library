import os
import re
import csv

def update_image_urls():
    # 1. Define paths
    # We use the absolute path to make sure the script runs correctly from anywhere.
    base_dir = "/home/lot-dashu/linux-local-lot/assets-library/images"
    csv_path = os.path.join(base_dir, "加图片.csv")
    
    # 2. Scan the images folder
    # We list all files in the directory to find image files.
    all_files = os.listdir(base_dir)
    
    # 3. Create a mapping of model (e.g. "U6") to its image URLs
    # Structure of model_mapping:
    # {
    #     'U6': {
    #         'Main': 'url_to_main',
    #         'Pic1': 'url_to_pic1',
    #         ...
    #     }
    # }
    model_mapping = {}
    
    # We use a regular expression to match model numbers.
    # r"^(U\d+)" means: Match "U" at the beginning of the string, followed by one or more digits (\d+).
    model_pattern = re.compile(r"^(U\d+)")
    
    for filename in all_files:
        # We only process image files with common extensions
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            match = model_pattern.match(filename)
            if match:
                model = match.group(1) # e.g. "U6"
                
                # Initialize the dictionary for this model if not already present
                if model not in model_mapping:
                    model_mapping[model] = {}
                
                # Construct the public Raw GitHub URL
                # In Git repositories hosted on GitHub, we can access raw files directly using this pattern.
                public_url = f"https://raw.githubusercontent.com/LightsOutTech/assets-library/main/images/{filename}"
                
                filename_lower = filename.lower()
                
                # Match files to columns according to user's criteria:
                if "main" in filename_lower:
                    model_mapping[model]["Main"] = public_url
                elif "pic1" in filename_lower:
                    model_mapping[model]["Pic1"] = public_url
                elif "pic2" in filename_lower:
                    model_mapping[model]["Pic2"] = public_url
                elif "size" in filename_lower:
                    model_mapping[model]["Size"] = public_url
                elif "pic3" in filename_lower:
                    model_mapping[model]["Pic3"] = public_url
                elif "pic4" in filename_lower:
                    model_mapping[model]["Pic4"] = public_url
                    
    # 4. Read the original CSV and update rows
    updated_rows = []
    headers = []
    
    # We use 'utf-8-sig' to automatically handle Byte Order Mark (BOM) in UTF-8 CSVs,
    # which is very common in files created or modified by Microsoft Excel.
    with open(csv_path, mode='r', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)
        headers = reader.fieldnames
        for row in reader:
            sku = row["SKU"]
            # The SKU structure is like 'CUPC-U6-LXL'.
            # We split by '-' to extract the second part, which is the model name.
            sku_parts = sku.split('-')
            if len(sku_parts) >= 2:
                model = sku_parts[1] # e.g., "U6"
                
                # If we have image mappings for this model, populate the corresponding columns
                if model in model_mapping:
                    row["Main Image URL"] = model_mapping[model].get("Main", "")
                    row["Other Image URL1"] = model_mapping[model].get("Pic1", "")
                    row["Other Image URL2"] = model_mapping[model].get("Pic2", "")
                    row["Other Image URL3"] = model_mapping[model].get("Size", "")
                    row["Other Image URL4"] = model_mapping[model].get("Pic3", "")
                    row["Other Image URL5"] = model_mapping[model].get("Pic4", "")
            
            updated_rows.append(row)
            
    # 5. Write the updated rows back to the CSV file
    # We write with utf-8-sig to preserve the BOM format if needed, or we can use utf-8.
    # Excel typically prefers utf-8-sig so it opens characters correctly.
    with open(csv_path, mode='w', encoding='utf-8-sig', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(updated_rows)
        
    print(f"Successfully processed {len(updated_rows)} rows and updated CSV!")

if __name__ == "__main__":
    update_image_urls()
