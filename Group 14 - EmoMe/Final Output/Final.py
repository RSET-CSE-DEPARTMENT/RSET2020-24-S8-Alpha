import multiprocessing
import subprocess

def run_python_file(file_path):
    try:
        subprocess.run(['python', file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {file_path}: {e}")

if __name__ == "__main__":
    python_files = [
        "D:\\Final Project\\Text\\Final Output\\run.py",
	"D:\\Final Project\\Text\\Final Output\\emotion_number.py",
	"D:\\Final Project\\Text\\Final Output\\uno.py"
    ]
    
    processes = []
    for file_path in python_files:
        process = multiprocessing.Process(target=run_python_file, args=(file_path,))
        process.start()
        processes.append(process)
    
    for process in processes:
        process.join()
