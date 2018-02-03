from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    #mock user for now
    user = {'username': 'Nick'}
    return render_template('index.html', title='Home', user=user)

"""
if __name__ == '__main__':
    app.run()
"""