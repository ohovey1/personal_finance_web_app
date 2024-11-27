from ..models.asset import Stock, RealEstate, Crypto, Cash

class AssetFactory:
    @staticmethod
    def create_asset(asset_type, *args, **kwargs):
        assets = {
            "stock": Stock,
            "realestate": RealEstate,
            "crypto": Crypto,
            "cash": Cash
        }
        
        asset_class = assets.get(asset_type)
        if not asset_class:
            raise ValueError(f"Unknown asset type: {asset_type}")
            
        return asset_class(*args, **kwargs)