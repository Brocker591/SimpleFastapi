from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db


#Erstellt alle Models auf der Datenbank
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def root():
    return{"message": "Hello world"}

#List muss explizit angeben werden, damit auch eine Liste zurück gegeben werden kann. Kommt vom "typing" Modul
@app.get("/posts", response_model=List[schemas.Post]) 
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(create_post: schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(title=create_post.title, content=create_post.content, published=create_post.published)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
   
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()

    return post_query.first()


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

