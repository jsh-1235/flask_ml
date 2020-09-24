#######################################################################
# CSS Update : Ctrl + Shift + R
#######################################################################
from flask import Flask, escape, url_for, render_template
from flask import request
from flask import make_response
from datetime import datetime

import tensorflow as tf

print("Tensorflow : {0}".format(tf.VERSION))

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

W = tf.Variable(tf.random_uniform([1], -1.0, 1.0), name="weight")
b = tf.Variable(tf.zeros([1]), name="bias")

saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    saver.restore(sess, './static/model/saved.cpkt')

    x = 0.2

    weight = sess.run(W)
    bias = sess.run(b)

    print('Weight : {0}'.format(weight))
    print('Bias : {0}'.format(bias))
    print('Y : {0}'.format(weight * x + bias))

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html', weight=weight[0], bias=bias[0])    


@app.route("/form", methods=['POST', 'GET'])
def form():
    inputs = []

    if request.method == "POST":
        xValue = request.form['inputXValue']
        yValue = weight[0] * float(xValue) + bias[0]

        inputs.clear()
        inputs.append(xValue)
        inputs.append(yValue)

        print("{0} {1}".format(xValue, yValue))
    else:
        print("Get Request")

    return render_template("form.html", title="Form", inputs=inputs)


if __name__ == '__main__':
    #app.run(debug=True)
    app.run()
