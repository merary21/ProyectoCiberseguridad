# ============================================================
# auth.py - REGISTRO E INICIO DE SESIÓN (POR EMPRESA)
# ============================================================

import re

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from datetime import datetime

from models import Empresa, Usuario, db

auth_bp = Blueprint("auth", __name__)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

SECTORES = [
    "Tecnología",
    "Finanzas",
    "Salud",
    "Retail / Comercio",
    "Manufactura",
    "Gobierno",
    "Educación",
    "Telecomunicaciones",
    "Otro",
]


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))

    if request.method == "GET":
        return render_template("registro.html", sectores=SECTORES)

    nombre_empresa = request.form.get("nombre_empresa", "").strip()
    nit = request.form.get("nit", "").strip()
    sector = request.form.get("sector", "").strip()
    nombre_completo = request.form.get("nombre_completo", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirmar_password = request.form.get("confirmar_password", "")

    datos_formulario = {
        "nombre_empresa": nombre_empresa,
        "nit": nit,
        "sector": sector,
        "nombre_completo": nombre_completo,
        "email": email,
    }

    errores = []

    if not nombre_empresa or len(nombre_empresa) < 2:
        errores.append("Ingresa el nombre de la empresa.")

    if not nit or len(nit) < 5:
        errores.append("Ingresa un NIT/RUC válido.")

    if sector not in SECTORES:
        errores.append("Selecciona un sector válido.")

    if not nombre_completo or len(nombre_completo) < 2:
        errores.append("Ingresa tu nombre completo.")

    if not EMAIL_RE.match(email):
        errores.append("Ingresa un correo electrónico corporativo válido.")

    if len(password) < 8:
        errores.append("La contraseña debe tener al menos 8 caracteres.")

    if password != confirmar_password:
        errores.append("Las contraseñas no coinciden.")

    if not errores and Empresa.query.filter_by(nit=nit).first():
        errores.append("Ya existe una empresa registrada con ese NIT/RUC.")

    if not errores and Usuario.query.filter_by(email=email).first():
        errores.append("Ya existe un usuario registrado con ese correo.")

    if errores:
        for error in errores:
            flash(error, "error")
        return render_template(
            "registro.html", sectores=SECTORES, datos=datos_formulario
        )

    empresa = Empresa(nombre=nombre_empresa, nit=nit, sector=sector)
    db.session.add(empresa)
    db.session.flush()

    usuario = Usuario(
        empresa_id=empresa.id,
        nombre_completo=nombre_completo,
        email=email,
        rol="admin",
    )
    usuario.set_password(password)
    db.session.add(usuario)
    db.session.commit()

    login_user(usuario)
    flash(f"Bienvenido a SOC-AI, {nombre_completo}.", "success")
    return redirect(url_for("inicio"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not usuario.check_password(password):
        flash("Correo o contraseña incorrectos.", "error")
        return render_template("login.html", email=email)

    usuario.ultimo_acceso = datetime.utcnow()
    db.session.commit()

    login_user(usuario)
    flash(f"Bienvenido de nuevo, {usuario.nombre_completo}.", "success")
    return redirect(url_for("inicio"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("auth.login"))
