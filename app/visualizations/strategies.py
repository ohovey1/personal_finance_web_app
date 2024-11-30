from abc import ABC, abstractmethod
#from ..models.portfolio import Portfolio

class VisualizationStrategy(ABC):
    """Abstract base class for visualization strategies"""
    @abstractmethod
    def generate_visualization_data(self, portfolio):
        """Generate visualization data"""
        pass

## Concrete strategies

class AssetBreakdownStrategy(VisualizationStrategy):
    """Break down portfolio by asset"""
    def generate_visualization_data(self, portfolio):
        # List to store all assets and their values
        assets_data = []
        
        # Get data for each asset in each account
        for account in portfolio.accounts.values():
            for asset in account.holdings.values():
                assets_data.append({
                    'name': f"{asset.name} ({account.name})",
                    'value': asset.calculate_value(),
                    'type': asset.__class__.__name__  # Get type dynamically
                })

        # Sort by value for better visualization
        assets_data.sort(key=lambda x: x['value'], reverse=True)

        # Return data for pie chart visualization
        return {
            'labels': [asset['name'] for asset in assets_data],
            'values': [asset['value'] for asset in assets_data],
            'types': [asset['type'] for asset in assets_data],
            'title': 'Portfolio Assets Breakdown'
        }      
    

class AccountBreakdownStrategy(VisualizationStrategy):
    """Break down portfolio by account"""
    def generate_visualization_data(self, portfolio):
        # Get data for each account, including type
        account_data = []
        for account in portfolio.accounts.values():
            account_data.append({
                'name': account.name,
                'value': account.calculate_total_value(),
                'type': account.account_type
            })

        # Sort by value
        account_data.sort(key=lambda x: x['value'], reverse=True)

        # Return data for pie chart visualization
        return {
            'labels': [acc['name'] for acc in account_data],
            'values': [acc['value'] for acc in account_data],
            'types': [acc['type'] for acc in account_data],
            'title': 'Portfolio Breakdown by Account'
        }