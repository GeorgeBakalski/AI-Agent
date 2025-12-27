import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        list_of_items = os.listdir(target_dir)
        list_of_records = []
        for item in list_of_items:
            path_to_item = os.path.normpath(os.path.join(target_dir, item))

            list_of_records.append(
                f"- {item}: file_size={os.path.getsize(path_to_item)} bytes, is_dir={os.path.isdir(path_to_item)}"
            )

        return "\n".join(list_of_records)
    
    except Exception as e:
        return f"Error: {e}"
