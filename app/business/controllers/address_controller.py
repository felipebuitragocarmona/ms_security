from app.data.database import db
from app.business.models.address import Address
from app.business.models.user import User
from sqlalchemy.exc import SQLAlchemyError

class AddressController:
    @staticmethod
    def get_all():
        """Get all addresses"""
        try:
            addresses = Address.query.all()
            return [address.to_dict() for address in addresses], 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_by_id(address_id):
        """Get an address by ID"""
        try:
            address = Address.query.get(address_id)
            if not address:
                return {"error": "Address not found"}, 404
            return address.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500
    
    @staticmethod
    def get_by_user_id(user_id):
        """Get an address by user ID"""
        try:
            address = Address.query.filter_by(user_id=user_id).first()
            if not address:
                return {"error": "Address not found for this user"}, 404
            return address.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    @staticmethod
    def create(user_id, data):
        """Create a new address for a user"""
        try:
            # Check if user exists
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found"}, 404
                
            # Check if user already has an address
            if Address.query.filter_by(user_id=user_id).first():
                return {"error": "User already has an address"}, 400
            
            # Validate required fields
            if 'street' not in data or 'number' not in data:
                return {"error": "Street and number are required"}, 400
            
            new_address = Address(
                user_id=user_id,
                street=data['street'],
                number=data['number'],
                latitude=data.get('latitude'),
                longitude=data.get('longitude')
            )
            
            db.session.add(new_address)
            db.session.commit()
            
            return new_address.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def update(address_id, data):
        """Update an address"""
        try:
            address = Address.query.get(address_id)
            if not address:
                return {"error": "Address not found"}, 404
            
            if 'street' in data:
                address.street = data['street']
            if 'number' in data:
                address.number = data['number']
            if 'latitude' in data:
                address.latitude = data['latitude']
            if 'longitude' in data:
                address.longitude = data['longitude']
                
            db.session.commit()
            return address.to_dict(), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def delete(address_id):
        """Delete an address"""
        try:
            address = Address.query.get(address_id)
            if not address:
                return {"error": "Address not found"}, 404
            
            db.session.delete(address)
            db.session.commit()
            
            return {"message": "Address deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500