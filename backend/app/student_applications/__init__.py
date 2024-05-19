
from flask import Blueprint

bp = Blueprint('student_applications', __name__)

from app.student_applications import routes
