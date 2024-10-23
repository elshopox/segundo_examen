from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'

@app.route('/')
def index():
    productos = session.get('productos', [])
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['POST'])
def agregar_producto():
    if 'productos' not in session:
        session['productos'] = []

    nombre = request.form['nombre']
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])
    fecha_vencimiento = request.form['fecha_vencimiento']
    categoria = request.form['categoria']
    
    productos = session['productos']
    nuevo_id = len(productos) + 1

    nuevo_producto = {
        'id': nuevo_id,
        'nombre': nombre,
        'cantidad': cantidad,
        'precio': precio,
        'fecha_vencimiento': fecha_vencimiento,
        'categoria': categoria
    }

    productos.append(nuevo_producto)
    session['productos'] = productos
    flash('Producto agregado exitosamente.')
    return redirect(url_for('index'))

@app.route('/editar/<int:producto_id>', methods=['GET', 'POST'])
def editar_producto(producto_id):
    productos = session.get('productos', [])
    producto = next((p for p in productos if p['id'] == producto_id), None)

    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']

        flash('Producto actualizado exitosamente.')
        return redirect(url_for('index'))

    return render_template('editar.html', producto=producto)

@app.route('/eliminar/<int:producto_id>')
def eliminar_producto(producto_id):
    productos = session.get('productos', [])
    productos = [producto for producto in productos if producto['id'] != producto_id]
    session['productos'] = productos
    flash('Producto eliminado exitosamente.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)