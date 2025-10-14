from firebase_config import db

def get_user_role(user_id, farm_id):
    try:
        role = db.child("farms").child(farm_id).child("members").child(user_id).get()
        if role.val():
            return role.val()
        return "no_role"
    except Exception as e:
        print("Error getting role:", e)
        return "no_role"

def check_permission(user_id, farm_id, action):
    role = get_user_role(user_id, farm_id)
    permissions = {
        "owner": ["view", "edit", "delete", "manage_members"],
        "animal_manager": ["view", "edit_animal", "delete_animal"],
        "plant_manager": ["view", "edit_plant", "delete_plant"],
        "viewer": ["view"],
        "no_role": []
    }
    return action in permissions.get(role, [])

def add_log(farm_id, user_id, action, data):
    try:
        log_data = {
            "user_id": user_id,
            "action": action,
            "data": data,
            "timestamp": db.child("farms").generate_key()
        }
        db.child("farms").child(farm_id).child("logs").push(log_data)
    except Exception as e:
        print("Error adding log:", e)