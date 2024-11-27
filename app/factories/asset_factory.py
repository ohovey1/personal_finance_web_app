from typing import Optional
from ..models.asset import Asset, Stock, Crypto, Cash

class AssetFactory:
    @staticmethod
    def create_asset(asset_type: str, **kwargs) -> Optional[Asset]:
        """
        Create an asset of specified type.
        
        Args:
            asset_type: Type of asset ('stock', 'crypto', 'cash')
            **kwargs: Asset-specific parameters
                For stock/crypto:
                    - name: Asset name
                    - ticker: Stock/crypto symbol
                    - units: Number of units held
                    - purchase_price: Price per unit
                For cash:
                    - amount: Cash amount
        """
        try:
            if asset_type == "stock":
                return Stock(
                    name=kwargs['name'],
                    ticker=kwargs['ticker'],
                    units=float(kwargs['units']),
                    purchase_price=float(kwargs['purchase_price'])
                )
            elif asset_type == "crypto":
                return Crypto(
                    name=kwargs['name'],
                    ticker=kwargs['ticker'],
                    units=float(kwargs['units']),
                    purchase_price=float(kwargs['purchase_price'])
                )
            elif asset_type == "cash":
                return Cash(amount=float(kwargs['amount']))
            else:
                raise ValueError(f"Unknown asset type: {asset_type}")
        except KeyError as e:
            print(f"Missing required parameter: {str(e)}")
            return None
        except Exception as e:
            print(f"Error creating asset: {str(e)}")
            return None