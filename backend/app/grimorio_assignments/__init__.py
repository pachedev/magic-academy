
from flask import Blueprint

bp = Blueprint('grimorio_assignments', __name__)

from app.grimorio_assignments import routes
