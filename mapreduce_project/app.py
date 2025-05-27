from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

# Các file JSON có thể chọn
json_files = [
    "input/books_clean.json",
    "input/tiki_book_data_clean.json"
]

# Danh sách các chức năng MapReduce
jobs = {
    "avg_rating": {
        "mapper": "mapper/avg_rating_mapper.py",
        "reducer": "reducer/avg_rating_reducer.py",
        "input_type": "single"
    },
    "max_price": {
        "mapper": "mapper/max_price_mapper.py",
        "reducer": "reducer/max_price_reducer.py",
        "input_type": "single"
    },
    "min_price": {
        "mapper": "mapper/min_price_mapper.py",
        "reducer": "reducer/min_price_reducer.py",
        "input_type": "single"
    },
    "count_rating": {
        "mapper": "mapper/count_rating_mapper.py",
        "reducer": "reducer/count_rating_reducer.py",
        "input_type": "single"
    },
    "avg_price": {
        "mapper": "mapper/avg_price_mapper.py",
        "reducer": "reducer/avg_price_reducer.py",
        "input_type": "single"
    },
    "compare_avg_price": {
        "mapper": "mapper/compare_avg_price_mapper.py",
        "reducer": "reducer/compare_avg_price_reducer.py",
        "input_type": "multiple"
    }
}

def run_mapreduce(mapper, reducer, input_files, job_name=None):
    try:
        if job_name == "compare_avg_price":
            mapper_outputs = []
            tags = ["books", "tiki"]
            for i, file in enumerate(input_files):
                with open(file, "r", encoding="utf-8") as f:
                    file_content = f.read()

                mapper_proc = subprocess.Popen(
                    ["python3", mapper, tags[i]],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                mapper_output, mapper_err = mapper_proc.communicate(input=file_content)
                if mapper_proc.returncode != 0:
                    return f"Mapper error for {tags[i]}:\n{mapper_err}"
                mapper_outputs.append(mapper_output)

            combined_output = "\n".join(mapper_outputs)

            reducer_proc = subprocess.Popen(
                ["python3", reducer],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            reducer_output, reducer_err = reducer_proc.communicate(input=combined_output)
            if reducer_proc.returncode != 0:
                return f"Reducer error:\n{reducer_err}"
            return reducer_output

        # Xử lý các job dạng single
        if isinstance(input_files, list):
            combined_input = ""
            for file in input_files:
                with open(file, "r", encoding="utf-8") as f:
                    combined_input += f.read()
        else:
            with open(input_files, "r", encoding="utf-8") as f:
                combined_input = f.read()

        # Chạy mapper
        mapper_proc = subprocess.Popen(
            ["python3", mapper],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        mapper_output, mapper_err = mapper_proc.communicate(input=combined_input)
        if mapper_proc.returncode != 0:
            return f"Mapper error:\n{mapper_err}"

        # Với job như count_rating, cần sort output
        if job_name == "count_rating":
            mapper_output = '\n'.join(sorted(mapper_output.strip().splitlines()))

        # Chạy reducer
        reducer_proc = subprocess.Popen(
            ["python3", reducer],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        reducer_output, reducer_err = reducer_proc.communicate(input=mapper_output)
        if reducer_proc.returncode != 0:
            return f"Reducer error:\n{reducer_err}"

        return reducer_output

    except Exception as e:
        return f"Exception occurred:\n{str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    selected_job = None
    selected_file = None
    disable_file_select = False

    if request.method == "POST":
        selected_job = request.form.get("job")
        selected_file = request.form.get("input_file")

        if selected_job in jobs:
            job = jobs[selected_job]
            if job["input_type"] == "single":
                if selected_file not in json_files:
                    result = "Vui lòng chọn file hợp lệ."
                else:
                    result = run_mapreduce(job["mapper"], job["reducer"], selected_file, job_name=selected_job)
            else:
                # Nếu multiple thì tự động chọn cả 2 file
                result = run_mapreduce(job["mapper"], job["reducer"], json_files, job_name=selected_job)

            disable_file_select = (job["input_type"] == "multiple")
        else:
            result = "Chức năng không hợp lệ."

    return render_template(
        "index.html",
        jobs=jobs.keys(),
        files=json_files,
        result=result,
        selected_job=selected_job,
        selected_file=selected_file,
        disable_file_select=disable_file_select
    )

if __name__ == "__main__":
    app.run(debug=True)
