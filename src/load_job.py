def load_job_description():
    file_path = "data/job_description.txt"
    print("Reading:", file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()