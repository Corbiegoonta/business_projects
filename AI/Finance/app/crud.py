from sqlalchemy.orm import Session
import models

def create_asset(db: Session, symbol: str, name: str, asset_class: str):
    asset = models.Asset(symbol=symbol, name=name, asset_class=asset_class)
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

def get_assets(db: Session):
    return db.query(models.Asset).all()