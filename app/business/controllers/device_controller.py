from app.data.database import db
from app.business.models.device import Device
from app.business.models.user import User
from sqlalchemy.exc import SQLAlchemyError

class DeviceController:
    @staticmethod
    def get_all():
        """Get all devices"""
        try:
            devices = Device.query.all()
            return [device.to_dict() for device in devices], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_by_id(device_id):
        """Get a device by ID"""
        try:
            device = Device.query.get(device_id)
            if not device:
                return {"error": "Device not found"}, 404
            return device.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500
    
    @staticmethod
    def get_by_user_id(user_id):
        """Get all devices for a specific user"""
        try:
            devices = Device.query.filter_by(user_id=user_id).all()
            return [device.to_dict() for device in devices], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def create(user_id, data):
        """Create a new device for a user"""
        try:
            # Check if user exists
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found"}, 404
            
            # Validate required fields
            if 'name' not in data or 'ip' not in data:
                return {"error": "Device name and IP address are required"}, 400
            
            # Create the new device
            new_device = Device(
                user_id=user_id,
                name=data['name'],
                ip=data['ip'],
                operating_system=data.get('operating_system', '')
            )
            
            db.session.add(new_device)
            db.session.commit()
            
            return new_device.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def update(device_id, data):
        """Update a device"""
        try:
            device = Device.query.get(device_id)
            if not device:
                return {"error": "Device not found"}, 404
            
            if 'name' in data:
                device.name = data['name']
            if 'ip' in data:
                device.ip = data['ip']
            if 'operating_system' in data:
                device.operating_system = data['operating_system']
                
            db.session.commit()
            return device.to_dict(), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def delete(device_id):
        """Delete a device"""
        try:
            device = Device.query.get(device_id)
            if not device:
                return {"error": "Device not found"}, 404
            
            db.session.delete(device)
            db.session.commit()
            
            return {"message": "Device deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500