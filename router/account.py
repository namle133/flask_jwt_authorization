from flask import jsonify, request, make_response, Blueprint
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity, unset_jwt_cookies

from service.user_service import *
from database.connection import *
from redis_db.token import *
from jwt_token.time import *
from util.salt_hash import *
from util.random import *
from smtp.send_email import *
from database import connection

bp = Blueprint('router', __name__)

# initial dabase postgres and redis
InitDB()
conn, rd = connection.Pg, connection.Rd

@bp.route('/create_user', methods=['POST'])
def create_user():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    email    = request.json.get('email', None)
    if username == "" or password == "" or email == "":
        return jsonify({"message": "Please fill out all of the informations"}), 400 
    
    hashed_pwd = hash_password(password)
    add_user_info(conn, username, email, hashed_pwd)
    return jsonify({"message": "Create user successfully"}), 200

@bp.route('/delete_account', methods=['DELETE'])
@jwt_required()
def delete_account():
    #* method 1:
    #* username = request.json.get('username', None)
    
    # * method 2:
    current_user = get_jwt_identity()
    delete_account_user(conn, str(current_user))
    
    # delete_token from redis db
    key_access = "acceess_token_" + str(current_user)
    key_refresh = "refresh_token_" + str(current_user)
    delete_token(rd, key_to_delete=key_access)
    delete_token(rd, key_to_delete=key_refresh)

    return jsonify({"message": "Delete user successfully"}), 200

@bp.route('/login', methods=['POST'])
def login():  
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username == "" or password == "":
        return jsonify({"message": "Please fill out username and password"}), 400
    
    if check_user_password(conn, username, password) == False :
        return jsonify({"message": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=username)
    ttl_access = calculate_time_to_live(access_token)
    add_token(rd, "acceess_token_" + username, access_token, ttl_access)
    
    refresh_token = create_refresh_token(identity=username)
    ttl_refresh = calculate_time_to_live(refresh_token)
    add_token(rd, "refresh_token_" + username, refresh_token, ttl_refresh)

    return jsonify(access_token=access_token, refresh_token=refresh_token)

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token)

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    # Revoke the current access token
    token_str = str(request.headers['Authorization'].replace('Bearer ', ''))
    ttl = calculate_time_to_live(token_str)
    add_revoked_token(rd, token_str, ttl)
    # Create a response with unset JWT cookies
    response = make_response(jsonify({"message": "Logged out {0} successfully".format(current_user)}))
    unset_jwt_cookies(response)
    return response

@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    token_str = str(request.headers['Authorization'].replace('Bearer ', ''))
    
    # Check if the token has been revoked
    if check_revoked_token(rd, token_str):
        return jsonify({"message": "Token has been revoked"}), 401
    return jsonify(logged_in_as=current_user)

@bp.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
    current_user = get_jwt_identity()
    current_password = request.json.get('current_password', None)
    new_password = request.json.get('new_password', None)
    confirm_password = request.json.get('confirm_password', None)
    
    if current_password == "" or new_password == "" or confirm_password == "":
        return jsonify({"message": "Please fill out all of the informations"}), 400 
    if check_user_password(conn, str(current_user), current_password) == False :
        return jsonify({"message": "Invalid credentials"}), 401
    if new_password != confirm_password:
        return jsonify({"message": "confirm password does not match"}), 401
    
    hashed_pwd = hash_password(new_password)
    update_new_password(conn, current_user, hashed_pwd)
    # Revoke the current access token
    token_str = str(request.headers['Authorization'].replace('Bearer ', ''))
    ttl = calculate_time_to_live(token_str)
    add_revoked_token(rd, token_str, ttl)
    return jsonify({"message": "Change password successfully"})

@bp.route('/send_email', methods=['POST'])
def send_email():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    
    if email == "" or password == "":
        return jsonify({"message": "Please fill out email and password"}), 400 
    if check_user_email(conn, email) == False:
        return jsonify({"message": "Your email does not match"}), 400
    
    random_number = generate_random_number()
    update_verification_code(conn, email, random_number)
    sending_mail(email, password, random_number)
    return jsonify({"message": "Send email successfully"})

@bp.route('/forgot_password', methods=['POST'])
@jwt_required()
def forgot_password():
    email = request.json.get('email', None)
    verification_code = request.json.get('verification_code', None)
    rs =  check_verification_code(conn, email, verification_code)
    
    if rs == 0:
        return jsonify({"message": "Please send mail before you want to reset password"}), 400
    if rs == 1:
        current_user = get_jwt_identity()
        new_password = request.json.get('new_password', None)
        confirm_password = request.json.get('confirm_password', None)
        
        if new_password != confirm_password:
            return jsonify({"message": "confirm password does not match"}), 401
    
        hashed_pwd = hash_password(new_password)
        update_new_password(conn, str(current_user), hashed_pwd)
        # Revoke the current access token
        token_str = str(request.headers['Authorization'].replace('Bearer ', ''))
        ttl = calculate_time_to_live(token_str)
        add_revoked_token(rd, token_str, ttl)
    if rs == 2:
        return jsonify({"message": "Verification code does not match or email does not exist"}), 400
        
    return jsonify({"message": "Change password successfully"})

    
    
    
    



