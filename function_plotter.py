from flask import Flask, request, render_template_string
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
import base64

app = Flask(__name__)

HTML_TEMPLATE = '''
<!doctype html>
<html>
<head>
    <title>Function Plotter</title>
</head>
<body>
    <h2>Function Plotter</h2>
    <form method="POST">
        <label for="func">Enter a function of x and y:</label><br>
        <input type="text" id="func" name="func" value="x**2 + y**2"><br><br>
        <input type="submit" value="Plot">
    </form>
    {% if image %}
        <h3>Plot:</h3>
        <img src="data:image/png;base64,{{ image }}" alt="Function plot">
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def plot_function():
    image = None
    if request.method == 'POST':
        func = request.form.get('func', 'x**2 + y**2')
        x = np.linspace(-5, 5, 400)
        y = np.linspace(-5, 5, 400)
        x, y = np.meshgrid(x, y)
        z = eval(func)

        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ax.plot_surface(x, y, z, cmap='viridis')

        img_bytes = BytesIO()
        plt.savefig(img_bytes, format='png')
        plt.close(fig)
        img_bytes.seek(0)
        image = base64.b64encode(img_bytes.read()).decode('utf-8')

    return render_template_string(HTML_TEMPLATE, image=image)

if __name__ == '__main__':
    app.run(debug=True)
