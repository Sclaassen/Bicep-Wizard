import os

def find_service_directories(local_directory, service_name):
    matching_directories = []
    service_keywords = service_name.lower().split()
    for root, dirs, files in os.walk(local_directory):
        for dir_name in dirs:
            dir_name_lower = dir_name.lower()
            if all(keyword in dir_name_lower for keyword in service_keywords):
                matching_directories.append(os.path.join(root, dir_name))
    return matching_directories

def get_main_bicep_directories(selected_directory):
    main_bicep_directories = []
    for root, dirs, files in os.walk(selected_directory):
        if 'main.bicep' in files:
            main_bicep_directories.append(root)
    return main_bicep_directories

def user_select_service(matching_directories):
    print("Select a service directory from the list below:")
    for idx, directory in enumerate(matching_directories, start=1):
        service_name = os.path.basename(directory)
        print(f"{idx}. {service_name}")

    while True:
        try:
            choice = int(input("Enter the number of the service directory: ")) - 1
            if 0 <= choice < len(matching_directories):
                return matching_directories[choice]
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def user_select_directory(main_bicep_directories):
    print("Please choose a service from the list below:")
    for idx, directory in enumerate(main_bicep_directories, start=1):
        directory_name = os.path.basename(directory)
        print(f"{idx}. {directory_name}")

    while True:
        try:
            choice = int(input("Enter the number of the directory: ")) - 1
            if 0 <= choice < len(main_bicep_directories):
                return main_bicep_directories[choice]
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
