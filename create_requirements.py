import subprocess

def create_requirements():
    # Use pip freeze to get the list of packages
    result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)

    if result.returncode == 0:
        with open('requirements.txt', 'w') as f:
            f.write(result.stdout)

    else:
        print("Error:", result.stderr)

create_requirements()