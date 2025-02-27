
from app import app
from flask import render_template, request, flash, redirect, url_for, session

# Importando mi conexión a BD
from conexion.conexionBD import connectionBD

# Para encriptar contraseña generate_password_hash
from werkzeug.security import check_password_hash

# Importando controllers para el modulo de login
from controllers.funciones_login import *
from controllers.funciones_home import *
PATH_URL_LOGIN = "/public/login"


@app.route('/', methods=['GET'])
def inicio():
    if 'conectado' in session:
        return render_template('public/base_cpanel.html', dataLogin=dataLoginSesion())
    else:
        return render_template(f'{PATH_URL_LOGIN}/base_login.html')


@app.route('/mi-perfil/<string:id>', methods=['GET'])
def perfil(id):
    if 'conectado' in session:
        
        return render_template(f'public/perfil/perfil.html', info_perfil_session=info_perfil_session(id), dataLogin=dataLoginSesion(), generos=lista_generoBD(), estado_civil=lista_Estado_CivilBD(), areas=lista_areasBD(), roles=lista_rolesBD())
    else:
        return redirect(url_for('inicio'))


# Crear cuenta de usuario
@app.route('/register-user', methods=['GET'])
def cpanelRegisterUser():
        return render_template(f'{PATH_URL_LOGIN}/auth_register.html',dataLogin = dataLoginSesion(), generos=lista_generoBD(), estado_civil=lista_Estado_CivilBD(), areas=lista_areasBD(), roles=lista_rolesBD(),accesos_rfid=lista_Codigo_RFIDBD())

from flask import redirect, url_for

@app.route('/color-perzonalizar', methods=['GET', 'POST'])
def color_casaBD():
    # Si es una solicitud POST, obtener el color seleccionado y actualizar la base de datos
    if request.method == 'POST':
        color_seleccionado = request.form.get('selectColorCasa')
        nroHogar = request.form.get('selectNumeroHogar')  # Usar el valor del formulario
        
        if color_seleccionado and nroHogar:
            # Llamar a la función para actualizar el color en la base de datos
            actualizar_color_hogar(nroHogar, color_seleccionado)
            
            # Redirigir a la misma página para que se refleje el cambio
            return redirect(url_for('color_casaBD', numero_hogar=nroHogar))

    # Si es una solicitud GET, obtener el número de hogar de la URL (si existe)
    nroHogar = request.args.get('numero_hogar')  # Obtener el número de hogar desde la URL
    if not nroHogar:
        # Si no existe nroHogar, devolver un error o una página de ayuda
        return "Número de hogar no proporcionado", 400

    # Obtener los colores disponibles
    colores_disponibles = lista_colores_hogarBD()

    return render_template(
        f'{PATH_URL_LOGIN}/color_perzonalizar.html',
        dataLogin=dataLoginSesion(),
        coloresDisponibles=colores_disponibles,
        nroHogar=nroHogar  # Pasar el número de hogar a la plantilla
    )



# Recuperar cuenta de usuario
@app.route('/recovery-password', methods=['GET'])
def cpanelRecoveryPassUser():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        return render_template(f'{PATH_URL_LOGIN}/auth_forgot_password.html')


# Crear cuenta de usuario
@app.route('/saved-register', methods=['POST'])
def cpanelRegisterUserBD():
    if request.method == 'POST' and 'cedula' in request.form and 'pass_user' in request.form:
        cedula = request.form['cedula']
        name = request.form['name']
        surname = request.form['surname']
        id_genero = request.form['selectGenero']
        id_estado_civil = request.form['selectEstadoCivil']
        id_area = request.form['selectArea']
        id_rol = request.form['selectRol']
        codigo_rfid = request.form['selectCodigoRFID']  # Cambiado a 'selectCodigoRFID'
        pass_user = request.form['pass_user']

        resultData = recibeInsertRegisterUser(
            cedula, name, surname, id_genero, id_estado_civil, id_area, id_rol, pass_user, codigo_rfid)  # Agregado codigo_rfid
        if resultData != 0:
            flash('La cuenta fue creada correctamente.', 'success')
            return redirect(url_for('usuarios'))
        else:
            flash('Error al crear la cuenta.', 'error')  # Mensaje de error
            return redirect(url_for('usuarios'))
    else:
        flash('El método HTTP es incorrecto', 'error')
        return redirect(url_for('inicio'))


# Actualizar datos de mi perfil
@app.route("/actualizar-datos-perfil/<int:id>", methods=['POST'])
def actualizarPerfil(id):
    if request.method == 'POST':
        if 'conectado' in session:
            respuesta = procesar_update_perfil(request.form,id)
            if respuesta == 1:
                flash('Los datos fuerón actualizados correctamente.', 'success')
                return redirect(url_for('usuarios'))
            elif respuesta == 0:
                flash(
                    'La contraseña actual esta incorrecta, por favor verifique.', 'error')
                return redirect(url_for('perfil',id=id))
            elif respuesta == 2:
                flash('Ambas claves deben se igual, por favor verifique.', 'error')
                return redirect(url_for('perfil',id=id))
            elif respuesta == 3:
                flash('La Clave actual es obligatoria.', 'error')
                return redirect(url_for('perfil',id=id))
            else: 
                flash('Clave actual incorrecta', 'error')
                return redirect(url_for('perfil',id=id))
        else:
            flash('primero debes iniciar sesión.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Validar sesión
@app.route('/login', methods=['GET', 'POST'])
def loginCliente():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        if request.method == 'POST' and 'cedula' in request.form and 'pass_user' in request.form:

            cedula = str(request.form['cedula'])
            pass_user = str(request.form['pass_user'])
            conexion_MySQLdb = connectionBD()
            print(conexion_MySQLdb)
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM usuarios WHERE cedula = %s", [cedula])
            account = cursor.fetchone()

            if account:
                if check_password_hash(account['password'], pass_user):
                    # Crear datos de sesión, para poder acceder a estos datos en otras rutas
                    session['conectado'] = True
                    session['id'] = account['id_usuario']
                    session['name'] = account['nombre_usuario']
                    session['cedula'] = account['cedula']
                    session['rol'] = account['id_rol']

                    flash('la sesión fue correcta.', 'success')
                    return redirect(url_for('inicio'))
                else:
                    # La cuenta no existe o el nombre de usuario/contraseña es incorrecto
                    flash('datos incorrectos por favor revise.', 'error')
                    return render_template(f'{PATH_URL_LOGIN}/base_login.html')
            else:
                flash('el usuario no existe, por favor verifique.', 'error')
                return render_template(f'{PATH_URL_LOGIN}/base_login.html')
        else:
            flash('primero debes iniciar sesión.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')


@app.route('/closed-session',  methods=['GET'])
def cerraSesion():
    if request.method == 'GET':
        if 'conectado' in session:
            # Eliminar datos de sesión, esto cerrará la sesión del usuario
            session.pop('conectado', None)
            session.pop('id', None)
            session.pop('name_surname', None)
            session.pop('email', None)
            flash('tu sesión fue cerrada correctamente.', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('recuerde debe iniciar sesión.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')



