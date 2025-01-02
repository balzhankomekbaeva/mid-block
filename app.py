from flask import Flask, render_template, request, redirect, url_for
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    tasks = blockchain.get_all_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        task_title = request.form['task_title']
        task_description = request.form['task_description']
        task_assignee = request.form['task_assignee']
        task_status = request.form['task_status']
        blockchain.add_task(task_title, task_description, task_assignee, task_status)
        return redirect(url_for('index'))
    return render_template('create_task.html')

@app.route('/update_task/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    task = blockchain.get_task(task_id)
    if request.method == 'POST':
        task_data = {
            'task_title': request.form['task_title'],
            'task_description': request.form['task_description'],
            'task_assignee': request.form['task_assignee'],
            'task_status': request.form['task_status']
        }
        blockchain.update_task(task_id, task_data)
        return redirect(url_for('index'))
    return render_template('update_task.html', task=task, task_id=task_id)

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    blockchain.delete_task(task_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
