from . import bp as api
from.forms import ItemForm
from app.blueprints.auth.auth import token_auth
from flask import request, make_response, g, abort
from flask import render_template, request, flash, redirect, url_for
from app.models import Item, Cart, User, db
from flask_login import current_user, login_required

@api.route('/create_item', methods = ['GET', 'POST'])

def create_item():
    form = ItemForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_item_data = {
                "name":form.name.data.title(),
                "price":form.price.data,
                "desc":form.desc.data,
                "img":form.img.data,
                "category":form.category.data,
            }
            new_item_object = Item()
    
            new_item_object.from_dict(new_item_data)
            
            new_item_object.save()
        except:
            flash('There was an unexpected error. Please Try Again', 'danger')
            return render_template('additem.html.j2', form=form)
        flash('You have successfully created the item', 'warning')
        return redirect(url_for('api.view_shop'))
    
    return render_template('additem.html.j2', form = form)

@api.route('/view_shop', methods=['GET'])
@login_required
def view_shop():
    items = Item.query.all()
    return render_template('view_shop.html.j2', items = items)

@api.route('/clothes', methods=['GET'])
@login_required
def shop_clothes():
    items = Item.query.filter_by(category = 'clothes').all()
    return render_template('view_shop.html.j2', items = items)

@api.route('/valuables', methods=['GET'])
@login_required
def shop_valuables():
    items = Item.query.filter_by(category = 'valuables').all()
    return render_template('view_shop.html.j2', items = items)

@api.route('/accessories', methods=['GET'])
@login_required
def shop_accessories():
    items = Item.query.filter_by(category = 'accessories').all()
    return render_template('view_shop.html.j2', items = items)

@api.route('/add_to_cart/<int:id>')
@login_required
def add_to_cart(id):
    item = Item.query.get((id))    
    current_user.user_item.append(item)
    db.session.commit()
    flash(f'You have added {item.name} to the cart', 'success')
    return redirect(url_for('api.view_shop'))

@api.route('/remove_from_cart/<int:id>')
@login_required
def remove_from_cart(id):
    item = Item.query.get((id))
    print(item)
    current_user.user_item.remove(item)
    db.session.commit()
    flash(f'You have removed this from your cart', 'success')
    return redirect(url_for('api.cart'))

@api.route('/remove_all_items')
@login_required
def remove_all_items():    
    items = Cart.query.filter_by(user_id = current_user.id).all()
    for item in items:
        print(item)
        Cart.delete(item)
    db.session.commit()
    flash(f'You have cleared your cart', 'danger')
    return redirect(url_for('api.cart'))

@api.route('/cart', methods=['GET'])
@login_required
def cart(): 
    items = current_user.user_item
    return render_template('cart.html.j2', items = items)

@api.route('/item/<int:id>')
@login_required
def get_item(id):
    item = Item.query.get(id)
    return render_template('single_item.html.j2', item=item)