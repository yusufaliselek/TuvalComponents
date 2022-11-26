from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# Models Started
class Item(declarative_base()):
    __tablename__ = "item"
    item_id = Column(String(length=100), primary_key=True, index=True)
    item_name = Column(String(length=255), index=True)
    item_likes = relationship("ItemLikes", backref="Item", lazy="joined") # If say joined table is already joined


class ItemLikes(declarative_base()):
    __tablename__ = "item_likes"
    like_id = Column(String(length=100), primary_key=True, index=True)
    liker_account_id = Column(String(length=255), index=True)
    item_id = Column(String(length=255), ForeignKey("item.item_id"))

# Models Finished


# Item Created
def create_item(item_id: str, item_name: str, db: Session):
    new_item = Item(item_id=item_id, item_name=item_name)

    print("Item created")

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

# Like Button Create Relationship
def like(like_id: str, liker_account_id: str, item_id: str, db: Session):
    new_like = ItemLikes(like_id=like_id, liker_account_id=liker_account_id, item_id=item_id)
    print("Liked")
    db.add(new_like)
    db.commit()
    db.refresh(new_like)

    return new_like

# Get Like By Id's
def get_like_by_id_s(item_id: str, account_id: str, db: Session) -> ItemLikes:
    get_like = db.query(ItemLikes).filter(
        ItemLikes.item_id == item_id,
        ItemLikes.liker_account_id == account_id
    ).first()
    return get_like


@router.post("/LikeOrUnlikeItem")
def like_item(session: SessionInfo = Depends(get_session), item_id: str = Form(...), db: Session = Depends(get_db)):
    try:
        like = get_like_by_id_s(item_id, session.account_id, db)
        if like is not None:
            db.delete(like)
            db.commit()
        elif like is None:
            like_id = str(uuid4())
            like(like_id, session.account_id, indicator_id, db)
        else:
            print("Like is not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
