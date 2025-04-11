from flask import Flask, render_template, request, url_for, send_from_directory

app = Flask(__name__)
filename = "data.txt"

def get_tasks():
    tasks = {}
    file = open(filename, "r")
    lines = file.readlines()
    for i in lines:
        tasks[i.split(",")[0]] = i[:-1].split(",")[1:]
    file.close()
    return tasks

def search():
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    return lines

def edit(line):
    file = open(filename, "w")
    file.write(line)
    file.close()

def update(update):
    file = open(filename, "a")
    file.write(update)
    file.close()

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print(request.form.keys())
        if "taskname" in request.form.keys(): 
            taskname = request.form["taskname"]
            tasktype = request.form['tasktype']
            update(taskname + "," + tasktype + ',0' +"\n")
        elif "taskform" in request.form.keys():
            lines = search()
            print(request.form.items())
            num = int(list(request.form.keys())[1])
            if lines[num][-2] == "0":
                lines[num] = lines[num][:-2]+"1\n"
            else:
                lines[num] = lines[num][:-2]+"0\n"
            print(list(request.form.keys()))
            file = "".join(lines)
            edit(file)
        elif "delete" in request.form.keys():
            id = list(request.form.keys())[1]
            lines = search()
            lines.remove(lines[int(id)])
            result = ""
            for i in lines:
                result += i
            edit(result)

    tasks = get_tasks()
    return render_template("index.html", tasknames=list(tasks.keys()), tasks=tasks, length=len(tasks.keys()), count = 0)

@app.route('/addtask/', methods=["GET", "POST"])
def addtask():
    if request.method == "POST":
        return render_template("addtask.html")


if __name__ == "__main__":
    app.run(debug=True)