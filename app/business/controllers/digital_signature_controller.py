import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename
from app.data.database import db
from app.business.models.digital_signature import DigitalSignature
from app.business.models.user import User
from sqlalchemy.exc import SQLAlchemyError

class DigitalSignatureController:
    @staticmethod
    def get_all():
        """Get all digital signatures"""
        try:
            signatures = DigitalSignature.query.all()
            return [signature.to_dict() for signature in signatures], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_by_id(signature_id):
        """Get a digital signature by ID"""
        try:
            signature = DigitalSignature.query.get(signature_id)
            if not signature:
                return {"error": "Digital signature not found"}, 404
            return signature.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500
    
    @staticmethod
    def get_by_user_id(user_id):
        """Get a digital signature by user ID"""
        try:
            signature = DigitalSignature.query.filter_by(user_id=user_id).first()
            if not signature:
                return {"error": "Digital signature not found for this user"}, 404
            return signature.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def create(user_id, photo):
        """Create a new digital signature for a user"""
        try:
            # Check if user exists
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found"}, 404
                
            # Check if user already has a digital signature
            if DigitalSignature.query.filter_by(user_id=user_id).first():
                return {"error": "User already has a digital signature"}, 400
            
            # Save photo
            if not photo:
                return {"error": "Digital signature image is required"}, 400
                
            filename = secure_filename(f"{uuid.uuid4()}_{photo.filename}")
            photo_path = os.path.join('digital-signatures', filename)
            os.makedirs(os.path.join(current_app.config['UPLOAD_FOLDER'], 'signatures'), exist_ok=True)
            photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], photo_path))
            photo_path = photo_path.replace('\\', '/')

            new_signature = DigitalSignature(
                user_id=user_id,
                photo=photo_path
            )
            
            db.session.add(new_signature)
            db.session.commit()
            
            return new_signature.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def update(signature_id, photo):
        """Update a digital signature"""
        try:
            signature = DigitalSignature.query.get(signature_id)
            if not signature:
                return {"error": "Digital signature not found"}, 404
            
            if not photo:
                return {"error": "Digital signature image is required"}, 400
                
            # If there's an existing photo, delete it
            if signature.photo:
                old_photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], signature.photo)
                if os.path.exists(old_photo_path):
                    os.remove(old_photo_path)
            
            # Save the new photo
            filename = secure_filename(f"{uuid.uuid4()}_{photo.filename}")
            photo_path = os.path.join('digital-signatures', filename)
            photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], photo_path))
            photo_path=photo_path.replace('\\', '/')

            signature.photo = photo_path
                
            db.session.commit()
            return signature.to_dict(), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def delete(signature_id):
        """Delete a digital signature"""
        try:
            signature = DigitalSignature.query.get(signature_id)
            if not signature:
                return {"error": "Digital signature not found"}, 404
            
            # Delete the photo file if it exists
            if signature.photo:
                photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], signature.photo)
                if os.path.exists(photo_path):
                    os.remove(photo_path)
            
            db.session.delete(signature)
            db.session.commit()
            
            return {"message": "Digital signature deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500