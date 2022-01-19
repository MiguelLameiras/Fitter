from ctypes import sizeof
import re
from flask import Flask, redirect, flash,url_for, render_template,request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import os
import base64
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from scipy.interpolate import CubicSpline
import numpy as np
from scipy.optimize import curve_fit
from lmfit.models import ExpressionModel
from lmfit import Parameters,model
from plotter import *