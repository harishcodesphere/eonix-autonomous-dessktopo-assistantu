from database.models import Interaction, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def test_interaction_model():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    interaction = Interaction(
        user_input="hello",
        intent="greeting",
        response="hi"
    )
    session.add(interaction)
    session.commit()
    
    saved = session.query(Interaction).first()
    assert saved.user_input == "hello"
    assert saved.intent == "greeting"
