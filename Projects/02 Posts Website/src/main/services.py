from . import db


def get_all(model):
    return db.session.scalars(db.select(model)).all()


def get_all_filter_by(model, **kwargs):
    return db.session.scalars(
        db.select(model).filter_by(**kwargs).order_by(model.id.desc())
    ).all()


def get_first_filter_by(model, **kwargs):
    return db.session.scalars(db.select(model).filter_by(**kwargs)).first()


def get_first_or_404_filter_by(model, **kwargs):
    return db.first_or_404(db.select(model).filter_by(**kwargs))


def add(model_instance):
    db.session.add(model_instance)
    db.session.commit()


def delete(model_instance):
    db.session.delete(model_instance)
    db.session.commit()


def update():
    db.session.commit()


def get_or_404(model, ident):
    return db.get_or_404(model, ident)
