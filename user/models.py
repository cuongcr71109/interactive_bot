from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256 as sha256
from db import *
import uuid

class Customer:
    