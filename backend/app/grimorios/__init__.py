
from flask import Blueprint

bp = Blueprint('grimorios', __name__)

from app.grimorios import routes
