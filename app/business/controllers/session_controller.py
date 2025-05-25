import uuid
from datetime import datetime, timedelta
from app.data.database import db
from app.business.models.session import Session
from app.business.models.user import User
from sqlalchemy.exc import SQLAlchemyError

class SessionController:
    @staticmethod
    def get_all():
        """Get all sessions"""
        try:
            sessions = Session.query.all()
            return [session.to_dict() for session in sessions], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_by_id(session_id):
        """Get a session by ID"""
        try:
            session = Session.query.get(session_id)
            if not session:
                return {"error": "Session not found"}, 404
            return session.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500
    
    @staticmethod
    def get_by_user_id(user_id):
        """Get all sessions for a specific user"""
        try:
            sessions = Session.query.filter_by(user_id=user_id).all()
            return [session.to_dict() for session in sessions], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def create(user_id, data):
        """Create a new session for a user"""
        try:
            # Check if user exists
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found"}, 404
            
            # Generate session token if not provided
            token = data.get('token') or str(uuid.uuid4())
            
            # Set default expiration to 24 hours from now if not provided
            expiration = data.get('expiration')
            if not expiration:
                expiration = datetime.utcnow() + timedelta(hours=24)
            expiration=datetime.strptime(expiration, "%Y-%m-%d %H:%M:%S")
            new_session = Session(
                id=str(uuid.uuid4()),
                user_id=user_id,
                token=token,
                expiration=expiration,
                FACode=data.get('FACode'),
                state=data.get('state', 'active')
            )
            
            db.session.add(new_session)
            db.session.commit()
            
            return new_session.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def update(session_id, data):
        """Update a session"""
        try:
            session = Session.query.get(session_id)
            if not session:
                return {"error": "Session not found"}, 404
            
            if 'token' in data:
                session.token = data['token']
            if 'expiration' in data:
                expiration = datetime.strptime(data['expiration'], "%Y-%m-%d %H:%M:%S")
                session.expiration = expiration
            if 'FACode' in data:
                session.FACode = data['FACode']
            if 'state' in data:
                session.state = data['state']
                
            db.session.commit()
            return session.to_dict(), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def delete(session_id):
        """Delete a session"""
        try:
            session = Session.query.get(session_id)
            if not session:
                return {"error": "Session not found"}, 404
            
            db.session.delete(session)
            db.session.commit()
            
            return {"message": "Session deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500