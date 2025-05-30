import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename
from app.data.database import db
from app.business.models.profile import Profile
from app.business.models.user import User
from sqlalchemy.exc import SQLAlchemyError

class ProfileController:
    @staticmethod
    def get_all():
        """Get all profiles"""
        try:
            profiles = Profile.query.all()
            return [profile.to_dict() for profile in profiles], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_by_id(profile_id):
        """Get a profile by ID"""
        try:
            profile = Profile.query.get(profile_id)
            if not profile:
                return {"error": "Profile not found"}, 404
            return profile.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500
    
    @staticmethod
    def get_by_user_id(user_id):
        """Get a profile by user ID"""
        try:
            profile = Profile.query.filter_by(user_id=user_id).first()
            if not profile:
                return {"error": "Profile not found for this user"}, 404
            return profile.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def create(user_id, data, photo=None):
        """Create a new profile for a user"""
        try:
            # Check if user exists
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found"}, 404
                
            # Check if user already has a profile
            if Profile.query.filter_by(user_id=user_id).first():
                return {"error": "User already has a profile"}, 400
            
            photo_path = None
            if photo:
                # Save photo if provided
                filename = secure_filename(f"{uuid.uuid4()}_{photo.filename}")
                photo_path = os.path.join('profiles', filename)
                photo_path = photo_path.replace('\\', '/')
                photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], photo_path))
            
            new_profile = Profile(
                user_id=user_id,
                phone=data.get('phone', ''),
                photo=photo_path
            )
            
            db.session.add(new_profile)
            db.session.commit()
            
            return new_profile.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def update(profile_id, data, photo=None):
        """Update a profile"""
        try:
            profile = Profile.query.get(profile_id)
            if not profile:
                return {"error": "Profile not found"}, 404
            
            if 'phone' in data:
                profile.phone = data['phone']
                
            if photo:
                # If there's an existing photo, delete it
                if profile.photo:
                    old_photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], profile.photo)
                    if os.path.exists(old_photo_path):
                        os.remove(old_photo_path)
                
                # Save the new photo
                filename = secure_filename(f"{uuid.uuid4()}_{photo.filename}")
                photo_path = os.path.join('profiles', filename)
                photo_path = photo_path.replace('\\', '/')
                photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], photo_path))
                profile.photo = photo_path
                
            db.session.commit()
            return profile.to_dict(), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def delete(profile_id):
        """Delete a profile"""
        try:
            profile = Profile.query.get(profile_id)
            if not profile:
                return {"error": "Profile not found"}, 404
            
            # Delete the photo file if it exists
            if profile.photo:
                photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], profile.photo)
                if os.path.exists(photo_path):
                    os.remove(photo_path)
            
            db.session.delete(profile)
            db.session.commit()
            
            return {"message": "Profile deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500