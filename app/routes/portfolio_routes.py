from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from ..factories.account_factory import AccountFactory
from ..factories.asset_factory import AssetFactory
from ..visualizations.strategies import (
    AssetBreakdownStrategy,
    AccountBreakdownStrategy,
)

bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

@bp.route('/')
@login_required
def view_portfolio():
    """Display user's portfolio dashboard"""
    return render_template('portfolio/dashboard.html')

@bp.route('/add_account', methods=['GET', 'POST'])
@login_required
def add_account():
    """Add a new account"""
    if request.method == 'POST':
        account_type = request.form.get('account_type')
        name = request.form.get('name')
        
        # Use account factory to create account
        account = AccountFactory.create_account(
            account_type=account_type,
            name=name
        )
        
        # If accoutn successfuly added, redirect to portfolio view
        if account and current_user.portfolio.add_account(account):
            return redirect(url_for('portfolio.view_portfolio'))
        return render_template('portfolio/add_account.html', error="Could not create account")
    
    return render_template('portfolio/add_account.html')

@bp.route('/add_asset/<int:account_id>', methods=['GET', 'POST'])
@login_required
def add_asset(account_id):
    """Add an asset to a specific account"""
    if account_id not in current_user.portfolio.accounts:
        return redirect(url_for('portfolio.view_portfolio'))
        
    if request.method == 'POST':
        asset_type = request.form.get('asset_type')
        try:
            # Create asset using asset factory
            asset = AssetFactory.create_asset(
                asset_type,
                name=request.form.get('name'),
                ticker=request.form.get('ticker'),
                units=request.form.get('units'),
                purchase_price=request.form.get('purchase_price'),
                amount=request.form.get('amount')  # For cash assets
            )
            
            # If successful creation, add asset to account and redirect to portfolio view
            if asset:
                account = current_user.portfolio.accounts[account_id]
                account.add_asset(asset)
                return redirect(url_for('portfolio.view_portfolio'))
                
        except Exception as e:
            print(f"Error adding asset: {str(e)}")
            # Return error if asset can't be added
            return render_template('portfolio/add_asset.html', 
                                account_id=account_id, 
                                error="Could not add asset")
    
    return render_template('portfolio/add_asset.html', account_id=account_id)

@bp.route('/remove_asset/<int:account_id>/<int:asset_id>', methods=['POST'])
@login_required
def remove_asset(account_id, asset_id):
    """Removes asset from account"""
    if account_id in current_user.portfolio.accounts: # Check if account exists first
        account = current_user.portfolio.accounts[account_id] 
        if account.remove_asset(asset_id): # Remove asset using account.remove_asset method (polymorphism)
            return redirect(url_for('portfolio.view_portfolio'))
    return "Error removing asset", 400

@bp.route('/remove_account/<int:account_id>', methods=['POST'])
@login_required
def remove_account(account_id):
    """Remove an account from the portfolio"""
    if current_user.portfolio.remove_account(account_id): # Remove account using portfolio.remove_account method
        return redirect(url_for('portfolio.view_portfolio'))
    return "Error removing account", 400


@bp.route('/visualize/<strategy_type>')
@login_required
def visualize_portfolio(strategy_type):
    """Generate portfolio visualization based on strategy"""
    strategies = {
        'asset': AssetBreakdownStrategy(),
        'account': AccountBreakdownStrategy(),
    }
    
    strategy = strategies.get(strategy_type)
    if not strategy:
        return "Invalid strategy type", 400
        
    data = current_user.portfolio.generate_visualization(strategy) # Generate visualization using current user's portfolio
    
    # Return visualization data in json format
    return jsonify(data)