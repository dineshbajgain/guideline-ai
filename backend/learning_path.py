from gen_ai import generate_learning_resources

def create_learning_path(dependencies, dev_dependencies):
    learning_path = []

    # Generate learning resources using Gen AI
    for dependency in dependencies:
        learning_path.append({
            'dependency': dependency,
            'progress': 0  # Track progress for each dependency
        })

    for dev_dependency in dev_dependencies:
        learning_path.append({
            'dependency': dev_dependency,
            'progress': 0  # Track progress for each devDependency
        })

    return learning_path

def update_progress(learning_path):
    while True:
        print("\nCurrent Learning Path Progress:")
        for i, item in enumerate(learning_path):
            print(f"{i+1}. {item['dependency']} - Progress: {item['progress']}%")

        choice = input("\nEnter the number of the dependency to update progress, or 'q' to quit: ")

        if choice.lower() == 'q':
            break

        try:
            index = int(choice) - 1
            if 0 <= index < len(learning_path):
                new_progress = int(input(f"Enter new progress for {learning_path[index]['dependency']} (0-100): "))
                learning_path[index]['progress'] = max(0, min(100, new_progress))
            else:
                print("Invalid choice. Please select a valid dependency number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
