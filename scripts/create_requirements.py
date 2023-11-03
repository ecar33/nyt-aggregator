from subprocess import CalledProcessError
import subprocess
def write_requirements():
    try:
        result = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
        return result.stdout

    except CalledProcessError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    result = write_requirements()
    with open("../requirements.txt", "w") as f:
        f.write(result)





